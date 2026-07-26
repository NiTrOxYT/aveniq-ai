"""
Document Versioning and Historical Snapshot Repository.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class KnowledgeSnapshot:
    snapshot_id: str
    document_id: str
    version: int
    title: str
    content: str
    checksum: str
    created_at: str = field(default_factory=_get_utc_now)

class KnowledgeSnapshotStore:
    def __init__(self):
        self._snapshots: Dict[str, List[KnowledgeSnapshot]] = {}

    def create_snapshot(self, document_id: str, version: int, title: str, content: str, checksum: str) -> KnowledgeSnapshot:
        snap = KnowledgeSnapshot(
            snapshot_id=f"snp_{document_id}_v{version}",
            document_id=document_id,
            version=version,
            title=title,
            content=content,
            checksum=checksum
        )
        if document_id not in self._snapshots:
            self._snapshots[document_id] = []
        self._snapshots[document_id].append(snap)
        return snap

    def get_snapshots(self, document_id: str) -> List[KnowledgeSnapshot]:
        return self._snapshots.get(document_id, [])

global_snapshot_store = KnowledgeSnapshotStore()
