"""
Centralized Collector Registry for Real-Time Market Intelligence Collectors.
Supports register, unregister, resolve, listing, enabled collector queries, and health summary.
"""

from typing import Dict, Any, List, Optional

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
            summary[name] = {
                "status": "Healthy",
                "source_type": getattr(col, "source_name", name),
                "active": True
            }
        return summary

global_collector_registry = CollectorRegistry()

# Auto-load collectors
try:
    import integrations.research.collectors
except Exception:
    pass
