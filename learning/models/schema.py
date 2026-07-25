"""
Data models schema for AVENIQ Learning Department.
Represents PublishingAnalysis, CampaignAnalysis, TopicSummary, DuplicateReport, BrandEvolution,
RecommendationItem, KnowledgeProposal, LearningMetrics, LearningScores, LearningQualityGate,
LearningContext, and LearningPackage.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class LearningContext:
    archive_package: Dict[str, Any]
    delivery_package: Dict[str, Any]
    historical_learning_memory: Dict[str, Any]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class PublishingAnalysis:
    total_campaigns_analyzed: int
    published_posts_count: int
    platform_coverage_pct: float
    publishing_cadence: str

@dataclass
class CampaignAnalysis:
    campaign_timeline_days: int
    workflow_efficiency_score: float
    platform_distribution: Dict[str, int]

@dataclass
class TopicSummary:
    top_topics: List[str]
    emerging_topics: List[str]
    retired_topics: List[str]
    content_pillars: Dict[str, float]

@dataclass
class DuplicateReport:
    duplicate_hooks_detected: int
    duplicate_prompts_detected: int
    duplicate_headlines_detected: int
    duplicate_reduction_recommendations: List[str]

@dataclass
class BrandEvolution:
    brand_voice_consistency: float
    visual_style_evolution: str
    tone_stability_score: float

@dataclass
class RecommendationItem:
    id: str
    target_department: str  # Strategy, Research, Planning, Content, Creative, Editorial, Delivery
    recommendation_text: str
    rationale: str
    confidence_score: float
    lifecycle_state: str   # PROPOSED, APPROVED, IMPLEMENTED, REJECTED, SUPERSEDED
    expected_benefit: str

@dataclass
class KnowledgeProposal:
    proposal_id: str
    target_file: str  # e.g., taxonomy.yaml, relationships.yaml, config.yaml
    proposed_change: str
    evidence_citation: str
    confidence_score: float
    review_status: str  # Pending Review, Approved, Integrated

@dataclass
class LearningMetrics:
    duplicate_reduction_rate: float
    content_diversity_score: float
    brand_consistency_score: float
    recommendation_acceptance_rate: float
    knowledge_growth_rate: float

@dataclass
class LearningScores:
    analysis_completeness_score: float
    pattern_recognition_score: float
    recommendation_confidence_score: float
    proposal_validity_score: float
    overall_learning_score: float

@dataclass
class LearningQualityGate:
    passed: bool
    score: float
    checklist: Dict[str, bool]
    diagnostics: List[str]

@dataclass
class LearningPackage:
    id: str
    date: str
    executive_summary: str
    publishing_analysis: PublishingAnalysis
    campaign_analysis: CampaignAnalysis
    topic_summary: TopicSummary
    duplicate_report: DuplicateReport
    brand_evolution: BrandEvolution
    recommendations: List[RecommendationItem]
    knowledge_proposals: List[KnowledgeProposal]
    learning_metrics: LearningMetrics
    scores: LearningScores
    version: str
    quality_gate: LearningQualityGate
    created_at: str = field(default_factory=_get_utc_now)
