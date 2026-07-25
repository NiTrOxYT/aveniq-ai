"""
Delivery Storage Manager for AVENIQ Delivery Department.
Persists delivery packages, manifests, export bundles, and version histories to disk storage.
"""

import os, json
from typing import Dict, Any, Optional
from delivery.models.schema import DeliveryPackage
from brain.utils.logger import get_logger

logger = get_logger("aveniq.delivery.storage")

class DeliveryStorageManager:
    def __init__(self, base_dir: str = "delivery/storage"):
        self.base_dir = base_dir
        self.deliveries_dir = os.path.join(base_dir, "deliveries")
        self.exports_dir = os.path.join(base_dir, "exports")
        self.history_dir = os.path.join(base_dir, "history")
        self.versions_dir = os.path.join(base_dir, "versions")

        for d in [self.deliveries_dir, self.exports_dir, self.history_dir, self.versions_dir]:
            os.makedirs(d, exist_ok=True)

    def save_package(self, pkg: DeliveryPackage) -> str:
        filepath = os.path.join(self.deliveries_dir, f"{pkg.id}.json")
        data = {
            "id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "overall_delivery_score": pkg.scores.overall_delivery_score,
            "delivery_status": pkg.manifest.delivery_status,
            "export_zip_path": pkg.exports.zip_path,
            "platform_bundles_count": len(pkg.platform_bundles),
            "attachments_count": len(pkg.attachments),
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

        logger.info(f"Saved delivery package to {filepath}")
        return filepath

    def get_latest_package(self) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.deliveries_dir) if f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.deliveries_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
