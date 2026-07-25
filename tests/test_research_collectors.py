"""
Unit tests for Research Department Collectors.
"""

import unittest
from research.collectors.statistics_collector import StatisticsCollector
from research.collectors.studies_collector import (
    StudiesCollector, TechnicalCollector, CompetitorCollector, SEOCollector, CaseStudyCollector
)

class TestResearchCollectors(unittest.TestCase):
    def test_statistics_collector(self):
        stats = StatisticsCollector.collect_statistics("AI Agents")
        self.assertGreater(len(stats), 0)
        self.assertIn("68%", stats[0].value)

    def test_studies_collector(self):
        studies = StudiesCollector.collect_studies("AI Agents")
        self.assertGreater(len(studies), 0)
        self.assertEqual(studies[0].publication_year, 2025)

    def test_technical_collector(self):
        claims = TechnicalCollector.collect_technical_claims("pgvector")
        self.assertGreater(len(claims), 0)
        self.assertEqual(claims[0].verification_status, "Verified")

    def test_seo_collector(self):
        seo = SEOCollector.collect_seo("AI Agents")
        self.assertIsNotNone(seo.primary_keyword)
        self.assertGreater(len(seo.user_questions), 0)

if __name__ == "__main__":
    unittest.main()
