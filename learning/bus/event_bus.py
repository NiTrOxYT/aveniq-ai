"""
Organization-Wide Learning Event Bus.
Publishes and dispatches LearningEvents across all 15 system components.
"""

from typing import List, Dict, Any, Callable
from learning.models.proposal import LearningEvent

class OrganizationLearningEventBus:
    def __init__(self):
        self._subscribers: List[Callable[[LearningEvent], None]] = []
        self._events: List[LearningEvent] = []

    def subscribe(self, callback: Callable[[LearningEvent], None]):
        self._subscribers.append(callback)

    def publish_event(self, event: LearningEvent):
        self._events.append(event)
        for sub in self._subscribers:
            try:
                sub(event)
            except Exception as e:
                pass

    def list_events(self, workspace_id: str = None) -> List[LearningEvent]:
        if workspace_id:
            return [e for e in self._events if e.workspace_id == workspace_id]
        return self._events

global_learning_event_bus = OrganizationLearningEventBus()
