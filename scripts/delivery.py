#!/usr/bin/env python3
"""
AVENIQ Delivery Department CLI Control Center
Command Line Tool for assembling delivery packages, exporting ZIP/Markdown bundles,
verifying SHA-256 asset checksums, and validating publishing readiness.

Commands:
  package     - Assemble complete multi-platform Delivery Package.
  export      - Generate multi-format exports (JSON, Markdown, HTML, PDF, ZIP).
  attachments - Display asset inventory, file paths, & SHA-256 checksums.
  validate    - Run delivery readiness validation & quality gate checks.
  report      - Display comprehensive Delivery Package Report.
  explain     - Display delivery manifest parameters, platform bundles, & posting recommendations.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from delivery.reports.generator import DeliveryReportGenerator
from delivery.engine.delivery_engine import DeliveryEngine

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Delivery Department CLI (AI Delivery Manager)")
    subparsers = parser.add_subparsers(dest="command", help="Delivery commands")

    subparsers.add_parser("package", help="Assemble complete Delivery Package")
    subparsers.add_parser("export", help="Generate multi-format exports")
    subparsers.add_parser("attachments", help="Display asset inventory & checksums")
    subparsers.add_parser("validate", help="Run delivery readiness validation")
    subparsers.add_parser("report", help="Display full Delivery Report")
    subparsers.add_parser("explain", help="Display delivery manifest & platform bundles")

    args = parser.parse_args()
    generator = DeliveryReportGenerator()

    if args.command == "package" or args.command == "report":
        report = generator.generate_delivery_report()
        print("\n=== MASTER DELIVERY PACKAGE REPORT ===")
        print(json.dumps(report, indent=2))
    elif args.command == "export":
        report = generator.generate_delivery_report()
        print("\n=== MULTI-FORMAT EXPORT BUNDLES ===")
        print(json.dumps(report["exports"], indent=2))
    elif args.command == "attachments":
        report = generator.generate_delivery_report()
        print("\n=== ASSET INVENTORY & SHA-256 CHECKSUMS ===")
        print(json.dumps({
            "attachments": report["attachments"],
            "checksums": report["manifest"]["checksums"]
        }, indent=2))
    elif args.command == "validate":
        report = generator.generate_delivery_report()
        print("\n=== DELIVERY READINESS & QUALITY GATE ===")
        print(json.dumps({
            "status": report["manifest"]["status"],
            "quality_gate": report["quality_gate"],
            "scores": report["scores"]
        }, indent=2))
    elif args.command == "explain":
        engine = DeliveryEngine()
        pkg = engine.assemble_delivery_package()
        print("\n=== DELIVERY MANIFEST & PLATFORM BUNDLES BREAKDOWN ===")
        print(json.dumps({
            "manifest": {
                "delivery_id": pkg.manifest.delivery_id,
                "campaign_id": pkg.manifest.campaign_id,
                "status": pkg.manifest.delivery_status
            },
            "platforms": list(pkg.platform_bundles.keys()),
            "zip_export_path": pkg.exports.zip_path,
            "overall_score": f"{pkg.scores.overall_delivery_score}/100"
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
