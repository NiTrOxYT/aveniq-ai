"""
Execution Event Bus & Event definitions for AVENIQ AI v2 Native Workflow Engine.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable, Type
from datetime import datetime, timezone
from collections import deque

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class WorkflowEvent:
    execution_id: str
    event_type: str
    timestamp: str = field(default_factory=_get_utc_now)
    payload: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkflowStarted(WorkflowEvent):
    event_type: str = "WORKFLOW_STARTED"

@dataclass
class WorkflowCompleted(WorkflowEvent):
    event_type: str = "WORKFLOW_COMPLETED"

@dataclass
class WorkflowFailed(WorkflowEvent):
    event_type: str = "WORKFLOW_FAILED"

@dataclass
class NodeStarted(WorkflowEvent):
    event_type: str = "NODE_STARTED"

@dataclass
class NodeCompleted(WorkflowEvent):
    event_type: str = "NODE_COMPLETED"

@dataclass
class NodeFailed(WorkflowEvent):
    event_type: str = "NODE_FAILED"

@dataclass
class NodeRetry(WorkflowEvent):
    event_type: str = "NODE_RETRY"

@dataclass
class CheckpointSaved(WorkflowEvent):
    event_type: str = "CHECKPOINT_SAVED"

class WorkflowEventBus:
    def __init__(self, max_history: int = 100):
        self._subscribers: Dict[str, List[Callable[[WorkflowEvent], None]]] = {}
        self._history: deque = deque(maxlen=max_history)

    def subscribe(self, event_type: str, callback: Callable[[WorkflowEvent], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event: WorkflowEvent):
        self._history.append(event)
        callbacks = self._subscribers.get(event.event_type, []) + self._subscribers.get("*", [])
        for cb in callbacks:
            try:
                cb(event)
            except Exception:
                pass

    def get_history(self) -> List[WorkflowEvent]:
        return list(self._history)

global_workflow_event_bus = WorkflowEventBus()
