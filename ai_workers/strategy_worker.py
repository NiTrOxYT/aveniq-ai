"""
Strategy Worker for AVENIQ AI Workers v2.1.
Capabilities: strategy_planning, opportunity_analysis.
Consumes research signals, prioritizes opportunities, produces StrategyCreated.
"""

from typing import Dict, Any, List
from ai_workers.base_worker import BaseWorker, WorkerContext, WorkerOutput
from runtime.event_bus import global_event_bus


class StrategyWorker(BaseWorker):
    def __init__(self):
        super().__init__(
            name="StrategyWorker",
            capabilities=["strategy_planning", "opportunity_analysis"]
        )

    def execute(self, context: WorkerContext) -> WorkerOutput:
        self.state = "busy"
        llm_tool = self.tools.get_tool("llm")
        strategy_text = llm_tool.generate(f"Create marketing campaign strategy for '{context.objective}'")

        artifact = {
            "title": f"Campaign Strategy for '{context.objective}'",
            "type": "StrategyPlan",
            "channels": ["Telegram", "LinkedIn", "Twitter/X"],
            "target_audience": "Enterprise CTOs & AI Engineers",
            "strategy_text": strategy_text
        }

        event_payload = {"goal_id": context.goal_id, "channels": ["Telegram", "LinkedIn"]}
        global_event_bus.publish("StrategyCreated", event_payload)

        self.state = "idle"
        return WorkerOutput(
            status="success",
            artifacts=[artifact],
            events=[{"name": "StrategyCreated", "payload": event_payload}],
            metrics={"channels_planned": 3}
        )


global_strategy_worker = StrategyWorker()
