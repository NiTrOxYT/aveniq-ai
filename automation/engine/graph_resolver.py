"""
Topological Indegree Graph Resolver, Cycle Detector & Condition Evaluator
for AVENIQ AI v2 Native Workflow Engine.
"""

from typing import List, Dict, Set, Optional
from automation.engine.workflow import WorkflowNode
from automation.engine.node_state import NodeState
from automation.engine.context import WorkflowContext

class GraphResolver:
    @staticmethod
    def detect_cycle(nodes: List[WorkflowNode]) -> bool:
        """Kahn's Algorithm for cycle detection."""
        adj = {n.id: list(n.depends_on) for n in nodes}
        in_degree = {n.id: 0 for n in nodes}
        graph_nodes = set(n.id for n in nodes)

        # Count incoming edges: node X depends_on Y means Y -> X (edge Y->X)
        for n in nodes:
            for parent in n.depends_on:
                if parent in in_degree:
                    in_degree[n.id] += 1

        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        visited_count = 0

        # Process queue
        # For Kahn's: build reverse adjacency (parent -> children)
        children_map: Dict[str, List[str]] = {nid: [] for nid in graph_nodes}
        for n in nodes:
            for parent in n.depends_on:
                if parent in children_map:
                    children_map[parent].append(n.id)

        while queue:
            curr = queue.pop(0)
            visited_count += 1
            for child in children_map.get(curr, []):
                in_degree[child] -= 1
                if in_degree[child] == 0:
                    queue.append(child)

        return visited_count < len(nodes)

    @staticmethod
    def get_ready_nodes(nodes: List[WorkflowNode], completed_node_ids: Set[str]) -> List[WorkflowNode]:
        """Finds all nodes in WAITING/READY state whose dependencies are satisfied and not completed."""
        ready = []
        for n in nodes:
            if n.id not in completed_node_ids and n.state in (NodeState.WAITING, NodeState.READY) and n.enabled:
                if n.any_dependency:
                    deps_met = any(dep in completed_node_ids for dep in n.depends_on)
                else:
                    deps_met = all(dep in completed_node_ids for dep in n.depends_on)
                if deps_met:
                    ready.append(n)
        return ready

    @staticmethod
    def eval_condition(condition: Optional[str], context: WorkflowContext) -> bool:
        """Evaluates node condition string against context data."""
        if not condition or not condition.strip():
            return True
        cond = condition.strip()
        try:
            # Safe evaluation context with quality, research, etc.
            ctx_data = context.to_dict().get("data", {})
            quality_score = ctx_data.get("quality", {}).get("overall_score", 100)
            
            # Simple expression evaluation rules
            if ">=" in cond:
                var_name, val_str = [p.strip() for p in cond.split(">=")]
                val = float(val_str)
                if "quality" in var_name:
                    return quality_score >= val
            elif "<" in cond:
                var_name, val_str = [p.strip() for p in cond.split("<")]
                val = float(val_str)
                if "quality" in var_name:
                    return quality_score < val
            elif "==" in cond:
                var_name, val_str = [p.strip() for p in cond.split("==")]
                if "quality" in var_name:
                    return quality_score == float(val_str)
            return True
        except Exception:
            return True
