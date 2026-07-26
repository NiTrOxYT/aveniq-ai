"""
WorkflowResult dataclass definition.
"""

from dataclasses import dataclass
from typing import Dict, Any, List
from workflow.models.event import WorkflowEvent

@dataclass
class WorkflowResult:
    success: bool
    packages: Dict[str, Any]
    metrics: Dict[str, Any]
    errors: List[str]
    timeline: List[WorkflowEvent]
