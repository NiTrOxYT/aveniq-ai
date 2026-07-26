"""
Centralized Collector Registry for Real-Time Market Intelligence Collectors.
Supports register, unregister, resolve, listing, enabled collector queries, and aggregate health summary.
"""

from typing import Dict, Any, List, Optional
from integrations.research.collectors.reddit import RedditCollector
from integrations.research.collectors.github import GitHubCollector
from integrations.research.collectors.rss import RSSCollector
from integrations.research.collectors.google_news import GoogleNewsCollector
from integrations.research.collectors.product_hunt import ProductHuntCollector
from integrations.research.collectors.website import WebsiteCrawlerCollector

class CollectorRegistry:
    def __init__(self):
        self._collectors: Dict[str, Any] = {}

    def register(self, name: str, collector_instance: Any):
        self._collectors[name] = collector_instance

    def unregister(self, name: str):
        self._collectors.pop(name, None)

    def resolve(self, name: str) -> Optional[Any]:
        return self._collectors.get(name)

    def list_collectors(self) -> List[str]:
        return list(self._collectors.keys())

    def enabled_collectors(self) -> List[Any]:
        return list(self._collectors.values())

    def health_summary(self) -> Dict[str, Any]:
        summary = {}
        for name, col in self._collectors.items():
            if hasattr(col, "health") and callable(col.health):
                h = col.health()
                summary[name] = {
                    "status": h.status,
                    "total_collected": h.total_collected,
                    "last_sync": h.last_sync,
                    "error_count": h.error_count,
                    "message": h.message
                }
            else:
                summary[name] = {
                    "status": "READY",
                    "total_collected": getattr(col, "total_collected", 0),
                    "message": f"Collector {name} ready"
                }
        return summary


global_collector_registry = CollectorRegistry()

# Register Production Collectors
global_collector_registry.register("reddit", RedditCollector())
global_collector_registry.register("github", GitHubCollector())
global_collector_registry.register("rss", RSSCollector())
global_collector_registry.register("google_news", GoogleNewsCollector())
global_collector_registry.register("product_hunt", ProductHuntCollector())
global_collector_registry.register("website", WebsiteCrawlerCollector())
