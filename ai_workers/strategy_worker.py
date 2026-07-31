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
        from integrations.llm.providers.hermes import RealHermesProvider
        hermes_provider = RealHermesProvider()
        
        ctx_data = getattr(context, "data", {}) or {}
        research_info = ctx_data.get("research", {}) if isinstance(ctx_data, dict) else {}
        hermes_intel = research_info.get("hermes_intel") or research_info.get("growth_intel", "")

        strategy_prompt = (
            f"You are Hermes Strategy Agent. Based on research intel ({hermes_intel}), create an aggressive competitive strategy plan for company 'AVENIQ AI' for objective: '{context.objective}'.\n"
            f"Define market positioning, channel priority, and campaign angles."
        )
        try:
            strategy_text = hermes_provider.generate(strategy_prompt).text_content
        except Exception:
            strategy_text = f"Hermes Strategy Plan for {context.objective}: Focus on enterprise B2B leadership with zero-mock AI worker orchestration."

        artifact = {
            "title": f"Campaign Strategy (Hermes Agent) for '{context.objective}'",
            "type": "StrategyPlan",
            "channels": ["Telegram", "LinkedIn", "Instagram", "Facebook", "X"],
            "target_audience": "Enterprise CTOs & AI Engineers",
            "strategy_text": strategy_text,
            "hermes_analysis": strategy_text
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
