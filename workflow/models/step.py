"""
WorkflowStep dataclass definition.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from workflow.models.status import WorkflowStatus

@dataclass
class WorkflowStep:
    name: str
    department: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    duration: float = 0.0
    retry_count: int = 0
    input_package: Optional[Dict[str, Any]] = None
    output_package: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
