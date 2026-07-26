"""
Base Market Collector Contract, Throttling RateLimiter, and HTTP Retries.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import time
import logging
import urllib.request
import urllib.error
import ssl
from dataclasses import dataclass, field
from datetime import datetime, timezone

from integrations.research.event import MarketEvent, generate_event_id
from integrations.research.document import ResearchDocument

log = logging.getLogger("aveniq.research.collector")

@dataclass
class CollectorHealth:
    source_name: str
    status: str              # 'READY', 'DEGRADED', 'UNAVAILABLE'
    total_collected: int = 0
    last_sync: str = ""
    error_count: int = 0
    last_error: str = ""
    message: str = "Collector operating normally."


class RateLimiter:
    """Per-source request rate limiter / throttle."""
    def __init__(self, min_interval_sec: float = 1.0):
        self.min_interval_sec = min_interval_sec
        self._last_request_time: float = 0.0

    def wait_if_needed(self):
        elapsed = time.time() - self._last_request_time
        if elapsed < self.min_interval_sec:
            time.sleep(self.min_interval_sec - elapsed)
        self._last_request_time = time.time()


def fetch_url_with_retry(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout_sec: float = 8.0,
    max_retries: int = 3,
    backoff_base_sec: float = 1.0
) -> Optional[str]:
    """
    Fetch URL with custom User-Agent, timeout, and exponential backoff retry.
    Returns decoded text string if successful, None if failed.
    """
    default_headers = {
        "User-Agent": "AVENIQ-MarketIntelligence/1.0 (Enterprise Market Research Bot; +https://aveniq.ai)"
    }
    if headers:
        default_headers.update(headers)

    req = urllib.request.Request(url, headers=default_headers)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout_sec, context=ctx) as resp:
                if resp.status == 200:
                    charset = resp.headers.get_content_charset() or "utf-8"
                    return resp.read().decode(charset, errors="ignore")
        except Exception as e:
            log.warning("[HTTP Fetch Warning] Attempt %d/%d for '%s' failed: %s", attempt, max_retries, url, e)
            if attempt < max_retries:
                time.sleep(backoff_base_sec * (2 ** (attempt - 1)))

    return None


class BaseMarketCollector(ABC):
    source_name: str = "base"

    def __init__(self):
        self.rate_limiter = RateLimiter(min_interval_sec=0.5)
        self.total_collected: int = 0
        self.last_sync: str = ""
        self.error_count: int = 0
        self.last_error: str = ""
        self._initialized: bool = False

    def initialize(self):
        """Idempotent initialization."""
        self._initialized = True

    def shutdown(self):
        self._initialized = False

    @abstractmethod
    def collect(self, topic: str = "", config: Any = None) -> List[MarketEvent]:
        """Main collector entry point returning normalized MarketEvents."""
        pass

    @abstractmethod
    def normalize(self, raw_item: Dict[str, Any]) -> MarketEvent:
        """Transforms a raw item dict to standard MarketEvent."""
        pass

    def health(self) -> CollectorHealth:
        status = "READY"
        if self.error_count > 0 and self.total_collected > 0:
            status = "DEGRADED"
        elif self.error_count > 0 and self.total_collected == 0:
            status = "UNAVAILABLE"

        msg = "Collector ready" if status == "READY" else f"Encountered {self.error_count} errors. Last: {self.last_error[:80]}"
        return CollectorHealth(
            source_name=self.source_name,
            status=status,
            total_collected=self.total_collected,
            last_sync=self.last_sync or datetime.now(timezone.utc).isoformat(),
            error_count=self.error_count,
            last_error=self.last_error,
            message=msg
        )

    # Legacy compatibility wrapper
    def collect_raw(self, topic: str, config: Any) -> List[ResearchDocument]:
        events = self.collect_safe(topic, config)
        return [evt.to_document() for evt in events]

    def collect_safe(self, topic: str = "", config: Any = None) -> List[MarketEvent]:
        """Exception-isolated collect wrapper."""
        self.initialize()
        self.rate_limiter.wait_if_needed()
        try:
            events = self.collect(topic, config)
            self.total_collected += len(events)
            self.last_sync = datetime.now(timezone.utc).isoformat()
            return events
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            log.warning("⚠️ [Collector Failure] %s collector failed: %s", self.source_name, e)
            return []
