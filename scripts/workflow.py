#!/usr/bin/env python3
"""
AVENIQ Workflow Engine CLI Control Center
Command Line Tool for executing the 13-department organization pipeline,
displaying execution status, timelines, metrics, and multi-format reports.

Commands:
  run      - Run full 13-department autonomous workflow execution.
  status   - Display current execution status & department step metrics.
  report   - Display full execution report (JSON, Markdown, or HTML).
  timeline - Display chronological timeline events & adapter execution logs.
  explain  - Display pipeline sequence, dependencies, & adapter versions.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from workflow.engine.orchestrator import Orchestrator
from workflow.reports.report_generator import WorkflowReportGenerator
from workflow.adapters.base import ADAPTER_REGISTRY

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Workflow Engine CLI (OS Orchestrator)")
    subparsers = parser.add_subparsers(dest="command", help="Workflow commands")

    run_parser = subparsers.add_parser("run", help="Run master workflow pipeline")
    run_parser.add_argument("--format", "-f", default="json", choices=["json", "markdown", "html"], help="Report output format")

    subparsers.add_parser("status", help="Display execution status & metrics")
    
    report_parser = subparsers.add_parser("report", help="Display full execution report")
    report_parser.add_argument("--format", "-f", default="markdown", choices=["json", "markdown", "html"], help="Report format")

    subparsers.add_parser("timeline", help="Display timeline events")
    subparsers.add_parser("explain", help="Display pipeline sequence & adapters")

    args = parser.parse_args()
    orchestrator = Orchestrator()

    if args.command == "run":
        res = orchestrator.execute_workflow()
        print(WorkflowReportGenerator.generate_report(res, args.format))
    elif args.command == "status":
        res = orchestrator.execute_workflow()
        print("\n=== EXECUTION STATUS & METRICS ===")
        print(json.dumps({
            "success": res.success,
            "metrics": res.metrics,
            "errors": res.errors
        }, indent=2))
    elif args.command == "report":
        res = orchestrator.execute_workflow()
        print(WorkflowReportGenerator.generate_report(res, args.format))
    elif args.command == "timeline":
        res = orchestrator.execute_workflow()
        print("\n=== CHRONOLOGICAL TIMELINE EVENTS ===")
        print(json.dumps([
            {
                "timestamp": e.timestamp,
                "department": e.department,
                "event": e.data.get("event_type", "Event")
            } for e in res.timeline
        ], indent=2))
    elif args.command == "explain":
        print("\n=== AVENIQ PIPELINE SEQUENCE & ADAPTER REGISTRY ===")
        pipeline_steps = orchestrator.pipeline.get_steps()
        adapters_info = [
            {
                "step": i + 1,
                "department": dept,
                "version": ADAPTER_REGISTRY[dept].version,
                "input_packages": ADAPTER_REGISTRY[dept].input_packages,
                "output_package": ADAPTER_REGISTRY[dept].output_package
            } for i, dept in enumerate(pipeline_steps) if dept in ADAPTER_REGISTRY
        ]
        print(json.dumps(adapters_info, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
