"""
Data models schema for AVENIQ Archive Department.
Represents CampaignRecord, PostRecord, ResearchRecord, PlanningRecord, ContentRecord,
CreativeRecord, EditorialReportRecord, DeliveryRecord, MediaAssetRecord, RelationshipGraph,
ArchiveEvent, SnapshotRecord, ArchiveManifest, ArchivePackage, ArchiveQualityGate,
ArchiveContext, and ArchiveSearchResult.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class ArchiveContext:
    delivery_package: Dict[str, Any]
    approved_content_package: Dict[str, Any]
    media_package: Dict[str, Any]
    research_package: Dict[str, Any]
    planning_report: Dict[str, Any]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class ArchiveEvent:
    event_id: str
    event_type: str  # PlanningCreated, ResearchCompleted, ContentGenerated, CreativeApproved, EditorialPassed, DeliveryPackaged, ArchiveStored
    aggregate_id: str
    timestamp: str
    payload: Dict[str, Any]

@dataclass
class SnapshotRecord:
    snapshot_id: str
    campaign_id: str
    version: str
    timestamp: str
    state_payload: Dict[str, Any]

@dataclass
class RelationshipGraph:
    nodes: List[Dict[str, str]]
    edges: List[Dict[str, str]]

@dataclass
class ArchiveManifest:
    archive_id: str
    campaign_id: str
    version: str
    created_at: str
    topic: str
    asset_count: int
    relationship_count: int
    checksums: Dict[str, str]
    lifecycle_state: str  # ACTIVE, ARCHIVED, SUPERSEDED, RESTORED, LOCKED

@dataclass
class ArchiveSearchResult:
    archive_id: str
    campaign_id: str
    topic: str
    score: float
    matched_field: str
    version: str
    created_at: str

@dataclass
class ArchiveQualityGate:
    passed: bool
    score: float
    checklist: Dict[str, bool]
    diagnostics: List[str]

@dataclass
class ArchivePackage:
    id: str
    topic: str
    date: str
    executive_summary: str
    manifest: ArchiveManifest
    events: List[ArchiveEvent]
    snapshots: List[SnapshotRecord]
    relationship_graph: RelationshipGraph
    campaign_record: Dict[str, Any]
    content_record: Dict[str, Any]
    creative_record: Dict[str, Any]
    editorial_record: Dict[str, Any]
    delivery_record: Dict[str, Any]
    vector_embedding: List[float]
    lifecycle_state: str
    version: str
    quality_gate: ArchiveQualityGate
    created_at: str = field(default_factory=_get_utc_now)
