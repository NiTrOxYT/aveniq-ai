"""
Approval Storage Manager for AVENIQ Human Approval System.
Persists approval sessions, decisions, timeline events, and version histories to disk storage.
"""

import os, json
from typing import Dict, Any, Optional
from approval.models.schema import ApprovalSession
from brain.utils.logger import get_logger

logger = get_logger("aveniq.approval.storage")

class ApprovalStorageManager:
    def __init__(self, base_dir: str = "approval/storage"):
        self.base_dir = base_dir
        self.sessions_dir = os.path.join(base_dir, "sessions")
        self.decisions_dir = os.path.join(base_dir, "decisions")
        self.history_dir = os.path.join(base_dir, "history")
        self.versions_dir = os.path.join(base_dir, "versions")

        for d in [self.sessions_dir, self.decisions_dir, self.history_dir, self.versions_dir]:
            os.makedirs(d, exist_ok=True)

    def save_session(self, session: ApprovalSession) -> str:
        filepath = os.path.join(self.sessions_dir, f"{session.id}.json")
        data = {
            "id": session.id,
            "topic": session.topic,
            "date": session.date,
            "current_state": session.current_state,
            "executive_summary": session.executive_summary,
            "decision": {
                "decision": session.decision.decision,
                "reviewer": session.decision.reviewer_id,
                "rationale": session.decision.rationale,
                "timestamp": session.decision.timestamp
            } if session.decision else None,
            "actions_count": len(session.action_requests),
            "version": session.version,
            "quality_gate": {
                "passed": session.quality_gate.passed,
                "score": session.quality_gate.score,
                "checklist": session.quality_gate.checklist
            }
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save to version control storage
        version_filepath = os.path.join(self.versions_dir, f"v_{session.version}_{session.id}.json")
        with open(version_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save to historical memory
        hist_path = os.path.join(self.history_dir, f"history_{session.date}_{session.id}.json")
        with open(hist_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved approval session to {filepath}")
        return filepath

    def get_latest_session(self) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.sessions_dir) if f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.sessions_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
