"""
Data models schema for AVENIQ Human Approval System.
Represents ApprovalSession, HumanDecision, ActionRequest, TelegramDashboardMarkup,
FeedbackRecord, ReviewComment, TimelineEvent, ApprovalMetrics, ApprovalQualityGate, and ApprovalContext.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class ApprovalContext:
    delivery_package: Dict[str, Any]
    editorial_report: Dict[str, Any]
    media_package: Dict[str, Any]
    research_package: Dict[str, Any]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class TimelineEvent:
    event_id: str
    event_type: str
    actor: str
    timestamp: str
    details: str

@dataclass
class ActionRequest:
    action_id: str
    action_type: str  # Approve, Reject, Regenerate, Rewrite, Technical, Simplify
    target_department: str  # Strategy, Research, Planning, Content, Creative, Editorial, Delivery, Archive
    reviewer_id: str
    notes: str
    timestamp: str = field(default_factory=_get_utc_now)

@dataclass
class HumanDecision:
    session_id: str
    decision: str  # Approved, Rejected, Changes Requested
    reviewer_id: str
    rationale: str
    timestamp: str = field(default_factory=_get_utc_now)

@dataclass
class ReviewComment:
    comment_id: str
    reviewer: str
    timestamp: str
    comment_text: str
    related_action: str

@dataclass
class TelegramDashboardMarkup:
    card_text: str
    inline_keyboard: List[List[Dict[str, str]]]

@dataclass
class FeedbackRecord:
    feedback_id: str
    target_department: str
    requested_change: str
    reviewer_notes: str

@dataclass
class ApprovalMetrics:
    review_duration_seconds: int
    approval_rate: float
    regeneration_rate: float
    revision_count: int

@dataclass
class ApprovalQualityGate:
    passed: bool
    score: float
    checklist: Dict[str, bool]
    diagnostics: List[str]

@dataclass
class ApprovalSession:
    id: str
    topic: str
    date: str
    current_state: str  # CREATED, PENDING_REVIEW, IN_REVIEW, CHANGES_REQUESTED, REGENERATING, APPROVED, REJECTED, ARCHIVED
    executive_summary: str
    telegram_markup: TelegramDashboardMarkup
    decision: Optional[HumanDecision]
    timeline: List[TimelineEvent]
    action_requests: List[ActionRequest]
    comments: List[ReviewComment]
    feedback_records: List[FeedbackRecord]
    metrics: ApprovalMetrics
    version: str
    quality_gate: ApprovalQualityGate
    created_at: str = field(default_factory=_get_utc_now)
