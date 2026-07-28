"""
Typed Artifact system for AVENIQ AI v2 Native Workflow Engine.
Provides strong contracts, validation, and structured storage for agent outputs.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class BaseArtifact:
    artifact_id: str
    artifact_type: str
    created_at: str = field(default_factory=_get_utc_now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ResearchArtifact(BaseArtifact):
    artifact_type: str = "research"
    trends: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    market_signals: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SEOArtifact(BaseArtifact):
    artifact_type: str = "seo"
    primary_keywords: List[str] = field(default_factory=list)
    secondary_keywords: List[str] = field(default_factory=list)
    title: str = ""
    meta_description: str = ""
    faqs: List[Dict[str, str]] = field(default_factory=list)
    internal_linking_ideas: List[str] = field(default_factory=list)

@dataclass
class BlogArtifact(BaseArtifact):
    artifact_type: str = "blog"
    title: str = ""
    body: str = ""
    word_count: int = 0
    cta: str = ""
    citations: List[str] = field(default_factory=list)

@dataclass
class SocialPostArtifact(BaseArtifact):
    artifact_type: str = "social"
    platform: str = "general"
    content: str = ""
    hashtags: List[str] = field(default_factory=list)
    cta: str = ""

@dataclass
class ImageArtifact(BaseArtifact):
    artifact_type: str = "image"
    prompt: str = ""
    image_url: str = ""
    provider: str = "imagen"

@dataclass
class CarouselArtifact(BaseArtifact):
    artifact_type: str = "carousel"
    slides: List[Dict[str, Any]] = field(default_factory=list)
    pdf_url: Optional[str] = None

@dataclass
class QualityArtifact(BaseArtifact):
    artifact_type: str = "quality"
    overall_score: float = 100.0
    passed: bool = True
    checks: Dict[str, Any] = field(default_factory=dict)
    feedback: str = ""
