#!/usr/bin/env python3
"""
AVENIQ External Integration Platform CLI Control Center
Command Line Tool for inspecting provider health, testing LLM & Image generation routing,
testing research aggregation, and inspecting integration metrics.

Commands:
  health        - Display health status across all registered providers.
  test-llm      - Execute LLM request via LLMRouter with failover.
  test-image    - Execute Image Generation request via ImageRouter.
  test-research - Execute Research connectors aggregation.
  stats         - Display integration request metrics, latency, & cache hit rates.
  profile       - Display active provider configuration profile.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from integrations.registry.global_registry import global_registry
from integrations.llm.router import LLMRouter
from integrations.image.router import ImageRouter
from integrations.research.document import ResearchAggregator, RedditConnector, HackerNewsConnector, GitHubTrendingConnector
from integrations.monitoring.metrics import global_metrics
from integrations.observability.tracing import SystemDiagnostics, global_tracer
from integrations.config.provider_config import global_config
from integrations.base.request import IntegrationRequest

def main():
    parser = argparse.ArgumentParser(description="AVENIQ External Integration Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Integration commands")

    subparsers.add_parser("health", help="Inspect provider health summary")
    
    p_llm = subparsers.add_parser("test-llm", help="Test LLM Provider Router")
    p_llm.add_argument("--prompt", default="Explain autonomous AI agents", help="Prompt text")
    p_llm.add_argument("--provider", default="mock_llm", help="Primary LLM provider")

    p_img = subparsers.add_parser("test-image", help="Test Image Provider Router")
    p_img.add_argument("--prompt", default="Enterprise AI Workspace Banner", help="Image prompt")

    p_res = subparsers.add_parser("test-research", help="Test Research Connectors")
    p_res.add_argument("--topic", default="AI Agents", help="Research topic")

    subparsers.add_parser("stats", help="Display integration metrics & traces")
    subparsers.add_parser("profile", help="Display active configuration profile")

    args = parser.parse_args()

    if args.command == "health":
        print("\n=== PROVIDER HEALTH SUMMARY ===")
        health_data = {
            name: {
                "status": h.status,
                "message": h.message,
                "checked_at": h.last_checked
            } for name, h in global_registry.health_summary().items()
        }
        print(json.dumps(health_data, indent=2))
    elif args.command == "test-llm":
        print(f"\n=== TESTING LLM ROUTER (Prompt: '{args.prompt}') ===")
        router = LLMRouter(default_provider=args.provider)
        response = router.generate(args.prompt)
        print(json.dumps({
            "id": response.id,
            "provider": response.provider,
            "model_name": response.model_name,
            "text": response.text_content
        }, indent=2))
    elif args.command == "test-image":
        print(f"\n=== TESTING IMAGE ROUTER (Prompt: '{args.prompt}') ===")
        router = ImageRouter()
        asset = router.generate_image(args.prompt)
        print(json.dumps({
            "id": asset.id,
            "filename": asset.filename,
            "provider": asset.provider,
            "url_or_path": asset.url_or_path
        }, indent=2))
    elif args.command == "test-research":
        print(f"\n=== TESTING RESEARCH CONNECTORS (Topic: '{args.topic}') ===")
        connectors = [RedditConnector(), HackerNewsConnector(), GitHubTrendingConnector()]
        docs = []
        for conn in connectors:
            req = IntegrationRequest(request_id="test_req", operation="fetch", payload={"topic": args.topic})
            res = conn.execute(req)
            if res.success:
                docs.append(res.data["document"])
        summary = ResearchAggregator.aggregate(docs)
        print(json.dumps(summary, indent=2))
    elif args.command == "stats":
        print("\n=== INTEGRATION METRICS & DIAGNOSTICS ===")
        print(json.dumps({
            "metrics": global_metrics.get_summary(),
            "diagnostics": SystemDiagnostics.inspect(global_tracer)
        }, indent=2))
    elif args.command == "profile":
        print("\n=== ACTIVE PROVIDER CONFIGURATION PROFILE ===")
        print(json.dumps({
            "active_profile": global_config.active_profile,
            "llm_settings": global_config.get_llm_settings(),
            "image_settings": global_config.get_image_settings()
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
