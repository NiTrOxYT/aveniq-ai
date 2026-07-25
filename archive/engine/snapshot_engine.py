"""
Historical Snapshot Time-Travel Engine for Archive Department.
"""

from typing import Dict, Any
from archive.models.schema import SnapshotRecord

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
