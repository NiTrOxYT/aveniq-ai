"""
Planning Context Loader & Builder for AVENIQ Planning Department.
Normalizes Strategy Report, Research Package, Company Brain, Brand Guidelines,
and Publishing History into unified PlanningContext.
"""

from typing import Dict, Any, List
from strategy.reports.generator import StrategyReportGenerator
from research.reports.generator import ResearchReportGenerator
from planning.models.schema import PlanningContext

class ContextLoader:
    @staticmethod
    def load_strategy_report() -> Dict[str, Any]:
        return StrategyReportGenerator().generate_daily_report()

    @staticmethod
    def load_research_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return ResearchReportGenerator().generate_package_report(topic)

class PlanningContextBuilder:
    @staticmethod
    def build_context(topic: str = "AI Agents in Enterprise Operations") -> PlanningContext:
        strat_report = ContextLoader.load_strategy_report()
        res_package = ContextLoader.load_research_package(topic)

        company_ctx = {
            "name": "AVENIQ",
            "services": strat_report.get("content", {}).get("platforms", []),
            "core_tech": ["React", "Next.js", "TypeScript", "PostgreSQL", "n8n"]
        }

        brand_rules = {
            "tone": "professional, confident, technical but business-friendly, honest",
            "forbidden_words": ["best company", "guaranteed", "cheapest", "magic"]
        }

        hist_camps = [
            {"id": "camp_hist_001", "name": "Q1 AI Automation Sprint", "performance": "High"}
        ]

        pub_hist = {
            "last_published_topic": "Scaling SaaS Multi-Tenancy",
            "cadence": "5 posts / week"
        }

        goals = ["Lead Generation", "Brand Authority", "SEO Growth", "Product Awareness"]

        return PlanningContext(
            strategy_report=strat_report,
            research_package=res_package,
            company_context=company_ctx,
            brand_guidelines=brand_rules,
            historical_campaigns=hist_camps,
            publishing_history=pub_hist,
            business_goals=goals
        )
