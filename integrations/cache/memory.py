"""
Cache providers: Memory Cache with TTL and Filesystem Cache.
"""

import time
import os
import json
from typing import Dict, Any, Optional

class MemoryCacheProvider:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self._store: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None
        if time.time() > entry["expires_at"]:
            del self._store[key]
            return None
        return entry["value"]

    def set(self, key: str, value: Any) -> None:
        self._store[key] = {
            "value": value,
            "expires_at": time.time() + self.ttl
        }

    def clear(self) -> None:
        self._store.clear()

class FilesystemCacheProvider:
    def __init__(self, cache_dir: str = ".cache/integrations", ttl_seconds: int = 3600):
        self.cache_dir = cache_dir
        self.ttl = ttl_seconds
        os.makedirs(cache_dir, exist_ok=True)

    def get(self, key: str) -> Optional[Any]:
        filepath = os.path.join(self.cache_dir, f"{key}.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if time.time() > data.get("expires_at", 0):
            os.remove(filepath)
            return None
        return data.get("value")

    def set(self, key: str, value: Any) -> None:
        filepath = os.path.join(self.cache_dir, f"{key}.json")
        data = {
            "value": value,
            "expires_at": time.time() + self.ttl
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
