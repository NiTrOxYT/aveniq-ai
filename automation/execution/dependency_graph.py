"""
DAG Dependency-Based Partial Regeneration Engine.
Solves affected workflow components based on action input to avoid unnecessary full pipeline reruns.
"""

from typing import List, Dict, Set

class DependencyGraphSolver:
    # Component DAG dependencies
    # Strategy -> Content -> Images -> SEO -> Summary -> Delivery
    GRAPH = {
        "strategy": ["content", "images", "seo", "summary"],
        "content": ["seo", "summary", "cta"],
        "images": ["thumbnails"],
        "seo": [],
        "summary": [],
        "cta": []
    }

    ACTION_MAP = {
        "action_RegenerateHero": ["images"],
        "action_GenerateVideo": ["images"],
        "action_Shorter": ["content", "seo", "summary"],
        "action_Simplify": ["content", "summary"],
        "action_Technical": ["content", "strategy"],
        "action_Rewrite": ["strategy", "content", "images", "seo", "summary"],
        "action_DifferentAngle": ["strategy", "content", "images", "seo", "summary"],
        "action_NewImages": ["images"]
    }

    @classmethod
    def resolve_affected_nodes(cls, action: str) -> List[str]:
        direct = cls.ACTION_MAP.get(action, ["strategy", "content", "images", "seo", "summary"])
        affected: Set[str] = set(direct)

        stack = list(direct)
        while stack:
            curr = stack.pop()
            children = cls.GRAPH.get(curr, [])
            for child in children:
                if child not in affected:
                    affected.add(child)
                    stack.append(child)

        return sorted(list(affected))

global_dependency_solver = DependencyGraphSolver()
