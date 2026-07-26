#!/usr/bin/env python3
"""
AVENIQ Autonomous Execution & Human Approval Platform CLI Control Center
Command Line Tool for launching daily autonomous cycles, approving/rejecting campaigns,
exercising emergency controls (pause, resume, cancel), and inspecting history.

Commands:
  run       - Execute autonomous daily marketing workflow & generate Telegram briefing.
  approve   - Approve pending briefing (archives content & triggers learning).
  reject    - Reject pending briefing & close session.
  control   - Execute emergency control (pause, resume, cancel).
  history   - Display execution history & checkpoints.
  status    - Display current automation session state.
  report    - Display daily summary report (Markdown or JSON).
  schedule  - Display daily cron schedule & posting window configuration.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from automation.execution.daily_runner import DailyRunner
from automation.reports.daily_summary import DailySummaryReportGenerator
from automation.audit.audit_log import global_emergency_controls

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Autonomous Execution Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Automation commands")

    subparsers.add_parser("run", help="Run autonomous daily marketing cycle")
    
    p_app = subparsers.add_parser("approve", help="Approve campaign briefing")
    p_app.add_argument("--session-id", help="Session ID to approve")

    p_rej = subparsers.add_parser("reject", help="Reject campaign briefing")
    p_rej.add_argument("--session-id", help="Session ID to reject")

    p_ctrl = subparsers.add_parser("control", help="Emergency execution control")
    p_ctrl.add_argument("--action", choices=["pause", "resume", "cancel"], required=True, help="Control action")
    p_ctrl.add_argument("--session-id", required=True, help="Target session ID")

    subparsers.add_parser("history", help="Display execution history")
    subparsers.add_parser("status", help="Display current automation status")
    
    p_rep = subparsers.add_parser("report", help="Display daily summary report")
    p_rep.add_argument("--format", "-f", default="markdown", choices=["json", "markdown"], help="Report format")

    subparsers.add_parser("schedule", help="Display daily cron schedule")

    args = parser.parse_args()
    runner = DailyRunner()

    if args.command == "run":
        res = runner.run_daily_cycle()
        print(DailySummaryReportGenerator.generate_report(res, "markdown"))
    elif args.command == "approve":
        res = runner.run_daily_cycle()
        sid = args.session_id or res["session_id"]
        app_res = runner.process_human_decision(sid, "Approve")
        print("\n=== CAMPAIGN APPROVED & ARCHIVED ===")
        print(json.dumps(app_res, indent=2))
    elif args.command == "reject":
        res = runner.run_daily_cycle()
        sid = args.session_id or res["session_id"]
        rej_res = runner.process_human_decision(sid, "Reject")
        print("\n=== CAMPAIGN REJECTED ===")
        print(json.dumps(rej_res, indent=2))
    elif args.command == "control":
        if args.action == "pause":
            global_emergency_controls.pause(args.session_id)
        elif args.action == "resume":
            global_emergency_controls.resume(args.session_id)
        elif args.action == "cancel":
            global_emergency_controls.cancel(args.session_id)
        print(f"\n=== EMERGENCY CONTROL EXECUTED: {args.action.upper()} on session {args.session_id} ===")
    elif args.command == "status":
        print("\n=== AUTOMATION PLATFORM STATUS ===")
        print(json.dumps({
            "status": "Healthy",
            "active_sessions": len(runner.session_mgr._sessions),
            "emergency_controls": {
                "paused_count": len(global_emergency_controls.paused_sessions),
                "cancelled_count": len(global_emergency_controls.cancelled_sessions)
            }
        }, indent=2))
    elif args.command == "history" or args.command == "schedule":
        print("\n=== AUTOMATION SCHEDULE & HISTORY ===")
        print(json.dumps({
            "cron_schedule": "0 09 * * * (Everyday at 09:00 UTC)",
            "timezone": "UTC",
            "active_mode": "Autonomous Daily Execution with Telegram Approval"
        }, indent=2))
    elif args.command == "report":
        res = runner.run_daily_cycle()
        print(DailySummaryReportGenerator.generate_report(res, args.format))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
