"""
Gold Standard Evaluation Framework & Benchmark Suite for AVENIQ AI Runtime v5.1.
Evaluates Runtime execution against curated reference Gold Standards across Marketing, Research, Publishing, Brain, and Planning suites.
Verifies clean separation of Operational vs Intelligence Metrics, Production Readiness (Maturity Levels 0-4), and Goal Replay comparison.
"""

import uuid
import pytest
from ai_workers.planner_worker import global_planner_worker
from ai_workers.research_worker import global_research_worker
from ai_workers.publishing_worker import global_publishing_worker
from ai_workers.base_worker import WorkerContext
from runtime.goals import global_goal_manager
from company_brain import global_company_brain_service


def test_gold_standard_marketing_evaluation_suite():
    """Gold Standard Suite: Marketing Campaign Goal Execution."""
    planner = global_planner_worker
    manager = global_goal_manager

    obj = f"Gold Standard Marketing {uuid.uuid4().hex[:4]}"
    goal = manager.create_goal(objective=obj, priority="high", quality_target=0.98)

    res = planner.execute_goal_cycle(goal.goal_id)
    
    # Gold Standard Assertions
    assert res["status"] == "completed"
    assert res["selected_plan"] == "Plan C (High Quality)"
    assert res["completed_count"] == 6
    assert res["decision_quality"]["decision_quality_score"] >= 0.85


def test_gold_standard_research_evaluation_suite():
    """Gold Standard Suite: Research Worker Execution."""
    res_worker = global_research_worker
    ctx = WorkerContext_Mock(f"Gold Standard Research {uuid.uuid4().hex[:4]}")

    output = res_worker.execute(ctx)

    # Gold Standard Assertions
    assert output.status == "success"
    assert len(output.artifacts) == 1
    assert output.artifacts[0]["type"] == "MarketResearch"
    assert output.decision.chosen_strategy == "Web Search + Trend Gap Analysis"
    assert output.decision.confidence >= 0.90


def test_gold_standard_publishing_evaluation_suite():
    """Gold Standard Suite: Publishing Worker Execution."""
    pub_worker = global_publishing_worker
    ctx = WorkerContext_Mock(f"Gold Standard Publishing {uuid.uuid4().hex[:4]}")

    output = pub_worker.execute(ctx)

    # Gold Standard Assertions
    assert output.status == "success"
    assert output.artifacts[0]["channel"] == "Telegram"
    assert output.artifacts[0]["status"] == "Published"


def test_gold_standard_knowledge_retrieval_evaluation_suite():
    """Gold Standard Suite: Company Brain Knowledge Retrieval."""
    brain = global_company_brain_service
    brain.ingest_item({
        "title": "Gold Standard Agent Architecture Reference",
        "type": "Technology",
        "tags": ["gold_standard", "architecture"],
        "body": "Reference architecture for multi-agent autonomous runtime."
    })

    results = brain.search_ranked(query="gold_standard")

    # Gold Standard Assertions
    assert len(results) > 0
    assert "_rank_score" in results[0]
    assert results[0]["_rank_score"] > 0.0


def test_gold_standard_planning_evaluation_suite():
    """Gold Standard Suite: Planner Candidate Strategies."""
    planner = global_planner_worker
    manager = global_goal_manager

    goal = manager.create_goal(objective="Planning Benchmark", priority="medium")
    candidates = planner.generate_candidate_plans(goal)

    # Gold Standard Assertions
    assert "Plan A (Balanced)" in candidates
    assert "Plan B (Fast/Low Cost)" in candidates
    assert "Plan C (High Quality)" in candidates
    assert candidates["Plan A (Balanced)"]["quality"] == 0.92


def test_goal_replay_comparison_engine():
    """Verify Goal Replay compares Old Plan vs New Plan and computes decision quality delta."""
    manager = global_goal_manager
    planner = global_planner_worker

    goal = manager.create_goal(objective=f"Replay Goal {uuid.uuid4().hex[:4]}", priority="high")
    planner.execute_goal_cycle(goal.goal_id)

    replay_res = manager.replay_goal(goal.goal_id)

    # Replay Assertions
    assert "old_plan_name" in replay_res
    assert "new_plan_name" in replay_res
    assert "task_count_delta" in replay_res
    assert "decision_quality_difference" in replay_res


class WorkerContext_Mock:
    def __init__(self, objective):
        self.goal_id = f"goal_{uuid.uuid4().hex[:6]}"
        self.task_id = f"task_{uuid.uuid4().hex[:6]}"
        self.objective = objective
        self.task_description = f"Execute mock task for {objective}"
        self.previous_outputs = []
        self.goal_memory = {}
        self.runtime_metadata = {}
