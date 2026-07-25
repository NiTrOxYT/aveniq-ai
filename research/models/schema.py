"""
Data models schema for AVENIQ Research Department.
Represents StatisticItem, AcademicStudy, TechnicalClaim, CompetitorFinding,
SEOResearchItem, CaseStudyItem, CitationItem, ResearchPackage, and QualityGateResult.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class CitationItem:
    id: str
    source_title: str
    url: str
    publication: str
    author: str
    publication_date: str
    evidence_level: str  # Peer-Reviewed, Industry Report, Official Docs, Company Blog, Community
    confidence_score: float

@dataclass
class StatisticItem:
    id: str
    metric_name: str
    value: str
    context: str
    citation: CitationItem
    confidence_score: float

@dataclass
class AcademicStudy:
    id: str
    paper_title: str
    authors: List[str]
    journal_or_publisher: str
    publication_year: int
    key_findings: List[str]
    citation: CitationItem

@dataclass
class TechnicalClaim:
    id: str
    claim: str
    framework_or_tech: str
    verification_status: str  # Verified, Conditional, Unverified
    technical_limitations: List[str]
    best_practices: List[str]
    citation: CitationItem

@dataclass
class CompetitorFinding:
    competitor_name: str
    features: List[str]
    pricing_model: str
    positioning_angle: str
    strengths: List[str]
    weaknesses: List[str]
    citation: CitationItem

@dataclass
class SEOResearchItem:
    primary_keyword: str
    search_volume_estimate: str
    search_intent: str
    top_ranking_urls: List[str]
    user_questions: List[str]
    content_gaps: List[str]

@dataclass
class CaseStudyItem:
    client_industry: str
    challenge: str
    solution_implemented: str
    business_outcomes: List[str]
    metrics_before_after: Dict[str, str]
    citation: CitationItem

@dataclass
class QualityGateResult:
    passed: bool
    score: float  # 0.0 to 100.0
    gate_checks: Dict[str, bool]
    diagnostics: List[str]

@dataclass
class ResearchPackage:
    id: str
    topic: str
    date: str
    executive_summary: str
    key_findings: List[str]
    verified_statistics: List[StatisticItem]
    supporting_studies: List[AcademicStudy]
    technical_validation: List[TechnicalClaim]
    competitor_insights: List[CompetitorFinding]
    real_world_examples: List[CaseStudyItem]
    seo_insights: SEOResearchItem
    frequently_asked_questions: List[Dict[str, str]]
    common_misconceptions: List[str]
    industry_trends: List[str]
    risk_factors: List[str]
    future_outlook: str
    citations: List[CitationItem]
    confidence_score: float
    knowledge_gaps: List[str]
    further_research_suggestions: List[str]
    quality_gate: QualityGateResult
    created_at: str = field(default_factory=_get_utc_now)
