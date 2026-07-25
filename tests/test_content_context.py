"""
Unit tests for Content Department Context Builder, Generators, and Editors.
"""

import unittest
from content.context.builder import ContentContextBuilder
from content.generators.article_generator import ArticleGenerator, LinkedInGenerator
from content.editors.technical_editor import TechnicalEditor, ComplianceEditor

class TestContentContextAndGenerators(unittest.TestCase):
    def test_context_builder(self):
        ctx = ContentContextBuilder.build_context("AI Agents")
        self.assertIsNotNone(ctx.planning_report)
        self.assertIsNotNone(ctx.research_package)
        self.assertIn("Lead Generation", ctx.campaign_goals)

    def test_article_generator(self):
        ctx = ContentContextBuilder.build_context("AI Agents")
        article = ArticleGenerator.generate_article(ctx)
        self.assertIsNotNone(article.title)
        self.assertGreater(article.word_count, 100)
        self.assertGreater(len(article.citations_used), 0)

    def test_editorial_compliance(self):
        is_valid, violations = ComplianceEditor.validate_brand_compliance(
            "This is a high performance architecture.", ["guaranteed", "best company"]
        )
        self.assertTrue(is_valid)

if __name__ == "__main__":
    unittest.main()
