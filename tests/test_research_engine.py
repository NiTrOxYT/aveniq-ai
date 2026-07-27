"""
Automated Integration Tests for AVENIQ Centralized Research Engine.
Verifies normalizers, live testers, cache persistence, health monitor, trend analyzer, and provider manager.
"""

import pytest
from research.engine.normalizer import normalize_github_repo, normalize_reddit_post, normalize_hackernews_item
from research.engine.cache import global_research_cache
from research.engine.health_monitor import global_health_monitor
from research.engine.collectors import ProviderCollector
from research.engine.trend_analyzer import global_trend_analyzer
from research.engine.provider_manager import global_research_manager


def test_github_normalizer():
    sample_repo = {
        "id": 12345,
        "name": "aveniq-ai",
        "full_name": "aveniq/aveniq-ai",
        "description": "Enterprise AI OS",
        "html_url": "https://github.com/aveniq/aveniq-ai",
        "stargazers_count": 500,
        "language": "Python"
    }
    item = normalize_github_repo(sample_repo)
    assert item.provider == "github"
    assert item.category == "code"
    assert item.title == "aveniq/aveniq-ai"
    assert item.score == 500.0


def test_reddit_normalizer():
    sample_post = {
        "id": "post123",
        "title": "Autonomous AI Agents in Production",
        "selftext": "Discussion on agentic AI workflows",
        "subreddit": "artificial",
        "score": 350
    }
    item = normalize_reddit_post(sample_post)
    assert item.provider == "reddit"
    assert item.category == "community"
    assert item.score == 350.0


def test_live_hackernews_tester():
    res = ProviderCollector.test_hackernews()
    assert res["provider"] == "hackernews"
    assert res["status"] == "Connected"
    assert isinstance(res["sample_data"], list)
    assert len(res["sample_data"]) > 0


def test_live_google_news_tester():
    res = ProviderCollector.test_google_news()
    assert res["provider"] == "google_news"
    assert res["status"] in ("Connected", "Offline")
    assert isinstance(res["sample_data"], list)


def test_cache_and_health_integration():
    # Save test item to cache
    global_research_cache.save_provider_cache(
        provider="test_prov",
        items=[{
            "id": "test_1",
            "provider": "test_prov",
            "category": "ai",
            "title": "Model Context Protocol Tooling",
            "summary": "AI Agent context protocol",
            "score": 100
        }],
        latency_ms=12.5
    )

    loaded = global_research_cache.load_provider_cache("test_prov")
    assert loaded["total_results"] == 1
    assert loaded["items"][0]["title"] == "Model Context Protocol Tooling"

    search_res = global_research_cache.search_cache(query="Context")
    assert len(search_res) >= 1
    assert search_res[0]["provider"] == "test_prov"


def test_trend_analyzer():
    sample_items = [
        {"title": "Model Context Protocol for Agents", "summary": "MCP protocol", "provider": "github", "score": 200},
        {"title": "Model Context Protocol Release", "summary": "MCP tools", "provider": "reddit", "score": 150},
        {"title": "Model Context Protocol in Enterprise", "summary": "MCP deployment", "provider": "google_news", "score": 80}
    ]
    trends = global_trend_analyzer.analyze_trends(sample_items)
    assert len(trends) > 0
    signals = global_trend_analyzer.compute_market_signals(sample_items, trends)
    assert len(signals) > 0


def test_provider_manager_overview():
    overview = global_research_manager.get_overview()
    assert "health" in overview
    assert "trending_topics" in overview
    assert "market_signals" in overview
    assert "ai_summary" in overview
