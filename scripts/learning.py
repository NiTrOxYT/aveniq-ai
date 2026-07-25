#!/usr/bin/env python3
"""
AVENIQ Learning Department CLI Control Center
Command Line Tool for executing continuous learning analysis, pattern recognition,
duplicate scanning, multi-department recommendations, and Company Brain proposals.

Commands:
  analyze         - Run full continuous learning analysis sweep.
  report          - Display comprehensive Learning Report.
  recommendations - Display multi-department recommendations & Knowledge Proposals.
  duplicates      - Display duplicate hook & prompt scan report.
  trends          - Display topic trends, content pillars, & brand evolution.
  explain         - Display recommendation rationales, confidence scores, & benefits.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from learning.reports.generator import LearningReportGenerator
from learning.engine.learning_engine import LearningEngine

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Learning Department CLI (AI Learning Manager)")
    subparsers = parser.add_subparsers(dest="command", help="Learning commands")

    subparsers.add_parser("analyze", help="Run learning analysis sweep")
    subparsers.add_parser("report", help="Display full Learning Report")
    subparsers.add_parser("recommendations", help="Display recommendations & proposals")
    subparsers.add_parser("duplicates", help="Display duplicate scan report")
    subparsers.add_parser("trends", help="Display topic & brand trends")
    subparsers.add_parser("explain", help="Display recommendation rationales & confidence")

    args = parser.parse_args()
    generator = LearningReportGenerator()

    if args.command == "analyze" or args.command == "report":
        report = generator.generate_learning_report()
        print("\n=== MASTER LEARNING PACKAGE REPORT ===")
        print(json.dumps(report, indent=2))
    elif args.command == "recommendations":
        report = generator.generate_learning_report()
        print("\n=== MULTI-DEPARTMENT RECOMMENDATIONS & PROPOSALS ===")
        print(json.dumps({
            "recommendations": report["recommendations"],
            "knowledge_proposals": report["knowledge_proposals"]
        }, indent=2))
    elif args.command == "duplicates":
        report = generator.generate_learning_report()
        print("\n=== DUPLICATE SCAN REPORT ===")
        print(json.dumps(report["duplicate_report"], indent=2))
    elif args.command == "trends":
        report = generator.generate_learning_report()
        print("\n=== TOPIC TRENDS & BRAND EVOLUTION ===")
        print(json.dumps({
            "topics": report["topic_summary"],
            "brand_evolution": report["brand_evolution"],
            "learning_metrics": report["learning_metrics"]
        }, indent=2))
    elif args.command == "explain":
        engine = LearningEngine()
        pkg = engine.generate_learning_package()
        print("\n=== RECOMMENDATION RATIONALES & CONFIDENCE BREAKDOWN ===")
        print(json.dumps({
            "learning_id": pkg.id,
            "recommendations": [
                {
                    "department": r.target_department,
                    "text": r.recommendation_text,
                    "rationale": r.rationale,
                    "confidence": f"{int(r.confidence_score * 100)}%",
                    "expected_benefit": r.expected_benefit
                } for r in pkg.recommendations
            ],
            "proposals": [
                {
                    "target_file": p.target_file,
                    "change": p.proposed_change,
                    "citation": p.evidence_citation
                } for p in pkg.knowledge_proposals
            ]
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
