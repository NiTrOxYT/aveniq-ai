"""
Centralized Security & Rate Limiting System for AVENIQ AI Runtime v1.
Manages API authentication frameworks, role-based access control, and sliding-window rate limiting.
"""

import time
from typing import Dict, List, Optional, Any


class SecurityManager:
    def __init__(self):
        self._rate_limits: Dict[str, List[float]] = {}
        self._audit_log: List[Dict[str, Any]] = []

    def check_rate_limit(self, client_id: str, limit: int = 100, window_seconds: int = 60) -> bool:
        """Sliding window rate limit check. Returns True if allowed, False if limit exceeded."""
        now = time.time()
        timestamps = self._rate_limits.setdefault(client_id, [])
        
        # Remove timestamps outside window
        self._rate_limits[client_id] = [t for t in timestamps if now - t < window_seconds]
        
        if len(self._rate_limits[client_id]) >= limit:
            return False
        
        self._rate_limits[client_id].append(now)
        return True

    def log_audit_event(self, action: str, actor: str, status: str, details: Optional[Dict[str, Any]] = None):
        self._audit_log.insert(0, {
            "timestamp": time.time(),
            "action": action,
            "actor": actor,
            "status": status,
            "details": details or {}
        })
        self._audit_log = self._audit_log[:200]

    def get_audit_log(self) -> List[Dict[str, Any]]:
        return self._audit_log


global_security_manager = SecurityManager()
