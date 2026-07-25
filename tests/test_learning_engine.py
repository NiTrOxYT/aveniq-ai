"""
Unit tests for Learning Department Context, Analyzers, Proposals, and Engine.
"""

import unittest
from learning.context.builder import LearningContextBuilder
from learning.proposals.proposal_registry import MemoryManager, ProposalRegistry
from learning.analyzers.campaign_analyzer import DuplicateDetector
from learning.engine.learning_engine import LearningEngine

class TestLearningDepartment(unittest.TestCase):
    def test_context_builder(self):
        ctx = LearningContextBuilder.build_context("AI Agents")
        self.assertIsNotNone(ctx.archive_package)
        self.assertIsNotNone(ctx.delivery_package)

    def test_memory_and_proposals(self):
        ctx = LearningContextBuilder.build_context("AI Agents")
        recs = MemoryManager.generate_recommendations(ctx)
        props = ProposalRegistry.generate_knowledge_proposals(ctx)

        self.assertGreater(len(recs), 0)
        self.assertGreater(len(props), 0)
        self.assertEqual(props[0].target_file, "knowledge/taxonomy.yaml")

    def test_duplicate_detector(self):
        ctx = LearningContextBuilder.build_context("AI Agents")
        report = DuplicateDetector.scan_duplicates(ctx)
        self.assertIsNotNone(report)
        self.assertEqual(report.duplicate_prompts_detected, 0)

    def test_learning_engine(self):
        engine = LearningEngine()
        pkg = engine.generate_learning_package("AI Agents in Enterprise Operations")
        self.assertIsNotNone(pkg)
        self.assertGreater(pkg.scores.overall_learning_score, 85.0)
        self.assertTrue(pkg.quality_gate.passed)

if __name__ == "__main__":
    unittest.main()
