"""
Traceable Attribution Graph for Performance Analytics.
Links Campaign -> Generated Assets -> Published Posts -> Performance Metrics -> Learning Recommendations.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class AttributionNode:
    id: str
    node_type: str  # Campaign, Asset, Post, Metric, Recommendation
    label: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AttributionEdge:
    source_id: str
    target_id: str
    relationship: str  # PRODUCES, PUBLISHES, MEASURES, INFORMS

class AttributionGraph:
    def __init__(self):
        self.nodes: Dict[str, AttributionNode] = {}
        self.edges: List[AttributionEdge] = []

    def add_node(self, node_id: str, node_type: str, label: str, metadata: Dict[str, Any] = None) -> AttributionNode:
        node = AttributionNode(id=node_id, node_type=node_type, label=label, metadata=metadata or {})
        self.nodes[node_id] = node
        return node

    def add_edge(self, source_id: str, target_id: str, relationship: str) -> AttributionEdge:
        edge = AttributionEdge(source_id=source_id, target_id=target_id, relationship=relationship)
        self.edges.append(edge)
        return edge

    def trace_recommendation_origin(self, recommendation_id: str) -> Dict[str, Any]:
        rec_node = self.nodes.get(recommendation_id)
        if not rec_node:
            return {"error": f"Recommendation '{recommendation_id}' not found in attribution graph"}

        incoming = [e for e in self.edges if e.target_id == recommendation_id]
        origin_chain = []
        for e in incoming:
            parent = self.nodes.get(e.source_id)
            if parent:
                origin_chain.append({"id": parent.id, "type": parent.node_type, "label": parent.label})

        return {
            "recommendation_id": recommendation_id,
            "originating_nodes": origin_chain
        }
