"""
Historical Snapshot Time-Travel Engine & Multi-Attribute Search Engine.
"""

from typing import List, Dict, Any
from archive.models.schema import SnapshotRecord, ArchiveSearchResult, ArchivePackage

class SnapshotEngine:
    @staticmethod
    def create_snapshot(campaign_id: str, version: str, state_payload: Dict[str, Any]) -> SnapshotRecord:
        return SnapshotRecord(
            snapshot_id=f"snap_{campaign_id}_{version}",
            campaign_id=campaign_id,
            version=version,
            timestamp=state_payload.get("created_at", "2026-07-25"),
            state_payload=state_payload
        )

class ArchiveSearchEngine:
    @staticmethod
    def search(query: str, packages: List[Dict[str, Any]]) -> List[ArchiveSearchResult]:
        results = []
        q_lower = query.lower()

        for pkg in packages:
            topic = pkg.get("topic", "")
            summary = pkg.get("executive_summary", "")
            pkg_id = pkg.get("id", "")
            cmp_id = pkg.get("campaign_id", "cmp_enterprise_ai_2026")

            score = 0.0
            matched_field = "None"

            if q_lower in topic.lower():
                score = 1.0
                matched_field = "topic"
            elif q_lower in summary.lower():
                score = 0.8
                matched_field = "executive_summary"
            elif q_lower in pkg_id.lower() or q_lower in cmp_id.lower():
                score = 0.9
                matched_field = "id"

            if score > 0.0:
                results.append(ArchiveSearchResult(
                    archive_id=pkg_id,
                    campaign_id=cmp_id,
                    topic=topic,
                    score=score,
                    matched_field=matched_field,
                    version=pkg.get("version", "1.0.0"),
                    created_at=pkg.get("date", "2026-07-25")
                ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results
