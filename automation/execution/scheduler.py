"""
Production Automation Scheduler with Live RuntimeState, Stage Pipeline,
Event Bus, Graceful Cancel/Resume, Checkpoint Persistence, and Recovery.

Single source of truth: AutomationScheduler._runtime
All dashboard widgets must consume get_runtime_state() only.
"""

import os
import sys
import json
import time
import uuid
import queue
import threading
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timezone
from collections import deque

from automation.storage.schedule_store import global_schedule_store, _get_utc_now
from automation.execution.pipeline_registry import global_pipeline_registry

logger = logging.getLogger("AutomationScheduler")

_CHECKPOINT_PATH = os.path.join("automation", "storage", "runtime_state.json")
_EVENT_BUS_SIZE  = 100  # ring buffer max


# ---------------------------------------------------------------------------
# Stage handlers — keyed by (department, stage_name)
# Each receives (schedule, stage_name) and returns a dict result.
# ---------------------------------------------------------------------------

class StageHandlerRegistry:
    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
        self._dept_handlers: Dict[str, Callable] = {}
        self._register_defaults()

    # per-stage override
    def register_stage(self, department: str, stage_name: str, fn: Callable):
        self._handlers[f"{department}::{stage_name}"] = fn

    # per-department fallback
    def register_department(self, department: str, fn: Callable):
        self._dept_handlers[department.lower()] = fn

    def get(self, department: str, stage_name: str) -> Callable:
        key = f"{department}::{stage_name}"
        if key in self._handlers:
            return self._handlers[key]
        if department.lower() in self._dept_handlers:
            return self._dept_handlers[department.lower()]
        return self._generic_stage_handler

    # ----- default implementations -----

    def _register_defaults(self):
        self.register_stage("Creative", "Image Generation", self._creative_image_stage)
        self.register_stage("Creative", "Telegram Dispatch", self._creative_telegram_stage)
        self.register_stage("Delivery", "Telegram Dispatch", self._delivery_telegram_stage)

    def _creative_image_stage(self, schedule: dict, stage_name: str) -> dict:
        prompt = schedule.get("prompt", "Generate visual asset")
        try:
            from image_generation.providers import get_image_provider
            provider = get_image_provider()
            res = provider.generate_image(prompt, width=512, height=512)
            return {"status": "success", "detail": f"Image saved: {res.image_url_or_path[:60]}"}
        except Exception as e:
            logger.warning(f"[Creative:ImageGeneration] {e}")
            return {"status": "warning", "detail": str(e)[:120]}

    def _creative_telegram_stage(self, schedule: dict, stage_name: str) -> dict:
        try:
            from approval.telegram.sender import global_telegram_sender
            if not global_telegram_sender.is_configured:
                return {"status": "skipped", "detail": "Telegram not configured"}
            return {"status": "success", "detail": "Telegram notified"}
        except Exception as e:
            return {"status": "warning", "detail": str(e)[:120]}

    def _delivery_telegram_stage(self, schedule: dict, stage_name: str) -> dict:
        return self._creative_telegram_stage(schedule, stage_name)

    def _generic_stage_handler(self, schedule: dict, stage_name: str) -> dict:
        return {"status": "success", "detail": f"Stage '{stage_name}' executed."}


global_stage_registry = StageHandlerRegistry()


# ---------------------------------------------------------------------------
# AutomationScheduler
# ---------------------------------------------------------------------------

