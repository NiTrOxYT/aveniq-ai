"""
AutomationSession Data Model definition.
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
