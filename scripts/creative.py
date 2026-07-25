#!/usr/bin/env python3
"""
AVENIQ Creative Department CLI Control Center
Command Line Tool for generating visual design briefs, AI image/video prompts,
carousel layouts, storyboards, thumbnails, and multi-format aspect ratio specs.

Commands:
  hero        - Display Hero Image Brief & AI prompts (Midjourney, DALL-E 3, Flux, SDXL).
  infographic - Display process & architecture infographic specifications.
  carousel    - Display multi-slide LinkedIn/Instagram carousel design.
  video       - Display video storyboard, shot list, and Sora/Runway video prompts.
  thumbnail   - Display YouTube/Social thumbnail spec & prompts.
  package     - Generate full multi-format Media Package.
  review      - Display quality scores, accessibility alt-text, & quality gate checks.
  explain     - Display art direction, scene graph parameters, & prompt adapter breakdown.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from creative.reports.generator import CreativeReportGenerator
from creative.engine.creative_engine import CreativeEngine

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Creative Department CLI (AI Creative Director)")
    subparsers = parser.add_subparsers(dest="command", help="Creative commands")

    subparsers.add_parser("hero", help="Display hero image brief & prompts")
    subparsers.add_parser("infographic", help="Display infographic specs")
    subparsers.add_parser("carousel", help="Display carousel design specs")
    subparsers.add_parser("video", help="Display video storyboard & Sora prompt")
    subparsers.add_parser("thumbnail", help="Display thumbnail spec & prompts")
    subparsers.add_parser("package", help="Generate full Media Package")
    subparsers.add_parser("review", help="Display creative scores & accessibility")
    subparsers.add_parser("explain", help="Display style guide & prompt adapter breakdown")

    args = parser.parse_args()
    generator = CreativeReportGenerator()

    if args.command == "package":
        report = generator.generate_media_report()
        print("\n=== MASTER MEDIA PACKAGE REPORT ===")
        print(json.dumps(report, indent=2))
    elif args.command == "hero":
        report = generator.generate_media_report()
        print("\n=== HERO IMAGE BRIEF & AI PROMPTS ===")
        print(json.dumps(report["hero_brief"], indent=2))
    elif args.command == "infographic":
        report = generator.generate_media_report()
        print("\n=== INFOGRAPHIC SPECIFICATION ===")
        print(json.dumps(report["infographic_spec"], indent=2))
    elif args.command == "carousel":
        report = generator.generate_media_report()
        print("\n=== CAROUSEL DESIGN SPECIFICATION ===")
        print(json.dumps(report["carousel_design"], indent=2))
    elif args.command == "video":
        report = generator.generate_media_report()
        print("\n=== VIDEO STORYBOARD & AI PROMPTS ===")
        print(json.dumps(report["video_storyboard"], indent=2))
    elif args.command == "thumbnail":
        report = generator.generate_media_report()
        print("\n=== THUMBNAIL SPECIFICATION ===")
        print(json.dumps(report["thumbnail_spec"], indent=2))
    elif args.command == "review":
        report = generator.generate_media_report()
        print("\n=== CREATIVE SCORES & ACCESSIBILITY ===")
        print(json.dumps({
            "scores": report["creative_scores"],
            "quality_gate": report["quality_gate"],
            "accessibility": report["captions_and_accessibility"]
        }, indent=2))
    elif args.command == "explain":
        engine = CreativeEngine()
        pkg = engine.generate_media_package()
        print("\n=== ART DIRECTION & PROMPT ADAPTER BREAKDOWN ===")
        print(json.dumps({
            "style_guide": {
                "theme": pkg.visual_theme,
                "colors": pkg.style_guide.color_palette,
                "mood": pkg.style_guide.mood,
                "lighting": pkg.style_guide.lighting
            },
            "scene_graph": {
                "subject": pkg.hero_brief.spec.scene_graph.primary_subject,
                "background": pkg.hero_brief.spec.scene_graph.background,
                "lighting": pkg.hero_brief.spec.scene_graph.lighting
            },
            "prompts": {
                "midjourney": pkg.hero_brief.spec.prompts.midjourney_prompt,
                "dalle3": pkg.hero_brief.spec.prompts.dalle3_prompt,
                "flux": pkg.hero_brief.spec.prompts.flux_prompt,
                "sora": pkg.hero_brief.spec.prompts.sora_video_prompt
            }
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
