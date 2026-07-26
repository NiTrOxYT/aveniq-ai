"""
Data models schema for AVENIQ Brand Growth Intelligence.
Represents BusinessGoal, ObjectiveTree, KPIForecast, GrowthPlan, ScenarioAnalysis,
CampaignPortfolioItem, FunnelAllocation, ContentMix, GrowthMetrics, GrowthQualityGate,
GrowthContext, and GrowthPackage.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class CalendarContextRef:
    strategy_package: Dict[str, Any]
    calendar_package: Dict[str, Any]
    archive_history: List[Dict[str, Any]]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class BusinessGoal:
    goal_id: str
    title: str
    target_metric: str
    target_value: float
    current_value: float
    deadline: str
    priority: str  # Critical, High, Medium

@dataclass
class ObjectiveTree:
    annual_goal: str
    quarterly_objectives: List[str]
    monthly_campaign_goals: List[str]
    weekly_initiatives: List[str]

@dataclass
class KPIForecast:
    expected_leads: int
    expected_reach: int
    expected_newsletter_subscribers: int
    expected_demo_requests: int
    expected_conversions: int
    confidence_score: float

@dataclass
class ScenarioAnalysis:
    scenario_name: str  # Conservative, Balanced, Aggressive
    projected_leads: int
    projected_reach: int
    required_campaigns_count: int

@dataclass
class CampaignPortfolioItem:
    portfolio_id: str
    campaign_name: str
    campaign_type: str  # Educational Series, Case Study, Founder Story, Tutorial, Product Announcement, Lead Magnet, Webinar
    funnel_stage: str   # Awareness, Interest, Consideration, Evaluation, Decision, Retention, Advocacy
    target_kpi: str
    allocated_weight_pct: float

@dataclass
class FunnelAllocation:
    awareness_pct: float
    interest_pct: float
    consideration_pct: float
    evaluation_pct: float
    decision_pct: float
    retention_pct: float
    advocacy_pct: float

@dataclass
class ContentMix:
    educational_pct: float
    thought_leadership_pct: float
    case_study_pct: float
    product_pct: float
    community_pct: float

@dataclass
class GrowthMetrics:
    kpi_coverage_score: float
    funnel_balance_score: float
    portfolio_diversity_score: float
    capacity_alignment_score: float
    overall_growth_score: float

@dataclass
class GrowthQualityGate:
    passed: bool
    score: float
    checklist: Dict[str, bool]
    diagnostics: List[str]

@dataclass
class GrowthPackage:
    id: str
    date: str
    executive_summary: str
    goals: List[BusinessGoal]
    objective_tree: ObjectiveTree
    kpi_forecast: KPIForecast
    scenarios: List[ScenarioAnalysis]
    portfolio: List[CampaignPortfolioItem]
    funnel_allocation: FunnelAllocation
    content_mix: ContentMix
    metrics: GrowthMetrics
    version: str
    quality_gate: GrowthQualityGate
    created_at: str = field(default_factory=_get_utc_now)
