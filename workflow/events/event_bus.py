"""
Pub/Sub Event Bus and Typed Workflow Events.
Decouples workflow engine orchestration from monitoring, reporting, and notifications.
"""

from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Type
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class BaseWorkflowEvent:
    event_type: str
    timestamp: str = field(default_factory=_get_utc_now)
    execution_id: str = ""

@dataclass
class WorkflowStarted(BaseWorkflowEvent):
    event_type: str = "WorkflowStarted"
    workflow_name: str = ""

@dataclass
class WorkflowCompleted(BaseWorkflowEvent):
    event_type: str = "WorkflowCompleted"
    duration: float = 0.0
    packages_count: int = 0

@dataclass
class WorkflowFailed(BaseWorkflowEvent):
    event_type: str = "WorkflowFailed"
    error: str = ""
    failed_step: str = ""

@dataclass
class DepartmentStarted(BaseWorkflowEvent):
    event_type: str = "DepartmentStarted"
    department: str = ""

@dataclass
class DepartmentCompleted(BaseWorkflowEvent):
    event_type: str = "DepartmentCompleted"
    department: str = ""
    duration: float = 0.0

@dataclass
class DepartmentFailed(BaseWorkflowEvent):
    event_type: str = "DepartmentFailed"
    department: str = ""
    error: str = ""

@dataclass
class PackageRegistered(BaseWorkflowEvent):
    event_type: str = "PackageRegistered"
    package_name: str = ""
    package_type: str = ""

@dataclass
class RetryStarted(BaseWorkflowEvent):
    event_type: str = "RetryStarted"
    department: str = ""
    attempt: int = 1
    reason: str = ""

@dataclass
class RetryCompleted(BaseWorkflowEvent):
    event_type: str = "RetryCompleted"
    department: str = ""
    attempt: int = 1
    success: bool = True

class EventBus:
    def __init__(self):
        self._subscribers: Dict[Type[BaseWorkflowEvent], List[Callable[[BaseWorkflowEvent], None]]] = {}
        self._global_subscribers: List[Callable[[BaseWorkflowEvent], None]] = []

    def subscribe(self, event_class: Type[BaseWorkflowEvent], handler: Callable[[BaseWorkflowEvent], None]) -> None:
        if event_class not in self._subscribers:
            self._subscribers[event_class] = []
        self._subscribers[event_class].append(handler)

    def subscribe_all(self, handler: Callable[[BaseWorkflowEvent], None]) -> None:
        self._global_subscribers.append(handler)

    def publish(self, event: BaseWorkflowEvent) -> None:
        # Call specific subscribers
        handlers = self._subscribers.get(type(event), [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"[EventBus Error] Subscriber failed: {e}")

        # Call global subscribers
        for handler in self._global_subscribers:
            try:
                handler(event)
            except Exception as e:
                print(f"[EventBus Error] Global subscriber failed: {e}")
