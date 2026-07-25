"""
Unit tests for Content Engine, Quality Gate, and Scoring Engine.
"""

import unittest
from content.engine.content_engine import ContentEngine
from content.context.builder import ContentContextBuilder
from content.generators.article_generator import ArticleGenerator
from content.analyzers.scoring_engine import ContentScoringEngine

class TestContentEngineAndQualityGate(unittest.TestCase):
    def test_content_engine(self):
        engine = ContentEngine()
        pkg = engine.generate_content_package("AI Agents in Enterprise Operations")
        self.assertIsNotNone(pkg)
        self.assertEqual(pkg.topic, "AI Agents in Enterprise Operations")
        self.assertGreater(pkg.master_article.word_count, 100)
        self.assertTrue(pkg.quality_gate.passed)

    def test_scoring_engine(self):
        ctx = ContentContextBuilder.build_context("AI Agents")
        article = ArticleGenerator.generate_article(ctx)
        scores = ContentScoringEngine.calculate_scores(article, ctx)
        self.assertGreaterEqual(scores.overall_score, 85.0)
        self.assertGreaterEqual(scores.brand_alignment_score, 90.0)

if __name__ == "__main__":
    unittest.main()