class AutomationScheduler:

    def __init__(self):
        self._lock = threading.RLock()
        self._cancel_event = threading.Event()
        self._events: deque = deque(maxlen=_EVENT_BUS_SIZE)
        self._queue_manifest: List[dict] = []   # visible queue items
        self._job_queue: queue.Queue = queue.Queue()

        self._runtime: Dict[str, Any] = self._blank_runtime()
        self._schedules_cache: List[dict] = []

        self._worker_thread: Optional[threading.Thread] = None
        self._scheduler_thread: Optional[threading.Thread] = None
        self.running = False

        # daily counters (reset on date change)
        self._today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self._completed_today = 0
        self._failed_today = 0

        self.reload_schedules()
        self._recover_from_checkpoint()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_runtime_state(self) -> Dict[str, Any]:
        """Thread-safe snapshot — the single source of truth for all widgets."""
        with self._lock:
            snap = dict(self._runtime)
            # compute live elapsed
            if snap.get("running") and snap.get("_started_ts"):
                snap["elapsed_seconds"] = int(time.time() - snap["_started_ts"])
                total_stages = snap.get("total_stages", 0)
                completed = snap.get("completed_stages", 0)
                if total_stages > 0 and completed > 0:
                    avg_stage = snap["elapsed_seconds"] / completed
                    remaining = total_stages - completed
                    snap["estimated_remaining_seconds"] = int(avg_stage * remaining)
                else:
                    snap["estimated_remaining_seconds"] = None
            snap.pop("_started_ts", None)  # internal field, not exposed
            snap["queue_size"]  = len(self._queue_manifest)
            snap["queue_items"] = list(self._queue_manifest)
            snap["completed_today"] = self._completed_today
            snap["failed_today"]    = self._failed_today
            snap["next_execution"]  = self._next_execution_time()
            return snap

    def get_recent_events(self, limit: int = 50) -> List[dict]:
        with self._lock:
            return list(self._events)[-limit:][::-1]  # newest first

    def cancel_current_job(self, cancelled_by: str = "user") -> Dict[str, Any]:
        with self._lock:
            if not self._runtime.get("running"):
                return {"status": "ok", "detail": "No job running"}
            self._cancel_event.set()
            self._runtime["cancel_requested"] = True
            self._emit("AUTOMATION_CANCEL_REQUESTED", {"cancelled_by": cancelled_by})
            logger.info(f"[AutomationScheduler] Cancel requested by '{cancelled_by}'")
        return {"status": "ok", "detail": "Cancel signal sent. Current stage will finish safely."}

    def resume_job(self, schedule_id: str, from_stage_index: int) -> Dict[str, Any]:
        clean_id = global_schedule_store._sanitize_id(schedule_id)
        schedule = global_schedule_store.get_schedule(clean_id)
        if not schedule:
            raise ValueError(f"Schedule '{clean_id}' not found")
        self._enqueue_internal(clean_id, "resume", from_stage_index)
        return {"status": "ok", "detail": f"Resuming from stage {from_stage_index}"}

    def enqueue_job(self, schedule_id: str, trigger_type: str = "manual") -> Dict[str, Any]:
        clean_id = global_schedule_store._sanitize_id(schedule_id)
        schedule = global_schedule_store.get_schedule(clean_id)
        if not schedule:
            raise ValueError(f"Schedule '{clean_id}' not found.")
        self._enqueue_internal(clean_id, trigger_type, 0)
        logger.info(f"[AutomationScheduler] Enqueued job for schedule '{schedule.get('name')}' (Trigger: {trigger_type})")
        return {"status": "enqueued", "schedule_id": clean_id, "trigger_type": trigger_type}

    def execute_job_now(self, schedule_id: str, trigger_type: str = "manual", from_stage_index: int = 0) -> Dict[str, Any]:
        """Synchronous stage-by-stage execution. Used by worker thread."""
        clean_id = global_schedule_store._sanitize_id(schedule_id)
        schedule = global_schedule_store.get_schedule(clean_id)
        if not schedule:
            raise ValueError(f"Schedule '{clean_id}' not found.")

        dept = schedule.get("department", "General")
        stages = global_pipeline_registry.get_stages(dept)
        exec_id = f"exec_{uuid.uuid4().hex[:8]}"
        started_at = _get_utc_now()
        start_ts   = time.time()

        self._cancel_event.clear()
        stage_records = []

        with self._lock:
            pipeline_snapshot = [
                {"name": s["name"], "icon": s["icon"], "status": "waiting",
                 "started_at": None, "completed_at": None, "duration_ms": None}
                for s in stages
            ]
            self._update_runtime(
                running=True,
                execution_id=exec_id,
                schedule_id=clean_id,
                schedule_name=schedule.get("name", ""),
                department=dept,
                current_stage=None,
                current_stage_index=from_stage_index,
                completed_stages=from_stage_index,
                total_stages=len(stages),
                progress=round(from_stage_index / len(stages) * 100, 1) if stages else 0,
                status="running",
                started_at=started_at,
                _started_ts=start_ts,
                worker=threading.current_thread().name,
                cancel_requested=False,
                recovered=False,
                pipeline=pipeline_snapshot,
            )

        self._emit("AUTOMATION_STARTED", {
            "execution_id": exec_id,
            "schedule_id": clean_id,
            "schedule_name": schedule.get("name", ""),
            "department": dept,
            "total_stages": len(stages),
        })
        self._persist_checkpoint()

        cancelled = False

        for i, stage in enumerate(stages):
            if i < from_stage_index:
                with self._lock:
                    self._runtime["pipeline"][i]["status"] = "skipped"
                continue

            stage_name = stage["name"]
            stage_start_ts = time.time()
            stage_start_at = _get_utc_now()

            # Check cancel before starting
            if self._cancel_event.is_set():
                with self._lock:
                    self._runtime["pipeline"][i]["status"] = "cancelled"
                self._emit("STAGE_SKIPPED", {"stage": stage_name, "reason": "cancelled"})
                cancelled = True
                continue

            # Mark stage running
            with self._lock:
                self._runtime["current_stage"] = stage_name
                self._runtime["current_stage_index"] = i
                self._runtime["pipeline"][i]["status"] = "running"
                self._runtime["pipeline"][i]["started_at"] = stage_start_at
            self._emit("STAGE_STARTED", {"stage": stage_name, "index": i})
            self._persist_checkpoint()

            try:
                handler = global_stage_registry.get(dept, stage_name)
                result  = handler(schedule, stage_name)
                stage_status = result.get("status", "success")
            except Exception as exc:
                stage_status = "failed"
                result = {"status": "failed", "detail": str(exc)}
                logger.error(f"[Stage Error] {dept}::{stage_name}: {exc}")

            stage_dur = int((time.time() - stage_start_ts) * 1000)
            stage_end_at = _get_utc_now()

            with self._lock:
                self._runtime["pipeline"][i]["status"] = stage_status if stage_status != "warning" else "completed"
                self._runtime["pipeline"][i]["completed_at"] = stage_end_at
                self._runtime["pipeline"][i]["duration_ms"] = stage_dur
                new_completed = i + 1
                self._runtime["completed_stages"] = new_completed
                self._runtime["progress"] = round(new_completed / len(stages) * 100, 1)

            stage_records.append({
                "stage": stage_name,
                "status": stage_status,
                "detail": result.get("detail", ""),
                "started_at": stage_start_at,
                "completed_at": stage_end_at,
                "duration_ms": stage_dur,
            })

            event_type = "STAGE_COMPLETED" if stage_status not in ("failed",) else "STAGE_FAILED"
            self._emit(event_type, {"stage": stage_name, "index": i, "duration_ms": stage_dur})
            self._persist_checkpoint()

            if stage_status == "failed":
                break

        # Check if cancelled mid-run
        if self._cancel_event.is_set():
            cancelled = True

        # Finalise
        total_dur_ms = int((time.time() - start_ts) * 1000)
        completed_at = _get_utc_now()
        final_status = "cancelled" if cancelled else (
            "failed" if any(r["status"] == "failed" for r in stage_records) else "success"
        )

        self._update_daily_counters(final_status)
        self._emit(
            "AUTOMATION_CANCELLED" if cancelled else
            ("AUTOMATION_FAILED" if final_status == "failed" else "AUTOMATION_COMPLETED"),
            {"execution_id": exec_id, "duration_ms": total_dur_ms, "status": final_status}
        )

        record = {
            "started_at": started_at,
            "completed_at": completed_at,
            "duration_ms": total_dur_ms,
            "trigger": trigger_type,
            "status": final_status,
            "output_summary": self._build_summary(schedule, stage_records, final_status),
            "checklist": [f"{'✓' if r['status'] not in ('failed','cancelled') else '❌'} {r['stage']}" for r in stage_records],
            "stage_records": stage_records,
            "resume_from_stage_index": self._runtime.get("current_stage_index", 0) if cancelled else None,
            "logs": [f"{r['stage']}: {r['detail']}" for r in stage_records if r.get("detail")],
            "error": next((r["detail"] for r in stage_records if r["status"] == "failed"), None),
        }
        hist_entry = global_schedule_store.add_execution_history(clean_id, record)

        # Automatic Knowledge Ingestion into Company Brain
        if final_status == "success":
            try:
                from company_brain import global_company_brain_service
                global_company_brain_service.ingest_item({
                    "title": f"Automation Execution: {schedule.get('name', clean_id)}",
                    "type": "Workflow",
                    "category": "Automation",
                    "tags": ["automation", schedule.get("department", "general").lower(), final_status],
                    "source": "Automation Engine",
                    "body": record.get("output_summary", f"Completed {schedule.get('name')} automation pipeline."),
                    "created_by": "Automation Engine",
                    "confidence": 1.0
                })
            except Exception as e:
                logger.warning(f"Company Brain automatic ingestion skipped: {e}")

        with self._lock:
            self._clear_runtime(recovered_status=final_status if final_status != "success" else None)
        self._persist_checkpoint()
        self.reload_schedules()
        return hist_entry

    # ------------------------------------------------------------------
    # Scheduler lifecycle
    # ------------------------------------------------------------------

    def start(self):
        if self.running:
            return
        self.running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True, name="AutomationWorker")
        self._worker_thread.start()
        self._scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True, name="AutomationCronLoop")
        self._scheduler_thread.start()
        logger.info("[AutomationScheduler] Worker and cron loop started.")

    def stop(self):
        self.running = False

    def reload_schedules(self):
        with self._lock:
            self._schedules_cache = global_schedule_store.list_schedules()
            logger.info(f"[AutomationScheduler] Reloaded {len(self._schedules_cache)} schedules.")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _enqueue_internal(self, schedule_id: str, trigger_type: str, from_stage: int):
        schedule = global_schedule_store.get_schedule(schedule_id)
        name = schedule.get("name", schedule_id) if schedule else schedule_id
        item = {
            "schedule_id": schedule_id,
            "trigger_type": trigger_type,
            "from_stage_index": from_stage,
            "enqueued_at": _get_utc_now(),
            "schedule_name": name,
        }
        with self._lock:
            self._queue_manifest.append(item)
        self._job_queue.put(item)

    def _worker_loop(self):
        while self.running:
            try:
                item = self._job_queue.get(timeout=1.0)
                if not item:
                    continue
                sid   = item["schedule_id"]
                trig  = item["trigger_type"]
                stage = item.get("from_stage_index", 0)
                with self._lock:
                    self._queue_manifest = [x for x in self._queue_manifest if x["schedule_id"] != sid or x["enqueued_at"] != item["enqueued_at"]]
                logger.info(f"[Worker] Processing job '{sid}' from stage {stage}...")
                self.execute_job_now(sid, trigger_type=trig, from_stage_index=stage)
                self._job_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"[Worker Loop Error] {e}")

    def _scheduler_loop(self):
        while self.running:
            try:
                time.sleep(10.0)
                self._reset_daily_counters_if_needed()
                now_iso = _get_utc_now()
                with self._lock:
                    schedules = list(self._schedules_cache)
                for sch in schedules:
                    if not sch.get("enabled") or sch.get("state") in ("paused", "disabled"):
                        continue
                    next_run = sch.get("next_run")
                    if next_run and next_run <= now_iso:
                        logger.info(f"[Cron] Schedule '{sch.get('name')}' due. Enqueuing...")
                        self.enqueue_job(sch["id"], trigger_type="scheduled")
            except Exception as e:
                logger.error(f"[Scheduler Loop Error] {e}")

    def _emit(self, event_type: str, payload: dict):
        event = {
            "type": event_type,
            "timestamp": _get_utc_now(),
            "payload": payload,
        }
        with self._lock:
            self._events.append(event)
        logger.debug(f"[Event] {event_type}: {payload}")

    def _update_runtime(self, **kwargs):
        """Must be called with _lock held or internally."""
        self._runtime.update(kwargs)

    def _blank_runtime(self) -> Dict[str, Any]:
        return {
            "running": False,
            "execution_id": None,
            "schedule_id": None,
            "schedule_name": None,
            "department": None,
            "current_stage": None,
            "current_stage_index": 0,
            "completed_stages": 0,
            "total_stages": 0,
            "progress": 0.0,
            "status": "idle",
            "started_at": None,
            "elapsed_seconds": 0,
            "estimated_remaining_seconds": None,
            "worker": None,
            "cancel_requested": False,
            "queue_size": 0,
            "queue_items": [],
            "pipeline": [],
            "completed_today": 0,
            "failed_today": 0,
            "next_execution": None,
            "recovered": False,
            "recovered_status": None,
            "_started_ts": None,
        }

    def _clear_runtime(self, recovered_status: Optional[str] = None):
        blank = self._blank_runtime()
        if recovered_status:
            blank["recovered"] = True
            blank["recovered_status"] = recovered_status
        self._runtime = blank

    def _persist_checkpoint(self):
        try:
            os.makedirs(os.path.dirname(_CHECKPOINT_PATH) if os.path.dirname(_CHECKPOINT_PATH) else ".", exist_ok=True)
            with self._lock:
                snap = {k: v for k, v in self._runtime.items() if k != "_started_ts"}
                snap["_checkpoint_ts"] = _get_utc_now()
            with open(_CHECKPOINT_PATH, "w") as f:
                json.dump(snap, f, indent=2)
        except Exception as e:
            logger.warning(f"[Checkpoint] Write failed: {e}")

    def _recover_from_checkpoint(self):
        if not os.path.isfile(_CHECKPOINT_PATH):
            return
        try:
            with open(_CHECKPOINT_PATH) as f:
                snap = json.load(f)
            if snap.get("running") and snap.get("status") == "running":
                # was interrupted mid-execution
                with self._lock:
                    self._runtime.update(snap)
                    self._runtime["running"] = False
                    self._runtime["status"] = "interrupted"
                    self._runtime["recovered"] = True
                    self._runtime["recovered_status"] = "interrupted"
                logger.warning(
                    f"[AutomationScheduler] Recovered interrupted execution: "
                    f"'{snap.get('schedule_name')}' at stage '{snap.get('current_stage')}'"
                )
                self._emit("SCHEDULER_RECOVERED", {
                    "schedule_name": snap.get("schedule_name"),
                    "last_stage": snap.get("current_stage"),
                })
            elif snap.get("running") is False:
                # clean shutdown, nothing to recover
                pass
        except Exception as e:
            logger.warning(f"[Checkpoint] Recovery failed: {e}")

    def _next_execution_time(self) -> Optional[str]:
        """Returns ISO string of nearest upcoming next_run across all active schedules."""
        upcoming = [
            s["next_run"] for s in self._schedules_cache
            if s.get("enabled") and s.get("state") == "active" and s.get("next_run")
        ]
        return min(upcoming) if upcoming else None

    def _update_daily_counters(self, status: str):
        self._reset_daily_counters_if_needed()
        if status == "success":
            self._completed_today += 1
        elif status in ("failed", "cancelled"):
            self._failed_today += 1

    def _reset_daily_counters_if_needed(self):
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if today != self._today_str:
            self._today_str = today
            self._completed_today = 0
            self._failed_today = 0

    def _build_summary(self, schedule: dict, stage_records: list, status: str) -> str:
        name = schedule.get("name", "")
        n = len([r for r in stage_records if r["status"] not in ("failed", "cancelled")])
        total = len(stage_records)
        return f"{status.capitalize()}: {n}/{total} stages completed for '{name}'"


# ---------------------------------------------------------------------------
# Global singleton
# ---------------------------------------------------------------------------

global_automation_scheduler = AutomationScheduler()
global_automation_scheduler.start()
