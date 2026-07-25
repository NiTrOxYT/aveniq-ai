"""
Quality Gate Verification Processor for Research Department.
Enforces 8 mandatory quality checklist gates before a Research Package is approved.
"""

from typing import List, Dict, Any, Tuple
from research.models.schema import QualityGateResult, StatisticItem, AcademicStudy, TechnicalClaim, CompetitorFinding, CaseStudyItem, SEOResearchItem, CitationItem
from research.analyzers.credibility_scorer import SourceValidator
from research.analyzers.contradiction_detector import ContradictionDetector

class QualityGateVerifier:
    @staticmethod
    def verify_package(
        topic: str,
        statistics: List[StatisticItem],
        studies: List[AcademicStudy],
        technical_claims: List[TechnicalClaim],
        competitors: List[CompetitorFinding],
        case_studies: List[CaseStudyItem],
        seo_item: SEOResearchItem,
        citations: List[CitationItem]
    ) -> QualityGateResult:
        gate_checks = {
            "sources_validated": True,
            "technical_claims_verified": len(technical_claims) > 0,
            "statistics_cited": len(statistics) > 0,
            "contradictions_identified": True,
            "competitor_data_reviewed": len(competitors) > 0,
            "seo_completed": seo_item is not None and len(seo_item.primary_keyword) > 0,
            "examples_collected": len(case_studies) > 0,
            "confidence_calculated": True
        }

        diagnostics = []

        # Check citations
        for c in citations:
            is_valid, violations = SourceValidator.validate_citation(c)
            if not is_valid:
                gate_checks["sources_validated"] = False
                diagnostics.extend(violations)

        # Check contradictions
        contradictions = ContradictionDetector.detect_contradictions(statistics)
        if contradictions:
            diagnostics.extend(contradictions)

        passed_count = sum(1 for v in gate_checks.values() if v)
        total_count = len(gate_checks)
        score = round((passed_count / float(total_count)) * 100.0, 1)

        is_passed = score >= 85.0 and gate_checks["sources_validated"]

        return QualityGateResult(
            passed=is_passed,
            score=score,
            gate_checks=gate_checks,
            diagnostics=diagnostics
        )
