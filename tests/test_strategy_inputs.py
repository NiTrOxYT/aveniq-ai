"""
Unit tests for Strategy Inputs and Normalizers.
"""

import unittest
from strategy.inputs.company_input import CompanyInputNormalizer
from strategy.inputs.market_input import MarketInputNormalizer

class TestStrategyInputs(unittest.TestCase):
    def test_company_input(self):
        norm = CompanyInputNormalizer()
        ctx = norm.load_company_context()
        self.assertEqual(ctx["company_name"], "AVENIQ")
        self.assertIn("web-development", ctx["core_services"])

    def test_market_input(self):
        norm = MarketInputNormalizer()
        signals = norm.load_market_signals()
        self.assertIsInstance(signals, list)
        self.assertGreater(len(signals), 0)
        self.assertIn("topic", signals[0])

if __name__ == "__main__":
    unittest.main()
