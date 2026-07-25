"""
Data models schema for AVENIQ Editorial Department.
Represents EditorialScorecard, ApprovalDecision, ClaimVerification, HallucinationCheck,
CopyrightCheck, EditorialIssue, EvidenceMap, RedFlagItem, PublishingReadiness,
ApprovedContentPackage, EditorialQualityGate, EditorialContext, and RevisionRecord.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class EditorialContext:
    content_package: Dict[str, Any]
    research_package: Dict[str, Any]
    planning_report: Dict[str, Any]
    brand_guidelines: Dict[str, Any]
    legal_rules: Dict[str, Any]
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class EditorialIssue:
    id: str
    severity: str  # Critical, High, Medium, Low
    category: str  # Grammar, SEO, Brand, Hallucination, Copyright, Claims, Accessibility
    location: str
    description: str
    suggested_fix: str
    status: str    # Open, Resolved, Ignored
    reviewer: str
    timestamp: str = field(default_factory=_get_utc_now)

@dataclass
class EvidenceMap:
    statement: str
    research_finding: str
    citation_text: str
    source_url: str
    confidence_score: float

@dataclass
class RedFlagItem:
    statement: str
    flag_type: str  # Absolute Guarantee, Defamation, Financial/Legal Advice, Unsupported Superlative
    risk_level: str # High, Medium
    recommendation: str

@dataclass
class ClaimVerification:
    claim_text: str
    claim_type: str  # Technical, Benchmark, Marketing
    verification_status: str  # Verified, Qualified, Unverified
    supporting_citation: Optional[str]
    notes: str

@dataclass
class HallucinationCheck:
    passed: bool
    total_assertions_checked: int
    unsupported_assertions_count: int
    unsupported_statements: List[str]

@dataclass
class CopyrightCheck:
    passed: bool
    risk_score: float
    quoted_material_sources: List[str]
    potential_infringements: List[str]

@dataclass
class EditorialScorecard:
    grammar_score: float
    seo_score: float
    brand_score: float
    readability_score: float
    citation_coverage_score: float
    claim_accuracy_score: float
    copyright_risk_score: float
    hallucination_risk_score: float
    accessibility_score: float
    overall_editorial_score: float

@dataclass
class ApprovalDecision:
    status: str  # Approved, Approved with Minor Changes, Requires Revision, Rejected
    reason_rationale: str
    supporting_reviewers: List[str]
    triggered_rules: List[str]
    blocking_issues_count: int
    confidence_score: float

@dataclass
class PublishingReadiness:
    ready_for_publishing: bool
    readiness_score: float
    checklist: Dict[str, bool]
    pending_requirements: List[str]

@dataclass
class RevisionRecord:
    revision_id: str
    timestamp: str
    author: str
    changes_summary: str

@dataclass
class EditorialQualityGate:
    passed: bool
    score: float
    checklist: Dict[str, bool]
    diagnostics: List[str]

@dataclass
class ApprovedContentPackage:
    id: str
    topic: str
    date: str
    executive_summary: str
    approved_content: Dict[str, Any]
    editorial_report: Dict[str, Any]
    issues: List[EditorialIssue]
    evidence_map: List[EvidenceMap]
    red_flags: List[RedFlagItem]
    claims_verification: List[ClaimVerification]
    hallucination_check: HallucinationCheck
    copyright_check: CopyrightCheck
    scorecard: EditorialScorecard
    approval_decision: ApprovalDecision
    publishing_readiness: PublishingReadiness
    revisions: List[RevisionRecord]
    confidence_score: float
    version: str
    quality_gate: EditorialQualityGate
    created_at: str = field(default_factory=_get_utc_now)
