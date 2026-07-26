"""
WorkflowEvent dataclass definition.
"""

from dataclasses import dataclass, field
from typing import Dict, Any
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class WorkflowEvent:
    timestamp: str = field(default_factory=_get_utc_now)
    execution_id: str = ""
    department: str = ""
    level: str = "INFO"
    message: str = ""
    duration: float = 0.0
    data: Dict[str, Any] = field(default_factory=dict)
