"""
Centralized Research Engine Provider Manager Singleton for AVENIQ.
Orchestrates providers, live testers, cache persistence, trend analysis, and background sync.
"""

from typing import Dict, Any, List
from research.engine.collectors import ALL_PROVIDERS
from research.engine.cache import global_research_cache
from research.engine.health_monitor import global_health_monitor
from research.engine.trend_analyzer import global_trend_analyzer
from research.engine.summarizer import global_research_summarizer


class ResearchProviderManager:
    def __init__(self):
        self.cache = global_research_cache
        self.health = global_health_monitor
        self.trend_analyzer = global_trend_analyzer
        self.summarizer = global_research_summarizer

    def test_provider(self, provider: str) -> Dict[str, Any]:
        """Perform a live API connection test without updating the research cache."""
        tester = ALL_PROVIDERS.get(provider.lower())
        if not tester:
            return {
                "provider": provider,
                "status": "Not Configured",
                "configured": False,
                "authenticated": False,
                "latency_ms": 0.0,
                "error": f"Unknown provider '{provider}'",
                "sample_data": []
            }
        
        result = tester()
        # Persist health update
        self.health.update_source_status(
            provider=provider,
            status=result.get("status", "Unknown"),
            configured=result.get("configured", False),
            authenticated=result.get("authenticated", False),
            latency_ms=result.get("latency_ms", 0.0),
            remaining_quota=result.get("rate_limit"),
            last_error=result.get("error")
        )
        return result

    def refresh_provider(self, provider: str) -> Dict[str, Any]:
        """Perform live fetch and update the persistent cache for a provider."""
        test_result = self.test_provider(provider)
        sample_items = test_result.get("sample_data", [])
        
        # Save to provider cache
        self.cache.save_provider_cache(
            provider=provider,
            items=sample_items,
            latency_ms=test_result.get("latency_ms", 0.0),
            rate_limit=str(test_result.get("rate_limit") or ""),
            error=test_result.get("error")
        )
        return test_result

    def refresh_all_providers(self) -> Dict[str, Any]:
        """Refresh all supported providers."""
        results = {}
        for p in ALL_PROVIDERS.keys():
            try:
                results[p] = self.refresh_provider(p)
            except Exception as e:
                results[p] = {"provider": p, "error": str(e), "status": "Failed"}
        return {"refreshed_count": len(results), "providers": results}

    def get_overview(self) -> Dict[str, Any]:
        """Return cached research overview, market signals, trends, and health summary."""
        health_summary = self.health.get_sources_summary()
        all_items = self.cache.load_all_cached_items()
        
        # If cache is empty on first boot, populate with sample fetches
        if not all_items:
            for p in ["github", "reddit", "google_news", "hackernews"]:
                try:
                    self.refresh_provider(p)
                except Exception:
                    pass
            all_items = self.cache.load_all_cached_items()

        trends = self.trend_analyzer.analyze_trends(all_items)
        signals = self.trend_analyzer.compute_market_signals(all_items, trends)
        summary = self.summarizer.get_latest_summary("daily")

        return {
            "health": health_summary,
            "trending_topics": trends,
            "market_signals": signals,
            "ai_summary": summary,
            "total_items": len(all_items)
        }


global_research_manager = ResearchProviderManager()
