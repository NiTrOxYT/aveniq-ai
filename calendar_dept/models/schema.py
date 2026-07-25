"""
Data models schema for AVENIQ Calendar & Campaign Management.
Represents CampaignItem, CalendarDay, WeeklyTheme, EventItem, MonthlyCampaign,
Calendar30Day, Roadmap90Day, DependencyGraph, CapacityPlan, ConflictReport,
CalendarMetrics, CalendarQualityGate, CalendarContext, and CalendarPackage.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class CalendarContext:
    strategy_package: Dict[str, Any]
    planning_package: Dict[str, Any]
    archive_history: List[Dict[str, Any]]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class EventItem:
    event_id: str
    name: str
    date: str
    category: str  # Industry Event, National Holiday, Product Launch, Awareness Day
    description: str

@dataclass
class CampaignItem:
    campaign_id: str
    name: str
    campaign_type: str  # Thought Leadership, Case Study, Product Launch, Educational, Feature Release
    start_date: str
    end_date: str
    priority: str  # High, Medium, Low
    target_audience: str
    platforms: List[str]
    status: str  # PLANNED, SCHEDULED, IN_PROGRESS, APPROVED, PUBLISHED, COMPLETED
    dependencies: List[str]

@dataclass
class WeeklyTheme:
    week_number: int
    start_date: str
    end_date: str
    theme_title: str
    primary_pillar: str
    secondary_pillar: str

@dataclass
class CalendarDay:
    date: str
    day_of_week: str
    scheduled_campaigns: List[str]
    events: List[EventItem]
    posting_slots: List[Dict[str, str]]

@dataclass
class Calendar30Day:
    start_date: str
    end_date: str
    days: List[CalendarDay]
    total_scheduled_posts: int

@dataclass
class Roadmap90Day:
    quarter: str
    key_objectives: List[str]
    monthly_milestones: Dict[str, List[str]]

@dataclass
class DependencyGraph:
    nodes: List[Dict[str, str]]
    edges: List[Dict[str, str]]

@dataclass
class CapacityPlan:
    writer_hours_allocated: int
    designer_hours_allocated: int
    reviewer_slots_available: int
    overbooked: bool

@dataclass
class ConflictReport:
    overlaps_detected: int
    repetition_issues: int
    blackout_violations: int
    conflicts: List[str]

@dataclass
class CalendarMetrics:
    calendar_fill_rate: float
    campaign_completion_rate: float
    pillar_balance_score: float
    platform_balance_score: float
    workload_efficiency: float

@dataclass
class CalendarQualityGate:
    passed: bool
    score: float
    checklist: Dict[str, bool]
    diagnostics: List[str]

@dataclass
class CalendarPackage:
    id: str
    date: str
    executive_summary: str
    calendar_30day: Calendar30Day
    roadmap_90day: Roadmap90Day
    campaigns: List[CampaignItem]
    weekly_themes: List[WeeklyTheme]
    events: List[EventItem]
    dependency_graph: DependencyGraph
    capacity_plan: CapacityPlan
    conflict_report: ConflictReport
    metrics: CalendarMetrics
    version: str
    quality_gate: CalendarQualityGate
    created_at: str = field(default_factory=_get_utc_now)
