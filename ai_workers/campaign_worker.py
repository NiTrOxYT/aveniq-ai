"""
Campaign Worker for AVENIQ AI Workers v3.1.
PipelinePhases: OBSERVE -> THINK -> DECIDE -> ACT -> EVALUATE.
Capabilities: copywriting, asset_generation, seo.
"""

from typing import Dict, Any, List
from ai_workers.base_worker import BaseWorker, WorkerContext, WorkerOutput, PipelinePhase, Decision
from runtime.event_bus import global_event_bus


class CampaignWorker(BaseWorker):
    def __init__(self):
        super().__init__(
            name="CampaignWorker",
            capabilities=["copywriting", "asset_generation", "seo"],
            pipeline_phases=[
                PipelinePhase.OBSERVE, PipelinePhase.THINK,
                PipelinePhase.DECIDE, PipelinePhase.ACT, PipelinePhase.EVALUATE
            ]
        )

    def think(self, context: WorkerContext, observed_memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "strategy": f"Generate multi-channel copywriting for '{context.objective}' using {len(observed_memories)} retrieved memories.",
            "selected_tools": ["llm"]
        }

    def decide(self, context: WorkerContext, thought: Dict[str, Any]) -> Decision:
        return Decision(
            reasoning=thought["strategy"],
            chosen_strategy="High-converting Copywriting",
            alternative_strategies=["Short Punchy Teaser Copy"],
            selected_tools=thought["selected_tools"],
            expected_outcome="Polished multi-channel copy & hashtag asset specs",
            confidence=0.94,
            estimated_cost=0.008,
            estimated_duration_ms=200.0
        )

    def act(self, context: WorkerContext, decision: Decision) -> WorkerOutput:
        llm_tool = self.tools.get_tool("llm")
        copy = llm_tool.generate(f"Write campaign copy for '{context.objective}'")

        artifact = {
            "title": f"Campaign Copy & Assets: {context.objective}",
            "type": "CampaignAsset",
            "caption": f"🚀 Discover the power of AVENIQ AI Runtime! Objective: {context.objective}.",
            "hashtags": ["#AVENIQ", "#AIWorkforce", "#AutonomousAI"],
            "copy": copy,
            "confidence_score": 0.94
        }

        event_payload = {"goal_id": context.goal_id, "confidence": 0.94}
        global_event_bus.publish("CampaignGenerated", event_payload)

        return WorkerOutput(
            status="success",
            artifacts=[artifact],
            events=[{"name": "CampaignGenerated", "payload": event_payload}],
            metrics={"confidence": 0.94}
        )


global_campaign_worker = CampaignWorker()
