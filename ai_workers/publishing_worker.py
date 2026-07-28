"""
Publishing Worker for AVENIQ AI Workers v3.1.
PipelinePhases: OBSERVE -> ACT.
Capabilities: platform_publishing, delivery_tracking.
"""

from typing import Dict, Any, List
from ai_workers.base_worker import BaseWorker, WorkerContext, WorkerOutput, PipelinePhase, Decision
from runtime.event_bus import global_event_bus


class PublishingWorker(BaseWorker):
    def __init__(self):
        super().__init__(
            name="PublishingWorker",
            capabilities=["platform_publishing", "delivery_tracking"],
            pipeline_phases=[
                PipelinePhase.OBSERVE, PipelinePhase.ACT
            ]
        )

    def act(self, context: WorkerContext, decision: Decision) -> WorkerOutput:
        pub_tool = self.tools.get_tool("publishing")
        pub_res = pub_tool.publish("Telegram", {"title": context.objective})

        artifact = {
            "title": f"Publishing Receipt: '{context.objective}'",
            "type": "PublishingReceipt",
            "channel": "Telegram",
            "external_id": pub_res.get("external_id"),
            "status": "Published"
        }

        event_payload = {"goal_id": context.goal_id, "channel": "Telegram", "external_id": pub_res.get("external_id")}
        global_event_bus.publish("CampaignPublished", event_payload)

        return WorkerOutput(
            status="success",
            artifacts=[artifact],
            events=[{"name": "CampaignPublished", "payload": event_payload}],
            metrics={"channels_published": 1}
        )


global_publishing_worker = PublishingWorker()
