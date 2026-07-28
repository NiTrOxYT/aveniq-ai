"""
Internal Event Bus for AVENIQ AI Runtime.
Decouples subsystems via publish/subscribe messaging.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Callable, Any

logger = logging.getLogger("aveniq.runtime.event_bus")


@dataclass
class Event:
    name: str
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable[[Event], None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[Event], None]):
        """Subscribe a callback to an event."""
        self._handlers.setdefault(event_name, []).append(handler)
        logger.debug(f"[EventBus] Subscribed to '{event_name}'")

    def publish(self, event_name: str, payload: Dict[str, Any]):
        """Publish an event to all subscribers (including wildcard '*' subscribers)."""
        event = Event(name=event_name, payload=payload)
        handlers = self._handlers.get(event_name, []) + self._handlers.get("*", [])
        for h in handlers:
            try:
                h(event)
            except Exception as e:
                logger.error(f"[EventBus] Error in handler for '{event_name}': {e}")


global_event_bus = EventBus()
