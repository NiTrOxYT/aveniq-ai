#!/usr/bin/env python3
"""
AVENIQ Research Department CLI Control Center
Command Line Tool for generating evidence-backed Research Packages,
verifying sources, inspecting citations, and executing Quality Gate sweeps.

Commands:
  package     - Generate full evidence-backed Research Package.
  topic       - Display research executive summary and key findings.
  verify      - Run Quality Gate verification sweep (8 mandatory gates).
  statistics  - Display verified industry statistics and benchmarks.
  competitors - Display competitor feature, pricing, and positioning findings.
  seo         - Display SEO search patterns, user questions, and SERP gaps.
  sources     - Display structured citations and reference list.
  explain     - Display research confidence scores and knowledge gap analysis.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from research.reports.generator import ResearchReportGenerator
from research.engine.research_engine import ResearchEngine

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Research Department CLI (Senior Research Analyst)")
    subparsers = parser.add_subparsers(dest="command", help="Research commands")

    subparsers.add_parser("package", help="Generate full Research Package")
    subparsers.add_parser("topic", help="Display research executive summary")
    subparsers.add_parser("verify", help="Run Quality Gate verification sweep")
    subparsers.add_parser("statistics", help="Display verified statistics")
    subparsers.add_parser("competitors", help="Display competitor research")
    subparsers.add_parser("seo", help="Display SEO insights and search questions")
    subparsers.add_parser("sources", help="Display structured citations")
    subparsers.add_parser("explain", help="Display research confidence & knowledge gaps")

    args = parser.parse_args()
    generator = ResearchReportGenerator()

    if args.command == "package":
        report = generator.generate_package_report()
        print("\n=== RESEARCH PACKAGE REPORT ===")
        print(json.dumps(report, indent=2))
    elif args.command == "topic":
        report = generator.generate_package_report()
        print("\n=== TOPIC EXECUTIVE SUMMARY ===")
        print(json.dumps({
            "topic": report["topic"],
            "confidence_score": report["confidence_score"],
            "executive_summary": report["executive_summary"],
            "key_findings": report["key_findings"]
        }, indent=2))
    elif args.command == "verify":
        engine = ResearchEngine()
        pkg = engine.generate_research_package()
        print("\n=== QUALITY GATE VERIFICATION SWEEP ===")
        print(json.dumps({
            "passed": pkg.quality_gate.passed,
            "score": f"{pkg.quality_gate.score}%",
            "gate_checks": pkg.quality_gate.gate_checks,
            "diagnostics": pkg.quality_gate.diagnostics
        }, indent=2))
    elif args.command == "statistics":
        report = generator.generate_package_report()
        print("\n=== VERIFIED INDUSTRY STATISTICS ===")
        print(json.dumps(report["verified_statistics"], indent=2))
    elif args.command == "competitors":
        report = generator.generate_package_report()
        print("\n=== COMPETITOR RESEARCH FINDINGS ===")
        print(json.dumps(report["competitor_insights"], indent=2))
    elif args.command == "seo":
        report = generator.generate_package_report()
        print("\n=== SEO SEARCH PATTERNS & GAPS ===")
        print(json.dumps(report["seo_insights"], indent=2))
    elif args.command == "sources":
        report = generator.generate_package_report()
        print("\n=== CITATIONS & REFERENCE LIST ===")
        print(json.dumps(report["citations"], indent=2))
    elif args.command == "explain":
        engine = ResearchEngine()
        pkg = engine.generate_research_package()
        print("\n=== RESEARCH EXPLAINABILITY & GAPS ===")
        print(json.dumps({
            "confidence_score": f"{int(pkg.confidence_score * 100)}%",
            "quality_score": f"{pkg.quality_gate.score}%",
            "knowledge_gaps": pkg.knowledge_gaps,
            "further_research_suggestions": pkg.further_research_suggestions
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
