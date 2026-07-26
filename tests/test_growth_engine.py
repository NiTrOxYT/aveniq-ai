"""
Unit tests for Brand Growth Intelligence Engine, Planners, and Quality Gate.
"""

import unittest
from growth.context.builder import GrowthContextBuilder
from growth.forecasting.forecast_engine import GoalManager, ForecastEngine
from growth.planners.growth_planner import GrowthPlanner
from growth.engine.growth_engine import GrowthEngine

class TestGrowthDepartment(unittest.TestCase):
    def test_context_builder(self):
        ctx = GrowthContextBuilder.build_context("AI Agents")
        self.assertIsNotNone(ctx.strategy_package)
        self.assertIsNotNone(ctx.calendar_package)

    def test_goals_and_forecasting(self):
        goals = GoalManager.get_active_goals()
        self.assertGreater(len(goals), 0)

        forecast = ForecastEngine.generate_kpi_forecast()
        self.assertGreater(forecast.expected_leads, 0)

        scenarios = ForecastEngine.generate_scenarios()
        self.assertEqual(len(scenarios), 3)

    def test_planners(self):
        funnel = GrowthPlanner.allocate_funnel()
        self.assertEqual(funnel.awareness_pct, 30.0)

        portfolio = GrowthPlanner.build_campaign_portfolio()
        self.assertGreater(len(portfolio), 0)

    def test_growth_engine(self):
        engine = GrowthEngine()
        pkg = engine.generate_growth_package("AI Agents in Enterprise Operations")
        self.assertIsNotNone(pkg)
        self.assertGreater(pkg.metrics.overall_growth_score, 85.0)
        self.assertTrue(pkg.quality_gate.passed)

if __name__ == "__main__":
    unittest.main()
