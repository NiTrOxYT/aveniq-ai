"""
Planner Worker & Calibration Orchestrator for AVENIQ AI Runtime v4.1.
Generates candidate execution strategies (Plan A/B/C), evaluates planning calibration accuracy,
diagnoses granular failures with corrective recommendations, and scores outcome-based decision quality.
"""

import time
import logging
from typing import Dict, Any, List, Optional
from ai_workers.base_worker import BaseWorker, WorkerContext, WorkerOutput, PipelinePhase, Decision
from ai_workers.registry import global_worker_registry
from runtime.goals import global_goal_manager, Goal, GoalTaskNode

logger = logging.getLogger("aveniq.ai_workers.planner")

FAILURE_TAXONOMY = {
    "no worker found": ("Missing Worker Capability", "Register a worker advertising the required capability"),
    "quality failed": ("Weak Reasoning / Quality Failure", "Revise prompt templates or increase quality target"),
    "timeout": ("Timeout Failure", "Increase worker execution timeout or simplify task steps"),
    "rate limit": ("Rate Limit Failure", "Enforce API sliding window backoff"),
    "policy restriction": ("Policy Restriction Failure", "Submit for human approval gate review")
}


class PlannerWorker(BaseWorker):
    def __init__(self):
        super().__init__(
            name="PlannerWorker",
            capabilities=["goal_decomposition", "task_scheduling", "graph_planning"],
            pipeline_phases=[PipelinePhase.OBSERVE, PipelinePhase.THINK, PipelinePhase.PLAN, PipelinePhase.DECIDE, PipelinePhase.ACT, PipelinePhase.EVALUATE]
        )

    def generate_candidate_plans(self, goal: Goal) -> Dict[str, Dict[str, Any]]:
        plan_a_tasks = [
            GoalTaskNode("task_1_research", "market_research", f"Research: '{goal.objective}'"),
            GoalTaskNode("task_2_strategy", "strategy_planning", "Synthesize strategy", ["task_1_research"]),
            GoalTaskNode("task_3_campaign", "copywriting", "Generate copy & assets", ["task_2_strategy"]),
            GoalTaskNode("task_4_approval", "quality_approval", "Review compliance", ["task_3_campaign"]),
            GoalTaskNode("task_5_publishing", "platform_publishing", "Publish content", ["task_4_approval"]),
            GoalTaskNode("task_6_learning", "pattern_learning", "Learn insights", ["task_5_publishing"]),
        ]

        plan_b_tasks = [
            GoalTaskNode("task_1_research", "market_research", f"Rapid Research: '{goal.objective}'"),
            GoalTaskNode("task_3_campaign", "copywriting", "Direct copy generation", ["task_1_research"]),
            GoalTaskNode("task_5_publishing", "platform_publishing", "Direct dispatch", ["task_3_campaign"]),
        ]

        plan_c_tasks = list(plan_a_tasks)

        return {
            "Plan A (Balanced)": {"quality": 0.92, "estimated_cost": 0.05, "estimated_duration_ms": 500.0, "tasks": plan_a_tasks},
            "Plan B (Fast/Low Cost)": {"quality": 0.82, "estimated_cost": 0.015, "estimated_duration_ms": 250.0, "tasks": plan_b_tasks},
            "Plan C (High Quality)": {"quality": 0.98, "estimated_cost": 0.12, "estimated_duration_ms": 800.0, "tasks": plan_c_tasks},
        }

    def select_optimal_plan(self, goal: Goal, candidate_plans: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        if goal.priority == "high" or goal.quality_target >= 0.95:
            selected_name = "Plan C (High Quality)"
        elif goal.budget < 0.03 or goal.priority == "low":
            selected_name = "Plan B (Fast/Low Cost)"
        else:
            selected_name = "Plan A (Balanced)"

        selected_plan = candidate_plans[selected_name]
        selected_plan["name"] = selected_name
        return selected_plan

    def decompose_goal(self, goal: Goal) -> List[GoalTaskNode]:
        candidates = self.generate_candidate_plans(goal)
        selected = self.select_optimal_plan(goal, candidates)
        goal.memory["candidate_plans"] = {k: {v_k: v_v for v_k, v_v in v.items() if v_k != "tasks"} for k, v in candidates.items()}
        goal.memory["selected_plan"] = selected
        goal.memory["selected_plan_name"] = selected["name"]
        return selected["tasks"]

    def diagnose_failure(self, error_message: str) -> Dict[str, Any]:
        """Categorize failure into granular taxonomy with corrective recommendation."""
        err_lower = error_message.lower()
        for key, (category, rec) in FAILURE_TAXONOMY.items():
            if key in err_lower:
                return {"category": category, "error": error_message, "corrective_action": rec}
        return {"category": "Execution Failure", "error": error_message, "corrective_action": "Inspect stack trace and worker dependencies"}

    def compute_calibration_accuracy(self, expected_dur: float, actual_dur: float) -> float:
        """Compute Planner Calibration Accuracy score (0.0 to 1.0)."""
        if expected_dur <= 0 or actual_dur <= 0:
            return 1.0
        ratio = min(expected_dur, actual_dur) / max(expected_dur, actual_dur)
        return round(ratio, 2)

    def evaluate_goal_decision_quality(self, goal: Goal) -> Dict[str, Any]:
        """Compute outcome-based Decision Quality Score and Explainability Score."""
        tasks_comp = sum(1 for t in goal.tasks if t.status == "completed")
        total_tasks = max(len(goal.tasks), 1)
        completion_ratio = tasks_comp / total_tasks

        decisions = goal.memory.get("worker_decisions", [])
        avg_conf = (sum(d.get("decision", {}).get("confidence", 0.90) for d in decisions) / len(decisions)) if decisions else 0.90

        decision_quality_score = round((completion_ratio * 0.5) + (avg_conf * 0.5), 2)
        explainability_score = round(0.95 if decisions and goal.memory.get("candidate_plans") else 0.80, 2)

        return {
            "decision_quality_score": decision_quality_score,
            "explainability_score": explainability_score,
            "completion_ratio": round(completion_ratio, 2),
            "average_worker_confidence": round(avg_conf, 2)
        }

    def execute_goal_cycle(self, goal_id: str) -> Dict[str, Any]:
        """Executes goal cycle, tracking calibration accuracy and outcome decision quality."""
        goal = global_goal_manager.get_goal(goal_id)
        if not goal:
            return {"status": "error", "message": f"Goal '{goal_id}' not found"}

        if not goal.tasks:
            goal.tasks = self.decompose_goal(goal)
            goal.status = "active"
            global_goal_manager.update_goal(goal)

        completed_outputs = []
        cycle_start = time.time()

        for task in goal.tasks:
            if task.status == "completed":
                completed_outputs.extend(task.output_artifacts)
                continue

            deps_completed = all(
                t.status == "completed" for t in goal.tasks if t.task_id in task.dependencies
            )
            if not deps_completed:
                task.status = "blocked"
                global_goal_manager.update_goal(goal)
                continue

            worker = global_worker_registry.find_worker_by_capability(task.required_capability)
            if not worker:
                task.status = "failed"
                diag = self.diagnose_failure(f"No worker found with capability '{task.required_capability}'")
                task.error_message = diag["error"]
                goal.memory.setdefault("failure_reports", []).append(diag)
                global_goal_manager.update_goal(goal)
                continue

            task.status = "in_progress"
            task.assigned_worker = worker.name
            task.started_at = time.time()
            global_goal_manager.update_goal(goal)

            context = WorkerContext(
                goal_id=goal.goal_id,
                task_id=task.task_id,
                objective=goal.objective,
                task_description=task.description,
                previous_outputs=completed_outputs,
                goal_memory=goal.memory
            )

            try:
                start_t = time.time()
                output = worker.execute(context)
                dur_ms = (time.time() - start_t) * 1000
                worker.task_count += 1
                worker.total_execution_ms += dur_ms

                if output.decision:
                    goal.memory.setdefault("worker_decisions", []).append({
                        "task_id": task.task_id,
                        "worker": worker.name,
                        "decision": output.decision.__dict__
                    })

                if output.status == "success":
                    worker.success_count += 1
                    task.status = "completed"
                    task.completed_at = time.time()
                    task.output_artifacts = output.artifacts
                    completed_outputs.extend(output.artifacts)
                else:
                    worker.failure_count += 1
                    task.status = "failed"
                    diag = self.diagnose_failure(output.error_message or "Worker execution failed")
                    task.error_message = diag["error"]
                    goal.memory.setdefault("failure_reports", []).append(diag)

            except Exception as e:
                worker.failure_count += 1
                task.status = "failed"
                diag = self.diagnose_failure(str(e))
                task.error_message = diag["error"]
                goal.memory.setdefault("failure_reports", []).append(diag)

            global_goal_manager.update_goal(goal)

        actual_dur_ms = (time.time() - cycle_start) * 1000
        selected_plan = goal.memory.get("selected_plan", {})
        expected_dur_ms = selected_plan.get("estimated_duration_ms", 500.0)

        # Compute calibration accuracy and outcome decision quality
        calibration = self.compute_calibration_accuracy(expected_dur_ms, actual_dur_ms)
        quality = self.evaluate_goal_decision_quality(goal)

        goal.memory["planning_calibration_accuracy"] = calibration
        goal.memory["decision_quality"] = quality

        if all(t.status == "completed" for t in goal.tasks):
            goal.status = "completed"

        global_goal_manager.update_goal(goal)

        return {
            "status": goal.status,
            "goal_id": goal.goal_id,
            "selected_plan": goal.memory.get("selected_plan_name"),
            "planning_calibration_accuracy": calibration,
            "decision_quality": quality,
            "completed_count": sum(1 for t in goal.tasks if t.status == "completed")
        }


global_planner_worker = PlannerWorker()
