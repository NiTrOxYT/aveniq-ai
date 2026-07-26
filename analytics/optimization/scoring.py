"""
0-100 Scale Performance Scorer and Benchmark Engine.
Computes normalized Engagement, Conversion, SEO, Audience Quality, and Overall Campaign Scores.
"""

from typing import Dict, Any, List
from analytics.models.campaign_metrics import CampaignMetrics

class CampaignScorer:
    @staticmethod
    def calculate_scores(metrics: CampaignMetrics) -> Dict[str, float]:
        # 1. Engagement Score
        eng = metrics.engagement
        eng_total = eng.reactions + eng.likes + (eng.comments * 2) + (eng.shares * 3) + (eng.reposts * 3)
        eng_score = min(100.0, round((eng_total / 800.0) * 100.0, 1))

        # 2. Conversion Score
        biz = metrics.business
        conv_total = (biz.leads * 2) + (biz.signups * 3) + (biz.demo_requests * 4) + (biz.conversions * 5)
        conv_score = min(100.0, round((conv_total / 100.0) * 100.0, 1))

        # 3. SEO & Website Score
        web = metrics.website
        seo_score = min(100.0, round((web.cta_clicks / 250.0) * 100.0, 1))

        # 4. Audience Quality Score
        aud_score = round((eng_score * 0.4) + (conv_score * 0.6), 1)

        # 5. Overall Score
        overall_score = round(
            (eng_score * 0.3) + (conv_score * 0.35) + (seo_score * 0.15) + (aud_score * 0.2), 1
        )

        return {
            "engagement_score": eng_score,
            "conversion_score": conv_score,
            "seo_score": seo_score,
            "audience_quality_score": aud_score,
            "overall_campaign_score": overall_score
        }

class BenchmarkEngine:
    HISTORICAL_AVERAGES = {
        "overall_score": 75.0,
        "engagement_score": 70.0,
        "conversion_score": 72.0,
        "leads_per_campaign": 15
    }

    @staticmethod
    def benchmark_campaign(scores: Dict[str, float], leads: int) -> Dict[str, Any]:
        overall = scores.get("overall_campaign_score", 0.0)
        avg_overall = BenchmarkEngine.HISTORICAL_AVERAGES["overall_score"]
        diff_pct = round(((overall - avg_overall) / avg_overall) * 100.0, 1)

        status = "OUTPERFORMING" if diff_pct >= 0 else "UNDERPERFORMING"

        return {
            "benchmark_status": status,
            "performance_diff_pct": f"{diff_pct}%",
            "historical_avg_score": avg_overall,
            "campaign_score": overall,
            "leads_vs_benchmark": f"{leads} vs {BenchmarkEngine.HISTORICAL_AVERAGES['leads_per_campaign']}"
        }
