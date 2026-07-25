"""
Unit tests for Planning Department Context Builder and Analyzers.
"""

import unittest
from planning.context.builder import PlanningContextBuilder
from planning.analyzers.risk_analyzer import RiskAnalyzer, CapacityPlanner

class TestPlanningContextAndAnalyzers(unittest.TestCase):
    def test_context_builder(self):
        ctx = PlanningContextBuilder.build_context("AI Agents")
        self.assertIsNotNone(ctx.strategy_report)
        self.assertIsNotNone(ctx.research_package)
        self.assertEqual(ctx.company_context["name"], "AVENIQ")

    def test_risk_analyzer(self):
        ctx = PlanningContextBuilder.build_context("AI Agents")
        risk = RiskAnalyzer.analyze_risks(ctx)
        self.assertIsNotNone(risk)
        self.assertLessEqual(risk.risk_score, 100.0)

    def test_capacity_planner(self):
        cap = CapacityPlanner.estimate_capacity(5)
        self.assertEqual(cap.deliverable_count, 5)
        self.assertEqual(cap.estimated_production_hours, 17.5)

if __name__ == "__main__":
    unittest.main()
