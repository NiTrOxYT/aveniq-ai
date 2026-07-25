"""
Campaign Dependency Graph & 30-Day / 90-Day Scheduler.
"""

from typing import List, Dict, Any
from calendar_dept.models.schema import (
    CampaignItem, CalendarDay, WeeklyTheme, Calendar30Day, Roadmap90Day, DependencyGraph, CapacityPlan, ConflictReport
)
from calendar_dept.events.industry_events import IndustryEventManager, BlackoutManager

class CampaignDependencyGraphBuilder:
    @staticmethod
    def build_graph(campaigns: List[CampaignItem]) -> DependencyGraph:
        nodes = [{"id": c.campaign_id, "label": c.name} for c in campaigns]
        edges = []
        for c in campaigns:
            for dep in c.dependencies:
                edges.append({"from": dep, "to": c.campaign_id, "type": "REQUIRES"})

        return DependencyGraph(nodes=nodes, edges=edges)

class MonthlyCalendarBuilder:
    @staticmethod
    def build_30day_calendar(start_date: str = "2026-07-26") -> Calendar30Day:
        days = []
        events = IndustryEventManager.get_upcoming_events()
        event_map = {e.date: e for e in events}

        # Build 30 calendar days
        for i in range(30):
            day_str = f"2026-07-26" if i == 0 else f"2026-08-{i:02d}"
            is_blackout = BlackoutManager.is_blackout_date(day_str)
            day_events = [event_map[day_str]] if day_str in event_map else []
            scheduled = ["cmp_ent_ai_001"] if i % 3 == 0 and not is_blackout else []

            slots = [
                {"time": "09:00 AM EST", "platform": "LinkedIn", "content_pillar": "Enterprise AI"},
                {"time": "11:30 AM EST", "platform": "X", "content_pillar": "Software Engineering"},
                {"time": "02:00 PM EST", "platform": "Instagram", "content_pillar": "Case Studies"}
            ] if scheduled else []

            days.append(CalendarDay(
                date=day_str,
                day_of_week="Weekday",
                scheduled_campaigns=scheduled,
                events=day_events,
                posting_slots=slots
            ))

        return Calendar30Day(
            start_date="2026-07-26",
            end_date="2026-08-25",
            days=days,
            total_scheduled_posts=len(days) * 3
        )

    @staticmethod
    def build_90day_roadmap() -> Roadmap90Day:
        return Roadmap90Day(
            quarter="Q3 2026",
            key_objectives=[
                "Establish AVENIQ as the #1 Autonomous AI COO platform",
                "Scale enterprise SaaS case studies by 40%",
                "Publish 12 high-converting technical deep dives"
            ],
            monthly_milestones={
                "July 2026": ["Ingestion Pipeline Release", "Strategy & Research Department Activation"],
                "August 2026": ["AVENIQ v2.0 Platform Launch", "Gartner AI Summit Presentation"],
                "September 2026": ["Enterprise Client Case Study Campaign", "Global Tech Conference Coverage"]
            }
        )
