#!/usr/bin/env python3
"""
AVENIQ Human Approval System CLI Control Center
Command Line Tool for human review sessions, Telegram dashboard rendering,
human decision logging (Approve/Reject/Action), and feedback department routing.

Commands:
  session    - Create & render interactive Approval Session dashboard.
  approve    - Simulate human operator approval & release to Archive/Learning.
  reject     - Simulate human operator rejection & campaign termination.
  feedback   - Display review feedback & department routing history.
  history    - Display historical approval session logs.
  explain    - Display approval timeline, state transitions, & department routing.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from approval.reports.generator import ApprovalReportGenerator
from approval.engine.approval_engine import ApprovalEngine

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Human Approval System CLI (Human-in-the-Loop)")
    subparsers = parser.add_subparsers(dest="command", help="Approval commands")

    subparsers.add_parser("session", help="Create interactive Approval Session")
    subparsers.add_parser("approve", help="Approve package and release")
    subparsers.add_parser("reject", help="Reject package and terminate")
    subparsers.add_parser("feedback", help="Display feedback & department routing")
    subparsers.add_parser("history", help="Display session history")
    subparsers.add_parser("explain", help="Display timeline & state transitions")

    args = parser.parse_args()
    generator = ApprovalReportGenerator()

    if args.command == "session" or args.command == "history":
        engine = ApprovalEngine()
        session = engine.create_session()
        print("\n=== TELEGRAM DASHBOARD MARKUP CARD ===")
        print(session.telegram_markup.card_text)
        print("\n=== INLINE KEYBOARD ACTIONS ===")
        print(json.dumps(session.telegram_markup.inline_keyboard, indent=2))
    elif args.command == "approve":
        report = generator.generate_approval_report()
        print("\n=== HUMAN APPROVAL REPORT (APPROVED) ===")
        print(json.dumps(report, indent=2))
    elif args.command == "reject":
        engine = ApprovalEngine()
        session = engine.create_session()
        session = engine.process_action(session, "Reject", "operator_001", "Does not align with current sprint goals")
        print("\n=== HUMAN APPROVAL REPORT (REJECTED) ===")
        print(json.dumps({
            "session_id": session.id,
            "status": session.current_state,
            "decision": {
                "decision": session.decision.decision,
                "reviewer": session.decision.reviewer_id,
                "rationale": session.decision.rationale
            }
        }, indent=2))
    elif args.command == "feedback":
        engine = ApprovalEngine()
        session = engine.create_session()
        session = engine.process_action(session, "Technical", "operator_001", "Add more benchmark metrics and architecture diagrams")
        print("\n=== DEPARTMENT FEEDBACK ROUTING ===")
        print(json.dumps({
            "session_id": session.id,
            "current_state": session.current_state,
            "action_requests": [
                {
                    "action_type": a.action_type,
                    "target_department": a.target_department,
                    "reviewer": a.reviewer_id,
                    "notes": a.notes
                } for a in session.action_requests
            ]
        }, indent=2))
    elif args.command == "explain":
        report = generator.generate_approval_report()
        print("\n=== APPROVAL TIMELINE & QUALITY GATE ===")
        print(json.dumps({
            "session_id": report["session_id"],
            "current_state": report["current_state"],
            "timeline": report["timeline"],
            "quality_gate": report["quality_gate"]
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
