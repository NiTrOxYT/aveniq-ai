"""
Unit tests for Editorial Department Context, Reviewers, Policy, and Engine.
"""

import unittest
from editorial.context.builder import EditorialContextBuilder
from editorial.issues.tracker import IssueTracker
from editorial.analyzers.evidence_mapper import EvidenceMapper, RedFlagDetector
from editorial.engine.policy_engine import EditorialScorer, PolicyEngine
from editorial.engine.editorial_engine import EditorialEngine

class TestEditorialDepartment(unittest.TestCase):
    def test_context_builder(self):
        ctx = EditorialContextBuilder.build_context("AI Agents")
        self.assertIsNotNone(ctx.content_package)
        self.assertIsNotNone(ctx.research_package)
        self.assertEqual(ctx.brand_guidelines["name"], "AVENIQ")

    def test_evidence_mapper(self):
        ctx = EditorialContextBuilder.build_context("AI Agents")
        maps = EvidenceMapper.map_evidence(ctx)
        self.assertGreater(len(maps), 0)
        self.assertIn("68%", maps[0].statement)

    def test_policy_engine(self):
        tracker = IssueTracker()
        scorecard = EditorialScorer.calculate_scorecard(98.0, 94.0, 100.0, 91.0, True, 2.5)
        approval = PolicyEngine.evaluate_approval_policy(scorecard, tracker, 0)
        self.assertEqual(approval.status, "Approved")
        self.assertGreater(approval.confidence_score, 0.90)

    def test_editorial_engine(self):
        engine = EditorialEngine()
        pkg = engine.review_and_approve_content("AI Agents in Enterprise Operations")
        self.assertIsNotNone(pkg)
        self.assertEqual(pkg.topic, "AI Agents in Enterprise Operations")
        self.assertEqual(pkg.approval_decision.status, "Approved")
        self.assertTrue(pkg.publishing_readiness.ready_for_publishing)
        self.assertTrue(pkg.quality_gate.passed)

if __name__ == "__main__":
    unittest.main()
