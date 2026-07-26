#!/usr/bin/env python3
"""
AVENIQ Integration Platform CLI Control Center & Real Market Intelligence CLI
Command Line Tool for inspecting provider health, testing LLM & Image Routers,
and running real-time market research collectors (Reddit, HN, Google Trends, GitHub, Dev.to).

Commands:
  health       - Display health status across all registered providers & market collectors.
  test-llm     - Test LLM Provider Router with failover.
  test-image   - Test Image Generation Provider Router.
  research     - Execute real-time market research pipeline.
  sources      - Display active market intelligence collectors & RSS feeds.
  topics       - Display trending semantic topic clusters & trend scores.
  opportunities- Display evidence-backed market opportunities.
  stats        - Display integration metrics & traces.
  profile      - Display active provider configuration profile.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from integrations.registry.global_registry import global_registry
from integrations.llm.router import global_llm_router
from integrations.image.router import global_image_router
from integrations.research.aggregation.aggregator import ResearchAggregator
from integrations.research.registry.collector_registry import global_collector_registry

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Integration Platform & Real Market Intelligence CLI")
    subparsers = parser.add_subparsers(dest="command", help="Integration commands")

    subparsers.add_parser("health", help="Display health summary")
    
    p_llm = subparsers.add_parser("test-llm", help="Test LLM router")
    p_llm.add_argument("--prompt", default="Explain AI Agents", help="Prompt text")

    p_img = subparsers.add_parser("test-image", help="Test image router")
    p_img.add_argument("--prompt", default="Enterprise AI Architecture", help="Prompt text")

    p_res = subparsers.add_parser("research", help="Execute real market research pipeline")
    p_res.add_argument("--topic", default="AI Agents", help="Research topic")

    subparsers.add_parser("sources", help="Display active research sources")
    subparsers.add_parser("topics", help="Display trending topic clusters")
    subparsers.add_parser("opportunities", help="Display evidence-backed market opportunities")
    subparsers.add_parser("stats", help="Display integration metrics")
    subparsers.add_parser("profile", help="Display active profile")

    args = parser.parse_args()

    if args.command == "health":
        print("\n=== PROVIDER & COLLECTOR HEALTH SUMMARY ===")
        health = global_registry.health_summary()
        collectors_health = global_collector_registry.health_summary()
        health.update(collectors_health)
        print(json.dumps(health, indent=2))
    elif args.command == "test-llm":
        res = global_llm_router.generate(args.prompt)
        print(f"\n=== TESTING LLM ROUTER (Prompt: '{args.prompt}') ===")
        print(json.dumps({
            "id": res.id,
            "provider": res.provider,
            "model_name": res.model_name,
            "text": res.text
        }, indent=2))
    elif args.command == "test-image":
        img = global_image_router.generate_image(args.prompt)
        print(f"\n=== TESTING IMAGE ROUTER (Prompt: '{args.prompt}') ===")
        print(json.dumps({
            "id": img.id,
            "provider": img.provider,
            "image_url": img.image_url,
            "format": img.format
        }, indent=2))
    elif args.command == "research":
        agg = ResearchAggregator()
        pkg = agg.collect_and_aggregate(args.topic)
        print(f"\n=== REAL MARKET INTELLIGENCE PACKAGE (Topic: '{args.topic}') ===")
        print(json.dumps({
            "id": pkg.id,
            "summary": pkg.summary,
            "signals": pkg.signals,
            "trends": pkg.trends,
            "opportunities": pkg.opportunities,
            "sources_count": len(pkg.sources)
        }, indent=2))
    elif args.command == "sources":
        print("\n=== ACTIVE MARKET INTELLIGENCE COLLECTORS ===")
        print(json.dumps({
            "collectors": global_collector_registry.list_collectors(),
            "sources_count": len(global_collector_registry.list_collectors())
        }, indent=2))
    elif args.command == "topics" or args.command == "opportunities":
        agg = ResearchAggregator()
        pkg = agg.collect_and_aggregate("AI Agents")
        print("\n=== TRENDING TOPICS & EVIDENCE-BACKED OPPORTUNITIES ===")
        print(json.dumps({
            "trends": pkg.trends,
            "opportunities": pkg.opportunities
        }, indent=2))
    elif args.command == "stats" or args.command == "profile":
        print("\n=== INTEGRATION PROFILE & STATS ===")
        print(json.dumps({
            "active_profile": "testing",
            "registered_providers": len(global_registry._providers),
            "registered_collectors": len(global_collector_registry._collectors)
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
