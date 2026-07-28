"""
Adaptive Cognitive Worker Framework & Data Contracts for AVENIQ AI Runtime v3.1.
Defines PipelinePhase, Decision, UncertaintyModel, phase-selective execution engine, and self-revision loop.
"""

import time
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Set
from ai_workers.tools import global_tool_registry


class PipelinePhase(str, Enum):
    OBSERVE = "OBSERVE"
    THINK = "THINK"
    PLAN = "PLAN"
    DECIDE = "DECIDE"
    ACT = "ACT"
    REFLECT = "REFLECT"
    LEARN = "LEARN"
    EVALUATE = "EVALUATE"


@dataclass
class UncertaintyModel:
    overall: float = 0.95
    reasoning: float = 0.95
    execution: float = 0.95
    uncertainty: float = 0.05
    missing_information: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    recommended_next_action: str = "proceed"
    need_human_review: bool = False


@dataclass
class Decision:
    reasoning: str
    chosen_strategy: str
    alternative_strategies: List[str] = field(default_factory=list)
    selected_tools: List[str] = field(default_factory=list)
    expected_outcome: str = "Task Completion"
    confidence: float = 0.95
    estimated_cost: float = 0.001
    estimated_duration_ms: float = 100.0


@dataclass
class WorkerContext:
    goal_id: str
    task_id: str
    objective: str
    task_description: str
    previous_outputs: List[Dict[str, Any]] = field(default_factory=list)
    goal_memory: Dict[str, Any] = field(default_factory=dict)
    runtime_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkerOutput:
    status: str  # success, failure, pending_approval, blocked
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    knowledge: List[Dict[str, Any]] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    next_tasks: List[Dict[str, Any]] = field(default_factory=list)
    decision: Optional[Decision] = None
    uncertainty: Optional[UncertaintyModel] = None
    revision_count: int = 0
    error_message: Optional[str] = None


