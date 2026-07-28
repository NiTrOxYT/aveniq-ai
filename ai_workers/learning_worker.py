"""
Learning Worker for AVENIQ AI Workers v4.1.
PipelinePhases: OBSERVE -> THINK -> DECIDE -> ACT -> REFLECT -> LEARN -> EVALUATE.
Capabilities: pattern_learning, knowledge_synthesis.
Implements Evidence-Grounded Learning (requires min_observations >= 2 before promoting to Company Brain).
"""

from typing import Dict, Any, List, Optional
from ai_workers.base_worker import BaseWorker, WorkerContext, WorkerOutput, PipelinePhase, Decision
from runtime.event_bus import global_event_bus
from company_brain import global_company_brain_service


class LearningWorker(BaseWorker):
    def __init__(self):
        super().__init__(
            name="LearningWorker",
            capabilities=["pattern_learning", "knowledge_synthesis"],
            pipeline_phases=[
                PipelinePhase.OBSERVE, PipelinePhase.THINK, PipelinePhase.DECIDE,
                PipelinePhase.ACT, PipelinePhase.REFLECT, PipelinePhase.LEARN, PipelinePhase.EVALUATE
            ]
        )
        self.evidence_ledger: Dict[str, int] = {}  # Tracks observation occurrences
        self.min_observations = 2

    def think(self, context: WorkerContext, observed_memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "strategy": f"Synthesize evidence-grounded learnings for goal '{context.goal_id}'",
            "selected_tools": ["company_brain", "llm"]
        }

    def decide(self, context: WorkerContext, thought: Dict[str, Any]) -> Decision:
        return Decision(
            reasoning=thought["strategy"],
            chosen_strategy="Evidence-Grounded Pattern Synthesis",
            alternative_strategies=["Single Execution Ingestion"],
            selected_tools=thought["selected_tools"],
            expected_outcome="Validated organizational memory update backed by evidence",
            confidence=0.96,
            estimated_cost=0.002,
            estimated_duration_ms=120.0
        )

    def act(self, context: WorkerContext, decision: Decision) -> WorkerOutput:
        topic_key = context.objective.strip().lower()
        self.evidence_ledger[topic_key] = self.evidence_ledger.get(topic_key, 0) + 1
        count = self.evidence_ledger[topic_key]

        knowledge_items = []
        # Enforce Evidence Threshold: Only promote to Company Brain if observations >= min_observations
        if count >= self.min_observations:
            knowledge_item = {
                "title": f"Autonomous Marketing Lesson: {context.objective}",
                "type": "Learning",
                "category": "Workflow",
                "tags": ["autonomous_workflow", "campaign_lesson", "evidence_grounded"],
                "source": "LearningWorker",
                "body": f"Evidence-grounded multi-agent pattern (supported by {count} executions) for: '{context.objective}'."
            }

            global_company_brain_service.ingest_item(knowledge_item)
            knowledge_items.append(knowledge_item)

            event_payload = {"goal_id": context.goal_id, "knowledge_title": knowledge_item["title"], "evidence_count": count}
            global_event_bus.publish("KnowledgeImproved", event_payload)

        return WorkerOutput(
            status="success",
            knowledge=knowledge_items,
            events=[{"name": "KnowledgeImproved", "payload": {"evidence_count": count}}] if knowledge_items else [],
            metrics={"knowledge_added": len(knowledge_items), "evidence_count": count}
        )

    def learn(self, reflection: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Only promote if evidence threshold met
        return None


global_learning_worker = LearningWorker()
