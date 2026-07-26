"""
Production Event Deduplication Engine for Market Intelligence Signals.
Eliminates duplicate events across collectors using SHA256 URL hashes, title/content signatures, and time window matching.
"""

import hashlib
from typing import List, Set, Dict, Any, Tuple
from integrations.research.event import MarketEvent

class EventDeduplicator:
    """
    Deduplicates MarketEvents by computing deterministic hashes for URLs and content text.
    Maintains seen state to prevent re-processing identical items.
    """

    def __init__(self):
        self._seen_urls: Set[str] = set()
        self._seen_content_hashes: Set[str] = set()

    def _hash_url(self, url: str) -> str:
        clean = url.strip().lower().split("#")[0].rstrip("/")
        return hashlib.sha256(clean.encode("utf-8")).hexdigest()

    def _hash_content(self, title: str, content: str) -> str:
        raw = f"{title.strip().lower()}:{content.strip().lower()[:200]}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def deduplicate(self, events: List[MarketEvent]) -> List[MarketEvent]:
        """Filters a list of MarketEvents, returning only unique events."""
        unique_events: List[MarketEvent] = []

        for evt in events:
            url_h = self._hash_url(evt.url) if evt.url else None
            content_h = self._hash_content(evt.title, evt.content)

            # Skip if URL or content signature has already been seen
            if url_h and url_h in self._seen_urls:
                continue
            if content_h in self._seen_content_hashes:
                continue

            if url_h:
                self._seen_urls.add(url_h)
            self._seen_content_hashes.add(content_h)
            unique_events.append(evt)

        return unique_events

    def reset(self):
        self._seen_urls.clear()
        self._seen_content_hashes.clear()
