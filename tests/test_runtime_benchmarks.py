"""
Repeatable Baseline Benchmark Suite & Intelligence Regression Tests for AVENIQ AI Runtime v4.1.
Verifies Knowledge Decay/Recovery, Evidence-Grounded Learning, Planner Calibration Accuracy, Failure Taxonomy, Tool ROI, and Repeatable Benchmarks.
"""

import time
import uuid
import pytest
from company_brain.services.lifecycle_service import global_lifecycle_service
from ai_workers.learning_worker import global_learning_worker
from ai_workers.planner_worker import global_planner_worker
from ai_workers.tools import global_tool_registry
from ai_workers.base_worker import WorkerContext
from runtime.goals import global_goal_manager


def test_dynamic_knowledge_decay_and_recovery():
    """Verify confidence score decays on aging and recovers upon successful reuse."""
    service = global_lifecycle_service
    item = {
        "title": "Legacy API Authentication Key",
        "source": "Manual Entry",
        "status": "Verified",
        "trust_score": 0.90,
        "ref_count": 1
    }
    service.assign_trust_metadata(item)
    assert item["trust_score"] == 0.90

    # Decay
    service.decay_confidence(item)
    assert item["trust_score"] == 0.85

    # Recover
    service.recover_confidence(item)
    assert item["trust_score"] == 0.90
    assert item["ref_count"] == 2


def test_evidence_grounded_learning_threshold():
    """Verify LearningWorker requires min_observations >= 2 before promoting knowledge into Company Brain."""
    learner = global_learning_worker
    unique_obj = f"Evidence Test {uuid.uuid4().hex[:6]}"
    ctx = WorkerContext_Mock(unique_obj)

    # First observation (count = 1) -> No Company Brain promotion
    out1 = learner.execute(ctx)
    assert len(out1.knowledge) == 0

    # Second observation (count = 2) -> Evidence threshold met -> Promoted to Company Brain
    out2 = learner.execute(ctx)
    assert len(out2.knowledge) == 1
    assert "evidence_grounded" in out2.knowledge[0]["tags"]


def test_planner_calibration_and_failure_taxonomy():
    """Verify Planner calibration accuracy calculation and granular failure taxonomy recommendations."""
    planner = global_planner_worker

    # Calibration accuracy
    accuracy = planner.compute_calibration_accuracy(expected_dur=500.0, actual_dur=520.0)
    assert accuracy >= 0.90

    # Failure diagnosis
    diag = planner.diagnose_failure("No worker found with capability 'quantum_computing'")
    assert diag["category"] == "Missing Worker Capability"
    assert "Register a worker" in diag["corrective_action"]


def test_tool_roi_analytics():
    """Verify ToolRegistry records tool usage, success rates, and decision impact metrics."""
    registry = global_tool_registry
    tool = registry.get_tool("search")
    tool.execute("AI Workforce Benchmark")

    analytics = registry.get_tool_analytics()
    assert "search" in analytics
    assert analytics["search"]["usage_count"] > 0
    assert "decision_impact_boost" in analytics["search"]


def test_benchmark_marketing_campaign_workflow():
    """Benchmark: Complete Marketing Campaign Goal execution."""
    planner = global_planner_worker
    manager = global_goal_manager

    goal = manager.create_goal(
        objective=f"Benchmark Marketing Campaign {uuid.uuid4().hex[:4]}",
        priority="high"
    )

    res = planner.execute_goal_cycle(goal.goal_id)
    assert res["status"] == "completed"
    assert res["completed_count"] == 6

    # Verify decision quality score
    assert "decision_quality" in res
    assert res["decision_quality"]["decision_quality_score"] >= 0.85


class WorkerContext_Mock:
    def __init__(self, objective):
        self.goal_id = f"goal_{uuid.uuid4().hex[:6]}"
        self.task_id = f"task_{uuid.uuid4().hex[:6]}"
        self.objective = objective
        self.task_description = f"Execute mock task for {objective}"
        self.previous_outputs = []
        self.goal_memory = {}
        self.runtime_metadata = {}
