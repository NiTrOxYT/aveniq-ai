"""
WorkflowExecution dataclass schema.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from workflow.models.status import WorkflowStatus
from workflow.models.step import WorkflowStep

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class WorkflowExecution:
    execution_id: str
    workflow_name: str
    started_at: str = field(default_factory=_get_utc_now)
    finished_at: Optional[str] = None
    status: WorkflowStatus = WorkflowStatus.PENDING
    current_step: Optional[str] = None
    steps: List[WorkflowStep] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
