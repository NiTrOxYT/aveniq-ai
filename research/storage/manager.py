"""
Research Storage Manager for AVENIQ Research Department.
Persists research packages and structured evidence items to disk.
"""

import os, json
from typing import Dict, Any, Optional
from research.models.schema import ResearchPackage
from brain.utils.logger import get_logger

logger = get_logger("aveniq.research.storage")

class ResearchStorageManager:
    def __init__(self, base_dir: str = "research/storage"):
        self.base_dir = base_dir
        self.daily_dir = os.path.join(base_dir, "daily")
        self.packages_dir = os.path.join(base_dir, "packages")
        self.sources_dir = os.path.join(base_dir, "sources")
        self.statistics_dir = os.path.join(base_dir, "statistics")
        self.studies_dir = os.path.join(base_dir, "studies")
        self.competitors_dir = os.path.join(base_dir, "competitors")
        self.examples_dir = os.path.join(base_dir, "examples")
        self.seo_dir = os.path.join(base_dir, "seo")
        self.history_dir = os.path.join(base_dir, "history")

        for d in [self.daily_dir, self.packages_dir, self.sources_dir, self.statistics_dir, self.studies_dir, self.competitors_dir, self.examples_dir, self.seo_dir, self.history_dir]:
            os.makedirs(d, exist_ok=True)

    def save_package(self, pkg: ResearchPackage) -> str:
        filepath = os.path.join(self.packages_dir, f"{pkg.id}.json")
        data = {
            "id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "confidence_score": pkg.confidence_score,
            "key_findings": pkg.key_findings,
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": pkg.quality_gate.score,
                "gate_checks": pkg.quality_gate.gate_checks,
                "diagnostics": pkg.quality_gate.diagnostics
            },
            "statistics_count": len(pkg.verified_statistics),
            "studies_count": len(pkg.supporting_studies),
            "technical_claims_count": len(pkg.technical_validation),
            "citations_count": len(pkg.citations)
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save to historical history
        hist_path = os.path.join(self.history_dir, f"history_{pkg.date}_{pkg.id}.json")
        with open(hist_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved research package to {filepath}")
        return filepath

    def get_latest_package(self) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.packages_dir) if f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.packages_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
