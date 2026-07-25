"""
Editorial Context Loader & Builder for AVENIQ Editorial Department.
Normalizes Content Package, Research Package, Planning Package, and Brand Rules into EditorialContext.
"""

from typing import Dict, Any
from content.reports.generator import ContentReportGenerator
from research.reports.generator import ResearchReportGenerator
from planning.reports.generator import PlanningReportGenerator
from editorial.models.schema import EditorialContext

class ContextLoader:
    @staticmethod
    def load_content_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return ContentReportGenerator().generate_content_report(topic)

    @staticmethod
    def load_research_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return ResearchReportGenerator().generate_package_report(topic)

    @staticmethod
    def load_planning_report() -> Dict[str, Any]:
        return PlanningReportGenerator().generate_planning_report()

class EditorialContextBuilder:
    @staticmethod
    def build_context(topic: str = "AI Agents in Enterprise Operations") -> EditorialContext:
        cnt_package = ContextLoader.load_content_package(topic)
        res_package = ContextLoader.load_research_package(topic)
        plan_report = ContextLoader.load_planning_report()

        brand_rules = {
            "name": "AVENIQ",
            "forbidden_words": ["best company", "guaranteed", "cheapest", "magic", "overnight success"]
        }

        legal_rules = {
            "disclaimer_required": False,
            "sensitive_topics": ["medical", "financial", "defamation"]
        }

        return EditorialContext(
            content_package=cnt_package,
            research_package=res_package,
            planning_report=plan_report,
            brand_guidelines=brand_rules,
            legal_rules=legal_rules
        )
