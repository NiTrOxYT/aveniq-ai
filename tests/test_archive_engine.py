"""
Unit tests for Archive Department Context, Events, Knowledge Graph, Search, and Engine.
"""

import unittest
from archive.context.builder import ArchiveContextBuilder
from archive.events.event_store import EventStore, KnowledgeGraphBuilder
from archive.search.archive_search import ArchiveSearchEngine
from archive.engine.archive_engine import ArchiveEngine

class TestArchiveDepartment(unittest.TestCase):
    def test_context_builder(self):
        ctx = ArchiveContextBuilder.build_context("AI Agents")
        self.assertIsNotNone(ctx.delivery_package)
        self.assertIsNotNone(ctx.approved_content_package)
        self.assertIsNotNone(ctx.media_package)

    def test_event_store_and_graph(self):
        ctx = ArchiveContextBuilder.build_context("AI Agents")
        events = EventStore.generate_campaign_events("cmp_001", ctx)
        graph = KnowledgeGraphBuilder.build_graph("cmp_001", "AI Agents")

        self.assertEqual(len(events), 8)
        self.assertGreater(len(graph.nodes), 5)
        self.assertGreater(len(graph.edges), 5)

    def test_search_engine(self):
        pkgs = [{"id": "arc_001", "campaign_id": "cmp_001", "topic": "AI Agents in Enterprise", "executive_summary": "Summary", "date": "2026-07-25"}]
        results = ArchiveSearchEngine.search("Enterprise", pkgs)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].matched_field, "topic")

    def test_archive_engine(self):
        engine = ArchiveEngine()
        pkg = engine.archive_delivery_package("AI Agents in Enterprise Operations")
        self.assertIsNotNone(pkg)
        self.assertEqual(pkg.topic, "AI Agents in Enterprise Operations")
        self.assertEqual(pkg.lifecycle_state, "ACTIVE")
        self.assertEqual(len(pkg.vector_embedding), 128)
        self.assertTrue(pkg.quality_gate.passed)

if __name__ == "__main__":
    unittest.main()
