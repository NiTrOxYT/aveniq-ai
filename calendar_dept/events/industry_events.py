"""
Industry Event Manager & Blackout Window Manager for Calendar Department.
"""

from typing import List, Dict, Any
from calendar_dept.models.schema import EventItem

class IndustryEventManager:
    @staticmethod
    def get_upcoming_events() -> List[EventItem]:
        return [
            EventItem(
                event_id="evt_gartner_2026",
                name="Gartner Enterprise AI Summit 2026",
                date="2026-08-10",
                category="Industry Event",
                description="Global summit on enterprise AI agent orchestration and ROI."
            ),
            EventItem(
                event_id="evt_aws_reinvent_2026",
                name="AWS re:Invent 2026",
                date="2026-11-30",
                category="Industry Event",
                description="Cloud computing and serverless AI infrastructure conference."
            ),
            EventItem(
                event_id="evt_labor_day_2026",
                name="Labor Day Holiday",
                date="2026-09-07",
                category="National Holiday",
                description="US National Holiday (No high-priority marketing product launches)."
            ),
            EventItem(
                event_id="evt_aveniq_v2_launch",
                name="AVENIQ v2.0 Platform Launch",
                date="2026-08-01",
                category="Product Launch",
                description="Major platform release for autonomous enterprise AI departments."
            )
        ]

class BlackoutManager:
    @staticmethod
    def get_blackout_dates() -> List[str]:
        return ["2026-09-07", "2026-11-26", "2026-12-25"]

    @staticmethod
    def is_blackout_date(date_str: str) -> bool:
        return date_str in BlackoutManager.get_blackout_dates()
