"""
Unit tests for Approval Department Context, Routing, Telegram Renderer, and Engine.
"""

import unittest
from approval.context.builder import ApprovalContextBuilder
from approval.routing.action_router import ActionRouter, ApprovalStateMachine
from approval.telegram.renderer import TelegramRenderer
from approval.engine.approval_engine import ApprovalEngine

class TestApprovalDepartment(unittest.TestCase):
    def test_context_builder(self):
        ctx = ApprovalContextBuilder.build_context("AI Agents")
        self.assertIsNotNone(ctx.delivery_package)
        self.assertIsNotNone(ctx.editorial_report)

    def test_state_machine_and_router(self):
        self.assertTrue(ApprovalStateMachine.can_transition("PENDING_REVIEW", "IN_REVIEW"))
        self.assertFalse(ApprovalStateMachine.can_transition("PENDING_REVIEW", "ARCHIVED"))

        req, desc = ActionRouter.route_action("Technical", "operator_001", "Add benchmarks")
        self.assertEqual(req.target_department, "Content")

    def test_telegram_renderer(self):
        ctx = ApprovalContextBuilder.build_context("AI Agents")
        markup = TelegramRenderer.render_dashboard(ctx)
        self.assertIn("AVENIQ TODAY'S MARKETING PACKAGE", markup.card_text)
        self.assertGreater(len(markup.inline_keyboard), 0)

    def test_approval_engine(self):
        engine = ApprovalEngine()
        session = engine.create_session("AI Agents in Enterprise Operations")
        self.assertEqual(session.current_state, "PENDING_REVIEW")

        approved_session = engine.process_action(session, "Approve", "operator_001", "Approved")
        self.assertEqual(approved_session.current_state, "APPROVED")
        self.assertTrue(approved_session.quality_gate.passed)

if __name__ == "__main__":
    unittest.main()
