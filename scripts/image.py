#!/usr/bin/env python3
"""
AVENIQ Image Generation Platform CLI Control Center
Command Line Tool for generating visual marketing assets across 11 platform layout templates, listing templates & history, and regenerating assets.

Commands:
  generate    - Generate campaign visual assets (Hero, Carousel, Infographic, Thumbnail, etc.).
  templates   - Display supported layout templates & resolution safe zones.
  history     - Display Asset Library Store generation history.
  regenerate  - Regenerate an asset with feedback tags (e.g. 'More Premium', 'More Minimal').
  status      - Display Image Generation Platform health & active providers.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from image_generation.router.image_router import global_campaign_image_router
from image_generation.templates.templates import TemplateEngine
from image_generation.storage.asset_store import global_asset_store
from image_generation.providers.gemini_image import GeminiImageProvider

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Image Generation Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Image commands")

    p_gen = subparsers.add_parser("generate", help="Generate visual marketing assets")
    p_gen.add_argument("--template", default="hero", help="Target layout template")
    p_gen.add_argument("--campaign", default="cmp_2026-07-26_001", help="Campaign ID")
    p_gen.add_argument("--topic", default="Autonomous AI Marketing Platform", help="Topic name")

    subparsers.add_parser("templates", help="List layout templates")
    subparsers.add_parser("history", help="Display asset store history")

    p_reg = subparsers.add_parser("regenerate", help="Regenerate asset with feedback tag")
    p_reg.add_argument("--asset-id", required=True, help="Asset ID")
    p_reg.add_argument("--feedback", default="More Premium", help="Feedback tag")

    subparsers.add_parser("status", help="Display platform status")

    args = parser.parse_args()

    if args.command == "generate":
        job = global_campaign_image_router.generate_campaign_assets(
            campaign_id=args.campaign,
            creative_package_data={"topic": args.topic, "visual_theme": "Modern Glassmorphism"},
            requested_templates=[args.template]
        )
        for a in job.generated_assets:
            global_asset_store.save_asset(a)

        print(f"\n=== VISUAL ASSET GENERATED (Template: '{args.template}') ===")
        print(json.dumps([{
            "asset_id": a.asset_id,
            "template_type": a.template_type,
            "platform": a.platform,
            "file_path": a.file_path,
            "resolution": f"{a.width}x{a.height}",
            "aspect_ratio": a.aspect_ratio,
            "provider": a.provider_used
        } for a in job.generated_assets], indent=2))
    elif args.command == "templates":
        print("\n=== SUPPORTED LAYOUT TEMPLATES ===")
        print(json.dumps(TemplateEngine.list_templates(), indent=2))
    elif args.command == "history":
        print("\n=== ASSET LIBRARY STORE HISTORY ===")
        assets = global_asset_store.list_assets()
        print(json.dumps([{
            "asset_id": a.asset_id,
            "template_type": a.template_type,
            "platform": a.platform,
            "version": a.version,
            "status": a.approval_status.value
        } for a in assets], indent=2))
    elif args.command == "regenerate":
        updated = global_asset_store.update_feedback(args.asset_id, args.feedback)
        print(f"\n=== ASSET REGENERATED (Feedback: '{args.feedback}') ===")
        if updated:
            print(json.dumps({
                "asset_id": updated.asset_id,
                "version": updated.version,
                "feedback_tag": updated.feedback_tag,
                "status": updated.approval_status.value
            }, indent=2))
    elif args.command == "status":
        prov = GeminiImageProvider()
        print("\n=== IMAGE GENERATION PLATFORM STATUS ===")
        print(json.dumps({
            "active_provider": prov.health(),
            "supported_templates_count": len(TemplateEngine.list_templates()),
            "stored_assets_count": len(global_asset_store.list_assets())
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
