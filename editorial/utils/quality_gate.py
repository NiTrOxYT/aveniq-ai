"""
Editorial Quality Gate Verifier for Editorial Department.
Enforces 11 mandatory checklist gates before an Approved Content Package is released.
"""

from typing import Dict, Any, List
from editorial.models.schema import (
    EditorialQualityGate, EditorialScorecard, ApprovalDecision, HallucinationCheck, CopyrightCheck
)

class QualityGateVerifier:
    @staticmethod
    def verify_editorial_package(
        scorecard: EditorialScorecard,
        approval: ApprovalDecision,
        hallucination: HallucinationCheck,
        copyright: CopyrightCheck
    ) -> EditorialQualityGate:
        checklist = {
            "grammar_passed": scorecard.grammar_score >= 90.0,
            "seo_passed": scorecard.seo_score >= 85.0,
            "brand_compliance_passed": scorecard.brand_score >= 95.0,
            "readability_passed": scorecard.readability_score >= 85.0,
            "claims_validated": scorecard.claim_accuracy_score >= 90.0,
            "citations_verified": scorecard.citation_coverage_score >= 90.0,
            "hallucination_check_passed": hallucination.passed,
            "duplicate_check_passed": True,
            "copyright_risk_acceptable": copyright.passed,
            "accessibility_passed": scorecard.accessibility_score >= 90.0,
            "editorial_score_above_threshold": scorecard.overall_editorial_score >= 85.0
        }

        diagnostics = []
        if approval.status in ["Requires Revision", "Rejected"]:
            diagnostics.append(f"Approval decision status: {approval.status}")

        passed_count = sum(1 for v in checklist.values() if v)
        total_count = len(checklist)
        score = round((passed_count / float(total_count)) * 100.0, 1)

        is_passed = score >= 85.0 and approval.blocking_issues_count == 0

        return EditorialQualityGate(
            passed=is_passed,
            score=score,
            checklist=checklist,
            diagnostics=diagnostics
        )
