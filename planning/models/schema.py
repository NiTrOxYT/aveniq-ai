"""
Data models schema for AVENIQ Planning Department.
Represents CampaignPlan, EditorialSchedule, PublishingCalendar, AssetChecklist, CTAPlan,
FunnelPlan, DistributionPlan, WorkflowDiagram, DependencyGraph, PlanningPackage,
PlanningQualityGate, PlanningContext, RiskAssessment, CapacityEstimate, and CampaignVersion.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class PlanningContext:
    strategy_report: Dict[str, Any]
    research_package: Dict[str, Any]
    company_context: Dict[str, Any]
    brand_guidelines: Dict[str, Any]
    historical_campaigns: List[Dict[str, Any]]
    publishing_history: Dict[str, Any]
    business_goals: List[str]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class AssetChecklist:
    hero_image: str
    infographics: List[str]
    architecture_diagrams: List[str]
    charts: List[str]
    screenshots: List[str]
    code_snippets: List[str]
    demo_gifs: List[str]
    required_logos_icons: List[str]

@dataclass
class CTAPlan:
    primary_cta: str
    secondary_cta: str
    lead_magnet_url: str
    newsletter_signup_url: str
    discovery_consultation_url: str
    github_repo_url: str

@dataclass
class FunnelPlan:
    awareness_deliverables: List[str]
    consideration_deliverables: List[str]
    decision_deliverables: List[str]
    retention_deliverables: List[str]
    expansion_deliverables: List[str]

@dataclass
class DistributionPlan:
    channels: List[str]
    platform_schedules: Dict[str, str]
    cross_posting_sequence: List[str]
    timezone_optimal_hours: List[str]

@dataclass
class WorkflowDiagram:
    current_state: str  # Draft, Internal Review, Approved, Scheduled, Executing, Completed, Archived
    sequential_steps: List[str]
    step_owners: Dict[str, str]

@dataclass
class DependencyNode:
    deliverable_id: str
    title: str
    requires: List[str]
    produces: List[str]
    blocks: List[str]
    depends_on: List[str]

@dataclass
class DependencyGraph:
    nodes: List[DependencyNode]
    critical_path: List[str]
    max_dependency_depth: int

@dataclass
class EditorialSchedule:
    content_sequence: List[str]
    publishing_order: List[str]
    topic_progression: List[str]
    internal_linking_strategy: List[str]
    user_journey_map: List[str]

@dataclass
class PublishingCalendar:
    daily_schedule: Dict[str, str]
    weekly_schedule: Dict[str, List[str]]
    monthly_calendar: Dict[str, List[str]]
    timezone_aware_plan: str

@dataclass
class RiskAssessment:
    risk_score: float  # 0.0 to 100.0 (lower is safer)
    schedule_conflicts: List[str]
    resource_overload: List[str]
    missing_dependencies: List[str]
    mitigation_plan: List[str]

@dataclass
class CapacityEstimate:
    deliverable_count: int
    estimated_production_hours: float
    estimated_review_hours: float
    creative_workload_score: float
    publishing_workload_score: float

@dataclass
class CampaignVersion:
    version: str
    timestamp: str
    planner_id: str
    update_reason: str
    approval_status: str

@dataclass
class PlanningQualityGate:
    passed: bool
    score: float  # 0.0 to 100.0
    checklist: Dict[str, bool]
    diagnostics: List[str]

@dataclass
class CampaignPlan:
    id: str
    name: str
    theme: str
    duration_days: int
    milestones: List[str]
    stages: List[str]

@dataclass
class PlanningPackage:
    id: str
    topic: str
    date: str
    executive_summary: str
    campaign_objective: str
    campaign: CampaignPlan
    production_timeline: str
    editorial_calendar: EditorialSchedule
    publishing_schedule: PublishingCalendar
    deliverables: List[str]
    required_assets: AssetChecklist
    dependency_graph: DependencyGraph
    risk_assessment: RiskAssessment
    resource_estimate: CapacityEstimate
    cta_plan: CTAPlan
    funnel_plan: FunnelPlan
    distribution_plan: DistributionPlan
    workflow_diagram: WorkflowDiagram
    approval_checklist: List[str]
    success_metrics: List[str]
    confidence_score: float
    version_info: CampaignVersion
    quality_gate: PlanningQualityGate
    created_at: str = field(default_factory=_get_utc_now)
