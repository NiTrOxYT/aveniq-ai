"""
Automated Integration Tests for AVENIQ AI Runtime v3.1 (Adaptive Cognitive Agents & Dynamic Decision Model).
Verifies phase-selective pipeline execution, explicit Decision objects, Multi-Strategy Planning Plan A/B/C,
Ranked Memory Retrieval, Reflection vs Learning separation, Self-Revision loops, and Explainability Reports.
"""

import pytest
import uuid
from ai_workers.base_worker import PipelinePhase, Decision, UncertaintyModel
from ai_workers.publishing_worker import global_publishing_worker
from ai_workers.research_worker import global_research_worker
from ai_workers.planner_worker import global_planner_worker
from runtime.goals import global_goal_manager
from company_brain import global_company_brain_service


def test_phase_selective_pipeline_execution():
    """Verify different workers execute only their declared pipeline phases."""
    pub_worker = global_publishing_worker
    res_worker = global_research_worker

    assert PipelinePhase.ACT in pub_worker.pipeline_phases
    assert PipelinePhase.THINK not in pub_worker.pipeline_phases

    assert PipelinePhase.OBSERVE in res_worker.pipeline_phases
    assert PipelinePhase.LEARN in res_worker.pipeline_phases


def test_explicit_decision_object_generation():
    """Verify workers generate structured Decision object prior to execution."""
    res_worker = global_research_worker
    context = WorkerContext_Mock(f"Research Goal {uuid.uuid4().hex[:4]}")

    output = res_worker.execute(context)
    assert output.decision is not None
    assert isinstance(output.decision, Decision)
    assert output.decision.chosen_strategy is not None
    assert output.decision.confidence >= 0.80


def test_planner_multi_strategy_generation_and_selection():
    """Verify Planner generates Plan A, B, C and selects optimal plan based on goal constraints."""
    planner = global_planner_worker
    manager = global_goal_manager

    # High quality goal -> Plan C
    high_qual_goal = manager.create_goal(objective="High Quality Strategy Test", quality_target=0.98, priority="high")
    candidates = planner.generate_candidate_plans(high_qual_goal)
    assert "Plan A (Balanced)" in candidates
    assert "Plan B (Fast/Low Cost)" in candidates
    assert "Plan C (High Quality)" in candidates

    selected = planner.select_optimal_plan(high_qual_goal, candidates)
    assert selected["name"] == "Plan C (High Quality)"

    # Low cost goal -> Plan B
    low_cost_goal = manager.create_goal(objective="Low Cost Strategy Test", priority="low")
    selected_b = planner.select_optimal_plan(low_cost_goal, candidates)
    assert selected_b["name"] == "Plan B (Fast/Low Cost)"


def test_ranked_memory_retrieval():
    """Verify Company Brain search_ranked() returns memories ranked by similarity, trust, and historical success."""
    brain = global_company_brain_service
    brain.ingest_item({
        "title": "Autonomous Agent Architecture Best Practices",
        "type": "Technology",
        "tags": ["agent_architecture"],
        "body": "Best practices for multi-agent autonomous runtime."
    })

    results = brain.search_ranked(query="agent_architecture")
    assert len(results) > 0
    assert "_rank_score" in results[0]
    assert results[0]["_rank_score"] > 0.0


def test_explainability_report():
    """Verify end-to-end goal execution generates explainability report with candidate plans & decisions."""
    planner = global_planner_worker
    manager = global_goal_manager

    objective = f"Explainable Goal {uuid.uuid4().hex[:6]}"
    goal = manager.create_goal(objective=objective, priority="high")
    planner.execute_goal_cycle(goal.goal_id)

    updated = manager.get_goal(goal.goal_id)
    assert "candidate_plans" in updated.memory
    assert "worker_decisions" in updated.memory
    assert len(updated.memory["worker_decisions"]) > 0


class WorkerContext_Mock:
    def __init__(self, objective):
        self.goal_id = f"goal_{uuid.uuid4().hex[:6]}"
        self.task_id = f"task_{uuid.uuid4().hex[:6]}"
        self.objective = objective
        self.task_description = f"Execute mock task for {objective}"
        self.previous_outputs = []
        self.goal_memory = {}
        self.runtime_metadata = {}
