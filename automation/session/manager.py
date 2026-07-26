"""
AutomationSession Data Model and AutomationSessionManager with State Machine validation.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from automation.session.state import AutomationState

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class AutomationSession:
    session_id: str
    campaign_id: str
    workflow_execution_id: str = ""
    started_at: str = field(default_factory=_get_utc_now)
    completed_at: Optional[str] = None
    current_state: AutomationState = AutomationState.CREATED
    approval_state: str = "PENDING_REVIEW"
    execution_metadata: Dict[str, Any] = field(default_factory=dict)
    regenerated_components: List[str] = field(default_factory=list)
    notifications_sent: List[str] = field(default_factory=list)
    archived: bool = False
    learning_complete: bool = False

class AutomationSessionManager:
    VALID_TRANSITIONS = {
        AutomationState.CREATED: [AutomationState.SCHEDULED, AutomationState.RUNNING, AutomationState.CANCELLED],
        AutomationState.SCHEDULED: [AutomationState.RUNNING, AutomationState.CANCELLED],
        AutomationState.RUNNING: [AutomationState.WAITING_FOR_APPROVAL, AutomationState.FAILED, AutomationState.CANCELLED],
        AutomationState.WAITING_FOR_APPROVAL: [AutomationState.APPROVED, AutomationState.REJECTED, AutomationState.REGENERATING, AutomationState.CANCELLED],
        AutomationState.REGENERATING: [AutomationState.WAITING_FOR_APPROVAL, AutomationState.FAILED],
        AutomationState.APPROVED: [AutomationState.ARCHIVED, AutomationState.LEARNING, AutomationState.COMPLETED],
        AutomationState.REJECTED: [AutomationState.COMPLETED, AutomationState.CANCELLED],
        AutomationState.ARCHIVED: [AutomationState.LEARNING, AutomationState.COMPLETED],
        AutomationState.LEARNING: [AutomationState.COMPLETED],
        AutomationState.COMPLETED: [],
        AutomationState.FAILED: [AutomationState.RUNNING, AutomationState.CANCELLED],
        AutomationState.CANCELLED: []
    }

    def __init__(self):
        self._sessions: Dict[str, AutomationSession] = {}

    def create_session(self, campaign_id: str) -> AutomationSession:
        now_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        sid = f"aut_sess_{now_str}_{abs(hash(campaign_id))%1000:03d}"
        session = AutomationSession(session_id=sid, campaign_id=campaign_id)
        self._sessions[sid] = session
        return session

    def transition_state(self, session_id: str, new_state: AutomationState) -> bool:
        session = self._sessions.get(session_id)
        if not session:
            return False
        allowed = self.VALID_TRANSITIONS.get(session.current_state, [])
        if new_state in allowed:
            session.current_state = new_state
            if new_state in [AutomationState.COMPLETED, AutomationState.FAILED, AutomationState.CANCELLED]:
                session.completed_at = _get_utc_now()
            return True
        return False

    def get_session(self, session_id: str) -> Optional[AutomationSession]:
        return self._sessions.get(session_id)
