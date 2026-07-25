"""
Learning Report Generator for Learning Department.
Formats learning packages into actionable JSON optimization reports.
"""

from typing import Dict, Any
from learning.engine.learning_engine import LearningEngine
from learning.storage.manager import LearningStorageManager

class LearningReportGenerator:
    def __init__(self):
        self.engine = LearningEngine()
        self.storage = LearningStorageManager()

    def generate_learning_report(self, topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        pkg = self.engine.generate_learning_package(topic)
        self.storage.save_package(pkg)

        return {
            "report_type": "learning_package",
            "learning_id": pkg.id,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "overall_learning_score": f"{pkg.scores.overall_learning_score}/100",
            "version": pkg.version,
            "publishing_analysis": {
                "total_campaigns": pkg.publishing_analysis.total_campaigns_analyzed,
                "total_posts": pkg.publishing_analysis.published_posts_count,
                "coverage": f"{pkg.publishing_analysis.platform_coverage_pct}%",
                "cadence": pkg.publishing_analysis.publishing_cadence
            },
            "topic_summary": {
                "top_topics": pkg.topic_summary.top_topics,
                "emerging_topics": pkg.topic_summary.emerging_topics,
                "retired_topics": pkg.topic_summary.retired_topics,
                "pillars": pkg.topic_summary.content_pillars
            },
            "duplicate_report": {
                "duplicate_hooks": pkg.duplicate_report.duplicate_hooks_detected,
                "duplicate_prompts": pkg.duplicate_report.duplicate_prompts_detected,
                "recommendations": pkg.duplicate_report.duplicate_reduction_recommendations
            },
            "brand_evolution": {
                "voice_consistency": f"{pkg.brand_evolution.brand_voice_consistency}%",
                "visual_style": pkg.brand_evolution.visual_style_evolution,
                "tone_stability": f"{pkg.brand_evolution.tone_stability_score}%"
            },
            "recommendations": [
                {
                    "id": r.id,
                    "target_department": r.target_department,
                    "recommendation": r.recommendation_text,
                    "rationale": r.rationale,
                    "confidence": f"{int(r.confidence_score * 100)}%",
                    "state": r.lifecycle_state,
                    "expected_benefit": r.expected_benefit
                } for r in pkg.recommendations
            ],
            "knowledge_proposals": [
                {
                    "id": p.proposal_id,
                    "target_file": p.target_file,
                    "proposed_change": p.proposed_change,
                    "citation": p.evidence_citation,
                    "confidence": f"{int(p.confidence_score * 100)}%",
                    "status": p.review_status
                } for p in pkg.knowledge_proposals
            ],
            "learning_metrics": {
                "duplicate_reduction_rate": f"{pkg.learning_metrics.duplicate_reduction_rate}%",
                "content_diversity": f"{pkg.learning_metrics.content_diversity_score}%",
                "brand_consistency": f"{pkg.learning_metrics.brand_consistency_score}%",
                "recommendation_acceptance": f"{pkg.learning_metrics.recommendation_acceptance_rate}%",
                "knowledge_growth": f"{pkg.learning_metrics.knowledge_growth_rate}%"
            },
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": f"{pkg.quality_gate.score}%",
                "checklist": pkg.quality_gate.checklist
            }
        }
