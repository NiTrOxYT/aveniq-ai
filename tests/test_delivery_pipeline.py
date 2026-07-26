"""
Unit Test Suite for Phase 16 — Complete Daily Delivery Pipeline & Governance Engine.
Tests Imagen Provider, TelegramSender, Live Dashboard API, Versioning, DAG Partial Regeneration,
Reasoning, Timeline, Citations, Campaign Scorer, and DailyRunner.
"""

import unittest
import os
import shutil
from image_generation.providers.gemini_image import GeminiImageProvider
from approval.telegram.sender import TelegramSender
from automation.reasoning.reasoning_report import ReasoningReportGenerator
from automation.storage.version_manager import CampaignVersionManager
from automation.execution.dependency_graph import DependencyGraphSolver
from automation.audit.execution_timeline import ExecutionTimelineTracker
from brain.provenance.citation_manager import CitationManager
from automation.scoring.campaign_scorer import CampaignScorer
from automation.execution.daily_runner import DailyRunner

class TestDeliveryPipeline(unittest.TestCase):
    def setUp(self):
        self.test_storage = "storage/test_campaigns"
        os.makedirs(self.test_storage, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_storage):
            shutil.rmtree(self.test_storage, ignore_errors=True)

    def test_gemini_image_provider(self):
        provider = GeminiImageProvider()
        provider.storage_dir = self.test_storage
        provider.initialize()
        res = provider.generate_image("Modern AI Cloud Architecture", 1024, 1024)
        self.assertTrue(res.success)
        self.assertTrue(os.path.exists(res.image_url_or_path))
        self.assertEqual(res.provider, "gemini_image")
        self.assertIn("image_id", res.metadata)

    def test_telegram_sender(self):
        sender = TelegramSender(bot_token="test_token_123", chat_id="123456")
        self.assertTrue(sender.is_configured)
        res = sender.send_message("Test briefing message")
        self.assertIn("ok", res)

    def test_reasoning_report(self):
        rep = ReasoningReportGenerator.generate_report("sess_001", "cmp_001", "AI Operations")
        self.assertEqual(rep["session_id"], "sess_001")
        self.assertIn("market_signals_analyzed", rep)
        self.assertIn("risk_assessment", rep)

    def test_version_manager(self):
        mgr = CampaignVersionManager(base_storage_dir=self.test_storage)
        artifacts_v1 = {"summary.md": "Version 1 Summary", "strategy.json": {"goal": "Lead Gen"}}
        v1 = mgr.create_version("cmp_100", artifacts_v1, trigger_action="INITIAL_GENERATION")
        self.assertEqual(v1["version_id"], "v1")

        artifacts_v2 = {"summary.md": "Version 2 Summary"}
        v2 = mgr.create_version("cmp_100", artifacts_v2, parent_version="v1", trigger_action="action_Shorter")
        self.assertEqual(v2["version_id"], "v2")

        versions = mgr.list_versions("cmp_100")
        self.assertEqual(versions, ["v1", "v2"])

    def test_dependency_graph_solver(self):
        solver = DependencyGraphSolver()
        nodes_shorter = solver.resolve_affected_nodes("action_Shorter")
        self.assertIn("content", nodes_shorter)
        self.assertIn("seo", nodes_shorter)

        nodes_hero = solver.resolve_affected_nodes("action_RegenerateHero")
        self.assertEqual(nodes_hero, ["images", "thumbnails"])

    def test_execution_timeline(self):
        tracker = ExecutionTimelineTracker(log_path=os.path.join(self.test_storage, "timeline.json"))
        evt = tracker.record_event("sess_01", "cmp_01", "08:00 Market Intelligence")
        self.assertEqual(evt["session_id"], "sess_01")
        timeline = tracker.get_timeline("sess_01")
        self.assertEqual(len(timeline), 1)

    def test_citation_manager(self):
        cit = CitationManager.generate_citations("sess_01", "cmp_01")
        self.assertIn("rag_documents", cit)
        self.assertIn("provenance_chain", cit)

    def test_campaign_scorer(self):
        report = CampaignScorer.score_campaign({"test": "package"})
        self.assertGreater(report["overall_score"], 80.0)
        self.assertFalse(report["requires_flagged_review"])

    def test_daily_runner_pipeline(self):
        runner = DailyRunner()
        res = runner.run_daily_cycle("Autonomous Marketing Pipeline Test")
        self.assertTrue(res["success"])
        self.assertIn("session_id", res)
        self.assertIn("reasoning", res)
        self.assertIn("version_id", res)

        dec_res = runner.process_human_decision(res["session_id"], "action_Shorter")
        self.assertTrue(dec_res["success"])
        self.assertIn("affected_nodes", dec_res)

if __name__ == "__main__":
    unittest.main()
