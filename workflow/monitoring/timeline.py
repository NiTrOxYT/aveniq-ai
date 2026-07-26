"""
Monitoring modules: Structured Logger, MetricsCollector, and TimelineRecorder.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from workflow.models.event import WorkflowEvent
from workflow.events.event_bus import EventBus, BaseWorkflowEvent

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class WorkflowStructuredLogger:
    def __init__(self, execution_id: str):
        self.execution_id = execution_id
        self.logs: List[WorkflowEvent] = []

    def log(self, department: str, level: str, message: str, duration: float = 0.0, data: Dict[str, Any] = None) -> WorkflowEvent:
        evt = WorkflowEvent(
            timestamp=_get_utc_now(),
            execution_id=self.execution_id,
            department=department,
            level=level,
            message=message,
            duration=duration,
            data=data or {}
        )
        self.logs.append(evt)
        return evt

class MetricsCollector:
    def __init__(self):
        self.step_durations: Dict[str, float] = {}
        self.retry_counts: Dict[str, int] = {}
        self.total_duration: float = 0.0

    def record_step(self, department: str, duration: float, retries: int = 0):
        self.step_durations[department] = duration
        self.retry_counts[department] = retries

    def get_metrics_summary(self) -> Dict[str, Any]:
        return {
            "total_duration": self.total_duration,
            "step_durations": self.step_durations,
            "retry_counts": self.retry_counts,
            "total_steps": len(self.step_durations),
            "total_retries": sum(self.retry_counts.values())
        }

class TimelineRecorder:
    def __init__(self, event_bus: EventBus):
        self.events: List[WorkflowEvent] = []
        event_bus.subscribe_all(self._on_event)

    def _on_event(self, event: BaseWorkflowEvent):
        evt = WorkflowEvent(
            timestamp=event.timestamp,
            execution_id=event.execution_id,
            department=getattr(event, "department", "System"),
            level="INFO" if not event.event_type.endswith("Failed") else "ERROR",
            message=f"{event.event_type} event triggered",
            duration=getattr(event, "duration", 0.0),
            data={"event_type": event.event_type}
        )
        self.events.append(evt)
