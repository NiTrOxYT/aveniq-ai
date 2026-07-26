"""
Comprehensive Test Suite for Real Market Intelligence Platform.
Tests ResearchDocument, CollectorRegistry, Collectors, SemanticClusterer, MultiFactorTrendDetector, and ResearchAggregator.
"""

import unittest
from integrations.research.document import ResearchDocument
from integrations.research.registry.collector_registry import CollectorRegistry
from integrations.research.collectors.reddit import (
    RedditCollector, HackerNewsCollector, GoogleTrendsCollector, GitHubCollector, DevToCollector
)
from integrations.research.clustering.clusterer import SemanticClusterer
from integrations.research.ranking.trend_detector import MultiFactorTrendDetector, EvidenceOpportunityDetector
from integrations.research.aggregation.aggregator import ResearchAggregator

class TestRealMarketIntelligence(unittest.TestCase):
    def test_research_document(self):
        doc = ResearchDocument(id="doc_1", source="reddit", title="Test", url="https://test.com")
        self.assertEqual(doc.freshness_score, 100.0)
        self.assertEqual(doc.credibility_score, 85.0)

    def test_collector_registry(self):
        reg = CollectorRegistry()
        col = RedditCollector()
        reg.register("reddit", col)
        self.assertEqual(len(reg.list_collectors()), 1)
        self.assertEqual(reg.resolve("reddit"), col)

    def test_collectors(self):
        col = HackerNewsCollector()
        docs = col.collect_safe("AI Agents")
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0].source, "hackernews")

    def test_semantic_clustering_and_ranking(self):
        doc1 = ResearchDocument("1", "reddit", "Title 1", "https://t1.com", tags=["ai"])
        doc2 = ResearchDocument("2", "github", "Title 2", "https://t2.com", tags=["ai"])
        clusters = SemanticClusterer.cluster_documents([doc1, doc2])
        self.assertEqual(len(clusters), 1)

        score = MultiFactorTrendDetector.calculate_trend_score(clusters[0])
        self.assertGreater(score, 0.0)

        opps = EvidenceOpportunityDetector.detect_opportunities(clusters)
        self.assertEqual(len(opps), 1)
        self.assertGreater(opps[0].confidence_score, 0.8)

    def test_research_aggregator(self):
        agg = ResearchAggregator()
        pkg = agg.collect_and_aggregate("AI Agents")
        self.assertIsNotNone(pkg.id)
        self.assertGreater(len(pkg.sources), 0)
        self.assertGreater(len(pkg.trends), 0)

if __name__ == "__main__":
    unittest.main()
