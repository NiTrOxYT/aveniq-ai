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
        from approval.telegram.sender import global_telegram_sender

        caption = f"🚀 <b>AVENIQ AI Campaign Delivered</b>\n\n<b>Objective:</b> {context.objective}\n\n<b>Execution ID:</b> <code>{context.goal_id}</code>"

        tg_res = {"ok": False, "description": "Not configured"}
        if global_telegram_sender.is_configured:
            tg_res = global_telegram_sender.send_message(caption, parse_mode="HTML")

        msg_id = tg_res.get("result", {}).get("message_id") if tg_res.get("ok") else None

        artifact = {
            "title": f"Publishing Receipt: '{context.objective}'",
            "type": "PublishingReceipt",
            "channel": "Telegram",
            "external_id": f"msg_tg_{msg_id}" if msg_id else "tg_simulated",
            "status": "Delivered" if tg_res.get("ok") else "Skipped / Unconfigured",
            "telegram_response": tg_res
        }

        event_payload = {
            "goal_id": context.goal_id,
            "channel": "Telegram",
            "message_id": msg_id,
            "ok": tg_res.get("ok", False)
        }
        global_event_bus.publish("CampaignPublished", event_payload)

        return WorkerOutput(
            status="success",
            artifacts=[artifact],
            events=[{"name": "CampaignPublished", "payload": event_payload}],
            metrics={"channels_published": 1 if tg_res.get("ok") else 0}
        )


global_publishing_worker = PublishingWorker()
