"""
Data models schema for AVENIQ Strategy Department.
Represents MarketingPlan, CampaignPlan, AudienceProfile, KeywordPlan,
ContentRecommendation, Opportunity, PriorityScore, StrategyReport, StrategyContext, and DecisionReasoning.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class AudienceProfile:
    primary_audience: str
    secondary_audience: str
    buying_intent: str  # High, Medium, Low
    awareness_stage: str  # Problem-Aware, Solution-Aware, Product-Aware, Most Aware
    business_size: str
    industry: str
    customer_persona: str
    priority_score: float
    reasoning: str

@dataclass
class KeywordPlan:
    primary_keyword: str
    secondary_keywords: List[str]
    search_intent: str  # Informational, Commercial, Transactional, Navigational
    difficulty: str  # Low, Medium, High
    content_cluster: str
    recommended_landing_pages: List[str]
    internal_linking_opportunities: List[str]

@dataclass
class ContentRecommendation:
    category: str  # Educational, Authority, Case Study, Myth Busting, Framework, etc.
    content_format: str  # Article, Interactive Guide, Infographic, Video Script Outline
    suggested_title: str
    value_proposition: str
    unique_angle: str
    differentiator: str
    target_platforms: List[str]
    call_to_action: str

@dataclass
class PriorityScore:
    overall_score: float  # 0 to 100
    confidence: float     # 0.0 to 1.0
    trend_growth_score: float
    audience_fit_score: float
    business_value_score: float
    competition_score: float
    seo_potential_score: float
    revenue_impact_score: float
    brand_alignment_score: float
    reasoning: str

@dataclass
class Opportunity:
    id: str
    title: str
    topic: str
    category: str
    target_industry: str
    source_channels: List[str]
    priority_score: PriorityScore
    raw_signals: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class CampaignPlan:
    id: str
    name: str  # e.g., "AI Week", "Startup Week", "Restaurant Automation Week"
    goal: str
    duration_days: int
    primary_audience: str
    content_mix: List[str]
    target_platforms: List[str]
    call_to_action: str
    expected_outcome: str

@dataclass
class DecisionReasoning:
    publish_today: bool
    primary_reason: str
    supporting_evidence: List[str]
    confidence_score: float
    business_goal: str
    expected_impact: str

@dataclass
class MarketingPlan:
    id: str
    date: str
    primary_goal: str
    business_objective: str
    publish_today: bool
    audience: AudienceProfile
    content: ContentRecommendation
    seo: KeywordPlan
    campaign: Optional[CampaignPlan]
    decision_reasoning: DecisionReasoning
    opportunity: Opportunity
    priority_score: int
    confidence_percentage: float
    expected_result: List[str]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class StrategyContext:
    company_context: Dict[str, Any]
    market_intelligence: Dict[str, Any]
    business_goals: List[str]
    active_campaigns: List[Dict[str, Any]]
    publishing_calendar: Dict[str, Any]
    historical_performance: Dict[str, Any]
    brand_guardrails: Dict[str, Any]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class StrategyReport:
    report_type: str  # daily, weekly, monthly
    date: str
    summary: str
    primary_marketing_plan: Optional[MarketingPlan]
    weekly_campaign_mix: List[Dict[str, Any]] = field(default_factory=list)
    monthly_roadmap: Dict[str, Any] = field(default_factory=dict)
    top_opportunities: List[Opportunity] = field(default_factory=list)
    analytics_snapshot: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_get_utc_now)
