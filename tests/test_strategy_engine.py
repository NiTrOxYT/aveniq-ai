"""
Unit tests for Strategy Decision Engine and Guardrails.
"""

import unittest
from strategy.context.builder import StrategyContextBuilder
from strategy.inputs.market_input import MarketInputNormalizer
from strategy.analyzers.deduplicator import OpportunityDeduplicator
from strategy.engine.decision_engine import DecisionEngine
from strategy.guardrails.brand_guardrails import BrandGuardrails
from strategy.planners.content_planner import ContentPlanner

class TestStrategyEngineAndGuardrails(unittest.TestCase):
    def test_decision_engine(self):
        ctx = StrategyContextBuilder().build_context()
        signals = MarketInputNormalizer().load_market_signals()
        opps = OpportunityDeduplicator.deduplicate(signals)

        top_opp, reasoning = DecisionEngine.make_decision(ctx, opps)
        self.assertTrue(reasoning.publish_today)
        self.assertGreater(reasoning.confidence_score, 0.5)
        self.assertIn("AVENIQ", reasoning.primary_reason)

    def test_brand_guardrails(self):
        signals = MarketInputNormalizer().load_market_signals()
        opp = OpportunityDeduplicator.deduplicate(signals)[0]
        rec = ContentPlanner.recommend_content(opp, "Lead Generation")

        is_valid, violations = BrandGuardrails.validate_content_recommendation(rec)
        self.assertTrue(is_valid, f"Guardrails failed: {violations}")

if __name__ == "__main__":
    unittest.main()
