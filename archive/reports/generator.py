"""
Archive Report Generator for Archive Department.
Formats archived packages into structured JSON audit reports.
"""

from typing import Dict, Any
from archive.engine.archive_engine import ArchiveEngine
from archive.repository.manager import ArchiveRepositoryManager

class ArchiveReportGenerator:
    def __init__(self):
        self.engine = ArchiveEngine()
        self.repository = ArchiveRepositoryManager()

    def generate_archive_report(self, topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        pkg = self.engine.archive_delivery_package(topic)
        self.repository.save_package(pkg)

        return {
            "report_type": "archive_package",
            "archive_id": pkg.id,
            "campaign_id": pkg.manifest.campaign_id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "lifecycle_state": pkg.lifecycle_state,
            "version": pkg.version,
            "manifest": {
                "archive_id": pkg.manifest.archive_id,
                "campaign_id": pkg.manifest.campaign_id,
                "created_at": pkg.manifest.created_at,
                "asset_count": pkg.manifest.asset_count,
                "relationship_count": pkg.manifest.relationship_count,
                "checksums": pkg.manifest.checksums
            },
            "events_log": [
                {
                    "id": e.event_id,
                    "type": e.event_type,
                    "timestamp": e.timestamp,
                    "payload": e.payload
                } for e in pkg.events
            ],
            "relationship_graph": {
                "nodes_count": len(pkg.relationship_graph.nodes),
                "edges_count": len(pkg.relationship_graph.edges),
                "nodes": pkg.relationship_graph.nodes
            },
            "snapshots": [
                {
                    "snapshot_id": s.snapshot_id,
                    "version": s.version,
                    "timestamp": s.timestamp
                } for s in pkg.snapshots
            ],
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": f"{pkg.quality_gate.score}%",
                "checklist": pkg.quality_gate.checklist
            }
        }
