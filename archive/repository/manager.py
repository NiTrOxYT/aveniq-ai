"""
Archive Repository Manager for AVENIQ Archive Department.
Persists immutable archive packages, manifests, knowledge graph indexes, and version histories.
"""

import os, json
from typing import Dict, Any, Optional, List
from archive.models.schema import ArchivePackage
from brain.utils.logger import get_logger

logger = get_logger("aveniq.archive.repository")

class ArchiveRepositoryManager:
    def __init__(self, base_dir: str = "archive/repository"):
        self.base_dir = base_dir
        self.packages_dir = os.path.join(base_dir, "packages")
        self.manifests_dir = os.path.join(base_dir, "manifests")
        self.indexes_dir = os.path.join(base_dir, "indexes")
        self.history_dir = os.path.join(base_dir, "history")
        self.versions_dir = os.path.join(base_dir, "versions")

        for d in [self.packages_dir, self.manifests_dir, self.indexes_dir, self.history_dir, self.versions_dir]:
            os.makedirs(d, exist_ok=True)

    def save_package(self, pkg: ArchivePackage) -> str:
        filepath = os.path.join(self.packages_dir, f"{pkg.id}.json")
        data = {
            "id": pkg.id,
            "campaign_id": pkg.manifest.campaign_id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "lifecycle_state": pkg.lifecycle_state,
            "version": pkg.version,
            "events_count": len(pkg.events),
            "relationship_nodes": len(pkg.relationship_graph.nodes),
            "checksums": pkg.manifest.checksums,
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

        logger.info(f"Saved archive package to {filepath}")
        return filepath

    def list_archived_packages(self) -> List[Dict[str, Any]]:
        pkgs = []
        for f in sorted(os.listdir(self.packages_dir)):
            if f.endswith(".json"):
                with open(os.path.join(self.packages_dir, f), "r", encoding="utf-8") as fp:
                    pkgs.append(json.load(fp))
        return pkgs
