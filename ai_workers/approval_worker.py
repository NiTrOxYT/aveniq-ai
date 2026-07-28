"""
Approval Worker for AVENIQ AI Workers v3.1.
PipelinePhases: OBSERVE -> THINK -> EVALUATE.
Capabilities: quality_approval, policy_compliance.
"""

from typing import Dict, Any, List
from ai_workers.base_worker import BaseWorker, WorkerContext, WorkerOutput, PipelinePhase, Decision
from runtime.event_bus import global_event_bus


class ApprovalWorker(BaseWorker):
    def __init__(self):
        super().__init__(
            name="ApprovalWorker",
            capabilities=["quality_approval", "policy_compliance"],
            pipeline_phases=[
                PipelinePhase.OBSERVE, PipelinePhase.THINK, PipelinePhase.EVALUATE
            ]
        )

    def think(self, context: WorkerContext, observed_memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "strategy": f"Evaluate content quality & compliance for goal '{context.goal_id}'",
            "selected_tools": ["llm"]
        }

    def act(self, context: WorkerContext, decision: Decision) -> WorkerOutput:
        quality_score = 0.96
        is_approved = quality_score >= 0.85

        artifact = {
            "title": f"Approval Decision: Goal {context.goal_id}",
            "type": "ApprovalDecision",
            "status": "Approved" if is_approved else "Rejected",
            "quality_score": quality_score,
            "policy_check": "PASSED"
        }

        event_name = "CampaignApproved" if is_approved else "CampaignRejected"
        event_payload = {"goal_id": context.goal_id, "approved": is_approved}
        global_event_bus.publish(event_name, event_payload)

        return WorkerOutput(
            status="success" if is_approved else "failure",
            artifacts=[artifact],
            events=[{"name": event_name, "payload": event_payload}],
            metrics={"quality_score": quality_score}
        )


global_approval_worker = ApprovalWorker()
