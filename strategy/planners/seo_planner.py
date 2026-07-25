"""
SEO Strategist for Strategy Department.
Recommends primary/secondary keywords, search intent, difficulty, and internal linking.
"""

from typing import List
from strategy.models.schema import Opportunity, KeywordPlan

class SEOPlanner:
    @staticmethod
    def plan_seo(opportunity: Opportunity) -> KeywordPlan:
        topic_words = opportunity.topic.split()
        primary_kw = opportunity.topic
        sec_kw_1 = f"custom {opportunity.topic.lower()}"
        sec_kw_2 = f"{opportunity.target_industry.lower()} software automation"
        sec_kw_3 = "aveniq software engineering"

        return KeywordPlan(
            primary_keyword=primary_kw,
            secondary_keywords=[sec_kw_1, sec_kw_2, sec_kw_3],
            search_intent="Informational" if "how" in primary_kw.lower() else "Commercial",
            difficulty="Medium",
            content_cluster=f"{opportunity.category} Cluster",
            recommended_landing_pages=[
                f"/services/{opportunity.category.lower().replace(' ', '-')}",
                "/contact"
            ],
            internal_linking_opportunities=[
                "knowledge/services/web-development.md",
                "knowledge/services/ai-automation.md",
                "knowledge/services/saas-development.md"
            ]
        )
