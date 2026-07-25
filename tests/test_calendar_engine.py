"""
Unit tests for Calendar & Campaign Management Engine, Schedulers, and Quality Gate.
"""

import unittest
from calendar_dept.context.builder import CalendarContextBuilder
from calendar_dept.events.industry_events import IndustryEventManager, BlackoutManager
from calendar_dept.schedule.monthly_calendar import MonthlyCalendarBuilder, CampaignDependencyGraphBuilder
from calendar_dept.engine.calendar_engine import CalendarEngine

class TestCalendarDepartment(unittest.TestCase):
    def test_context_builder(self):
        ctx = CalendarContextBuilder.build_context("AI Agents")
        self.assertIsNotNone(ctx.strategy_package)
        self.assertIsNotNone(ctx.planning_package)

    def test_events_and_blackouts(self):
        events = IndustryEventManager.get_upcoming_events()
        self.assertGreater(len(events), 0)
        self.assertTrue(BlackoutManager.is_blackout_date("2026-09-07"))

    def test_monthly_calendar_and_dependencies(self):
        cal_30day = MonthlyCalendarBuilder.build_30day_calendar()
        self.assertEqual(len(cal_30day.days), 30)

        roadmap = MonthlyCalendarBuilder.build_90day_roadmap()
        self.assertEqual(roadmap.quarter, "Q3 2026")

    def test_calendar_engine(self):
        engine = CalendarEngine()
        pkg = engine.generate_calendar_package("AI Agents in Enterprise Operations")
        self.assertIsNotNone(pkg)
        self.assertEqual(len(pkg.campaigns), 2)
        self.assertTrue(pkg.quality_gate.passed)

if __name__ == "__main__":
    unittest.main()
