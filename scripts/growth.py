#!/usr/bin/env python3
"""
AVENIQ Brand Growth Intelligence CLI Control Center
Command Line Tool for business objective management, campaign portfolio synthesis,
7-stage funnel allocation, KPI outcome forecasting, and scenario modeling.

Commands:
  goals     - Display Active Business Goals & Objective Hierarchy.
  portfolio - Display Multi-Campaign Portfolio & Content Mix.
  funnel    - Display 7-Stage Funnel Allocation & KPI Forecasts.
  explain   - Display objective tree hierarchy, KPI forecasts, & scenario comparisons.
  validate  - Run Growth Quality Gate & KPI Alignment Audit.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from growth.reports.generator import GrowthReportGenerator
from growth.engine.growth_engine import GrowthEngine

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Brand Growth Intelligence CLI")
    subparsers = parser.add_subparsers(dest="command", help="Growth commands")

    subparsers.add_parser("goals", help="Display Business Goals & Objectives")
    subparsers.add_parser("portfolio", help="Display Campaign Portfolio & Mix")
    subparsers.add_parser("funnel", help="Display Funnel Allocation & Forecast")
    subparsers.add_parser("explain", help="Display rationale & scenario models")
    subparsers.add_parser("validate", help="Run Quality Gate & Alignment Audit")

    args = parser.parse_args()
    generator = GrowthReportGenerator()

    if args.command == "goals":
        report = generator.generate_growth_report()
        print("\n=== ACTIVE BUSINESS GOALS & OBJECTIVE TREE ===")
        print(json.dumps({
            "goals": report["goals"],
            "objective_tree": report["objective_tree"]
        }, indent=2))
    elif args.command == "portfolio":
        report = generator.generate_growth_report()
        print("\n=== CAMPAIGN PORTFOLIO & CONTENT MIX ===")
        print(json.dumps({
            "portfolio": report["portfolio"],
            "content_mix": report["content_mix"]
        }, indent=2))
    elif args.command == "funnel":
        report = generator.generate_growth_report()
        print("\n=== 7-STAGE FUNNEL ALLOCATION & KPI FORECAST ===")
        print(json.dumps({
            "funnel_allocation": report["funnel_allocation"],
            "forecast": report["forecast"]
        }, indent=2))
    elif args.command == "validate":
        report = generator.generate_growth_report()
        print("\n=== GROWTH QUALITY GATE & AUDIT ===")
        print(json.dumps({
            "growth_id": report["growth_id"],
            "metrics": report["metrics"],
            "quality_gate": report["quality_gate"]
        }, indent=2))
    elif args.command == "explain":
        engine = GrowthEngine()
        pkg = engine.generate_growth_package()
        print("\n=== STRATEGIC RATIONALE & SCENARIO MODELS ===")
        print(json.dumps({
            "growth_id": pkg.id,
            "annual_objective": pkg.objective_tree.annual_goal,
            "scenarios": [
                {
                    "name": s.scenario_name,
                    "leads": s.projected_leads,
                    "reach": s.projected_reach,
                    "campaigns": s.required_campaigns_count
                } for s in pkg.scenarios
            ],
            "metrics": {
                "kpi_coverage": f"{pkg.metrics.kpi_coverage_score}%",
                "overall_score": f"{pkg.metrics.overall_growth_score}%"
            }
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
