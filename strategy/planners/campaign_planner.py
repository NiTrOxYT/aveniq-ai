"""
Campaign Strategist & Channel Strategist.
"""

from typing import List, Optional
from strategy.models.schema import Opportunity, CampaignPlan, AudienceProfile

class CampaignPlanner:
    @staticmethod
    def plan_campaign(opportunity: Opportunity, audience: AudienceProfile) -> CampaignPlan:
        camp_name = f"{opportunity.target_industry} Digital Transformation Sprint"
        if "ai" in opportunity.topic.lower():
            camp_name = "Enterprise AI Automation Week"
        elif "saas" in opportunity.topic.lower():
            camp_name = "SaaS Product Scalability Sprint"

        return CampaignPlan(
            id=f"camp_{opportunity.target_industry.lower()}_001",
            name=camp_name,
            goal="Lead Generation & Product Awareness",
            duration_days=7,
            primary_audience=audience.primary_audience,
            content_mix=["Educational Guide", "Architecture Case Study", "Comparison Table", "Executive Checklist"],
            target_platforms=["LinkedIn", "Website", "X"],
            call_to_action="Schedule a custom discovery consultation",
            expected_outcome="High executive engagement, qualified discovery calls, and organic SEO growth."
        )

class ChannelPlanner:
    @staticmethod
    def select_channels(audience: AudienceProfile) -> List[str]:
        channels = ["LinkedIn", "Website"]
        if audience.industry == "SaaS" or "Founder" in audience.primary_audience:
            channels.append("X")
        if "Developer" in audience.secondary_audience:
            channels.append("GitHub Discussions")
        return channels
