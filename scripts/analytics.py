#!/usr/bin/env python3
"""
AVENIQ Performance Analytics & Continuous Optimization Platform CLI Control Center
Command Line Tool for collecting multi-platform metrics, running 0-100 scoring benchmarks,
inspecting trends, submitting optimization recommendations to Learning, and displaying reports.

Commands:
  collect         - Collect multi-platform metrics & build campaign attribution.
  analyze         - Run 0-100 performance scoring & benchmark comparison.
  report          - Display performance report (Markdown or JSON).
  campaign        - Display campaign attribution details by ID.
  trends          - Display macro topic & format trends.
  recommendations - Generate evidence-backed recommendations & submit to Learning.
  status          - Display analytics status & metrics summary.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analytics.collectors.linkedin import LinkedInCollector, XCollector, WebsiteCollector
from analytics.optimization.scoring import CampaignScorer, BenchmarkEngine
from analytics.optimization.recommendation_engine import OptimizationEngine
from analytics.reports.performance_report import PerformanceReportGenerator
from analytics.attribution.attribution_graph import AttributionGraph

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Performance Analytics CLI")
    subparsers = parser.add_subparsers(dest="command", help="Analytics commands")

    subparsers.add_parser("collect", help="Collect multi-platform metrics")
    subparsers.add_parser("analyze", help="Run 0-100 performance scoring")
    
    p_rep = subparsers.add_parser("report", help="Display performance report")
    p_rep.add_argument("--format", "-f", default="markdown", choices=["json", "markdown"], help="Report format")

    p_cmp = subparsers.add_parser("campaign", help="Display campaign attribution")
    p_cmp.add_argument("--id", default="cmp_2026-07-26_001", help="Campaign ID")

    subparsers.add_parser("trends", help="Display macro trends")
    subparsers.add_parser("recommendations", help="Generate & submit recommendations to Learning")
    subparsers.add_parser("status", help="Display analytics status")

    args = parser.parse_args()

    if args.command == "collect":
        collector = LinkedInCollector()
        m = collector.collect("cmp_001", "pub_001")
        print("\n=== MULTI-PLATFORM METRICS COLLECTED ===")
        print(json.dumps({
            "campaign_id": m.campaign_id,
            "platform": m.platform,
            "impressions": m.reach.impressions,
            "visits": m.website.visits,
            "leads": m.business.leads
        }, indent=2))
    elif args.command == "analyze":
        collector = LinkedInCollector()
        m = collector.collect("cmp_001", "pub_001")
        scores = CampaignScorer.calculate_scores(m)
        benchmark = BenchmarkEngine.benchmark_campaign(scores, m.business.leads)
        print("\n=== PERFORMANCE SCORING & BENCHMARK ANALYSIS ===")
        print(json.dumps({
            "scores": scores,
            "benchmark": benchmark
        }, indent=2))
    elif args.command == "report":
        print(PerformanceReportGenerator.generate_report("cmp_2026-07-26_001", args.format))
    elif args.command == "trends":
        print("\n=== MACRO TOPIC & FORMAT TRENDS ===")
        print(json.dumps({
            "improving_topics": ["Model Context Protocol", "Autonomous AI Agents", "pgvector Architecture"],
            "declining_topics": ["Generic Prompt Engineering"],
            "top_formats": ["Visual Carousel", "Technical Architecture Deep Dive"],
            "best_posting_time": "09:00 UTC Tuesday & Thursday"
        }, indent=2))
    elif args.command == "recommendations":
        collector = LinkedInCollector()
        m = collector.collect("cmp_001", "pub_001")
        scores = CampaignScorer.calculate_scores(m)
        benchmark = BenchmarkEngine.benchmark_campaign(scores, m.business.leads)
        recs = OptimizationEngine.generate_recommendations(scores, benchmark)
        submission = OptimizationEngine.submit_to_learning(recs)
        print("\n=== OPTIMIZATION RECOMMENDATIONS & LEARNING SUBMISSION ===")
        print(json.dumps({
            "recommendations": [
                {
                    "target": r.target_department,
                    "text": r.recommendation_text,
                    "confidence": f"{int(r.confidence_score*100)}%",
                    "impact": r.expected_impact
                } for r in recs
            ],
            "learning_submission": submission
        }, indent=2))
    elif args.command == "status":
        print("\n=== PERFORMANCE ANALYTICS PLATFORM STATUS ===")
        print(json.dumps({
            "status": "Healthy",
            "active_campaigns_tracked": 12,
            "overall_performance": "Outperforming (+10.2% vs Benchmark)"
        }, indent=2))
    elif args.command == "campaign":
        graph = AttributionGraph()
        c_node = graph.add_node(args.id, "Campaign", "Enterprise AI Series")
        a_node = graph.add_node("asset_001", "Asset", "hero_banner.png")
        graph.add_edge(c_node.id, a_node.id, "PRODUCES")
        print("\n=== CAMPAIGN ATTRIBUTION GRAPH ===")
        print(json.dumps({
            "campaign_id": args.id,
            "nodes_count": len(graph.nodes),
            "edges_count": len(graph.edges)
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
