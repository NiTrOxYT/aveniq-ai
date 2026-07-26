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
from approval.telegram.sender import global_telegram_sender
from automation.reasoning.reasoning_report import ReasoningReportGenerator
from automation.storage.version_manager import global_version_manager
from automation.execution.dependency_graph import global_dependency_solver
from automation.audit.execution_timeline import global_timeline_tracker
from brain.provenance.citation_manager import global_citation_manager
from automation.scoring.campaign_scorer import global_campaign_scorer

class DailyRunner:
    def __init__(self):
        self.orchestrator = Orchestrator()
        self.session_mgr = AutomationSessionManager()
        self.chk_mgr = CheckpointManager()

    def run_daily_cycle(self, campaign_topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        # 1. Create Session & Log Timeline
        session = self.session_mgr.create_session(campaign_topic)
        campaign_id = f"cmp_{session.session_id}"
        self.session_mgr.transition_state(session.session_id, AutomationState.RUNNING)
        global_audit_logger.log(session.session_id, "DAILY_RUN_STARTED", details={"topic": campaign_topic})
        global_timeline_tracker.record_event(session.session_id, campaign_id, "08:00:00 Market Intelligence Started")

        # 2. Execute Master Workflow
        result = self.orchestrator.execute_workflow(execution_id=session.session_id)
        session.workflow_execution_id = session.session_id

        if not result.success:
            self.session_mgr.transition_state(session.session_id, AutomationState.FAILED)
            global_audit_logger.log(session.session_id, "WORKFLOW_FAILED", details={"errors": result.errors})
            global_timeline_tracker.record_event(session.session_id, campaign_id, "08:01:00 Workflow Failed", status="FAILED")
            return {
                "session_id": session.session_id,
                "success": False,
                "state": session.current_state.value,
                "errors": result.errors
            }

        global_timeline_tracker.record_event(session.session_id, campaign_id, "08:01:30 Workflow Completed", duration_sec=result.metrics.get("total_duration", 0.12))

        # 3. Generate Reasoning Report, Citations, and Quality Scoring
        reasoning = ReasoningReportGenerator.generate_report(session.session_id, campaign_id, campaign_topic)
        citations = global_citation_manager.generate_citations(session.session_id, campaign_id)
        quality = global_campaign_scorer.score_campaign(result.packages)

        # 4. Save Immutable Campaign Version v1
        version_artifacts = {
            "strategy.json": result.packages.get("strategy", {}),
            "research.json": result.packages.get("research", {}),
            "captions.json": result.packages.get("content", {}),
            "hashtags.json": {"hashtags": ["#AI", "#SaaS", "#Automation", "#AVENIQ"]},
            "seo.json": {"title": f"AVENIQ AI: {campaign_topic}", "keywords": ["AI", "Enterprise", "Automation"]},
            "summary.md": f"# Daily Campaign Summary\nTopic: {campaign_topic}\nQuality Score: {quality['overall_score']}/100",
            "reasoning.json": reasoning,
            "citations.json": citations,
            "quality_report.json": quality,
            "execution.json": {"duration": result.metrics.get("total_duration", 0.12), "status": "SUCCESS"}
        }
        ver_res = global_version_manager.create_version(campaign_id, version_artifacts, trigger_action="INITIAL_GENERATION")

        # 5. Generate Telegram Briefing & Dispatch
        briefing_text = TelegramBriefingFormatter.format_briefing(result.packages.get("delivery", {}))
        
        # Dispatch to real Telegram API if configured
        if global_telegram_sender.is_configured:
            global_telegram_sender.send_message(briefing_text)
            global_timeline_tracker.record_event(session.session_id, campaign_id, "08:02:45 Telegram Delivered")
            self.session_mgr.transition_state(session.session_id, AutomationState.SENT_TO_TELEGRAM)

        self.session_mgr.transition_state(session.session_id, AutomationState.WAITING_FOR_APPROVAL)
        global_timeline_tracker.record_event(session.session_id, campaign_id, "08:03:00 Waiting for Human Approval")
        
        # Checkpoints
        self.chk_mgr.save_checkpoint(session, "waiting_for_approval", {"briefing": briefing_text, "version": ver_res["version_id"]})
        global_audit_logger.log(session.session_id, "WAITING_FOR_APPROVAL", details={"version": ver_res["version_id"]})

        return {
            "session_id": session.session_id,
            "campaign_id": campaign_id,
            "version_id": ver_res["version_id"],
            "success": True,
            "state": session.current_state.value,
            "briefing": briefing_text,
            "reasoning": reasoning,
            "citations": citations,
            "quality_score": quality["overall_score"],
            "duration": result.metrics.get("total_duration", 0.0),
            "packages_count": len(result.packages)
        }

    def process_human_decision(self, session_id: str, action: str, reviewer: str = "Human Operator", feedback: str = "") -> Dict[str, Any]:
        session = self.session_mgr.get_session(session_id)
        if not session:
            return {"success": False, "error": f"Session '{session_id}' not found"}

        campaign_id = f"cmp_{session_id}"
        global_approval_tracker.record_decision(session_id, action, reviewer, feedback)
        global_audit_logger.log(session_id, f"HUMAN_DECISION_{action.upper()}", actor=reviewer, details={"feedback": feedback})

        if action == "Approve":
            self.session_mgr.transition_state(session_id, AutomationState.APPROVED)
            session.archived = True
            session.learning_complete = True
            self.session_mgr.transition_state(session_id, AutomationState.COMPLETED)
            global_timeline_tracker.record_event(session_id, campaign_id, "Campaign Approved & Completed")
            self.chk_mgr.save_checkpoint(session, "archived_and_learned")
            return {"session_id": session_id, "success": True, "action": action, "state": session.current_state.value}
        elif action in ["Reject", "Skip Today"]:
            self.session_mgr.transition_state(session_id, AutomationState.REJECTED)
            self.session_mgr.transition_state(session_id, AutomationState.COMPLETED)
            global_timeline_tracker.record_event(session_id, campaign_id, "Campaign Rejected")
            self.chk_mgr.save_checkpoint(session, "rejected")
            return {"session_id": session_id, "success": True, "action": action, "state": session.current_state.value}
        else:
            # DAG Dependency-Based Partial Regeneration
            affected_nodes = global_dependency_solver.resolve_affected_nodes(action)
            self.session_mgr.transition_state(session_id, AutomationState.REGENERATING)
            session.regenerated_components.extend(affected_nodes)
            
            # Create new version in campaign repository (e.g., v2, v3)
            version_artifacts = {
                "summary.md": f"# Regenerated Campaign ({action})\nAffected Nodes: {', '.join(affected_nodes)}"
            }
            ver_res = global_version_manager.create_version(campaign_id, version_artifacts, trigger_action=action)
            
            self.session_mgr.transition_state(session_id, AutomationState.WAITING_FOR_APPROVAL)
            global_timeline_tracker.record_event(session_id, campaign_id, f"Partial Regeneration ({action})", details={"affected": affected_nodes, "version": ver_res["version_id"]})
            self.chk_mgr.save_checkpoint(session, "regenerated", {"affected": affected_nodes, "version": ver_res["version_id"]})
            
            return {
                "session_id": session_id,
                "campaign_id": campaign_id,
                "new_version_id": ver_res["version_id"],
                "success": True,
                "action": action,
                "state": session.current_state.value,
                "affected_nodes": affected_nodes
            }

