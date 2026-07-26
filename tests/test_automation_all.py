"""
Comprehensive Automation Test Suite for AVENIQ Autonomous Execution Platform.
Tests Session State Machine, DailyRunner, Telegram Briefing Formatter, Graph Solver, Checkpoints, and Emergency Controls.
"""

import unittest
from automation.session.manager import AutomationSessionManager
from automation.session.state import AutomationState
from automation.execution.daily_runner import DailyRunner
from automation.approval.telegram_formatter import TelegramBriefingFormatter
from automation.graph.execution_graph import ExecutionGraphSolver
from automation.recovery.checkpoint import CheckpointManager, RecoveryEngine
from automation.queue.notification_queue import NotificationQueue
from automation.audit.audit_log import global_emergency_controls, global_audit_logger

class TestAutomationPlatform(unittest.TestCase):
    def test_session_state_machine(self):
        mgr = AutomationSessionManager()
        session = mgr.create_session("AI Agents")
        self.assertEqual(session.current_state, AutomationState.CREATED)

        self.assertTrue(mgr.transition_state(session.session_id, AutomationState.RUNNING))
        self.assertTrue(mgr.transition_state(session.session_id, AutomationState.WAITING_FOR_APPROVAL))
        self.assertFalse(mgr.transition_state(session.session_id, AutomationState.CREATED))  # Invalid transition

    def test_graph_execution_solver(self):
        img_path = ExecutionGraphSolver.solve_path("Generate New Image")
        self.assertIn("creative", img_path)
        self.assertIn("editorial", img_path)
        self.assertIn("delivery", img_path)

        tech_path = ExecutionGraphSolver.solve_path("More Technical")
        self.assertIn("content", tech_path)
        self.assertIn("editorial", tech_path)

    def test_daily_runner_and_approval(self):
        runner = DailyRunner()
        res = runner.run_daily_cycle("AI Agents in Enterprise Operations")
        self.assertTrue(res["success"])
        self.assertEqual(res["state"], "WAITING_FOR_APPROVAL")
        self.assertIn("AVENIQ AI DAILY MARKETING BRIEFING", res["briefing"])

        # Process Approve Decision
        app_res = runner.process_human_decision(res["session_id"], "Approve")
        self.assertTrue(app_res["success"])
        self.assertEqual(app_res["state"], "COMPLETED")

    def test_checkpoints_and_recovery(self):
        mgr = AutomationSessionManager()
        chk_mgr = CheckpointManager()
        rec_eng = RecoveryEngine(chk_mgr)

        session = mgr.create_session("Test Checkpoint")
        chk_file = chk_mgr.save_checkpoint(session, "test_step", {"data": 123})
        self.assertTrue(chk_file.endswith(".json"))

        resumed = rec_eng.resume_session(session.session_id)
        self.assertTrue(resumed["resumed"])
        self.assertEqual(resumed["last_step"], "test_step")

    def test_notification_queue(self):
        queue = NotificationQueue()
        msg = queue.enqueue("telegram", "@reviewer", "Daily Briefing", "Campaign ready for review")
        self.assertEqual(msg.status, "QUEUED")
        processed = queue.process_all(lambda m: True)
        self.assertEqual(processed, 1)

    def test_emergency_controls(self):
        session_id = "aut_sess_test"
        global_emergency_controls.pause(session_id)
        self.assertTrue(global_emergency_controls.is_paused(session_id))
        global_emergency_controls.resume(session_id)
        self.assertFalse(global_emergency_controls.is_paused(session_id))

if __name__ == "__main__":
    unittest.main()
