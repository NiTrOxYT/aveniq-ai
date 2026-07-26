"""
Dependency & Execution Graph Solver for Partial Regeneration Pathing.
Computes the minimal required downstream execution path for any interactive user action.
"""

from typing import List, Dict, Any

class ExecutionGraphSolver:
    DEPARTMENT_DEPENDENCIES = {
        "company_brain": [],
        "market": [],
        "growth": [],
        "strategy": ["company_brain"],
        "calendar": ["strategy"],
        "planning": ["strategy", "calendar"],
        "content": ["planning"],
        "creative": ["planning", "content"],
        "editorial": ["content", "creative"],
        "delivery": ["editorial", "creative"],
        "approval": ["delivery"],
        "archive": ["delivery", "approval"],
        "learning": ["archive"]
    }

    ACTION_TARGETS = {
        "Generate New Image": "creative",
        "Generate Carousel": "creative",
        "More Technical": "content",
        "Shorter": "content",
        "Longer": "content",
        "Simpler": "content",
        "Different Angle": "strategy",
        "Approve": "archive",
        "Reject": "stop",
        "Skip Today": "stop"
    }

    FULL_PIPELINE = [
        "company_brain", "market", "growth", "strategy", "calendar",
        "planning", "content", "creative", "editorial", "delivery",
        "approval", "archive", "learning"
    ]

    @staticmethod
    def solve_path(action: str) -> List[str]:
        target = ExecutionGraphSolver.ACTION_TARGETS.get(action, "content")
        if target == "stop":
            return []

        try:
            start_idx = ExecutionGraphSolver.FULL_PIPELINE.index(target)
            end_idx = ExecutionGraphSolver.FULL_PIPELINE.index("delivery") + 1
            if start_idx >= end_idx:
                return ExecutionGraphSolver.FULL_PIPELINE[start_idx:]
            return ExecutionGraphSolver.FULL_PIPELINE[start_idx:end_idx]
        except ValueError:
            return ["content", "editorial", "delivery"]
