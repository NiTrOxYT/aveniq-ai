#!/usr/bin/env python3
"""
AVENIQ Operating System Top-Level Master Orchestration Script.
Running 'python run.py' executes all 13 departments of AVENIQ AI in exact sequential order:
  Company Brain -> Market -> Growth -> Strategy -> Calendar -> Planning
  -> Content -> Creative -> Editorial -> Delivery -> Human Approval -> Archive -> Learning
"""

import sys
import os
import json
import time

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from workflow.engine.orchestrator import Orchestrator
from workflow.reports.report_generator import WorkflowReportGenerator

def main():
    print("=" * 60)
    print("🚀 AVENIQ AI ORGANIZATIONAL OPERATING SYSTEM")
    print("Executing 13-Department Autonomous Pipeline...")
    print("=" * 60)

    start_time = time.time()
    orchestrator = Orchestrator()
    result = orchestrator.execute_workflow(workflow_name="aveniq_master_execution")

    print("\n" + "=" * 60)
    if result.success:
        print("✅ WORKFLOW EXECUTION COMPLETED SUCCESSFULLY!")
    else:
        print("❌ WORKFLOW EXECUTION FAILED!")
    print("=" * 60)

    print(f"⏱️ Total Execution Duration : {result.metrics.get('total_duration', 0.0)}s")
    print(f"📦 Packages Produced       : {len(result.packages)}")
    print(f"🔄 Total Retries Executed   : {result.metrics.get('total_retries', 0)}")
    print("-" * 60)

    print("\n📊 DEPARTMENT DURATION BREAKDOWN:")
    for dept, dur in result.metrics.get("step_durations", {}).items():
        print(f"  • {dept.ljust(25)} : {dur}s")

    if result.errors:
        print("\n❌ EXECUTION ERRORS:")
        for err in result.errors:
            print(f"  • {err}")

    print("\n" + "=" * 60)
    print("📄 EXPORTED MARKDOWN SUMMARY REPORT:")
    print("=" * 60)
    print(WorkflowReportGenerator.generate_report(result, "markdown"))

    if not result.success:
        sys.exit(1)

if __name__ == "__main__":
    main()
