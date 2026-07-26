"""
Unified Request, Response, Credentials, Exceptions, and Health models for Integration Base.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class IntegrationRequest:
    request_id: str
    operation: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class IntegrationResponse:
    request_id: str
    success: bool
    data: Dict[str, Any]
    provider: str
    latency: float = 0.0
    cached: bool = False
    error: Optional[str] = None
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class ProviderHealth:
    provider: str
    status: str  # Healthy, Degraded, Offline
    latency_ms: float = 0.0
    message: str = "Operating normally"
    last_checked: str = field(default_factory=_get_utc_now)

class CredentialsManager:
    @staticmethod
    def get(key: str, default: str = "") -> str:
        return os.getenv(key, default)

    @staticmethod
    def has(key: str) -> bool:
        val = os.getenv(key)
        return bool(val and val.strip())

class IntegrationError(Exception):
    """Base exception for all integration errors."""
    pass

class RetryableIntegrationError(IntegrationError):
    """Exception for temporary errors that can be retried (timeouts, rate limits, 503s)."""
    pass

class FatalIntegrationError(IntegrationError):
    """Exception for unrecoverable errors (invalid API keys, schema mismatch)."""
    pass
