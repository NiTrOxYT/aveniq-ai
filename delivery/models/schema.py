"""
Data models schema for AVENIQ Delivery Department.
Represents DeliveryManifest, PlatformBundle, PlatformProfile, AttachmentItem,
DeliveryReport, ExportBundle, DeliveryQualityGate, EditorialRef, DeliveryContext,
DeliveryPackage, and DeliveryScore.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class DeliveryContext:
    approved_content_package: Dict[str, Any]
    media_package: Dict[str, Any]
    research_package: Dict[str, Any]
    planning_report: Dict[str, Any]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class AttachmentItem:
    asset_id: str
    filename: str
    asset_type: str  # Image, Video, Carousel, Thumbnail, Diagram
    relative_path: str
    mime_type: str
    sha256_checksum: str
    file_size_bytes: int

@dataclass
class PlatformProfile:
    platform_name: str
    max_caption_length: int
    allowed_media_types: List[str]
    recommended_aspect_ratios: List[str]
    best_posting_window: str

@dataclass
class PlatformBundle:
    platform_name: str
    folder_name: str
    copy_text: str
    hashtags: List[str]
    cta_link: str
    metadata: Dict[str, Any]
    attachments: List[AttachmentItem]
    posting_recommendation: Dict[str, str]

@dataclass
class ExportBundle:
    json_path: str
    markdown_path: str
    html_path: str
    pdf_path: str
    zip_path: str

@dataclass
class DeliveryScore:
    completeness_score: float
    asset_integrity_score: float
    metadata_score: float
    platform_coverage_score: float
    export_success_score: float
    manifest_integrity_score: float
    overall_delivery_score: float

@dataclass
class DeliveryQualityGate:
    passed: bool
    score: float
    checklist: Dict[str, bool]
    diagnostics: List[str]

@dataclass
class DeliveryManifest:
    delivery_id: str
    campaign_id: str
    package_version: str
    timestamp: str
    topic: str
    platform_bundles: Dict[str, Dict[str, Any]]
    asset_inventory: List[Dict[str, Any]]
    export_formats: List[str]
    checksums: Dict[str, str]
    delivery_status: str

@dataclass
class DeliveryPackage:
    id: str
    topic: str
    date: str
    executive_summary: str
    manifest: DeliveryManifest
    platform_bundles: Dict[str, PlatformBundle]
    attachments: List[AttachmentItem]
    exports: ExportBundle
    metadata: Dict[str, Any]
    delivery_report: Dict[str, Any]
    scores: DeliveryScore
    version: str
    quality_gate: DeliveryQualityGate
    created_at: str = field(default_factory=_get_utc_now)
