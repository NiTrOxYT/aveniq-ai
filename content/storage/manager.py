"""
Content Storage Manager for AVENIQ Content Department.
Persists content packages, articles, social copy, and version histories to disk storage.
"""

import os, json
from typing import Dict, Any, Optional
from content.models.schema import ContentPackage
from brain.utils.logger import get_logger

logger = get_logger("aveniq.content.storage")

class ContentStorageManager:
    def __init__(self, base_dir: str = "content/storage"):
        self.base_dir = base_dir
        self.packages_dir = os.path.join(base_dir, "packages")
        self.history_dir = os.path.join(base_dir, "history")
        self.drafts_dir = os.path.join(base_dir, "drafts")
        self.published_dir = os.path.join(base_dir, "published")
        self.versions_dir = os.path.join(base_dir, "versions")

        for d in [self.packages_dir, self.history_dir, self.drafts_dir, self.published_dir, self.versions_dir]:
            os.makedirs(d, exist_ok=True)

    def save_package(self, pkg: ContentPackage) -> str:
        filepath = os.path.join(self.packages_dir, f"{pkg.id}.json")
        data = {
            "id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "master_article_title": pkg.master_article.title,
            "word_count": pkg.master_article.word_count,
            "overall_score": pkg.scores.overall_score,
            "workflow_state": pkg.workflow_state.current_state,
            "version_info": {
                "version": pkg.version_info.version,
                "timestamp": pkg.version_info.timestamp,
                "author": pkg.version_info.author
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

        logger.info(f"Saved content package to {filepath}")
        return filepath

    def get_latest_package(self) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.packages_dir) if f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.packages_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
