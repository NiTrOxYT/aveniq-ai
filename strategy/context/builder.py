"""
Strategy Context Loader & Builder for AVENIQ Strategy Department.
Assembles Company Brain, Market Intelligence, Historical Performance, Campaigns,
Calendar, and Business Goals into a single StrategyContext.
"""

from strategy.models.schema import StrategyContext
from strategy.inputs.company_input import CompanyInputNormalizer
from strategy.inputs.market_input import MarketInputNormalizer
from strategy.inputs.goals_input import (
    AnalyticsInputNormalizer, CampaignInputNormalizer,
    CalendarInputNormalizer, GoalsInputNormalizer
)

class StrategyContextBuilder:
    def __init__(self, root_dir: str = "."):
        self.company_input = CompanyInputNormalizer(root_dir)
        self.market_input = MarketInputNormalizer()
        self.analytics_input = AnalyticsInputNormalizer()
        self.campaign_input = CampaignInputNormalizer()
        self.calendar_input = CalendarInputNormalizer()
        self.goals_input = GoalsInputNormalizer()

    def build_context(self) -> StrategyContext:
        company_ctx = self.company_input.load_company_context()
        market_signals = self.market_input.load_market_signals()
        historical_perf = self.analytics_input.load_historical_performance()
        active_camps = self.campaign_input.load_active_campaigns()
        pub_calendar = self.calendar_input.load_publishing_calendar()
        b_goals = self.goals_input.load_current_goals()

        brand_guardrails = {
            "forbidden_words": ["best company", "guaranteed", "cheapest", "magic", "overnight success"],
            "required_tone": "professional, confident, technical but business-friendly, helpful",
            "allowed_services": company_ctx.get("core_services", [])
        }

        return StrategyContext(
            company_context=company_ctx,
            market_intelligence={"signals": market_signals},
            business_goals=b_goals,
            active_campaigns=active_camps,
            publishing_calendar=pub_calendar,
            historical_performance=historical_perf,
            brand_guardrails=brand_guardrails
        )
