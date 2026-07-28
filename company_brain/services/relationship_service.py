"""
Relationship & Dependency Domain Service for Company Brain.
Extracts graph relationships with provenance metadata and tracks item dependencies (`depends_on`).
If an upstream item changes, marks dependent items as 'Needs Review'.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from company_brain.repository.knowledge_repository import global_knowledge_repository


class RelationshipService:
    def __init__(self, repository=global_knowledge_repository):
        self.repo = repository

    def process_item_relationships(self, item: Dict[str, Any], extracted_entities: Dict[str, List[str]]):
        """Extract relationships and persist to repository."""
        data = self.repo.get_entities_and_relationships()
        ents = data.setdefault("entities", [])
        rels = data.setdefault("relationships", [])

        item_title = item.get("title")
        item_id = item.get("id")

        for category, names in extracted_entities.items():
            for name in names:
                if not any(e.get("name") == name for e in ents):
                    ents.append({
                        "name": name,
                        "category": category,
                        "discovered_at": datetime.now(timezone.utc).isoformat()
                    })
                rel_id = f"{item_id}->{name}"
                if not any(r.get("id") == rel_id for r in rels):
                    rels.append({
                        "id": rel_id,
                        "entity_a": item_title,
                        "entity_b": name,
                        "relationship": "mentions",
                        "confidence": 0.95,
                        "method": "heuristic",
                        "source_document": item.get("source", "Ingestion"),
                        "created_at": datetime.now(timezone.utc).isoformat(),
                        "verified": True
                    })
        self.repo.save_entities_and_relationships(data)

    def check_dependencies_and_mark_review(self, updated_item: Dict[str, Any]):
        """If an upstream item changes, mark dependent items as 'Needs Review'."""
        memories = self.repo.get_all_memories()
        updated_id = updated_item.get("id")
        updated_title = updated_item.get("title")
        modified_count = 0

        for m in memories:
            deps = m.get("depends_on", [])
            if updated_id in deps or updated_title in deps:
                if m.get("status") not in ("Archived", "Needs Review"):
                    m["status"] = "Needs Review"
                    m["updated_at"] = datetime.now(timezone.utc).isoformat()
                    modified_count += 1

        if modified_count > 0:
            self.repo.save_memories(memories)
            self.repo.log_activity(f"Dependency trigger: {modified_count} items marked 'Needs Review' after update to '{updated_title}'")


global_relationship_service = RelationshipService()
