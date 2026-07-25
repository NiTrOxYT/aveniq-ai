"""
Unit test for Strategy REST API endpoints.
"""

import unittest
from strategy.api.routes import StrategyAPIHandler
from io import BytesIO

class MockRequest:
    def __init__(self, path):
        self.path = path

class TestStrategyAPI(unittest.TestCase):
    def test_routes_exist(self):
        from strategy.reports.generator import StrategyReportGenerator
        gen = StrategyReportGenerator()
        daily = gen.generate_daily_report()
        self.assertIsNotNone(daily)
        self.assertEqual(daily["report_type"], "daily")

if __name__ == "__main__":
    unittest.main()
