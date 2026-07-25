"""
Research Report Generator for Research Department.
Formats research packages into structured JSON reports.
"""

from typing import Dict, Any
from research.engine.research_engine import ResearchEngine
from research.storage.manager import ResearchStorageManager
from research.analyzers.contradiction_detector import CitationManager

class ResearchReportGenerator:
    def __init__(self):
        self.engine = ResearchEngine()
        self.storage = ResearchStorageManager()

    def generate_package_report(self, topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        pkg = self.engine.generate_research_package(topic)
        self.storage.save_package(pkg)

        formatted_citations = CitationManager.format_citations(pkg.citations)

        return {
            "report_type": "research_package",
            "package_id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "confidence_score": f"{int(pkg.confidence_score * 100)}%",
            "executive_summary": pkg.executive_summary,
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": f"{pkg.quality_gate.score}%",
                "gate_checks": pkg.quality_gate.gate_checks
            },
            "key_findings": pkg.key_findings,
            "verified_statistics": [
                {
                    "metric": s.metric_name,
                    "value": s.value,
                    "context": s.context,
                    "source": f"{s.citation.publication} ({s.citation.publication_date})"
                } for s in pkg.verified_statistics
            ],
            "supporting_studies": [
                {
                    "title": st.paper_title,
                    "authors": ", ".join(st.authors),
                    "publisher": st.journal_or_publisher,
                    "year": st.publication_year,
                    "key_findings": st.key_findings
                } for st in pkg.supporting_studies
            ],
            "technical_validation": [
                {
                    "tech": tc.framework_or_tech,
                    "claim": tc.claim,
                    "status": tc.verification_status,
                    "best_practices": tc.best_practices
                } for tc in pkg.technical_validation
            ],
            "competitor_insights": [
                {
                    "competitor": c.competitor_name,
                    "features": c.features,
                    "weaknesses": c.weaknesses
                } for c in pkg.competitor_insights
            ],
            "seo_insights": {
                "primary_keyword": pkg.seo_insights.primary_keyword,
                "volume": pkg.seo_insights.search_volume_estimate,
                "intent": pkg.seo_insights.search_intent,
                "questions": pkg.seo_insights.user_questions,
                "gaps": pkg.seo_insights.content_gaps
            },
            "real_world_examples": [
                {
                    "industry": cs.client_industry,
                    "challenge": cs.challenge,
                    "solution": cs.solution_implemented,
                    "outcomes": cs.business_outcomes,
                    "before_after": cs.metrics_before_after
                } for cs in pkg.real_world_examples
            ],
            "citations": formatted_citations
        }
