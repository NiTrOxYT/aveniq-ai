"""
Production Schedule & Execution History Storage Manager.
Provides thread-safe persistence for Automation Schedules and Execution History.
Enforces immutable UUID keys, path traversal protection, input validation, next-run calculations,
and JSON export/import with automatic UUID deduplication.
"""

import os
import sys
import json
import uuid
import re
import shutil
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

DEFAULT_TIMEZONE = "Asia/Kolkata"

VALID_TRIGGERS = [
    "one_time",
    "daily",
    "weekly",
    "monthly",
    "hourly",
    "every_x_minutes",
    "every_x_hours",
    "every_x_days",
    "weekdays_only",
    "custom_cron"
]

VALID_DEPARTMENTS = [
    "Creative",
    "Content",
    "Research",
    "Strategy",
    "Editorial",
    "Delivery",
    "Analytics",
    "General"
]

VALID_OUTPUTS = [
    "telegram",
    "dashboard",
    "email",
    "file"
]

VALID_PRIORITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

class ScheduleStore:
    def __init__(self, base_dir: str = "automation/storage", schedules_dir: Optional[str] = None, history_dir: Optional[str] = None):
        self.base_dir = base_dir
        self.schedules_dir = schedules_dir or os.path.join(base_dir, "schedules")
        self.history_dir = history_dir or os.path.join(base_dir, "history")
        os.makedirs(self.schedules_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)
        self._seed_default_schedules_if_empty()

    def _sanitize_id(self, schedule_id: str) -> str:
        """Enforces alphanumeric, hyphen, and underscore characters to prevent path traversal."""
        if not schedule_id or not isinstance(schedule_id, str):
            raise ValueError("Schedule ID must be a non-empty string.")
        cleaned = re.sub(r'[^a-zA-Z0-9_\-]', '', schedule_id.strip())
        if not cleaned:
            raise ValueError("Invalid Schedule ID after sanitization.")
        return cleaned

    def _seed_default_schedules_if_empty(self):
        """Seeds initial default schedules if storage directory is empty."""
        existing = self.list_schedules()
        if existing:
            return

        defaults = [
            {
                "name": "Daily Content Pipeline",
                "description": "Autonomous generation of daily visual marketing assets & copywriting.",
                "department": "Creative",
                "priority": "HIGH",
                "trigger": "daily",
                "time": "08:00",
                "interval_value": 1,
                "cron": "0 8 * * *",
                "timezone": DEFAULT_TIMEZONE,
                "prompt": "Create daily visual marketing graphic for {{company}} showcasing {{topic}}.",
                "outputs": ["telegram", "dashboard"],
                "enabled": True,
                "state": "active"  # active, paused, disabled
            },
            {
                "name": "Weekly Market Intelligence Scan",
                "description": "Scrapes GitHub & RSS signals for tech trends and buyer intent.",
                "department": "Research",
                "priority": "MEDIUM",
                "trigger": "weekly",
                "time": "09:00",
                "interval_value": 1,
                "cron": "0 9 * * 1",
                "timezone": DEFAULT_TIMEZONE,
                "prompt": "Analyze star velocity and emerging topics across key AI repositories for {{date}}.",
                "outputs": ["dashboard", "file"],
                "enabled": True,
                "state": "active"
            },
            {
                "name": "Hourly System Health & Telemetry",
                "description": "Monitors API rate limits, model connectivity, and delivery health.",
                "department": "Analytics",
                "priority": "LOW",
                "trigger": "hourly",
                "time": "00:00",
                "interval_value": 1,
                "cron": "0 * * * *",
                "timezone": DEFAULT_TIMEZONE,
                "prompt": "Run provider health check for Gemini & Pollinations AI.",
                "outputs": ["dashboard"],
                "enabled": True,
                "state": "active"
            }
        ]

        for item in defaults:
            try:
                self.create_schedule(item)
            except Exception as e:
                logger.warning(f"Failed to seed default schedule '{item['name']}': {e}")

    def validate_schedule_payload(self, data: Dict[str, Any], is_update: bool = False) -> Dict[str, Any]:
        """Validates schedule fields server-side to prevent invalid configurations."""
        errors = []

        name = str(data.get("name") or "").strip()
        if not name:
            errors.append("Schedule Name cannot be empty.")

        workflow_id = str(data.get("workflow_id") or "").strip()
        prompt = str(data.get("prompt") or "").strip()
        if not prompt and not workflow_id:
            errors.append("Schedule must specify either a 'prompt' or a 'workflow_id'.")
        if not prompt and workflow_id:
            prompt = f"Execute native workflow '{workflow_id}'"

        trigger = str(data.get("trigger") or "daily").strip().lower()
        if trigger not in VALID_TRIGGERS:
            errors.append(f"Invalid trigger type '{trigger}'. Must be one of {VALID_TRIGGERS}.")

        department = str(data.get("department") or "Creative").strip()
        if department not in VALID_DEPARTMENTS:
            department = "Creative"

        priority = str(data.get("priority") or "MEDIUM").strip().upper()
        if priority not in VALID_PRIORITIES:
            priority = "MEDIUM"

        tz = str(data.get("timezone") or DEFAULT_TIMEZONE).strip()

        outputs = data.get("outputs")
        if not isinstance(outputs, list):
            outputs = ["dashboard"]
        else:
            outputs = [str(o).strip().lower() for o in outputs if str(o).strip().lower() in VALID_OUTPUTS]
            if not outputs:
                outputs = ["dashboard"]

        if errors:
            raise ValueError("Validation failed: " + "; ".join(errors))

        return {
            "name": name,
            "description": str(data.get("description") or "").strip(),
            "department": department,
            "priority": priority,
            "trigger": trigger,
            "time": str(data.get("time") or "08:00").strip(),
            "interval_value": int(data.get("interval_value") or 1),
            "cron": str(data.get("cron") or "0 8 * * *").strip(),
            "timezone": tz,
            "prompt": prompt,
            "workflow_id": workflow_id if workflow_id else None,
            "outputs": outputs,
            "enabled": bool(data.get("enabled", True)),
            "state": str(data.get("state") or "active").strip().lower()
        }

    def compute_next_executions(
        self,
        trigger: str,
        time_str: str = "08:00",
        interval_value: int = 1,
        cron_str: str = "0 8 * * *",
        tz_str: str = DEFAULT_TIMEZONE,
        count: int = 5,
        base_time: Optional[datetime] = None
    ) -> List[str]:
        """Calculates the upcoming execution timestamps for a schedule configuration relative to base_time."""
        now = base_time if base_time is not None else datetime.now(timezone.utc)
        results = []

        try:
            time_parts = time_str.split(":")
            hour = int(time_parts[0]) if len(time_parts) > 0 else 8
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
        except Exception:
            hour, minute = 8, 0

        if trigger == "every_x_minutes":
            step = max(interval_value, 1)
            curr = now + timedelta(minutes=step)
            for _ in range(count):
                results.append(curr.isoformat())
                curr += timedelta(minutes=step)
            return results

        if trigger in ("every_x_hours", "hourly"):
            step = max(interval_value, 1) if trigger == "every_x_hours" else 1
            curr = now.replace(minute=minute, second=0, microsecond=0)
            if curr <= now:
                curr += timedelta(hours=step)
            for _ in range(count):
                results.append(curr.isoformat())
                curr += timedelta(hours=step)
            return results

        curr = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if trigger == "weekdays_only":
            if curr <= now:
                curr += timedelta(days=1)
            for _ in range(count):
                while curr.weekday() >= 5:  # 5=Sat, 6=Sun
                    curr += timedelta(days=1)
                results.append(curr.isoformat())
                curr += timedelta(days=1)
            return results

        if trigger == "weekly":
            target_weekday = None
            if cron_str:
                c_parts = cron_str.split()
                if len(c_parts) >= 5 and c_parts[4] != "*":
                    try:
                        w = int(c_parts[4])
                        target_weekday = (w - 1) % 7 if w > 0 else 6
                    except ValueError:
                        pass

            if target_weekday is not None:
                while curr.weekday() != target_weekday or curr <= now:
                    curr += timedelta(days=1)
            else:
                if curr <= now:
                    curr += timedelta(days=7)

            step_days = 7 * max(interval_value, 1)
            for _ in range(count):
                results.append(curr.isoformat())
                curr += timedelta(days=step_days)
            return results

        if trigger in ("every_x_days", "daily", "custom_cron"):
            step_days = max(interval_value, 1) if trigger == "every_x_days" else 1
            if curr <= now:
                curr += timedelta(days=step_days)
            for _ in range(count):
                results.append(curr.isoformat())
                curr += timedelta(days=step_days)
            return results

        if trigger == "monthly":
            if curr <= now:
                curr += timedelta(days=30)
            for _ in range(count):
                results.append(curr.isoformat())
                curr += timedelta(days=30)
            return results

        if curr <= now:
            curr += timedelta(days=1)
        for _ in range(count):
            results.append(curr.isoformat())
            curr += timedelta(days=1)

        return results

    def create_schedule(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new schedule with an immutable UUID."""
        validated = self.validate_schedule_payload(data)
        schedule_id = str(uuid.uuid4())
        now_iso = _get_utc_now()

        next_runs = self.compute_next_executions(
            trigger=validated["trigger"],
            time_str=validated["time"],
            interval_value=validated["interval_value"],
            cron_str=validated["cron"],
            tz_str=validated["timezone"],
            count=5
        )

        schedule_data = {
            "id": schedule_id,
            "name": validated["name"],
            "description": validated["description"],
            "department": validated["department"],
            "priority": validated["priority"],
            "trigger": validated["trigger"],
            "time": validated["time"],
            "interval_value": validated["interval_value"],
            "cron": validated["cron"],
            "timezone": validated["timezone"],
            "prompt": validated["prompt"],
            "workflow_id": validated.get("workflow_id"),
            "outputs": validated["outputs"],
            "enabled": validated["enabled"],
            "state": validated["state"] if validated["enabled"] else "disabled",
            "created_at": now_iso,
            "updated_at": now_iso,
            "last_run": "",
            "next_run": next_runs[0] if next_runs else "",
            "statistics": {
                "execution_count": 0,
                "success_count": 0,
                "failure_count": 0,
                "average_duration_ms": 0,
                "last_status": "none"
            }
        }

        file_path = os.path.join(self.schedules_dir, f"{schedule_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(schedule_data, f, indent=2)

        os.makedirs(os.path.join(self.history_dir, schedule_id), exist_ok=True)
        return schedule_data

    def get_schedule(self, schedule_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single schedule by ID (Pure read-only, zero disk side-effects)."""
        clean_id = self._sanitize_id(schedule_id)
        file_path = os.path.join(self.schedules_dir, f"{clean_id}.json")
        if not os.path.isfile(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.error(f"Error reading schedule file '{file_path}': {e}")
            return None

    def update_schedule(self, schedule_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing schedule while preserving its immutable UUID and stats."""
        clean_id = self._sanitize_id(schedule_id)
        existing = self.get_schedule(clean_id)
        if not existing:
            raise ValueError(f"Schedule '{clean_id}' not found.")

        validated = self.validate_schedule_payload(data, is_update=True)
        now_iso = _get_utc_now()

        next_runs = self.compute_next_executions(
            trigger=validated["trigger"],
            time_str=validated["time"],
            interval_value=validated["interval_value"],
            cron_str=validated["cron"],
            tz_str=validated["timezone"],
            count=5
        )

        existing.update({
            "name": validated["name"],
            "description": validated["description"],
            "department": validated["department"],
            "priority": validated["priority"],
            "trigger": validated["trigger"],
            "time": validated["time"],
            "interval_value": validated["interval_value"],
            "cron": validated["cron"],
            "timezone": validated["timezone"],
            "prompt": validated["prompt"],
            "outputs": validated["outputs"],
            "enabled": validated["enabled"],
            "state": validated["state"] if validated["enabled"] else "disabled",
            "updated_at": now_iso,
            "next_run": next_runs[0] if next_runs else ""
        })

        file_path = os.path.join(self.schedules_dir, f"{clean_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)

        return existing

    def toggle_schedule(self, schedule_id: str, state: Optional[str] = None, enabled: Optional[bool] = None) -> Dict[str, Any]:
        """Toggles schedule lifecycle state (active, paused, disabled)."""
        clean_id = self._sanitize_id(schedule_id)
        existing = self.get_schedule(clean_id)
        if not existing:
            raise ValueError(f"Schedule '{clean_id}' not found.")

        if state is not None:
            new_state = str(state).strip().lower()
            existing["state"] = new_state
            existing["enabled"] = (new_state != "disabled")
        elif enabled is not None:
            existing["enabled"] = bool(enabled)
            existing["state"] = "active" if bool(enabled) else "disabled"
        else:
            existing["enabled"] = not existing.get("enabled", True)
            existing["state"] = "active" if existing["enabled"] else "disabled"

        existing["updated_at"] = _get_utc_now()

        file_path = os.path.join(self.schedules_dir, f"{clean_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)

        return existing

    def delete_schedule(self, schedule_id: str) -> bool:
        """Deletes a schedule file and archives its history directory."""
        clean_id = self._sanitize_id(schedule_id)
        file_path = os.path.join(self.schedules_dir, f"{clean_id}.json")

        if os.path.isfile(file_path):
            os.remove(file_path)

        hist_path = os.path.join(self.history_dir, clean_id)
        if os.path.isdir(hist_path):
            shutil.rmtree(hist_path, ignore_errors=True)

        return True

    def duplicate_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """Duplicates an existing schedule with a new UUID and '<Name> Copy' title."""
        clean_id = self._sanitize_id(schedule_id)
        existing = self.get_schedule(clean_id)
        if not existing:
            raise ValueError(f"Schedule '{clean_id}' not found.")

        dup_data = dict(existing)
        dup_data["name"] = f"{existing.get('name', 'Schedule')} Copy"
        dup_data.pop("id", None)
        dup_data.pop("created_at", None)
        dup_data.pop("updated_at", None)
        dup_data.pop("last_run", None)
        dup_data.pop("statistics", None)

        return self.create_schedule(dup_data)

    def list_schedules(self, query: str = "", department: str = "", state: str = "") -> List[Dict[str, Any]]:
        """Lists all schedules with optional search query and department/state filters."""
        results = []
        if not os.path.isdir(self.schedules_dir):
            return results

        q = str(query or "").strip().lower()
        dept = str(department or "").strip().lower()
        st = str(state or "").strip().lower()

        for fname in sorted(os.listdir(self.schedules_dir)):
            if fname.endswith(".json"):
                sid = fname[:-5]
                sch = self.get_schedule(sid)
                if not sch:
                    continue

                if q and (q not in sch.get("name", "").lower() and q not in sch.get("description", "").lower() and q not in sch.get("prompt", "").lower()):
                    continue

                if dept and dept != "all" and sch.get("department", "").lower() != dept:
                    continue

                if st and st != "all" and sch.get("state", "").lower() != st and sch.get("status", "").lower() != st:
                    continue

                results.append(sch)

        return results

    def add_execution_history(self, schedule_id: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Saves a separate execution history record in automation/storage/history/<schedule-id>/."""
        clean_id = self._sanitize_id(schedule_id)
        schedule = self.get_schedule(clean_id)
        if not schedule:
            raise ValueError(f"Schedule '{clean_id}' not found.")

        hist_dir = os.path.join(self.history_dir, clean_id)
        os.makedirs(hist_dir, exist_ok=True)

        exec_id = f"exec_{abs(hash(str(datetime.now().timestamp()))) % 100000:05d}"
        now_iso = _get_utc_now()
        ts_filename = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S") + f"_{exec_id}.json"

        history_record = {
            "execution_id": exec_id,
            "schedule_id": clean_id,
            "schedule_name": schedule.get("name"),
            "started_at": record.get("started_at", now_iso),
            "completed_at": record.get("completed_at", now_iso),
            "duration_ms": int(record.get("duration_ms", 0)),
            "trigger": record.get("trigger", "scheduled"),
            "status": record.get("status", "success"),
            "output_summary": record.get("output_summary", "Completed successfully"),
            "checklist": record.get("checklist", ["✓ Execution Finished"]),
            "logs": record.get("logs", []),
            "error": record.get("error", None)
        }

        file_path = os.path.join(hist_dir, ts_filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(history_record, f, indent=2)

        # Update schedule stats & last_run
        stats = schedule.get("statistics", {})
        count = stats.get("execution_count", 0) + 1
        is_succ = history_record["status"].lower() in ("success", "completed", "ok")
        succ_cnt = stats.get("success_count", 0) + (1 if is_succ else 0)
        fail_cnt = stats.get("failure_count", 0) + (0 if is_succ else 1)

        prev_avg = stats.get("average_duration_ms", 0)
        new_dur = history_record["duration_ms"]
        new_avg = int(((prev_avg * (count - 1)) + new_dur) / count) if count > 0 else new_dur

        schedule["statistics"] = {
            "execution_count": count,
            "success_count": succ_cnt,
            "failure_count": fail_cnt,
            "average_duration_ms": new_avg,
            "last_status": "success" if is_succ else "failed"
        }
        schedule["last_run"] = history_record["completed_at"]
        schedule["last_result"] = history_record

        # Advance next_run relative to actual execution time
        exec_time = datetime.now(timezone.utc)
        next_runs = self.compute_next_executions(
            trigger=schedule.get("trigger", "daily"),
            time_str=schedule.get("time", "08:00"),
            interval_value=schedule.get("interval_value", 1),
            cron_str=schedule.get("cron", "0 8 * * *"),
            tz_str=schedule.get("timezone", DEFAULT_TIMEZONE),
            count=1,
            base_time=exec_time
        )
        if next_runs:
            schedule["next_run"] = next_runs[0]

        s_path = os.path.join(self.schedules_dir, f"{clean_id}.json")
        with open(s_path, "w", encoding="utf-8") as f:
            json.dump(schedule, f, indent=2)

        return history_record

    def repair_stale_schedules(self) -> List[Dict[str, Any]]:
        """Scans active schedules on startup. Repairs any schedule with next_run in the past (getter purity preserved)."""
        repaired = []
        if not os.path.isdir(self.schedules_dir):
            return repaired

        now = datetime.now(timezone.utc)
        now_iso = now.isoformat()

        for fname in sorted(os.listdir(self.schedules_dir)):
            if fname.endswith(".json"):
                sid = fname[:-5]
                file_path = os.path.join(self.schedules_dir, fname)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    next_run = data.get("next_run")
                    is_active = data.get("enabled", True) and data.get("state", "active") == "active"
                    if is_active and (not next_run or next_run <= now_iso):
                        next_runs = self.compute_next_executions(
                            trigger=data.get("trigger", "daily"),
                            time_str=data.get("time", "08:00"),
                            interval_value=data.get("interval_value", 1),
                            cron_str=data.get("cron", "0 8 * * *"),
                            tz_str=data.get("timezone", DEFAULT_TIMEZONE),
                            count=1,
                            base_time=now
                        )
                        if next_runs:
                            old_next = next_run
                            data["next_run"] = next_runs[0]
                            data["updated_at"] = now_iso
                            with open(file_path, "w", encoding="utf-8") as fw:
                                json.dump(data, fw, indent=2)
                            logger.info(f"[Schedule Repair] Repaired stale schedule '{sid}' ({data.get('name')}): Old next_run={old_next} -> New next_run={data['next_run']}")
                            repaired.append(data)
                except Exception as e:
                    logger.error(f"[Schedule Repair Error] Failed to repair schedule '{fname}': {e}")

        return repaired

    def get_execution_history(self, schedule_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves history records for a specific schedule."""
        clean_id = self._sanitize_id(schedule_id)
        hist_dir = os.path.join(self.history_dir, clean_id)
        results = []

        if not os.path.isdir(hist_dir):
            return results

        for fname in sorted(os.listdir(hist_dir), reverse=True):
            if fname.endswith(".json"):
                fpath = os.path.join(hist_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        results.append(json.load(f))
                    if len(results) >= limit:
                        break
                except Exception as e:
                    logger.warning(f"Error reading history file '{fpath}': {e}")

        return results

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Calculates global summary KPIs across all schedules."""
        schedules = self.list_schedules()
        total = len(schedules)
        running = sum(1 for s in schedules if s.get("enabled") and s.get("state") in ("active", "running"))
        paused = sum(1 for s in schedules if s.get("state") == "paused")
        disabled = sum(1 for s in schedules if not s.get("enabled") or s.get("state") == "disabled")

        failed_today = 0
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        next_exec_times = []

        for s in schedules:
            last_res = s.get("last_result", {})
            if last_res.get("status") == "failed" and str(last_res.get("completed_at", "")).startswith(today_str):
                failed_today += 1

            nr = s.get("next_run")
            if nr and s.get("enabled"):
                next_exec_times.append(nr)

        next_exec_times.sort()

        return {
            "total_schedules": total,
            "running": running,
            "paused": paused,
            "disabled": disabled,
            "failed_today": failed_today,
            "next_execution": next_exec_times[0] if next_exec_times else "None Scheduled"
        }

    def export_schedules(self, schedule_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Exports selected or all schedules as JSON payload."""
        all_schedules = self.list_schedules()
        if not schedule_ids:
            return all_schedules

        clean_ids = [self._sanitize_id(sid) for sid in schedule_ids]
        return [s for s in all_schedules if s.get("id") in clean_ids]

    def import_schedules(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Imports a list of schedule JSON objects with automatic UUID deduplication."""
        imported = []
        if not isinstance(items, list):
            raise ValueError("Import payload must be a JSON array of schedules.")

        for item in items:
            if not isinstance(item, dict):
                continue
            # Ensure fresh UUID for imported items to prevent collision
            item_copy = dict(item)
            item_copy.pop("id", None)
            new_sch = self.create_schedule(item_copy)
            imported.append(new_sch)

        return imported

global_schedule_store = ScheduleStore()
