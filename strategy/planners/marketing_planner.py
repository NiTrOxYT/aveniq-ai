"""
Chief Strategy Officer Agent (Marketing Planner) for AVENIQ Strategy Department.
Orchestrates strategy execution pipeline: inputs -> deduplication -> ranking -> context -> decision engine -> guardrails validation.
"""

from datetime import datetime, timezone
from strategy.models.schema import MarketingPlan, StrategyContext, Opportunity
from strategy.context.builder import StrategyContextBuilder
from strategy.analyzers.deduplicator import OpportunityDeduplicator
from strategy.analyzers.opportunity_ranker import OpportunityRanker, AudienceMatcher
from strategy.engine.decision_engine import DecisionEngine
from strategy.planners.content_planner import ContentPlanner
from strategy.planners.seo_planner import SEOPlanner
from strategy.planners.campaign_planner import CampaignPlanner
from strategy.guardrails.brand_guardrails import BrandGuardrails

class ChiefStrategyOfficer:
    def __init__(self, root_dir: str = "."):
        self.context_builder = StrategyContextBuilder(root_dir)

    def generate_daily_marketing_plan(self) -> MarketingPlan:
        # 1. Build Unified Strategy Context
        context = self.context_builder.build_context()

        # 2. Extract and Deduplicate Signals
        signals = context.market_intelligence.get("signals", [])
        deduped_opps = OpportunityDeduplicator.deduplicate(signals)

        # 3. Rank Opportunities
        ranked_opps = OpportunityRanker.rank_opportunities(deduped_opps)

        # 4. Execute Decision Engine
        top_opp, reasoning = DecisionEngine.make_decision(context, ranked_opps)

        # 5. Execute Sub-Planners
        audience = AudienceMatcher.match_audience(top_opp)
        content_rec = ContentPlanner.recommend_content(top_opp, reasoning.business_goal)
        seo_plan = SEOPlanner.plan_seo(top_opp)
        campaign_plan = CampaignPlanner.plan_campaign(top_opp, audience)

        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        plan = MarketingPlan(
            id=f"plan_{today_str}_{top_opp.id}",
            date=today_str,
            primary_goal=reasoning.business_goal,
            business_objective="Authority Building & Lead Generation",
            publish_today=reasoning.publish_today,
            audience=audience,
            content=content_rec,
            seo=seo_plan,
            campaign=campaign_plan,
            decision_reasoning=reasoning,
            opportunity=top_opp,
            priority_score=int(top_opp.priority_score.overall_score),
            confidence_percentage=round(reasoning.confidence_score * 100, 1),
            expected_result=[
                "High executive authority and brand credibility",
                "Organic keyword search growth",
                "Qualified inbound lead generation"
            ]
        )

        # 6. Validate Brand Guardrails
        is_valid, violations = BrandGuardrails.validate_marketing_plan(plan)
        if not is_valid:
            raise ValueError(f"Generated marketing plan failed brand guardrails: {', '.join(violations)}")

        return plan
