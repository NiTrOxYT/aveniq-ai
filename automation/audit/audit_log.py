"""
Immutable Audit Logger and Emergency Execution Controls.
"""

import os
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class AuditRecord:
    id: str
    session_id: str
    action: str
    actor: str  # System, User, TelegramBot
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=_get_utc_now)

class AuditLogger:
    def __init__(self, storage_file: str = "automation/storage/audit_log.jsonl"):
        self.storage_file = storage_file
        os.makedirs(os.path.dirname(storage_file), exist_ok=True)

    def log(self, session_id: str, action: str, actor: str = "System", details: Dict[str, Any] = None) -> AuditRecord:
        rec_id = f"aud_{int(datetime.now().timestamp())}_{abs(hash(action))%1000:03d}"
        rec = AuditRecord(
            id=rec_id,
            session_id=session_id,
            action=action,
            actor=actor,
            details=details or {}
        )
        line = json.dumps({
            "id": rec.id,
            "session_id": rec.session_id,
            "action": rec.action,
            "actor": rec.actor,
            "details": rec.details,
            "timestamp": rec.timestamp
        }) + "\n"
        with open(self.storage_file, "a", encoding="utf-8") as f:
            f.write(line)
        return rec

    def get_logs(self, limit: int = 50) -> List[AuditRecord]:
        if not os.path.exists(self.storage_file):
            return []
        records = []
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        records.append(AuditRecord(
                            id=data.get("id", ""),
                            session_id=data.get("session_id", ""),
                            action=data.get("action", ""),
                            actor=data.get("actor", "System"),
                            details=data.get("details", {}),
                            timestamp=data.get("timestamp", _get_utc_now())
                        ))
        except Exception:
            pass
        return records[-limit:]

class EmergencyControls:
    def __init__(self):
        self.paused_sessions: set = set()
        self.cancelled_sessions: set = set()

    def pause(self, session_id: str) -> bool:
        self.paused_sessions.add(session_id)
        return True

    def resume(self, session_id: str) -> bool:
        self.paused_sessions.discard(session_id)
        return True

    def cancel(self, session_id: str) -> bool:
        self.cancelled_sessions.add(session_id)
        return True

    def is_paused(self, session_id: str) -> bool:
        return session_id in self.paused_sessions

    def is_cancelled(self, session_id: str) -> bool:
        return session_id in self.cancelled_sessions

global_audit_logger = AuditLogger()
global_emergency_controls = EmergencyControls()
