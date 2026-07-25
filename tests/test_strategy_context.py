"""
Unit tests for Strategy Context Builder and Opportunity Deduplicator.
"""

import unittest
from strategy.context.builder import StrategyContextBuilder
from strategy.inputs.market_input import MarketInputNormalizer
from strategy.analyzers.deduplicator import OpportunityDeduplicator

class TestStrategyContextAndDeduplicator(unittest.TestCase):
    def test_context_builder(self):
        builder = StrategyContextBuilder()
        ctx = builder.build_context()
        self.assertIsNotNone(ctx.company_context)
        self.assertIn("Lead Generation", ctx.business_goals)

    def test_deduplicator(self):
        signals = MarketInputNormalizer().load_market_signals()
        opps = OpportunityDeduplicator.deduplicate(signals)
        self.assertEqual(len(opps), len(signals))
        self.assertGreater(opps[0].priority_score.overall_score, 0)

if __name__ == "__main__":
    unittest.main()
