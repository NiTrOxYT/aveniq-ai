#!/usr/bin/env python3
"""
AVENIQ Editorial Department CLI Control Center
Command Line Tool for executing quality assurance, hallucination checking,
claim verification, copyright risk assessment, and approval workflows.

Commands:
  review    - Display editorial scorecard, issue count, & review summary.
  grammar   - Display grammar score & sentence structure findings.
  seo       - Display SEO compliance score & keyword placement verification.
  claims    - Display technical/marketing claim verifications & evidence mapping.
  copyright - Display copyright risk score & quoted material attribution.
  approve   - Run full editorial review & generate Approved Content Package.
  report    - Display comprehensive Editorial & Publishing Readiness Report.
  explain   - Display approval decision rationale, triggered policy rules, & red flags.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from editorial.reports.generator import EditorialReportGenerator
from editorial.engine.editorial_engine import EditorialEngine

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Editorial Department CLI (AI Editor-in-Chief)")
    subparsers = parser.add_subparsers(dest="command", help="Editorial commands")

    subparsers.add_parser("review", help="Display editorial review summary")
    subparsers.add_parser("grammar", help="Display grammar review findings")
    subparsers.add_parser("seo", help="Display SEO review findings")
    subparsers.add_parser("claims", help="Display claim verification & evidence map")
    subparsers.add_parser("copyright", help="Display copyright risk assessment")
    subparsers.add_parser("approve", help="Run editorial approval sweep")
    subparsers.add_parser("report", help="Display full Editorial Report")
    subparsers.add_parser("explain", help="Display decision rationale & red flags")

    args = parser.parse_args()
    generator = EditorialReportGenerator()

    if args.command == "approve" or args.command == "report":
        report = generator.generate_editorial_report()
        print("\n=== APPROVED CONTENT PACKAGE REPORT ===")
        print(json.dumps(report, indent=2))
    elif args.command == "review":
        report = generator.generate_editorial_report()
        print("\n=== EDITORIAL SCORECARD & REVIEW SUMMARY ===")
        print(json.dumps({
            "decision": report["approval_decision"],
            "scorecard": report["scorecard"],
            "publishing_readiness": report["publishing_readiness"],
            "quality_gate": report["quality_gate"]
        }, indent=2))
    elif args.command == "grammar":
        report = generator.generate_editorial_report()
        print("\n=== GRAMMAR REVIEW FINDINGS ===")
        print(json.dumps({
            "grammar_score": report["scorecard"]["grammar"],
            "issues": [i for i in report["issues"] if i["category"] == "Grammar"]
        }, indent=2))
    elif args.command == "seo":
        report = generator.generate_editorial_report()
        print("\n=== SEO REVIEW FINDINGS ===")
        print(json.dumps({
            "seo_score": report["scorecard"]["seo"],
            "issues": [i for i in report["issues"] if i["category"] == "SEO"]
        }, indent=2))
    elif args.command == "claims":
        report = generator.generate_editorial_report()
        print("\n=== CLAIMS VERIFICATION & EVIDENCE MAP ===")
        print(json.dumps({
            "claims": report["claims_verification"],
            "evidence_map": report["evidence_map"]
        }, indent=2))
    elif args.command == "copyright":
        report = generator.generate_editorial_report()
        print("\n=== COPYRIGHT RISK ASSESSMENT ===")
        print(json.dumps({
            "copyright_risk_score": report["scorecard"]["copyright_risk"],
            "hallucination_risk_score": report["scorecard"]["hallucination_risk"]
        }, indent=2))
    elif args.command == "explain":
        engine = EditorialEngine()
        pkg = engine.review_and_approve_content()
        print("\n=== APPROVAL DECISION RATIONALE & RED FLAGS ===")
        print(json.dumps({
            "status": pkg.approval_decision.status,
            "rationale": pkg.approval_decision.reason_rationale,
            "triggered_rules": pkg.approval_decision.triggered_rules,
            "blocking_issues_count": pkg.approval_decision.blocking_issues_count,
            "red_flags": [rf.statement for rf in pkg.red_flags],
            "confidence_score": f"{int(pkg.confidence_score * 100)}%"
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
