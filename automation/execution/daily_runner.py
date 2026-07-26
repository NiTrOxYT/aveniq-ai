"""
Autonomous Daily Runner for AVENIQ AI.
Executes master Workflow Engine, manages session checkpoints, enqueues notifications, and processes human approval decisions.
"""

from typing import Dict, Any, Optional
from workflow.engine.orchestrator import Orchestrator
from automation.session.manager import AutomationSessionManager
from automation.session.state import AutomationState
from automation.recovery.checkpoint import CheckpointManager
from automation.audit.audit_log import global_audit_logger
from automation.approval.telegram_formatter import TelegramBriefingFormatter, global_approval_tracker
from automation.graph.execution_graph import ExecutionGraphSolver

class DailyRunner:
    def __init__(self):
        self.orchestrator = Orchestrator()
        self.session_mgr = AutomationSessionManager()
        self.chk_mgr = CheckpointManager()

    def run_daily_cycle(self, campaign_topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        # 1. Create Session
        session = self.session_mgr.create_session(campaign_topic)
        self.session_mgr.transition_state(session.session_id, AutomationState.RUNNING)
        global_audit_logger.log(session.session_id, "DAILY_RUN_STARTED", details={"topic": campaign_topic})

        # 2. Execute Master Workflow
        result = self.orchestrator.execute_workflow(execution_id=session.session_id)
        session.workflow_execution_id = session.session_id

        if not result.success:
            self.session_mgr.transition_state(session.session_id, AutomationState.FAILED)
            global_audit_logger.log(session.session_id, "WORKFLOW_FAILED", details={"errors": result.errors})
            return {
                "session_id": session.session_id,
                "success": False,
                "state": session.current_state.value,
                "errors": result.errors
            }

        # 3. Save Checkpoint 1
        self.chk_mgr.save_checkpoint(session, "workflow_completed", {"packages_count": len(result.packages)})

        # 4. Generate Telegram Briefing & Transition State
        briefing_text = TelegramBriefingFormatter.format_briefing(result.packages.get("delivery", {}))
        self.session_mgr.transition_state(session.session_id, AutomationState.WAITING_FOR_APPROVAL)
        
        # Save Checkpoint 2
        self.chk_mgr.save_checkpoint(session, "waiting_for_approval", {"briefing": briefing_text})
        global_audit_logger.log(session.session_id, "WAITING_FOR_APPROVAL", details={"briefing_lines": len(briefing_text.splitlines())})

        return {
            "session_id": session.session_id,
            "success": True,
            "state": session.current_state.value,
            "briefing": briefing_text,
            "duration": result.metrics.get("total_duration", 0.0),
            "packages_count": len(result.packages)
        }

    def process_human_decision(self, session_id: str, action: str, reviewer: str = "Human Operator", feedback: str = "") -> Dict[str, Any]:
        session = self.session_mgr.get_session(session_id)
        if not session:
            return {"success": False, "error": f"Session '{session_id}' not found"}

        global_approval_tracker.record_decision(session_id, action, reviewer, feedback)
        global_audit_logger.log(session_id, f"HUMAN_DECISION_{action.upper()}", actor=reviewer, details={"feedback": feedback})

        if action == "Approve":
            self.session_mgr.transition_state(session_id, AutomationState.APPROVED)
            session.archived = True
            session.learning_complete = True
            self.session_mgr.transition_state(session_id, AutomationState.COMPLETED)
            self.chk_mgr.save_checkpoint(session, "archived_and_learned")
            return {"session_id": session_id, "success": True, "action": action, "state": session.current_state.value}
        elif action in ["Reject", "Skip Today"]:
            self.session_mgr.transition_state(session_id, AutomationState.REJECTED)
            self.session_mgr.transition_state(session_id, AutomationState.COMPLETED)
            self.chk_mgr.save_checkpoint(session, "rejected")
            return {"session_id": session_id, "success": True, "action": action, "state": session.current_state.value}
        else:
            # Partial Regeneration
            path = ExecutionGraphSolver.solve_path(action)
            self.session_mgr.transition_state(session_id, AutomationState.REGENERATING)
            session.regenerated_components.extend(path)
            self.session_mgr.transition_state(session_id, AutomationState.WAITING_FOR_APPROVAL)
            self.chk_mgr.save_checkpoint(session, "regenerated", {"path": path})
            return {
                "session_id": session_id,
                "success": True,
                "action": action,
                "state": session.current_state.value,
                "regeneration_path": path
            }
