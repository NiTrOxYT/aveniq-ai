"""
Visualization-Agnostic Graph Data Builder for Company Brain.
Exposes clean node & edge graph payload for frontend visualizers.
"""

from typing import Dict, Any, List
from company_brain.repository.knowledge_repository import global_knowledge_repository


class GraphService:
    def __init__(self, repository=global_knowledge_repository):
        self.repo = repository

    def get_graph_payload(self) -> Dict[str, Any]:
        """Return nodes, edges, and metadata for interactive knowledge graph rendering."""
        data = self.repo.get_entities_and_relationships()
        entities = data.get("entities", [])
        relationships = data.get("relationships", [])
        memories = self.repo.get_all_memories()

        nodes = []
        node_ids = set()

        # Add entity nodes
        for e in entities:
            name = e.get("name")
            if name and name not in node_ids:
                node_ids.add(name)
                nodes.append({
                    "id": name,
                    "label": name,
                    "type": "Entity",
                    "category": e.get("category", "General")
                })

        # Add knowledge item nodes
        for m in memories[:30]:
            title = m.get("title")
            if title and title not in node_ids:
                node_ids.add(title)
                nodes.append({
                    "id": title,
                    "label": title,
                    "type": m.get("type", "Item"),
                    "category": m.get("category", "General")
                })

        edges = []
        for r in relationships:
            src = r.get("entity_a") or r.get("source")
            tgt = r.get("entity_b") or r.get("target")
            if src and tgt and src in node_ids and tgt in node_ids:
                edges.append({
                    "id": r.get("id", f"{src}->{tgt}"),
                    "source": src,
                    "target": tgt,
                    "label": r.get("relationship") or r.get("predicate") or "relates_to",
                    "confidence": r.get("confidence", 1.0)
                })

        return {
            "metadata": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
            },
            "nodes": nodes,
            "edges": edges
        }


global_graph_service = GraphService()
