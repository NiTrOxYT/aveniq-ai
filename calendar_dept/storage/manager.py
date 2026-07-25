"""
Calendar Storage Manager for AVENIQ Calendar & Campaign Management.
Persists calendar packages, schedules, roadmaps, and version histories to disk storage.
"""

import os, json
from typing import Dict, Any, Optional
from calendar_dept.models.schema import CalendarPackage
from brain.utils.logger import get_logger

logger = get_logger("aveniq.calendar.storage")

class CalendarStorageManager:
    def __init__(self, base_dir: str = "calendar_dept/storage"):
        self.base_dir = base_dir
        self.calendars_dir = os.path.join(base_dir, "calendars")
        self.schedules_dir = os.path.join(base_dir, "schedules")
        self.history_dir = os.path.join(base_dir, "history")
        self.versions_dir = os.path.join(base_dir, "versions")

        for d in [self.calendars_dir, self.schedules_dir, self.history_dir, self.versions_dir]:
            os.makedirs(d, exist_ok=True)

    def save_package(self, pkg: CalendarPackage) -> str:
        filepath = os.path.join(self.calendars_dir, f"{pkg.id}.json")
        data = {
            "id": pkg.id,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "campaigns_count": len(pkg.campaigns),
            "events_count": len(pkg.events),
            "30day_posts_count": pkg.calendar_30day.total_scheduled_posts,
            "version": pkg.version,
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": pkg.quality_gate.score,
                "checklist": pkg.quality_gate.checklist
            }
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save to version control storage
        version_filepath = os.path.join(self.versions_dir, f"v_{pkg.version}_{pkg.id}.json")
        with open(version_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save to historical memory
        hist_path = os.path.join(self.history_dir, f"history_{pkg.date}_{pkg.id}.json")
        with open(hist_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved calendar package to {filepath}")
        return filepath

    def get_latest_package(self) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.calendars_dir) if f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.calendars_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
