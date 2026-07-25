"""
Learning Storage Manager for AVENIQ Learning Department.
Persists learning packages, recommendations, knowledge proposals, and version histories to disk storage.
"""

import os, json
from typing import Dict, Any, Optional
from learning.models.schema import LearningPackage
from brain.utils.logger import get_logger

logger = get_logger("aveniq.learning.storage")

class LearningStorageManager:
    def __init__(self, base_dir: str = "learning/storage"):
        self.base_dir = base_dir
        self.learning_dir = os.path.join(base_dir, "learning")
        self.proposals_dir = os.path.join(base_dir, "proposals")
        self.history_dir = os.path.join(base_dir, "history")
        self.versions_dir = os.path.join(base_dir, "versions")

        for d in [self.learning_dir, self.proposals_dir, self.history_dir, self.versions_dir]:
            os.makedirs(d, exist_ok=True)

    def save_package(self, pkg: LearningPackage) -> str:
        filepath = os.path.join(self.learning_dir, f"{pkg.id}.json")
        data = {
            "id": pkg.id,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "overall_learning_score": pkg.scores.overall_learning_score,
            "recommendations_count": len(pkg.recommendations),
            "proposals_count": len(pkg.knowledge_proposals),
            "version": pkg.version,
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": pkg.quality_gate.score,
                "checklist": pkg.quality_gate.checklist
            }
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save proposals separately
        prop_file = os.path.join(self.proposals_dir, f"proposals_{pkg.id}.json")
        prop_data = [
            {
                "id": p.proposal_id,
                "target_file": p.target_file,
                "change": p.proposed_change,
                "citation": p.evidence_citation,
                "confidence": p.confidence_score,
                "status": p.review_status
            } for p in pkg.knowledge_proposals
        ]
        with open(prop_file, "w", encoding="utf-8") as f:
            json.dump(prop_data, f, indent=2)

        # Save to version control storage
        version_filepath = os.path.join(self.versions_dir, f"v_{pkg.version}_{pkg.id}.json")
        with open(version_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save to historical memory
        hist_path = os.path.join(self.history_dir, f"history_{pkg.date}_{pkg.id}.json")
        with open(hist_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved learning package to {filepath}")
        return filepath

    def get_latest_package(self) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.learning_dir) if f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.learning_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
