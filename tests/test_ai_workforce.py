"""
Automated Integration Tests for AVENIQ AI Workforce v2.1 (Goal-Oriented Multi-Agent Runtime).
Verifies Goal Engine, DAG Task Graph Planner, Capability Matching, 3-Layer Memory, Tool Registry, and End-to-End Cycle.
"""

import pytest
import uuid
from runtime.goals import global_goal_manager, Goal
from ai_workers.registry import global_worker_registry
from ai_workers.planner_worker import global_planner_worker
from ai_workers.tools import global_tool_registry
from company_brain import global_company_brain_service


def test_capability_based_worker_registry():
    """Verify worker registration and capability-based resolution."""
    registry = global_worker_registry
    workers = registry.list_workers()
    assert len(workers) >= 7

    researcher = registry.find_worker_by_capability("market_research")
    assert researcher is not None
    assert researcher.name == "ResearchWorker"

    copywriter = registry.find_worker_by_capability("copywriting")
    assert copywriter is not None
    assert copywriter.name == "CampaignWorker"

    publisher = registry.find_worker_by_capability("platform_publishing")
    assert publisher is not None
    assert publisher.name == "PublishingWorker"


def test_goal_engine_and_persistence():
    """Verify Goal creation, data structure, and persistence."""
    manager = global_goal_manager
    goal = manager.create_goal(
        objective="Promote Autonomous Multi-Agent Runtime",
        goal_type="MarketingCampaign",
        priority="high",
        approval_policy="medium_risk"
    )

    assert goal.goal_id.startswith("goal_")
    assert goal.priority == "high"

    fetched = manager.get_goal(goal.goal_id)
    assert fetched is not None
    assert fetched.objective == goal.objective


def test_planner_dag_decomposition():
    """Verify PlannerWorker decomposes goal into DAG task graph with capability requirements."""
    planner = global_planner_worker
    manager = global_goal_manager
    goal = manager.create_goal(objective="Test DAG Graph")

    tasks = planner.decompose_goal(goal)
    assert len(tasks) == 6
    assert tasks[0].required_capability == "market_research"
    assert tasks[1].required_capability == "strategy_planning"
    assert tasks[2].required_capability == "copywriting"
    assert tasks[3].required_capability == "quality_approval"
    assert tasks[4].required_capability == "platform_publishing"
    assert tasks[5].required_capability == "pattern_learning"


def test_end_to_end_autonomous_workflow():
    """Verify full autonomous multi-agent cycle: Goal -> Task Graph -> Capability Matching -> Execution -> Goal Completion."""
    planner = global_planner_worker
    manager = global_goal_manager
    objective = f"Promote AI Workforce {uuid.uuid4().hex[:6]}"

    goal1 = manager.create_goal(objective=objective, priority="high")
    res1 = planner.execute_goal_cycle(goal1.goal_id)
    assert res1["status"] == "completed"

    # Second goal cycle with same objective satisfies min_observations=2 evidence threshold
    goal2 = manager.create_goal(objective=objective, priority="high")
    res2 = planner.execute_goal_cycle(goal2.goal_id)
    assert res2["status"] == "completed"

    # Verify Company Brain memory ingestion from LearningWorker
    brain_items = global_company_brain_service.search(query=objective)
    assert len(brain_items) > 0
