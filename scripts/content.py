#!/usr/bin/env python3
"""
AVENIQ Content Department CLI Control Center
Command Line Tool for generating platform-ready written assets, inspecting articles,
social copy, newsletters, SEO metadata, and quality scores.

Commands:
  article    - Display master technical article and engineering breakdown.
  linkedin   - Display LinkedIn post and carousel copy.
  instagram  - Display Instagram visual caption copy.
  newsletter - Display technical newsletter issue.
  package    - Generate full multi-channel Content Package.
  seo        - Display SEO metadata, slugs, and internal linking structure.
  review     - Display 8-state review workflow status and quality gate scores.
  explain    - Display content decision reasoning, variations, and scoring breakdown.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from content.reports.generator import ContentReportGenerator
from content.engine.content_engine import ContentEngine

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Content Department CLI (AI Content Director)")
    subparsers = parser.add_subparsers(dest="command", help="Content commands")

    subparsers.add_parser("article", help="Display master technical article")
    subparsers.add_parser("linkedin", help="Display LinkedIn post & carousel copy")
    subparsers.add_parser("instagram", help="Display Instagram caption")
    subparsers.add_parser("newsletter", help="Display technical newsletter")
    subparsers.add_parser("package", help="Generate full Content Package")
    subparsers.add_parser("seo", help="Display SEO metadata & links")
    subparsers.add_parser("review", help="Display review workflow & quality scores")
    subparsers.add_parser("explain", help="Display content decision reasoning & variations")

    args = parser.parse_args()
    generator = ContentReportGenerator()

    if args.command == "package":
        report = generator.generate_content_report()
        print("\n=== MASTER CONTENT PACKAGE REPORT ===")
        print(json.dumps(report, indent=2))
    elif args.command == "article":
        report = generator.generate_content_report()
        print("\n=== MASTER TECHNICAL ARTICLE ===")
        print(json.dumps(report["master_article"], indent=2))
    elif args.command == "linkedin":
        report = generator.generate_content_report()
        print("\n=== LINKEDIN POST & CAROUSEL COPY ===")
        print(json.dumps({
            "post": report["social_posts"]["linkedin"],
            "carousel": report["carousel_copy"]
        }, indent=2))
    elif args.command == "instagram":
        report = generator.generate_content_report()
        print("\n=== INSTAGRAM CAPTION ===")
        print(json.dumps(report["social_posts"]["linkedin"], indent=2))
    elif args.command == "newsletter":
        report = generator.generate_content_report()
        print("\n=== TECHNICAL NEWSLETTER ===")
        print(json.dumps(report["newsletter"], indent=2))
    elif args.command == "seo":
        report = generator.generate_content_report()
        print("\n=== SEO METADATA & LINKS ===")
        print(json.dumps({
            "slug": report["master_article"]["slug"],
            "meta_title": report["master_article"]["meta_title"],
            "meta_description": report["master_article"]["meta_description"],
            "internal_links": report["master_article"]["internal_links"]
        }, indent=2))
    elif args.command == "review":
        report = generator.generate_content_report()
        print("\n=== EDITORIAL REVIEW & QUALITY SCORES ===")
        print(json.dumps({
            "workflow_state": report["workflow_state"],
            "quality_gate": report["quality_gate"],
            "scores": report["content_scores"]
        }, indent=2))
    elif args.command == "explain":
        engine = ContentEngine()
        pkg = engine.generate_content_package()
        print("\n=== CONTENT DECISION REASONING & VARIATIONS ===")
        print(json.dumps({
            "decisions": pkg.decision_reasoning,
            "variations": {
                "titles": pkg.variations.alternative_titles,
                "hooks": pkg.variations.alternative_hooks,
                "ctas": pkg.variations.cta_variations
            },
            "scores": {
                "overall": pkg.scores.overall_score,
                "brand": pkg.scores.brand_alignment_score,
                "seo": pkg.scores.seo_score,
                "authority": pkg.scores.authority_score
            }
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
