"""
Content Strategist for Strategy Department.
Recommends optimal content category, format, and structure across 20 categories without generating raw text content.
"""

from typing import List, Dict, Any
from strategy.models.schema import Opportunity, ContentRecommendation
from strategy.analyzers.opportunity_ranker import PositioningStrategist
from strategy.goals.objectives import ObjectiveMapper

SUPPORTED_CONTENT_CATEGORIES = [
    "Educational", "Authority", "Story", "Founder Story", "Behind the Scenes",
    "Client Problem", "Case Study", "Tutorial", "Opinion", "Industry News",
    "Myth Busting", "Comparison", "Framework", "Checklist", "FAQ",
    "Product Update", "Trend Analysis", "Tool Review", "Guide", "Explainer"
]

class ContentPlanner:
    @staticmethod
    def recommend_content(opportunity: Opportunity, goal: str) -> ContentRecommendation:
        category = "Educational"
        content_format = "Technical Guide & Architecture Deep-Dive"

        if "how" in opportunity.topic.lower() or "tutorial" in opportunity.topic.lower():
            category = "Tutorial"
            content_format = "Step-by-Step Technical Guide"
        elif "vs" in opportunity.topic.lower() or "comparison" in opportunity.topic.lower():
            category = "Comparison"
            content_format = "Architectural Comparison Breakdown"
        elif "agents" in opportunity.topic.lower() or "automation" in opportunity.topic.lower():
            category = "Educational"
            content_format = "Strategic System Architecture Guide"
        elif "case study" in opportunity.topic.lower():
            category = "Case Study"
            content_format = "Client Implementation Results Analysis"

        positioning = PositioningStrategist.determine_positioning(opportunity)
        cta = ObjectiveMapper.get_preferred_cta(goal)

        suggested_title = f"How {opportunity.topic} Transforms {opportunity.target_industry} Operations"

        return ContentRecommendation(
            category=category,
            content_format=content_format,
            suggested_title=suggested_title,
            value_proposition=positioning["value_proposition"],
            unique_angle=positioning["unique_angle"],
            differentiator=positioning["differentiator"],
            target_platforms=["LinkedIn", "Website", "X"],
            call_to_action=cta
        )
