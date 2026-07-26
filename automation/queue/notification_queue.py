"""
Async Notification Queue & Worker for delayed, prioritized, and retryable notification delivery.
"""

import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class NotificationMessage:
    id: str
    channel: str  # telegram, email
    recipient: str
    subject: str
    body: str
    priority: int = 1  # 1 = High, 2 = Medium, 3 = Low
    attempts: int = 0
    status: str = "QUEUED"  # QUEUED, SENT, FAILED
    enqueued_at: str = field(default_factory=_get_utc_now)

class NotificationQueue:
    def __init__(self):
        self._queue: List[NotificationMessage] = []
        self._history: List[NotificationMessage] = []

    def enqueue(self, channel: str, recipient: str, subject: str, body: str, priority: int = 1) -> NotificationMessage:
        msg_id = f"msg_{int(time.time())}_{abs(hash(body))%1000:03d}"
        msg = NotificationMessage(
            id=msg_id,
            channel=channel,
            recipient=recipient,
            subject=subject,
            body=body,
            priority=priority
        )
        self._queue.append(msg)
        self._queue.sort(key=lambda m: m.priority)
        return msg

    def pop(self) -> Optional[NotificationMessage]:
        if not self._queue:
            return None
        return self._queue.pop(0)

    def process_all(self, dispatcher_func) -> int:
        processed = 0
        while self._queue:
            msg = self.pop()
            if not msg:
                break
            msg.attempts += 1
            ok = dispatcher_func(msg)
            if ok:
                msg.status = "SENT"
                self._history.append(msg)
                processed += 1
            else:
                if msg.attempts < 3:
                    msg.status = "QUEUED"
                    self._queue.append(msg)
                else:
                    msg.status = "FAILED"
                    self._history.append(msg)
        return processed
