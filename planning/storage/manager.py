"""
Planning Storage Manager for AVENIQ Planning Department.
Persists planning packages, campaign plans, and version histories to disk storage.
"""

import os, json
from typing import Dict, Any, Optional
from planning.models.schema import PlanningPackage
from brain.utils.logger import get_logger

logger = get_logger("aveniq.planning.storage")

class PlanningStorageManager:
    def __init__(self, base_dir: str = "planning/storage"):
        self.base_dir = base_dir
        self.campaigns_dir = os.path.join(base_dir, "campaigns")
        self.schedules_dir = os.path.join(base_dir, "schedules")
        self.calendars_dir = os.path.join(base_dir, "calendars")
        self.assets_dir = os.path.join(base_dir, "assets")
        self.workflows_dir = os.path.join(base_dir, "workflows")
        self.versions_dir = os.path.join(base_dir, "versions")
        self.history_dir = os.path.join(base_dir, "history")

        for d in [self.campaigns_dir, self.schedules_dir, self.calendars_dir, self.assets_dir, self.workflows_dir, self.versions_dir, self.history_dir]:
            os.makedirs(d, exist_ok=True)

    def save_package(self, pkg: PlanningPackage) -> str:
        filepath = os.path.join(self.campaigns_dir, f"{pkg.id}.json")
        data = {
            "id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "confidence_score": pkg.confidence_score,
            "campaign": {
                "id": pkg.campaign.id,
                "name": pkg.campaign.name,
                "theme": pkg.campaign.theme,
                "duration_days": pkg.campaign.duration_days,
                "milestones": pkg.campaign.milestones
            },
            "production_timeline": pkg.production_timeline,
            "deliverables_count": len(pkg.deliverables),
            "version_info": {
                "version": pkg.version_info.version,
                "timestamp": pkg.version_info.timestamp,
                "approval_status": pkg.version_info.approval_status
            },
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": pkg.quality_gate.score,
                "checklist": pkg.quality_gate.checklist
            }
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save to version control storage
        version_filepath = os.path.join(self.versions_dir, f"v_{pkg.version_info.version}_{pkg.id}.json")
        with open(version_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save to historical memory
        hist_path = os.path.join(self.history_dir, f"history_{pkg.date}_{pkg.id}.json")
        with open(hist_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved planning package to {filepath}")
        return filepath

    def get_latest_package(self) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.campaigns_dir) if f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.campaigns_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
