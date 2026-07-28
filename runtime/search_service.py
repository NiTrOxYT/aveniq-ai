"""
Platform-Wide Unified Search Service for AVENIQ AI Runtime.
Aggregates search results across Company Brain, Research Engine, Campaigns, Automation, and Documentation.
"""

from typing import List, Dict, Any, Callable


class UnifiedSearchService:
    def __init__(self):
        self._providers: List[Callable[[str, int], List[Dict[str, Any]]]] = []

    def register_provider(self, provider_fn: Callable[[str, int], List[Dict[str, Any]]]):
        """Register a search provider function that takes (query, limit) and returns matching item dicts."""
        self._providers.append(provider_fn)

    def search(self, query: str = "", limit: int = 50) -> List[Dict[str, Any]]:
        """Query all registered platform search providers and aggregate results."""
        if not query:
            return []
        
        q_lower = query.lower().strip()
        aggregated = []

        for p in self._providers:
            try:
                res = p(q_lower, limit)
                if res:
                    aggregated.extend(res)
            except Exception:
                continue

        # Deduplicate results by ID or title
        seen = set()
        unique_results = []
        for item in aggregated:
            key = item.get("id") or item.get("title")
            if key and key not in seen:
                seen.add(key)
                unique_results.append(item)

        return unique_results[:limit]


global_unified_search_service = UnifiedSearchService()
