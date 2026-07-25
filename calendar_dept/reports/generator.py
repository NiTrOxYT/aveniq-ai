"""
Calendar Report Generator for Calendar & Campaign Management.
Formats calendar packages into structured JSON scheduling reports.
"""

from typing import Dict, Any
from calendar_dept.engine.calendar_engine import CalendarEngine
from calendar_dept.storage.manager import CalendarStorageManager

class CalendarReportGenerator:
    def __init__(self):
        self.engine = CalendarEngine()
        self.storage = CalendarStorageManager()

    def generate_calendar_report(self, topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        pkg = self.engine.generate_calendar_package(topic)
        self.storage.save_package(pkg)

        return {
            "report_type": "calendar_package",
            "calendar_id": pkg.id,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "version": pkg.version,
            "30day_calendar": {
                "start_date": pkg.calendar_30day.start_date,
                "end_date": pkg.calendar_30day.end_date,
                "days_count": len(pkg.calendar_30day.days),
                "total_scheduled_posts": pkg.calendar_30day.total_scheduled_posts
            },
            "90day_roadmap": {
                "quarter": pkg.roadmap_90day.quarter,
                "objectives": pkg.roadmap_90day.key_objectives,
                "milestones": pkg.roadmap_90day.monthly_milestones
            },
            "campaigns": [
                {
                    "id": c.campaign_id,
                    "name": c.name,
                    "type": c.campaign_type,
                    "dates": f"{c.start_date} to {c.end_date}",
                    "priority": c.priority,
                    "platforms": c.platforms,
                    "status": c.status
                } for c in pkg.campaigns
            ],
            "weekly_themes": [
                {
                    "week": w.week_number,
                    "dates": f"{w.start_date} to {w.end_date}",
                    "title": w.theme_title,
                    "pillars": f"{w.primary_pillar} / {w.secondary_pillar}"
                } for w in pkg.weekly_themes
            ],
            "events": [
                {
                    "id": e.event_id,
                    "name": e.name,
                    "date": e.date,
                    "category": e.category
                } for e in pkg.events
            ],
            "capacity_plan": {
                "writer_hours": pkg.capacity_plan.writer_hours_allocated,
                "designer_hours": pkg.capacity_plan.designer_hours_allocated,
                "overbooked": pkg.capacity_plan.overbooked
            },
            "conflict_report": {
                "overlaps": pkg.conflict_report.overlaps_detected,
                "repetitions": pkg.conflict_report.repetition_issues,
                "blackout_violations": pkg.conflict_report.blackout_violations
            },
            "metrics": {
                "fill_rate": f"{pkg.metrics.calendar_fill_rate}%",
                "completion_rate": f"{pkg.metrics.campaign_completion_rate}%",
                "pillar_balance": f"{pkg.metrics.pillar_balance_score}%",
                "platform_balance": f"{pkg.metrics.platform_balance_score}%"
            },
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": f"{pkg.quality_gate.score}%",
                "checklist": pkg.quality_gate.checklist
            }
        }
