#!/usr/bin/env python3
"""
AVENIQ Calendar & Campaign Management CLI Control Center
Command Line Tool for 30-day rolling calendar generation, 90-day roadmap planning,
industry event tracking, campaign dependency graphs, and conflict detection.

Commands:
  month     - Display 30-Day Rolling Marketing Calendar.
  week      - Display Weekly Strategic Themes & Content Pillars.
  roadmap   - Display 90-Day Strategic Roadmap & Milestones.
  events    - Display Industry Conferences, Tech Summits, & Holidays.
  validate  - Run Calendar Quality Gate & Conflict Validation.
  explain   - Display scheduling rationale, blackout window checks, & capacity plans.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from calendar_dept.reports.generator import CalendarReportGenerator
from calendar_dept.engine.calendar_engine import CalendarEngine

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Calendar & Campaign Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Calendar commands")

    subparsers.add_parser("month", help="Display 30-Day Rolling Calendar")
    subparsers.add_parser("week", help="Display Weekly Themes & Pillars")
    subparsers.add_parser("roadmap", help="Display 90-Day Roadmap")
    subparsers.add_parser("events", help="Display Industry Events & Holidays")
    subparsers.add_parser("validate", help="Run Quality Gate & Conflict Checks")
    subparsers.add_parser("explain", help="Display scheduling rationale & capacity")

    args = parser.parse_args()
    generator = CalendarReportGenerator()

    if args.command == "month":
        report = generator.generate_calendar_report()
        print("\n=== 30-DAY ROLLING MARKETING CALENDAR ===")
        print(json.dumps(report["30day_calendar"], indent=2))
    elif args.command == "week":
        report = generator.generate_calendar_report()
        print("\n=== WEEKLY STRATEGIC THEMES & PILLARS ===")
        print(json.dumps(report["weekly_themes"], indent=2))
    elif args.command == "roadmap":
        report = generator.generate_calendar_report()
        print("\n=== 90-DAY STRATEGIC ROADMAP ===")
        print(json.dumps(report["90day_roadmap"], indent=2))
    elif args.command == "events":
        report = generator.generate_calendar_report()
        print("\n=== INDUSTRY CONFERENCES & HOLIDAYS ===")
        print(json.dumps(report["events"], indent=2))
    elif args.command == "validate":
        report = generator.generate_calendar_report()
        print("\n=== CALENDAR QUALITY GATE & CONFLICT AUDIT ===")
        print(json.dumps({
            "calendar_id": report["calendar_id"],
            "conflict_report": report["conflict_report"],
            "quality_gate": report["quality_gate"]
        }, indent=2))
    elif args.command == "explain":
        engine = CalendarEngine()
        pkg = engine.generate_calendar_package()
        print("\n=== SCHEDULING RATIONALE & CAPACITY BREAKDOWN ===")
        print(json.dumps({
            "calendar_id": pkg.id,
            "campaigns": [
                {
                    "name": c.name,
                    "type": c.campaign_type,
                    "priority": c.priority,
                    "dependencies": c.dependencies
                } for c in pkg.campaigns
            ],
            "capacity_plan": {
                "writer_hours": pkg.capacity_plan.writer_hours_allocated,
                "designer_hours": pkg.capacity_plan.designer_hours_allocated,
                "overbooked": pkg.capacity_plan.overbooked
            },
            "metrics": {
                "fill_rate": f"{pkg.metrics.calendar_fill_rate}%",
                "completion_rate": f"{pkg.metrics.campaign_completion_rate}%"
            }
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