class BaseWorker:
    def __init__(self, name: str, capabilities: List[str], pipeline_phases: Optional[List[PipelinePhase]] = None):
        self.name = name
        self.capabilities: Set[str] = set(capabilities)
        self.pipeline_phases: List[PipelinePhase] = pipeline_phases or [
            PipelinePhase.OBSERVE, PipelinePhase.THINK, PipelinePhase.DECIDE,
            PipelinePhase.ACT, PipelinePhase.REFLECT, PipelinePhase.EVALUATE
        ]
        self.state = "idle"  # idle, busy, error, disabled
        self.task_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.total_execution_ms = 0.0
        self.memory: Dict[str, Any] = {}  # Worker Memory (Transient Context)
        self.tools = global_tool_registry
        self.max_revisions = 2

    def initialize(self, kernel: Any):
        self.state = "idle"

    def health(self) -> Dict[str, Any]:
        success_rate = round(self.success_count / max(self.task_count, 1), 2)
        avg_time_ms = round(self.total_execution_ms / max(self.task_count, 1), 2)
        return {
            "name": self.name,
            "capabilities": list(self.capabilities),
            "pipeline_phases": [p.value if isinstance(p, PipelinePhase) else p for p in self.pipeline_phases],
            "state": self.state,
            "tasks_completed": self.success_count,
            "tasks_failed": self.failure_count,
            "success_rate": success_rate,
            "avg_time_ms": avg_time_ms
        }

    def can_handle(self, capability: str) -> bool:
        return capability in self.capabilities

    def observe(self, context: WorkerContext) -> List[Dict[str, Any]]:
        """Phase 1: Pre-action retrieval from Company Brain."""
        try:
            from company_brain import global_company_brain_service
            memories = global_company_brain_service.search(query=context.objective, limit=5)
            return memories
        except Exception:
            return []

    def think(self, context: WorkerContext, observed_memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Phase 2: Reasoning and strategy formulation."""
        return {
            "strategy": f"Execute capability for '{context.objective}' leveraging {len(observed_memories)} prior memories.",
            "selected_tools": ["search", "llm"]
        }

    def plan_steps(self, context: WorkerContext, thought: Dict[str, Any]) -> List[str]:
        """Phase 3: Multi-step action plan."""
        return [f"Step 1: Retrieve context for {context.objective}", "Step 2: Synthesize output", "Step 3: Evaluate quality"]

    def decide(self, context: WorkerContext, thought: Dict[str, Any]) -> Decision:
        """Phase 4: Generate explicit Decision object before action."""
        return Decision(
            reasoning=thought.get("strategy", "Standard execution"),
            chosen_strategy="Primary Capability Path",
            alternative_strategies=["Fallback Strategy Path"],
            selected_tools=thought.get("selected_tools", ["llm"]),
            expected_outcome=f"Completed {context.task_description}",
            confidence=0.95
        )

    def act(self, context: WorkerContext, decision: Decision) -> WorkerOutput:
        """Phase 5: Execution using selected tools."""
        raise NotImplementedError("Subclasses must implement act().")

    def reflect(self, result: WorkerOutput) -> Optional[Dict[str, Any]]:
        """Phase 6: Temporary observation synthesis."""
        if result.status == "success":
            return {
                "worker": self.name,
                "timestamp": time.time(),
                "observation": f"Worker '{self.name}' completed task with confidence {result.decision.confidence if result.decision else 0.95}"
            }
        return None

    def learn(self, reflection: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Phase 7: Evaluate if reflection is worthy of long-term Company Brain storage."""
        return None

    def evaluate_output(self, output: WorkerOutput) -> UncertaintyModel:
        """Phase 8: Self-evaluation and uncertainty modeling."""
        conf = output.decision.confidence if output.decision else 0.90
        return UncertaintyModel(
            overall=conf,
            reasoning=conf,
            execution=conf,
            uncertainty=round(1.0 - conf, 2),
            need_human_review=(conf < 0.70)
        )

    def execute(self, context: WorkerContext) -> WorkerOutput:
        """Phase-selective Adaptive Cognitive Pipeline Execution with Self-Revision Loop."""
        self.state = "busy"
        start_time = time.time()
        revision = 0

        while revision <= self.max_revisions:
            observed = []
            if PipelinePhase.OBSERVE in self.pipeline_phases:
                observed = self.observe(context)

            thought = {}
            if PipelinePhase.THINK in self.pipeline_phases:
                thought = self.think(context, observed)

            steps = []
            if PipelinePhase.PLAN in self.pipeline_phases:
                steps = self.plan_steps(context, thought)

            decision = Decision(reasoning="Direct Act Phase", chosen_strategy="Direct", confidence=0.95)
            if PipelinePhase.DECIDE in self.pipeline_phases:
                decision = self.decide(context, thought)

            # ACT phase
            output = self.act(context, decision)
            output.decision = decision
            output.revision_count = revision

            # REFLECT phase
            reflection = None
            if PipelinePhase.REFLECT in self.pipeline_phases:
                reflection = self.reflect(output)

            # LEARN phase
            if PipelinePhase.LEARN in self.pipeline_phases and reflection:
                learned_item = self.learn(reflection)
                if learned_item:
                    output.knowledge.append(learned_item)

            # EVALUATE phase
            uncertainty = UncertaintyModel(overall=decision.confidence)
            if PipelinePhase.EVALUATE in self.pipeline_phases:
                uncertainty = self.evaluate_output(output)
            output.uncertainty = uncertainty

            # Check if self-revision is needed (if confidence < 0.75 and under max_revisions)
            if uncertainty.overall < 0.75 and revision < self.max_revisions:
                revision += 1
                decision.confidence = min(0.95, decision.confidence + 0.15)
                continue
            else:
                break

        dur_ms = (time.time() - start_time) * 1000
        self.total_execution_ms += dur_ms
        self.state = "idle"
        return output

    def shutdown(self):
        self.state = "disabled"
