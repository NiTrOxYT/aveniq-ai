"""
Event Store & Replay Engine for AVENIQ AI Runtime v1.
Persists runtime event history and supports replaying non-destructive events for simulation and debugging.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from runtime.event_bus import global_event_bus, Event

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
EVENTS_FILE = WORKSPACE_ROOT / "runtime" / "storage" / "events.json"

NON_DESTRUCTIVE_EVENTS = {
    "ResearchCompleted", "AutomationCompleted", "KnowledgeIndexed",
    "ReflectionCreated", "KnowledgeAdded", "RelationshipsUpdated"
}


class EventStore:
    def __init__(self, events_file: Path = EVENTS_FILE):
        self.events_file = events_file
        self.events_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Subscribe to all events on EventBus
        global_event_bus.subscribe("*", self._record_event)

    def _load_events(self) -> List[Dict[str, Any]]:
        if not self.events_file.exists():
            return []
        try:
            with open(self.events_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_events(self, events: List[Dict[str, Any]]):
        with open(self.events_file, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2)

    def _record_event(self, event: Event):
        events = self._load_events()
        events.insert(0, {
            "event_id": f"evt_{int(time.time()*1000)}",
            "name": event.name,
            "payload": event.payload,
            "timestamp": event.timestamp
        })
        self._save_events(events[:500])

    def get_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._load_events()[:limit]

    def replay_event(self, event_id: str) -> Dict[str, Any]:
        """Replay a non-destructive event by re-publishing to EventBus."""
        events = self._load_events()
        evt_data = next((e for e in events if e.get("event_id") == event_id), None)
        
        if not evt_data:
            return {"status": "error", "message": f"Event '{event_id}' not found"}

        name = evt_data.get("name")
        if name not in NON_DESTRUCTIVE_EVENTS:
            return {"status": "blocked", "message": f"Replaying event '{name}' is blocked (destructive or non-whitelisted)"}

        # Re-publish event to EventBus
        global_event_bus.publish(name, evt_data.get("payload", {}))
        return {"status": "replayed", "event_id": event_id, "name": name}


global_event_store = EventStore()
