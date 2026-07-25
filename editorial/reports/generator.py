"""
Editorial Report Generator for Editorial Department.
Formats approved content packages into publishing-ready JSON reports.
"""

from typing import Dict, Any
from editorial.engine.editorial_engine import EditorialEngine
from editorial.storage.manager import EditorialStorageManager

class EditorialReportGenerator:
    def __init__(self):
        self.engine = EditorialEngine()
        self.storage = EditorialStorageManager()

    def generate_editorial_report(self, topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        pkg = self.engine.review_and_approve_content(topic)
        self.storage.save_package(pkg)

        return {
            "report_type": "approved_content_package",
            "package_id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "overall_editorial_score": f"{pkg.scorecard.overall_editorial_score}/100",
            "confidence_score": f"{int(pkg.confidence_score * 100)}%",
            "version": pkg.version,
            "approval_decision": {
                "status": pkg.approval_decision.status,
                "rationale": pkg.approval_decision.reason_rationale,
                "reviewers": pkg.approval_decision.supporting_reviewers,
                "triggered_rules": pkg.approval_decision.triggered_rules,
                "blocking_issues": pkg.approval_decision.blocking_issues_count
            },
            "publishing_readiness": {
                "ready": pkg.publishing_readiness.ready_for_publishing,
                "score": f"{pkg.publishing_readiness.readiness_score}%",
                "checklist": pkg.publishing_readiness.checklist
            },
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": f"{pkg.quality_gate.score}%",
                "checklist": pkg.quality_gate.checklist
            },
            "scorecard": {
                "grammar": pkg.scorecard.grammar_score,
                "seo": pkg.scorecard.seo_score,
                "brand": pkg.scorecard.brand_score,
                "readability": pkg.scorecard.readability_score,
                "citation_coverage": pkg.scorecard.citation_coverage_score,
                "claim_accuracy": pkg.scorecard.claim_accuracy_score,
                "copyright_risk": f"{pkg.scorecard.copyright_risk_score}%",
                "hallucination_risk": f"{pkg.scorecard.hallucination_risk_score}%",
                "overall": pkg.scorecard.overall_editorial_score
            },
            "evidence_map": [
                {
                    "statement": em.statement,
                    "finding": em.research_finding,
                    "citation": em.citation_text,
                    "url": em.source_url,
                    "confidence": f"{int(em.confidence_score * 100)}%"
                } for em in pkg.evidence_map
            ],
            "claims_verification": [
                {
                    "claim": cv.claim_text,
                    "type": cv.claim_type,
                    "status": cv.verification_status,
                    "citation": cv.supporting_citation
                } for cv in pkg.claims_verification
            ],
            "issues": [
                {
                    "id": i.id,
                    "severity": i.severity,
                    "category": i.category,
                    "location": i.location,
                    "description": i.description,
                    "suggested_fix": i.suggested_fix,
                    "status": i.status
                } for i in pkg.issues
            ],
            "red_flags": [
                {
                    "statement": rf.statement,
                    "type": rf.flag_type,
                    "risk": rf.risk_level,
                    "recommendation": rf.recommendation
                } for rf in pkg.red_flags
            ],
            "approved_content_preview": {
                "title": pkg.approved_content.get("title", ""),
                "slug": pkg.approved_content.get("slug", ""),
                "word_count": pkg.approved_content.get("word_count", 0)
            }
        }
