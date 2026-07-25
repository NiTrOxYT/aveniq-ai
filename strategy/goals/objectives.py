"""
Objective Alignment & Mapping Engine for AVENIQ Strategy Department.
"""

from typing import List, Dict, Any
from strategy.goals.business_goals import SUPPORTED_BUSINESS_GOALS, get_goal_info

class ObjectiveMapper:
    @staticmethod
    def map_topic_to_goal(topic: str, category: str) -> str:
        topic_lower = topic.lower()
        category_lower = category.lower()

        if "how" in topic_lower or "guide" in topic_lower or "tutorial" in topic_lower:
            return "Customer Education"
        elif "case study" in category_lower or "results" in topic_lower or "roi" in topic_lower:
            return "Lead Generation"
        elif "vs" in topic_lower or "comparison" in category_lower or "why" in topic_lower:
            return "Brand Authority"
        elif "seo" in topic_lower or "keyword" in topic_lower:
            return "SEO Growth"
        elif "agent" in topic_lower or "n8n" in topic_lower or "ai" in topic_lower:
            return "Product Awareness"
        else:
            return "Lead Generation"

    @staticmethod
    def get_preferred_cta(goal: str) -> str:
        info = get_goal_info(goal)
        ctas = info.get("preferred_ctas", ["Schedule a consultation"])
        return ctas[0]
