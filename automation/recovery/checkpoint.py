"""
Checkpoint Manager and Recovery Engine for Automation Sessions.
Persists checkpoints to disk and resumes execution from latest checkpoint upon application restart.
"""

import os
import json
from typing import Dict, Any, Optional
from automation.session.session import AutomationSession
from automation.session.state import AutomationState

class CheckpointManager:
    def __init__(self, storage_dir: str = "automation/storage/checkpoints"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_checkpoint(self, session: AutomationSession, step_name: str, checkpoint_data: Dict[str, Any] = None) -> str:
        filepath = os.path.join(self.storage_dir, f"chk_{session.session_id}_{step_name}.json")
        data = {
            "session_id": session.session_id,
            "campaign_id": session.campaign_id,
            "workflow_execution_id": session.workflow_execution_id,
            "step_name": step_name,
            "current_state": session.current_state.value,
            "approval_state": session.approval_state,
            "checkpoint_data": checkpoint_data or {},
            "saved_at": session.started_at
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return filepath

    def get_latest_checkpoint(self, session_id: str) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.storage_dir) if f.startswith(f"chk_{session_id}_") and f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.storage_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)

class RecoveryEngine:
    def __init__(self, checkpoint_manager: Optional[CheckpointManager] = None):
        self.chk_mgr = checkpoint_manager or CheckpointManager()

    def resume_session(self, session_id: str) -> Dict[str, Any]:
        chk = self.chk_mgr.get_latest_checkpoint(session_id)
        if not chk:
            return {"resumed": False, "reason": "No checkpoint found"}
        return {
            "resumed": True,
            "session_id": chk["session_id"],
            "last_step": chk["step_name"],
            "state": chk["current_state"],
            "data": chk["checkpoint_data"]
        }
