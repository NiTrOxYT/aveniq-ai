#!/usr/bin/env python3
"""
AVENIQ Market Intelligence CLI Control Center
Command Line Tool for executing production data collectors, viewing collector health, searching persisted market events, and managing research source configurations.

Commands:
  collect   - Execute all active market collectors, deduplicate, and persist events.
  status    - Display event count, category breakdown, and storage metrics.
  health    - Display health status for all registered collectors.
  sources   - List configured research sources, subreddits, RSS feeds, and competitors.
  search    - Search persisted market events by keyword, source, or category.
"""

import sys
import os
import argparse
import json

# Add project root to sys.path and remove the scripts/ directory entry
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_scripts_dir = os.path.abspath(os.path.dirname(__file__))
if _scripts_dir in sys.path:
    sys.path.remove(_scripts_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Auto-load .env
_env_file = os.path.join(_project_root, ".env")
if os.path.isfile(_env_file):
    with open(_env_file) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                os.environ.setdefault(_k.strip(), _v.strip())

from integrations.research.registry.collector_registry import global_collector_registry
from integrations.research.storage.market_storage import global_market_storage
from integrations.research.deduplication.deduplicator import EventDeduplicator
from integrations.research.config.workspace_config import WorkspaceResearchConfig
from integrations.research.event import MarketEvent

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Production Market Intelligence CLI Control Center")
    subparsers = parser.add_subparsers(dest="command", help="Market intelligence commands")

    p_collect = subparsers.add_parser("collect", help="Run active market collectors and store events")
    p_collect.add_argument("--topic", default="AI Agents", help="Target topic or keyword")

    subparsers.add_parser("status", help="Display market event storage metrics and stats")
    subparsers.add_parser("health", help="Display health status of all registered collectors")
    subparsers.add_parser("sources", help="List configured sources, subreddits, RSS feeds, and competitors")

    p_search = subparsers.add_parser("search", help="Search stored market events")
    p_search.add_argument("query", nargs="?", default="", help="Keyword query")
    p_search.add_argument("--source", default=None, help="Filter by source (reddit, github, rss, google_news, product_hunt, website)")
    p_search.add_argument("--category", default=None, help="Filter by category (trends, launches, funding, discussions, competitors)")
    p_search.add_argument("--limit", type=int, default=10, help="Maximum results to return")

    args = parser.parse_args()

    if args.command == "collect":
        print(f"\n=== EXECUTING MARKET INTELLIGENCE COLLECTORS (Topic: '{args.topic}') ===")
        collectors = global_collector_registry.enabled_collectors()
        raw_events: list[MarketEvent] = []

        for col in collectors:
            name = getattr(col, "source_name", "unknown")
            print(f"  • Running collector [{name}]...")
            events = col.collect_safe(args.topic)
            raw_events.extend(events)
            print(f"    └── Collected {len(events)} events.")

        deduper = EventDeduplicator()
        unique_events = deduper.deduplicate(raw_events)
        new_saved = global_market_storage.save_events(unique_events)

        print("\n" + "=" * 60)
        print(f"✅ COLLECTION COMPLETED")
        print(f"   Total Raw Collected : {len(raw_events)}")
        print(f"   Unique Deduplicated : {len(unique_events)}")
        print(f"   New Events Persisted: {new_saved}")
        print("=" * 60)

    elif args.command == "status":
        print("\n=== MARKET INTELLIGENCE STORAGE STATUS ===")
        stats = global_market_storage.get_stats()
        print(json.dumps(stats, indent=2))

    elif args.command == "health":
        print("\n=== MARKET INTELLIGENCE COLLECTORS HEALTH SUMMARY ===")
        health = global_collector_registry.health_summary()
        all_ready = all(data.get("status") in ("READY", "Healthy") for data in health.values())
        overall_status = "READY" if all_ready else "DEGRADED"

        output = {
            "overall_status": overall_status,
            "collectors_count": len(health),
            "collectors": health
        }
        print(json.dumps(output, indent=2))

    elif args.command == "sources":
        print("\n=== CONFIGURED MARKET RESEARCH SOURCES ===")
        cfg = WorkspaceResearchConfig(workspace_id="ws_default")
        sources_info = {
            "enabled_collectors": global_collector_registry.list_collectors(),
            "custom_rss_feeds": cfg.custom_rss_feeds,
            "competitor_domains": cfg.competitor_domains,
            "monitored_keywords": cfg.monitored_keywords,
            "excluded_keywords": cfg.excluded_keywords,
            "preferred_languages": cfg.preferred_languages
        }
        print(json.dumps(sources_info, indent=2))

    elif args.command == "search":
        print(f"\n=== SEARCHING MARKET EVENTS (Query: '{args.query}', Source: {args.source}, Category: {args.category}) ===")
        results = global_market_storage.search(
            query=args.query,
            source=args.source,
            category=args.category,
            limit=args.limit
        )

        if not results:
            # If storage is empty, auto-collect and search again
            print("No stored events found matching query. Running collectors now...")
            collectors = global_collector_registry.enabled_collectors()
            raw_events = []
            for col in collectors:
                raw_events.extend(col.collect_safe(args.query or "AI Agents"))
            deduper = EventDeduplicator()
            unique_events = deduper.deduplicate(raw_events)
            global_market_storage.save_events(unique_events)

            results = global_market_storage.search(
                query=args.query,
                source=args.source,
                category=args.category,
                limit=args.limit
            )

        print(f"Found {len(results)} matching market events:\n")
        for idx, evt in enumerate(results, 1):
            print(f"[{idx}] {evt.title}")
            print(f"    Source: {evt.source} | Category: {evt.category} | Published: {evt.published_at[:10]}")
            print(f"    URL   : {evt.url}")
            print(f"    Author: {evt.author} | Confidence: {evt.confidence * 100:.0f}%")
            print(f"    Text  : {evt.content[:150]}...")
            print("-" * 60)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
