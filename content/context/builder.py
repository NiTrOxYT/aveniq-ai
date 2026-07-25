"""
Content Context Loader & Builder for AVENIQ Content Department.
Normalizes Planning Package, Research Package, Brand Rules, and SEO Guidelines into ContentContext.
"""

from typing import Dict, Any, List
from planning.reports.generator import PlanningReportGenerator
from research.reports.generator import ResearchReportGenerator
from content.models.schema import ContentContext

class ContextLoader:
    @staticmethod
    def load_planning_report() -> Dict[str, Any]:
        return PlanningReportGenerator().generate_planning_report()

    @staticmethod
    def load_research_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return ResearchReportGenerator().generate_package_report(topic)

class ContentContextBuilder:
    @staticmethod
    def build_context(topic: str = "AI Agents in Enterprise Operations") -> ContentContext:
        plan_report = ContextLoader.load_planning_report()
        res_package = ContextLoader.load_research_package(topic)

        brand_rules = {
            "name": "AVENIQ",
            "tone": "professional, technical but business-friendly, confident, honest",
            "forbidden_words": ["best company", "guaranteed", "cheapest", "magic", "overnight success"]
        }

        seo_rules = {
            "primary_keyword": plan_report.get("topic", topic),
            "keyword_density_target": "1.5%",
            "min_internal_links": 2
        }

        goals = ["Lead Generation", "Brand Authority", "SEO Growth"]

        return ContentContext(
            planning_report=plan_report,
            research_package=res_package,
            brand_guidelines=brand_rules,
            seo_rules=seo_rules,
            campaign_goals=goals
        )
