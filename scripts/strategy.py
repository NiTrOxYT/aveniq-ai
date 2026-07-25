#!/usr/bin/env python3
"""
AVENIQ Strategy Department CLI Control Center
Command Line Tool for generating daily, weekly, and monthly marketing plans,
inspecting strategic reasoning, target audiences, SEO setups, and campaign roadmaps.

Commands:
  today         - Generate today's actionable Daily Marketing Strategy Plan.
  weekly        - Generate weekly marketing strategy and campaign focus.
  monthly       - Generate monthly strategic roadmap and content calendar.
  opportunities - List ranked market opportunities.
  campaigns     - Display active and planned marketing campaigns.
  audience      - Display target audience persona profile and intent mapping.
  seo           - Display SEO keyword priorities and content cluster plans.
  explain       - Display structured strategic reasoning and evidence for today's plan.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from strategy.reports.generator import StrategyReportGenerator

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Strategy Department CLI (AI CMO)")
    subparsers = parser.add_subparsers(dest="command", help="Strategy commands")

    subparsers.add_parser("today", help="Generate today's marketing strategy plan")
    subparsers.add_parser("weekly", help="Generate weekly marketing strategy")
    subparsers.add_parser("monthly", help="Generate monthly strategic roadmap")
    subparsers.add_parser("opportunities", help="Display ranked market opportunities")
    subparsers.add_parser("campaigns", help="Display active & planned campaigns")
    subparsers.add_parser("audience", help="Display target audience persona profile")
    subparsers.add_parser("seo", help="Display SEO keyword priorities")
    subparsers.add_parser("explain", help="Display decision reasoning & supporting evidence")

    args = parser.parse_args()

    generator = StrategyReportGenerator()

    if args.command == "today":
        report = generator.generate_daily_report()
        print("\n=== TODAY'S MARKETING STRATEGY PLAN ===")
        print(json.dumps(report, indent=2))
    elif args.command == "weekly":
        report = generator.generate_weekly_report()
        print("\n=== WEEKLY MARKETING STRATEGY SUMMARY ===")
        print(json.dumps(report, indent=2))
    elif args.command == "monthly":
        report = generator.generate_monthly_report()
        print("\n=== MONTHLY STRATEGIC ROADMAP ===")
        print(json.dumps(report, indent=2))
    elif args.command == "opportunities":
        report = generator.generate_daily_report()
        print("\n=== RANKED MARKET OPPORTUNITIES ===")
        print(json.dumps({
            "topic": report["content"]["suggested_title"],
            "priority": report["priority"],
            "category": report["content"]["category"]
        }, indent=2))
    elif args.command == "campaigns":
        report = generator.generate_weekly_report()
        print("\n=== STRATEGIC CAMPAIGNS ===")
        print(json.dumps({
            "top_campaign": report["top_campaign"],
            "content_mix": report["content_mix"]
        }, indent=2))
    elif args.command == "audience":
        report = generator.generate_daily_report()
        print("\n=== TARGET AUDIENCE PROFILE ===")
        print(json.dumps(report["audience"], indent=2))
    elif args.command == "seo":
        report = generator.generate_daily_report()
        print("\n=== SEO KEYWORD PRIORITIES ===")
        print(json.dumps(report["seo"], indent=2))
    elif args.command == "explain":
        report = generator.generate_daily_report()
        print("\n=== STRATEGIC DECISION REASONING & EVIDENCE ===")
        print(json.dumps({
            "decision": f"Publish recommendation on '{report['content']['suggested_title']}'",
            "business_goal": report["primary_goal"],
            "confidence": report["confidence"],
            "reasoning": report["reasoning"]
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
