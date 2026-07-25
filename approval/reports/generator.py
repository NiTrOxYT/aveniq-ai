"""
Approval Report Generator for Human Approval System.
Formats approval sessions into structured JSON audit reports.
"""

from typing import Dict, Any
from approval.engine.approval_engine import ApprovalEngine
from approval.storage.manager import ApprovalStorageManager

class ApprovalReportGenerator:
    def __init__(self):
        self.engine = ApprovalEngine()
        self.storage = ApprovalStorageManager()

    def generate_approval_report(self, topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        session = self.engine.create_session(topic)
        session = self.engine.process_action(session, "Approve", "operator_001", "Approved for distribution and archiving")
        self.storage.save_session(session)

        return {
            "report_type": "approval_session",
            "session_id": session.id,
            "topic": session.topic,
            "date": session.date,
            "current_state": session.current_state,
            "executive_summary": session.executive_summary,
            "decision": {
                "decision": session.decision.decision if session.decision else None,
                "reviewer": session.decision.reviewer_id if session.decision else None,
                "rationale": session.decision.rationale if session.decision else None,
                "timestamp": session.decision.timestamp if session.decision else None
            },
            "telegram_dashboard": {
                "card_text": session.telegram_markup.card_text,
                "keyboards_count": len(session.telegram_markup.inline_keyboard)
            },
            "timeline": [
                {
                    "event_id": t.event_id,
                    "event_type": t.event_type,
                    "actor": t.actor,
                    "timestamp": t.timestamp,
                    "details": t.details
                } for t in session.timeline
            ],
            "action_requests": [
                {
                    "id": a.action_id,
                    "action_type": a.action_type,
                    "target_department": a.target_department,
                    "reviewer": a.reviewer_id,
                    "notes": a.notes
                } for a in session.action_requests
            ],
            "metrics": {
                "duration_seconds": session.metrics.review_duration_seconds,
                "approval_rate": f"{session.metrics.approval_rate}%",
                "regeneration_rate": f"{session.metrics.regeneration_rate}%",
                "revision_count": session.metrics.revision_count
            },
            "quality_gate": {
                "passed": session.quality_gate.passed,
                "score": f"{session.quality_gate.score}%",
                "checklist": session.quality_gate.checklist
            }
        }
