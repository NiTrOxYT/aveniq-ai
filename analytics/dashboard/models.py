"""
Executive Dashboard Models for Web UI Dashboards.
Provides structured objects for Campaign Overview, Platform Comparison, Engagement Summary, Trend Summary, and KPI Scorecards.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class CampaignOverviewDashboard:
    campaign_id: str
    overall_score: float
    benchmark_status: str
    impressions: int
    visits: int
    leads: int

@dataclass
class PlatformComparisonDashboard:
    platforms: List[Dict[str, Any]]  # [{platform, impressions, engagement_rate, leads}]

@dataclass
class ExecutiveDashboard:
    overview: CampaignOverviewDashboard
    platform_comparison: PlatformComparisonDashboard
    kpi_scorecards: Dict[str, float]
    recommendations_count: int

class ExecutiveDashboardBuilder:
    @staticmethod
    def build_dashboard(campaign_id: str = "cmp_2026-07-26_001") -> ExecutiveDashboard:
        overview = CampaignOverviewDashboard(
            campaign_id=campaign_id,
            overall_score=86.5,
            benchmark_status="OUTPERFORMING (+10.2%)",
            impressions=75800,
            visits=7460,
            leads=75
        )
        comparison = PlatformComparisonDashboard(platforms=[
            {"platform": "LinkedIn", "impressions": 24500, "engagement_rate": "4.2%", "leads": 18},
            {"platform": "X", "impressions": 38900, "engagement_rate": "3.8%", "leads": 22},
            {"platform": "Website", "impressions": 12400, "engagement_rate": "5.5%", "leads": 35}
        ])
        return ExecutiveDashboard(
            overview=overview,
            platform_comparison=comparison,
            kpi_scorecards={
                "engagement_score": 82.0,
                "conversion_score": 88.5,
                "seo_score": 85.0,
                "overall_score": 86.5
            },
            recommendations_count=2
        )
