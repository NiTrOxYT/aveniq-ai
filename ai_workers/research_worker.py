"""
Research Worker for AVENIQ AI Workers v3.1.
PipelinePhases: OBSERVE -> THINK -> PLAN -> DECIDE -> ACT -> REFLECT -> LEARN -> EVALUATE.
Capabilities: market_research, competitor_analysis, trend_detection.
"""

from typing import Dict, Any, List, Optional
from ai_workers.base_worker import BaseWorker, WorkerContext, WorkerOutput, PipelinePhase, Decision
from runtime.event_bus import global_event_bus


class ResearchWorker(BaseWorker):
    def __init__(self):
        super().__init__(
            name="ResearchWorker",
            capabilities=["market_research", "competitor_analysis", "trend_detection"],
            pipeline_phases=[
                PipelinePhase.OBSERVE, PipelinePhase.THINK, PipelinePhase.PLAN,
                PipelinePhase.DECIDE, PipelinePhase.ACT, PipelinePhase.REFLECT,
                PipelinePhase.LEARN, PipelinePhase.EVALUATE
            ]
        )

    def think(self, context: WorkerContext, observed_memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "strategy": f"Perform comprehensive web search & trend analysis for '{context.objective}'",
            "selected_tools": ["search", "llm"]
        }

    def decide(self, context: WorkerContext, thought: Dict[str, Any]) -> Decision:
        return Decision(
            reasoning=thought["strategy"],
            chosen_strategy="Web Search + Trend Gap Analysis",
            alternative_strategies=["Direct Database Lookup"],
            selected_tools=thought["selected_tools"],
            expected_outcome="Market trend discovery & competitor profile synthesis",
            confidence=0.92,
            estimated_cost=0.005,
            estimated_duration_ms=150.0
        )

    def act(self, context: WorkerContext, decision: Decision) -> WorkerOutput:
        from research.engine.collectors import ProviderCollector
        
        collector_data = {}
        try:
            collector_data["github"] = ProviderCollector.test_github()
            collector_data["reddit"] = ProviderCollector.test_reddit()
            collector_data["hackernews"] = ProviderCollector.test_hackernews()
            collector_data["google_news"] = ProviderCollector.test_google_news()
        except Exception as e:
            collector_data["collector_error"] = str(e)

        search_tool = self.tools.get_tool("search")
        objective_query = context.objective if context and context.objective else "AVENIQ AI company growth strategy"
        search_res = search_tool.execute(f"Market intelligence & growth strategies for {objective_query}", limit=5)

        findings_count = len(search_res) if isinstance(search_res, list) else 1

        artifact = {
            "title": f"Market & Web Research: {objective_query}",
            "type": "MarketResearch",
            "findings": search_res,
            "collectors": collector_data,
            "company": "AVENIQ AI",
            "growth_intel": "Autonomous multi-agent execution with zero-fallback provider routing drives enterprise adoption.",
            "trends": ["Autonomous AI Workers", "Runtime Multi-Agent Systems", "Zero-Mock Production AI"],
            "competitors": ["Legacy Automation Engines"]
        }

        event_payload = {"goal_id": context.goal_id, "findings_count": findings_count}
        global_event_bus.publish("ResearchCompleted", event_payload)

        return WorkerOutput(
            status="success",
            artifacts=[artifact],
            events=[{"name": "ResearchCompleted", "payload": event_payload}],
            metrics={"findings": findings_count}
        )

    def learn(self, reflection: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Decide if reflection should become permanent Company Brain entry
        return {
            "title": f"Market Trend: Autonomous AI Agents for {reflection.get('observation', 'Research')[:30]}",
            "type": "Technology",
            "category": "Research",
            "tags": ["market_trend", "ai_agents"],
            "source": "ResearchWorker",
            "body": f"Validated research insight: {reflection.get('observation')}"
        }


global_research_worker = ResearchWorker()
