"""
Unit tests for Research Analyzers, Engine, and Quality Gate.
"""

import unittest
from research.engine.research_engine import ResearchEngine
from research.utils.quality_gate import QualityGateVerifier
from research.collectors.source_collector import SourceCollector

class TestResearchAnalyzersAndEngine(unittest.TestCase):
    def test_research_engine(self):
        engine = ResearchEngine()
        pkg = engine.generate_research_package("AI Agents in Enterprise Operations")
        self.assertIsNotNone(pkg)
        self.assertEqual(pkg.topic, "AI Agents in Enterprise Operations")
        self.assertGreater(len(pkg.verified_statistics), 0)
        self.assertGreater(len(pkg.citations), 0)
        self.assertTrue(pkg.quality_gate.passed)

    def test_quality_gate(self):
        engine = ResearchEngine()
        pkg = engine.generate_research_package("Test Topic")
        qg = QualityGateVerifier.verify_package(
            pkg.topic, pkg.verified_statistics, pkg.supporting_studies,
            pkg.technical_validation, pkg.competitor_insights,
            pkg.real_world_examples, pkg.seo_insights, pkg.citations
        )
        self.assertTrue(qg.passed)
        self.assertGreaterEqual(qg.score, 85.0)

if __name__ == "__main__":
    unittest.main()
