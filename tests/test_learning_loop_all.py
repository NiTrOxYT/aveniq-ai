"""
Comprehensive Test Suite for Closed-Loop Learning Platform (Phase 11).
Tests Events, Bus, Extractors, Patterns, Simulation, Proposal Manager, Governance, and Readiness Engine.
"""

import unittest
from learning.models.proposal import LearningEvent, KnowledgeProposal, ProposalCategory, ProposalState
from learning.bus.event_bus import global_learning_event_bus
from learning.extractors.extractors import PositiveKnowledgeExtractor, NegativeKnowledgeExtractor
from learning.patterns.pattern_recognizer import CrossCampaignPatternRecognizer, ImpactSimulator
from learning.proposals.proposal_manager import ProposalManager
from learning.monitoring.readiness import LearningReadinessEngine, OrganizationalMemoryTimeline

class TestClosedLoopLearningPlatform(unittest.TestCase):
    def test_learning_event_bus(self):
        received = []
        global_learning_event_bus.subscribe(lambda e: received.append(e))

        evt = LearningEvent(
            event_id="evt_01",
            workspace_id="ws_01",
            execution_id="exc_01",
            campaign_id="cmp_01",
            department="content",
            event_type="CONTENT_APPROVED"
        )
        global_learning_event_bus.publish_event(evt)
        self.assertGreater(len(received), 0)

    def test_extractors(self):
        evt1 = LearningEvent(event_id="e1", workspace_id="w1", execution_id="ex1", campaign_id="c1", department="content", event_type="CONTENT_APPROVED")
        evt2 = LearningEvent(event_id="e2", workspace_id="w1", execution_id="ex2", campaign_id="c2", department="creative", event_type="IMAGE_REGENERATED")

        pos = PositiveKnowledgeExtractor.extract_winning_copy([evt1])
        self.assertEqual(len(pos), 1)

        neg = NegativeKnowledgeExtractor.extract_negative_lessons([evt2])
        self.assertEqual(len(neg), 1)

    def test_pattern_recognizer_and_simulator(self):
        patterns = CrossCampaignPatternRecognizer.detect_patterns([])
        self.assertGreater(len(patterns), 0)

        sim = ImpactSimulator.simulate_proposal_impact(patterns[0]["pattern_id"])
        self.assertGreater(sim.expected_ctr_change, 0.0)

    def test_proposal_manager_and_governance(self):
        mgr = ProposalManager()
        prop = mgr.create_proposal(
            title="LinkedIn Technical Graphics",
            description="Technical diagrams perform best.",
            proposed_change="Include diagrams.",
            category=ProposalCategory.CONTENT
        )
        self.assertEqual(prop.state, ProposalState.PROPOSED)

        approved = mgr.approve_proposal(prop.proposal_id, user="Operations Lead")
        self.assertEqual(approved.state, ProposalState.APPROVED)
        self.assertEqual(approved.approving_user, "Operations Lead")

    def test_readiness_score_engine(self):
        readiness = LearningReadinessEngine.calculate_readiness_score()
        self.assertGreaterEqual(readiness["readiness_score"], 80.0)
        self.assertLessEqual(readiness["readiness_score"], 100.0)

    def test_memory_timeline(self):
        timeline = OrganizationalMemoryTimeline.get_timeline()
        self.assertGreater(len(timeline), 0)

if __name__ == "__main__":
    unittest.main()
