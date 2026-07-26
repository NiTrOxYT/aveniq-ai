"""
Growth Strategy Planner, Funnel Planner, & Campaign Portfolio Allocator.
"""

from typing import List, Dict, Any
from growth.models.schema import CampaignPortfolioItem, FunnelAllocation, ContentMix

class GrowthPlanner:
    @staticmethod
    def allocate_funnel() -> FunnelAllocation:
        return FunnelAllocation(
            awareness_pct=30.0,
            interest_pct=20.0,
            consideration_pct=20.0,
            evaluation_pct=10.0,
            decision_pct=10.0,
            retention_pct=5.0,
            advocacy_pct=5.0
        )

    @staticmethod
    def determine_content_mix() -> ContentMix:
        return ContentMix(
            educational_pct=35.0,
            thought_leadership_pct=25.0,
            case_study_pct=20.0,
            product_pct=10.0,
            community_pct=10.0
        )

    @staticmethod
    def build_campaign_portfolio() -> List[CampaignPortfolioItem]:
        return [
            CampaignPortfolioItem(
                portfolio_id="port_001",
                campaign_name="Enterprise AI Agent Architecture Series",
                campaign_type="Educational Series",
                funnel_stage="Awareness",
                target_kpi="Website Traffic & Reach",
                allocated_weight_pct=30.0
            ),
            CampaignPortfolioItem(
                portfolio_id="port_002",
                campaign_name="FinTech SaaS Case Studies & Benchmark ROI",
                campaign_type="Case Study",
                funnel_stage="Consideration",
                target_kpi="Qualified Leads",
                allocated_weight_pct=25.0
            ),
            CampaignPortfolioItem(
                portfolio_id="port_003",
                campaign_name="Founder Blueprint: Building Autonomous Systems",
                campaign_type="Founder Story",
                funnel_stage="Interest",
                target_kpi="Founder Authority & Signups",
                allocated_weight_pct=20.0
            ),
            CampaignPortfolioItem(
                portfolio_id="port_004",
                campaign_name="AVENIQ v2.0 Platform Launch Webinar",
                campaign_type="Webinar",
                funnel_stage="Decision",
                target_kpi="Demo Requests & Conversions",
                allocated_weight_pct=15.0
            ),
            CampaignPortfolioItem(
                portfolio_id="port_005",
                campaign_name="Model Context Protocol Technical Tutorial",
                campaign_type="Tutorial",
                funnel_stage="Evaluation",
                target_kpi="Newsletter Subscribers",
                allocated_weight_pct=10.0
            )
        ]
