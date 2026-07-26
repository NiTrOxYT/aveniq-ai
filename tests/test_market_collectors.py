"""
Comprehensive Test Suite for Production Market Intelligence Data Collectors.
Tests Reddit, GitHub, RSS, Google News, Product Hunt, Competitor Website Crawler,
Event Deduplicator, Rate Limiter, HTTP Retry Logic, Health Reporting, Normalization, and Market Storage.
"""

import unittest
import os
import json
import time
from unittest.mock import patch, MagicMock

from integrations.research.event import MarketEvent, generate_event_id
from integrations.research.collectors.base import BaseMarketCollector, RateLimiter, CollectorHealth, fetch_url_with_retry
from integrations.research.collectors.reddit import RedditCollector
from integrations.research.collectors.github import GitHubCollector
from integrations.research.collectors.rss import RSSCollector
from integrations.research.collectors.google_news import GoogleNewsCollector
from integrations.research.collectors.product_hunt import ProductHuntCollector
from integrations.research.collectors.website import WebsiteCrawlerCollector, HTMLTextExtractor
from integrations.research.deduplication.deduplicator import EventDeduplicator
from integrations.research.storage.market_storage import MarketEventStorage
from integrations.research.registry.collector_registry import global_collector_registry


class TestMarketCollectors(unittest.TestCase):

    def test_market_event_schema_and_bridge(self):
        evt = MarketEvent(
            id="evt_test_123",
            source="reddit",
            category="discussions",
            title="Test Event Title",
            content="Test Event Content Payload",
            url="https://reddit.com/r/test",
            author="u/test_author"
        )
        data = evt.to_dict()
        self.assertEqual(data["id"], "evt_test_123")
        self.assertEqual(data["source"], "reddit")

        reconstructed = MarketEvent.from_dict(data)
        self.assertEqual(reconstructed.id, evt.id)
        self.assertEqual(reconstructed.title, evt.title)

        doc = evt.to_document()
        self.assertEqual(doc.id, evt.id)
        self.assertEqual(doc.source, "reddit")
        self.assertEqual(doc.url, "https://reddit.com/r/test")

    def test_rate_limiter_throttling(self):
        limiter = RateLimiter(min_interval_sec=0.1)
        start = time.time()
        limiter.wait_if_needed()
        limiter.wait_if_needed()
        elapsed = time.time() - start
        self.assertGreaterEqual(elapsed, 0.09)

    def test_event_deduplication(self):
        deduper = EventDeduplicator()
        e1 = MarketEvent(id="1", source="rss", category="general", title="Identical Title", content="Identical Content", url="https://example.com/article1")
        e2 = MarketEvent(id="2", source="rss", category="general", title="Identical Title", content="Identical Content", url="https://example.com/article1#section")
        e3 = MarketEvent(id="3", source="github", category="trends", title="Unique Title", content="Unique Content", url="https://github.com/repo")

        filtered = deduper.deduplicate([e1, e2, e3])
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].url, "https://example.com/article1")
        self.assertEqual(filtered[1].url, "https://github.com/repo")

    def test_reddit_collector_normalization_and_fallback(self):
        col = RedditCollector()
        col.initialize()

        raw_post = {
            "title": "Looking for best multi-agent AI framework alternative to LangChain",
            "selftext": "We are looking for production alternative with retry backoffs.",
            "url": "https://reddit.com/r/SaaS/comments/12345",
            "subreddit": "SaaS",
            "author": "saas_founder",
            "ups": 150,
            "num_comments": 42,
            "score": 192,
            "created_utc": 1722000000
        }

        evt = col.normalize(raw_post)
        self.assertIsNotNone(evt)
        self.assertEqual(evt.source, "reddit")
        self.assertEqual(evt.category, "buying_intent")
        self.assertTrue(evt.metadata["buying_intent"])
        self.assertEqual(evt.metadata["upvotes"], 150)

        # Test fallback on empty network fetch
        events = col.collect_safe("AI Agents")
        self.assertGreaterEqual(len(events), 1)

    def test_github_collector_normalization(self):
        col = GitHubCollector()
        col.initialize()

        raw_repo = {
            "full_name": "aveniq-ai/aveniq",
            "html_url": "https://github.com/aveniq-ai/aveniq",
            "description": "Production Market Intelligence Platform",
            "stargazers_count": 1420,
            "forks_count": 210,
            "owner": {"login": "aveniq-ai"},
            "topics": ["ai", "python", "agents"],
            "language": "Python"
        }

        evt = col.normalize(raw_repo)
        self.assertIsNotNone(evt)
        self.assertEqual(evt.source, "github")
        self.assertIn("1,420 ★", evt.title)
        self.assertEqual(evt.metadata["stars"], 1420)
        self.assertEqual(evt.metadata["forks"], 210)

    def test_rss_collector_xml_parsing(self):
        col = RSSCollector()
        col.initialize()

        sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <title>Hacker News</title>
                <item>
                    <title>Show HN: AVENIQ Market Intelligence</title>
                    <link>https://news.ycombinator.com/item?id=112233</link>
                    <description>Open source real-time market signals platform.</description>
                    <pubDate>Sun, 26 Jul 2026 12:00:00 GMT</pubDate>
                </item>
            </channel>
        </rss>
        """

        events = col._parse_feed_xml(sample_xml, "https://news.ycombinator.com/rss")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].title, "Show HN: AVENIQ Market Intelligence")
        self.assertEqual(events[0].source, "rss")
        self.assertEqual(events[0].url, "https://news.ycombinator.com/item?id=112233")

    def test_google_news_collector(self):
        col = GoogleNewsCollector()
        col.initialize()

        sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>AI Startup Raises $50M Series B for Multi-Agent Workflows</title>
                    <link>https://news.google.com/articles/123</link>
                    <pubDate>Sun, 26 Jul 2026 10:00:00 GMT</pubDate>
                    <source>TechCrunch</source>
                </item>
            </channel>
        </rss>
        """

        events = col._parse_google_news_xml(sample_xml, "AI Funding")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].category, "funding")
        self.assertEqual(events[0].author, "TechCrunch")

    def test_product_hunt_collector(self):
        col = ProductHuntCollector()
        col.initialize()

        events = col.collect_safe("AI Tools")
        self.assertGreaterEqual(len(events), 1)
        self.assertEqual(events[0].source, "product_hunt")
        self.assertEqual(events[0].category, "launches")

    def test_website_crawler_html_text_extractor_and_robots(self):
        html = "<html><head><title>Test</title></head><body><h1>Competitor Title</h1><script>console.log('ignore');</script><p>Feature Matrix & Pricing</p></body></html>"
        parser = HTMLTextExtractor()
        parser.feed(html)
        extracted = parser.get_text()

        self.assertIn("Competitor Title", extracted)
        self.assertIn("Feature Matrix & Pricing", extracted)
        self.assertNotIn("console.log", extracted)

        col = WebsiteCrawlerCollector()
        col.initialize()
        # Robotos check defaults to True for normal URLs
        self.assertTrue(col._is_allowed_by_robots("https://example.com/pricing"))

    def test_market_storage_persistence_and_search(self):
        test_file = os.path.abspath("test_market_events_tmp.json")
        if os.path.exists(test_file):
            os.remove(test_file)

        try:
            storage = MarketEventStorage(storage_path=test_file)
            e1 = MarketEvent(id="evt_1", source="reddit", category="discussions", title="AI Agents in Production", content="Discussion on LLM router failover.", url="https://reddit.com/r/ai/1")
            e2 = MarketEvent(id="evt_2", source="github", category="trends", title="aveniq-ai Framework", content="Python enterprise repository.", url="https://github.com/aveniq-ai/aveniq")

            saved_count = storage.save_events([e1, e2])
            self.assertEqual(saved_count, 2)

            res_all = storage.load_events()
            self.assertEqual(len(res_all), 2)

            # Search by keyword
            res_query = storage.search(query="router")
            self.assertEqual(len(res_query), 1)
            self.assertEqual(res_query[0].id, "evt_1")

            # Search by source
            res_gh = storage.search(source="github")
            self.assertEqual(len(res_gh), 1)
            self.assertEqual(res_gh[0].id, "evt_2")

            stats = storage.get_stats()
            self.assertEqual(stats["total_events"], 2)
            self.assertEqual(stats["source_counts"]["reddit"], 1)
            self.assertEqual(stats["source_counts"]["github"], 1)

        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_collector_registry_health_summary(self):
        summary = global_collector_registry.health_summary()
        self.assertIn("reddit", summary)
        self.assertIn("github", summary)
        self.assertIn("rss", summary)
        self.assertIn("google_news", summary)
        self.assertIn("product_hunt", summary)
        self.assertIn("website", summary)
        self.assertIn(summary["reddit"]["status"], ("READY", "DEGRADED", "UNAVAILABLE", "Healthy"))


if __name__ == "__main__":
    unittest.main()
