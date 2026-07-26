"""
LearningEvent, KnowledgeProposal, and CampaignScorecard Data Models.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class ProposalState(str, Enum):
    PROPOSED = "PROPOSED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    IMPLEMENTED = "IMPLEMENTED"
    ACTIVE = "ACTIVE"

class ProposalCategory(str, Enum):
    BRAND = "Brand"
    CREATIVE = "Creative"
    CONTENT = "Content"
    SCHEDULING = "Scheduling"
    AUDIENCE = "Audience"
    SEO = "SEO"
    PUBLISHING = "Publishing"
    PERFORMANCE = "Performance"
    KNOWLEDGE = "Knowledge"
    OPERATIONAL = "Operational"

@dataclass
class LearningEvent:
    event_id: str
    workspace_id: str
    execution_id: str
    campaign_id: str
    department: str
    event_type: str  # CONTENT_APPROVED, CONTENT_REJECTED, IMAGE_REGENERATED, CAMPAIGN_PUBLISHED, LOW_CTR, HIGH_ENGAGEMENT, BRAND_VIOLATION
    confidence: float = 0.95
    metadata: Dict[str, Any] = field(default_factory=dict)
    evidence: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=_get_utc_now)

@dataclass
class ImpactSimulation:
    expected_ctr_change: float = 0.0
    expected_conversion_delta: float = 0.0
    approval_probability: float = 0.90
    confidence_interval: str = "95%"

@dataclass
class KnowledgeProposal:
    proposal_id: str
    workspace_id: str
    category: ProposalCategory
    title: str
    description: str
    proposed_change: str
    confidence: float
    evidence_count: int
    campaign_count: int
    simulation: ImpactSimulation = field(default_factory=ImpactSimulation)
    evidence_list: List[str] = field(default_factory=list)
    state: ProposalState = ProposalState.PROPOSED
    approving_user: Optional[str] = None
    created_at: str = field(default_factory=_get_utc_now)
    approved_at: Optional[str] = None

@dataclass
class CampaignScorecard:
    campaign_id: str
    workspace_id: str
    overall_score: float  # 0 to 100
    content_quality_score: float
    visual_quality_score: float
    brand_consistency_score: float
    approval_latency_mins: float
    ctr: float
    conversion_rate: float
    timestamp: str = field(default_factory=_get_utc_now)
