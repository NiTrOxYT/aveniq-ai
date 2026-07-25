"""
Data models schema for AVENIQ Creative Department.
Represents VisualStyle, HeroBrief, InfographicSpec, CarouselDesign, ComparisonChartSpec,
ArchitectureDiagramSpec, ThumbnailSpec, VideoStoryboard, AIPrompts, MediaPackage,
CreativeQualityGate, CreativeVersion, CreativeContext, CreativeSpecification, SceneGraph, and CreativeScores.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class VisualStyle:
    style_name: str
    color_palette: Dict[str, str]  # primary, accent, background, text
    typography_primary: str
    typography_secondary: str
    mood: str
    lighting: str
    camera_angle: str
    composition_rule: str

@dataclass
class AIPrompts:
    dalle3_prompt: str
    midjourney_prompt: str
    flux_prompt: str
    sdxl_positive_prompt: str
    sdxl_negative_prompt: str
    sora_video_prompt: str
    runway_motion_prompt: str

@dataclass
class SceneGraph:
    background: str
    foreground: str
    primary_subject: str
    secondary_subject: str
    environment: str
    lighting: str
    camera: str
    text_elements: List[str]
    brand_elements: List[str]

@dataclass
class CreativeSpecification:
    asset_id: str
    asset_type: str
    intent: str
    audience: str
    composition: str
    scene_graph: SceneGraph
    prompts: AIPrompts

@dataclass
class HeroBrief:
    title: str
    concept_summary: str
    spec: CreativeSpecification
    aspect_ratios: Dict[str, str]

@dataclass
class InfographicSpec:
    title: str
    process_steps: List[Dict[str, str]]
    spec: CreativeSpecification

@dataclass
class CarouselDesign:
    title: str
    slides: List[Dict[str, Any]]
    total_slides: int
    cta_slide: Dict[str, str]

@dataclass
class VideoStoryboard:
    video_title: str
    duration_seconds: int
    scenes: List[Dict[str, Any]]
    voiceover_script: str
    subtitle_script: str
    video_prompt: str

@dataclass
class ThumbnailSpec:
    headline_text: str
    contrast_focal_point: str
    thumbnail_prompt: str

@dataclass
class CreativeScores:
    brand_alignment_score: float
    composition_score: float
    readability_score: float
    contrast_score: float
    prompt_quality_score: float
    accessibility_score: float
    platform_optimization_score: float
    overall_score: float

@dataclass
class CreativeQualityGate:
    passed: bool
    score: float
    checklist: Dict[str, bool]
    diagnostics: List[str]

@dataclass
class CreativeVersion:
    version: str
    timestamp: str
    director_id: str
    content_version: str
    planning_version: str

@dataclass
class CreativeContext:
    planning_report: Dict[str, Any]
    research_package: Dict[str, Any]
    content_package: Dict[str, Any]
    brand_guidelines: Dict[str, Any]
    design_system: Dict[str, Any]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class MediaPackage:
    id: str
    topic: str
    date: str
    executive_summary: str
    visual_theme: str
    style_guide: VisualStyle
    hero_brief: HeroBrief
    infographic: InfographicSpec
    carousel_design: CarouselDesign
    architecture_diagram_spec: Dict[str, Any]
    thumbnail: ThumbnailSpec
    video_storyboard: VideoStoryboard
    captions_and_alt_text: Dict[str, str]
    export_specifications: Dict[str, List[str]]
    scores: CreativeScores
    version_info: CreativeVersion
    quality_gate: CreativeQualityGate
    created_at: str = field(default_factory=_get_utc_now)
