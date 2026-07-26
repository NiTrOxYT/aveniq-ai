"""
Persistence Storage Engine for Production Market Intelligence Signals.
Stores normalized MarketEvents to JSON persistence, supporting querying by source, keyword, category, competitor, and date.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from integrations.research.event import MarketEvent
from integrations.research.deduplication.deduplicator import EventDeduplicator

log = logging.getLogger("aveniq.research.storage")

DEFAULT_STORAGE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "market_events.json")
)


class MarketEventStorage:
    def __init__(self, storage_path: str = DEFAULT_STORAGE_PATH):
        self.storage_path = storage_path
        self._deduplicator = EventDeduplicator()
        self._ensure_storage_dir()

    def _ensure_storage_dir(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load_events(self) -> List[MarketEvent]:
        self._ensure_storage_dir()
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [MarketEvent.from_dict(item) for item in data]
        except Exception as e:
            log.warning("Failed to load market events from %s: %s", self.storage_path, e)
            return []

    def save_events(self, new_events: List[MarketEvent]) -> int:
        existing = self.load_events()
        # Seed deduplicator with existing events
        self._deduplicator.deduplicate(existing)

        # Deduplicate incoming new events against existing
        unique_new = self._deduplicator.deduplicate(new_events)
        if not unique_new:
            return 0

        combined = existing + unique_new
        data = [evt.to_dict() for evt in combined]

        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            log.info("Saved %d new market events to %s", len(unique_new), self.storage_path)
            return len(unique_new)
        except Exception as e:
            log.error("Failed to save market events: %s", e)
            return 0

    def search(
        self,
        query: str = "",
        source: Optional[str] = None,
        category: Optional[str] = None,
        competitor: Optional[str] = None,
        limit: int = 50
    ) -> List[MarketEvent]:
        events = self.load_events()
        results: List[MarketEvent] = []

        q_clean = query.strip().lower()

        for evt in events:
            if source and evt.source.lower() != source.lower():
                continue
            if category and evt.category.lower() != category.lower():
                continue
            if competitor and competitor.lower() not in (evt.title + evt.content + json.dumps(evt.metadata)).lower():
                continue

            if q_clean:
                text_corpus = f"{evt.title} {evt.content} {evt.source} {evt.category} {' '.join(evt.metadata.get('tags', []))}".lower()
                if q_clean not in text_corpus:
                    continue

            results.append(evt)
            if len(results) >= limit:
                break

        return results

    def get_stats(self) -> Dict[str, Any]:
        events = self.load_events()
        source_counts: Dict[str, int] = {}
        category_counts: Dict[str, int] = {}

        for evt in events:
            source_counts[evt.source] = source_counts.get(evt.source, 0) + 1
            category_counts[evt.category] = category_counts.get(evt.category, 0) + 1

        return {
            "total_events": len(events),
            "source_counts": source_counts,
            "category_counts": category_counts,
            "storage_path": self.storage_path
        }


global_market_storage = MarketEventStorage()
