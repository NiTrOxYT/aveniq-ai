"""
Editorial Storage Manager for AVENIQ Editorial Department.
Persists approved content packages, editorial reviews, and version histories to disk storage.
"""

import os, json
from typing import Dict, Any, Optional
from editorial.models.schema import ApprovedContentPackage
from brain.utils.logger import get_logger

logger = get_logger("aveniq.editorial.storage")

class EditorialStorageManager:
    def __init__(self, base_dir: str = "editorial/storage"):
        self.base_dir = base_dir
        self.reviews_dir = os.path.join(base_dir, "reviews")
        self.approvals_dir = os.path.join(base_dir, "approvals")
        self.revisions_dir = os.path.join(base_dir, "revisions")
        self.reports_dir = os.path.join(base_dir, "reports")
        self.history_dir = os.path.join(base_dir, "history")
        self.versions_dir = os.path.join(base_dir, "versions")

        for d in [self.reviews_dir, self.approvals_dir, self.revisions_dir, self.reports_dir, self.history_dir, self.versions_dir]:
            os.makedirs(d, exist_ok=True)

    def save_package(self, pkg: ApprovedContentPackage) -> str:
        filepath = os.path.join(self.approvals_dir, f"{pkg.id}.json")
        data = {
            "id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "approval_status": pkg.approval_decision.status,
            "overall_editorial_score": pkg.scorecard.overall_editorial_score,
            "ready_for_publishing": pkg.publishing_readiness.ready_for_publishing,
            "issues_count": len(pkg.issues),
            "evidence_mappings_count": len(pkg.evidence_map),
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

        logger.info(f"Saved approved content package to {filepath}")
        return filepath

    def get_latest_package(self) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.approvals_dir) if f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.approvals_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
