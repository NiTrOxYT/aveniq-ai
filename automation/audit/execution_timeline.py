"""
Timestamped Execution Timeline Tracker & Audit Trail.
Logs every pipeline step with exact timestamps, stage durations, and status codes.
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class ExecutionTimelineTracker:
    def __init__(self, log_path: str = "storage/logs/execution_timeline.json"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        self._events: List[Dict[str, Any]] = []

    def record_event(
        self,
        session_id: str,
        campaign_id: str,
        execution_stage: str,
        duration_sec: float = 0.0,
        status: str = "SUCCESS",
        details: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        event = {
            "timestamp": _get_utc_now(),
            "session_id": session_id,
            "campaign_id": campaign_id,
            "execution_stage": execution_stage,
            "duration_sec": duration_sec,
            "status": status,
            "details": details or {},
            "error": error
        }
        self._events.append(event)
        self._flush()
        return event

    def _flush(self):
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(self._events, f, indent=2)

    def get_timeline(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if not session_id:
            return self._events
        return [e for e in self._events if e["session_id"] == session_id]

global_timeline_tracker = ExecutionTimelineTracker()
