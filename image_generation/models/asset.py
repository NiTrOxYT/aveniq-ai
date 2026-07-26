"""
VisualAsset, CarouselAsset, and GenerationJob Batch Data Models.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class AssetApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REGENERATING = "REGENERATING"

@dataclass
class VisualAsset:
    asset_id: str
    campaign_id: str
    template_type: str  # hero, carousel, infographic, thumbnail, reel_cover, story, banner, linkedin, square_post, email_header
    platform: str      # linkedin, instagram, facebook, youtube, blog, email, website
    file_path: str
    width: int
    height: int
    aspect_ratio: str
    version: int = 1
    approval_status: AssetApprovalStatus = AssetApprovalStatus.PENDING
    prompt_used: str = ""
    provider_used: str = "gemini_image"
    feedback_tag: Optional[str] = None
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class CarouselAsset:
    carousel_id: str
    campaign_id: str
    title: str
    slides: List[VisualAsset] = field(default_factory=list)
    aspect_ratio: str = "1:1"
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class GenerationJob:
    job_id: str
    campaign_id: str
    workspace_id: str
    status: str = "IN_PROGRESS"
    requested_templates: List[str] = field(default_factory=list)
    generated_assets: List[VisualAsset] = field(default_factory=list)
    created_at: str = field(default_factory=_get_utc_now)
