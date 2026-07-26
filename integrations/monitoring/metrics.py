"""
Integration Metrics Collector & Health Monitor across all registered providers.
"""

from typing import Dict, Any, List
from integrations.registry.global_registry import global_registry
from integrations.base.request import ProviderHealth

class IntegrationMetricsCollector:
    def __init__(self):
        self.provider_requests: Dict[str, int] = {}
        self.provider_latencies: Dict[str, List[float]] = {}
        self.retry_counts: Dict[str, int] = {}
        self.error_counts: Dict[str, int] = {}
        self.fallback_activations: int = 0
        self.cache_hits: int = 0
        self.cache_misses: int = 0

    def record_request(self, provider: str, latency: float, success: bool, retries: int = 0, cached: bool = False):
        self.provider_requests[provider] = self.provider_requests.get(provider, 0) + 1
        
        if provider not in self.provider_latencies:
            self.provider_latencies[provider] = []
        self.provider_latencies[provider].append(latency)

        self.retry_counts[provider] = self.retry_counts.get(provider, 0) + retries
        if not success:
            self.error_counts[provider] = self.error_counts.get(provider, 0) + 1

        if cached:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def record_fallback(self):
        self.fallback_activations += 1

    def get_summary(self) -> Dict[str, Any]:
        total_cache = self.cache_hits + self.cache_misses
        hit_ratio = round((self.cache_hits / total_cache) * 100.0, 1) if total_cache else 0.0

        return {
            "provider_requests": self.provider_requests,
            "retry_counts": self.retry_counts,
            "error_counts": self.error_counts,
            "fallback_activations": self.fallback_activations,
            "cache_hit_ratio": f"{hit_ratio}%",
            "cache_hits": self.cache_hits
        }

class HealthMonitor:
    @staticmethod
    def check_all() -> Dict[str, ProviderHealth]:
        return global_registry.health_summary()

global_metrics = IntegrationMetricsCollector()
