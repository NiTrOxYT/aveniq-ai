#!/usr/bin/env python3
"""
AVENIQ Planning Department CLI Control Center
Command Line Tool for generating operational Planning Packages, inspecting calendars,
asset requirements, workflow diagrams, and dependency graphs.

Commands:
  campaign     - Display active campaign objectives, themes, and milestones.
  calendar     - Display editorial calendar and content sequence.
  schedule     - Display timezone-aware publishing schedule.
  assets       - Display required asset checklist and visual requirements.
  workflow     - Display 7-state execution workflow and step owners.
  dependencies - Display asset-first dependency graph and critical path.
  report       - Generate full operational Planning Package.
  explain      - Display operational decision reasoning, risks, and capacity estimates.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from planning.reports.generator import PlanningReportGenerator
from planning.engine.planning_engine import PlanningEngine

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Planning Department CLI (AI COO)")
    subparsers = parser.add_subparsers(dest="command", help="Planning commands")

    subparsers.add_parser("campaign", help="Display campaign details")
    subparsers.add_parser("calendar", help="Display editorial calendar")
    subparsers.add_parser("schedule", help="Display publishing schedule")
    subparsers.add_parser("assets", help="Display asset checklist")
    subparsers.add_parser("workflow", help="Display workflow diagram")
    subparsers.add_parser("dependencies", help="Display dependency graph")
    subparsers.add_parser("report", help="Generate full Planning Package")
    subparsers.add_parser("explain", help="Display operational decision reasoning & risks")

    args = parser.parse_args()
    generator = PlanningReportGenerator()

    if args.command == "report":
        report = generator.generate_planning_report()
        print("\n=== MASTER OPERATIONAL PLANNING PACKAGE ===")
        print(json.dumps(report, indent=2))
    elif args.command == "campaign":
        report = generator.generate_planning_report()
        print("\n=== CAMPAIGN PLAN ===")
        print(json.dumps(report["campaign"], indent=2))
    elif args.command == "calendar":
        report = generator.generate_planning_report()
        print("\n=== EDITORIAL CALENDAR ===")
        print(json.dumps(report["editorial_calendar"], indent=2))
    elif args.command == "schedule":
        report = generator.generate_planning_report()
        print("\n=== PUBLISHING SCHEDULE ===")
        print(json.dumps(report["publishing_schedule"], indent=2))
    elif args.command == "assets":
        report = generator.generate_planning_report()
        print("\n=== ASSET CHECKLIST ===")
        print(json.dumps(report["required_assets"], indent=2))
    elif args.command == "workflow":
        report = generator.generate_planning_report()
        print("\n=== EXECUTION WORKFLOW DIAGRAM ===")
        print(json.dumps(report["workflow_diagram"], indent=2))
    elif args.command == "dependencies":
        report = generator.generate_planning_report()
        print("\n=== DEPENDENCY GRAPH & CRITICAL PATH ===")
        print(json.dumps(report["dependency_graph"], indent=2))
    elif args.command == "explain":
        engine = PlanningEngine()
        pkg = engine.generate_planning_package()
        print("\n=== OPERATIONAL DECISION REASONING & RISKS ===")
        print(json.dumps({
            "confidence_score": f"{int(pkg.confidence_score * 100)}%",
            "quality_score": f"{pkg.quality_gate.score}%",
            "risk_assessment": {
                "score": f"{pkg.risk_assessment.risk_score}/100",
                "mitigations": pkg.risk_assessment.mitigation_plan
            },
            "capacity": {
                "deliverables": pkg.resource_estimate.deliverable_count,
                "production_hours": pkg.resource_estimate.estimated_production_hours
            }
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
