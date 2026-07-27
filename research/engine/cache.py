"""
Cache Engine for AVENIQ AI Research System.
Stores and retrieves normalized research results per provider in research/storage/cache/.
Supports unified cross-provider search and querying.
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = WORKSPACE_ROOT / "research" / "storage" / "cache"


class ResearchCache:
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def save_provider_cache(
        self,
        provider: str,
        items: List[Dict[str, Any]],
        latency_ms: float = 0.0,
        rate_limit: Optional[str] = None,
        error: Optional[str] = None
    ) -> Path:
        file_path = self.cache_dir / f"{provider}.json"
        payload = {
            "provider": provider,
            "last_fetch": datetime.now(timezone.utc).isoformat(),
            "total_results": len(items),
            "latency_ms": round(latency_ms, 2),
            "rate_limit": rate_limit,
            "error": error,
            "items": items
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return file_path

    def load_provider_cache(self, provider: str) -> Dict[str, Any]:
        file_path = self.cache_dir / f"{provider}.json"
        if not file_path.exists():
            return {
                "provider": provider,
                "last_fetch": None,
                "total_results": 0,
                "latency_ms": 0.0,
                "rate_limit": None,
                "error": None,
                "items": []
            }
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {
                "provider": provider,
                "last_fetch": None,
                "total_results": 0,
                "latency_ms": 0.0,
                "rate_limit": None,
                "error": str(e),
                "items": []
            }

    def load_all_cached_items(self) -> List[Dict[str, Any]]:
        all_items = []
        for p in self.cache_dir.glob("*.json"):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    items = data.get("items", [])
                    all_items.extend(items)
            except Exception:
                continue
        # Sort by published_at or score descending
        all_items.sort(key=lambda x: x.get("published_at") or "", reverse=True)
        return all_items

    def search_cache(
        self,
        query: str = "",
        category: str = "",
        provider: str = "",
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        items = self.load_all_cached_items()
        filtered = []
        q_lower = query.lower().strip()

        for item in items:
            if category and item.get("category") != category:
                continue
            if provider and item.get("provider") != provider:
                continue
            if q_lower:
                title = (item.get("title") or "").lower()
                summary = (item.get("summary") or "").lower()
                tags = " ".join(item.get("tags") or []).lower()
                prov = (item.get("provider") or "").lower()
                if q_lower not in title and q_lower not in summary and q_lower not in tags and q_lower not in prov:
                    continue
            filtered.append(item)
            if len(filtered) >= limit:
                break

        return filtered


global_research_cache = ResearchCache()
