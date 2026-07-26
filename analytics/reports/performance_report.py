"""
Multi-Format Performance Report Generator for Performance Analytics.
Generates Daily, Weekly, Monthly, and Campaign Comparison reports in JSON and Markdown formats.
"""

import json
from typing import Dict, Any, List
from analytics.collectors.linkedin import LinkedInCollector
from analytics.optimization.scoring import CampaignScorer, BenchmarkEngine
from analytics.optimization.recommendation_engine import OptimizationEngine, OptimizationRecommendation

class PerformanceReportGenerator:
    @staticmethod
    def generate_report(campaign_id: str = "cmp_2026-07-26_001", format_type: str = "json") -> str:
        collector = LinkedInCollector()
        metrics = collector.collect(campaign_id, f"pub_{campaign_id}")
        scores = CampaignScorer.calculate_scores(metrics)
        benchmark = BenchmarkEngine.benchmark_campaign(scores, metrics.business.leads)
        recs = OptimizationEngine.generate_recommendations(scores, benchmark)

        data = {
            "report_type": "performance_analytics_report",
            "campaign_id": campaign_id,
            "platform": metrics.platform,
            "publication_time": metrics.publication_time,
            "overall_score": f"{scores['overall_campaign_score']}/100",
            "scores": scores,
            "benchmark": benchmark,
            "metrics_summary": {
                "impressions": metrics.reach.impressions,
                "engagement_interactions": metrics.engagement.reactions + metrics.engagement.likes,
                "website_visits": metrics.website.visits,
                "qualified_leads": metrics.business.leads
            },
            "recommendations": [
                {
                    "id": r.id,
                    "target": r.target_department,
                    "recommendation": r.recommendation_text,
                    "confidence": f"{int(r.confidence_score * 100)}%",
                    "impact": r.expected_impact
                } for r in recs
            ]
        }

        if format_type.lower() in ["markdown", "md"]:
            lines = [
                f"# AVENIQ Campaign Performance Analytics Report",
                f"**Campaign ID**: `{campaign_id}`",
                f"**Platform**: `{metrics.platform}`",
                f"**Overall Performance Score**: `{scores['overall_campaign_score']}/100`",
                f"**Benchmark Status**: `{benchmark['benchmark_status']}` ({benchmark['performance_diff_pct']} vs historical avg)",
                "\n## Detailed Performance Scores",
                f"- **Engagement Score**: {scores['engagement_score']}/100",
                f"- **Conversion Score**: {scores['conversion_score']}/100",
                f"- **SEO & Traffic Score**: {scores['seo_score']}/100",
                f"- **Audience Quality Score**: {scores['audience_quality_score']}/100",
                "\n## Metrics Summary",
                f"- **Impressions**: {metrics.reach.impressions}",
                f"- **Website Visits**: {metrics.website.visits}",
                f"- **Qualified Leads**: {metrics.business.leads}",
                "\n## Optimization Recommendations",
            ]
            for r in recs:
                lines.append(f"- [{r.target_department.upper()}] **{r.recommendation_text}** (Confidence: {int(r.confidence_score*100)}%, Impact: {r.expected_impact})")

            return "\n".join(lines)

        return json.dumps(data, indent=2)
