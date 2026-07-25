#!/usr/bin/env python3
"""
AVENIQ Archive Department CLI Control Center
Command Line Tool for persisting Delivery Packages into immutable archive packages,
executing multi-attribute search, displaying relationship graphs, & retrieving snapshots.

Commands:
  archive  - Persist Delivery Package into immutable Archive Package.
  search   - Execute multi-attribute search query across archived packages.
  retrieve - Retrieve exact Archive Package by ID or version snapshot.
  validate - Run archive integrity validation & quality gate checks.
  report   - Display full Archive Package & Audit Report.
  explain  - Display relationship graph, event log, & vector embedding metrics.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from archive.reports.generator import ArchiveReportGenerator
from archive.repository.manager import ArchiveRepositoryManager
from archive.search.archive_search import ArchiveSearchEngine
from archive.engine.archive_engine import ArchiveEngine

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Archive Department CLI (AI Archivist)")
    subparsers = parser.add_subparsers(dest="command", help="Archive commands")

    subparsers.add_parser("archive", help="Persist Delivery Package to Archive")
    
    search_parser = subparsers.add_parser("search", help="Search archived packages")
    search_parser.add_argument("--query", "-q", default="AI", help="Search query string")

    subparsers.add_parser("retrieve", help="Retrieve archived package")
    subparsers.add_parser("validate", help="Run archive validation")
    subparsers.add_parser("report", help="Display full Archive Report")
    subparsers.add_parser("explain", help="Display event log & relationship graph")

    args = parser.parse_args()
    generator = ArchiveReportGenerator()
    repository = ArchiveRepositoryManager()

    if args.command == "archive" or args.command == "report" or args.command == "retrieve":
        report = generator.generate_archive_report()
        print("\n=== IMMUTABLE ARCHIVE PACKAGE REPORT ===")
        print(json.dumps(report, indent=2))
    elif args.command == "search":
        report = generator.generate_archive_report()
        pkgs = repository.list_archived_packages()
        results = ArchiveSearchEngine.search(args.query, pkgs)
        print(f"\n=== SEARCH RESULTS FOR '{args.query}' ===")
        print(json.dumps({
            "query": args.query,
            "total_matches": len(results),
            "results": [
                {
                    "archive_id": r.archive_id,
                    "campaign_id": r.campaign_id,
                    "topic": r.topic,
                    "score": r.score,
                    "matched_field": r.matched_field
                } for r in results
            ]
        }, indent=2))
    elif args.command == "validate":
        report = generator.generate_archive_report()
        print("\n=== ARCHIVE INTEGRITY & QUALITY GATE ===")
        print(json.dumps({
            "archive_id": report["archive_id"],
            "lifecycle_state": report["lifecycle_state"],
            "quality_gate": report["quality_gate"]
        }, indent=2))
    elif args.command == "explain":
        engine = ArchiveEngine()
        pkg = engine.archive_delivery_package()
        print("\n=== KNOWLEDGE GRAPH & EVENT LOG BREAKDOWN ===")
        print(json.dumps({
            "archive_id": pkg.id,
            "campaign_id": pkg.manifest.campaign_id,
            "events_count": len(pkg.events),
            "relationship_nodes": pkg.relationship_graph.nodes,
            "vector_embedding_dims": len(pkg.vector_embedding)
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
