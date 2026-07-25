"""
Delivery Report Generator for Delivery Department.
Formats delivery packages into release-ready JSON reports.
"""

from typing import Dict, Any
from delivery.engine.delivery_engine import DeliveryEngine
from delivery.storage.manager import DeliveryStorageManager

class DeliveryReportGenerator:
    def __init__(self):
        self.engine = DeliveryEngine()
        self.storage = DeliveryStorageManager()

    def generate_delivery_report(self, topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        pkg = self.engine.assemble_delivery_package(topic)
        self.storage.save_package(pkg)

        bundles_info = {}
        for k, b in pkg.platform_bundles.items():
            bundles_info[k] = {
                "platform": b.platform_name,
                "folder": b.folder_name,
                "copy_preview": b.copy_text[:100] + "...",
                "hashtags": b.hashtags,
                "cta_link": b.cta_link,
                "attachments_count": len(b.attachments),
                "posting_window": b.posting_recommendation.get("best_posting_window")
            }

        return {
            "report_type": "delivery_package",
            "package_id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "overall_delivery_score": f"{pkg.scores.overall_delivery_score}/100",
            "version": pkg.version,
            "manifest": {
                "delivery_id": pkg.manifest.delivery_id,
                "campaign_id": pkg.manifest.campaign_id,
                "status": pkg.manifest.delivery_status,
                "checksums": pkg.manifest.checksums,
                "asset_inventory": pkg.manifest.asset_inventory
            },
            "platform_bundles": bundles_info,
            "attachments": [
                {
                    "id": a.asset_id,
                    "filename": a.filename,
                    "type": a.asset_type,
                    "path": a.relative_path,
                    "sha256": a.sha256_checksum
                } for a in pkg.attachments
            ],
            "exports": {
                "json": pkg.exports.json_path,
                "markdown": pkg.exports.markdown_path,
                "html": pkg.exports.html_path,
                "pdf": pkg.exports.pdf_path,
                "zip": pkg.exports.zip_path
            },
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": f"{pkg.quality_gate.score}%",
                "checklist": pkg.quality_gate.checklist
            },
            "scores": {
                "completeness": pkg.scores.completeness_score,
                "asset_integrity": pkg.scores.asset_integrity_score,
                "metadata": pkg.scores.metadata_score,
                "platform_coverage": pkg.scores.platform_coverage_score,
                "export_success": pkg.scores.export_success_score,
                "overall": pkg.scores.overall_delivery_score
            }
        }
