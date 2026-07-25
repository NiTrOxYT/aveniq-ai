"""
Unit tests for Chief Strategy Officer and Planners.
"""

import unittest
from strategy.planners.marketing_planner import ChiefStrategyOfficer
from strategy.reports.generator import StrategyReportGenerator

class TestStrategyPlanners(unittest.TestCase):
    def test_cso_daily_plan(self):
        cso = ChiefStrategyOfficer()
        plan = cso.generate_daily_marketing_plan()
        self.assertIsNotNone(plan)
        self.assertTrue(plan.publish_today)
        self.assertGreater(plan.confidence_percentage, 50.0)

    def test_report_generator(self):
        gen = StrategyReportGenerator()
        daily = gen.generate_daily_report()
        weekly = gen.generate_weekly_report()
        monthly = gen.generate_monthly_report()

        self.assertEqual(daily["report_type"], "daily")
        self.assertEqual(weekly["report_type"], "weekly")
        self.assertEqual(monthly["report_type"], "monthly")

if __name__ == "__main__":
    unittest.main()
