"""
Operational Health Domain Service for Company Brain.
Calculates mathematically derived operational & graph health metrics.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from company_brain.repository.knowledge_repository import global_knowledge_repository


class HealthService:
    def __init__(self, repository=global_knowledge_repository):
        self.repo = repository

    def calculate_health(self) -> Dict[str, Any]:
        memories = self.repo.get_all_memories()
        data = self.repo.get_entities_and_relationships()
        entities = data.get("entities", [])
        relationships = data.get("relationships", [])

        total = len(memories)
        verified = sum(1 for m in memories if m.get("status") in ("Verified", "Trusted"))
        draft = sum(1 for m in memories if m.get("status") == "Draft")
        needs_review = sum(1 for m in memories if m.get("status") == "Needs Review")
        archived = sum(1 for m in memories if m.get("status") == "Archived")

        duplicate_merge_count = sum(m.get("ref_count", 1) - 1 for m in memories)

        # Orphan entities: entities not referenced in any relationship
        related_nodes = set()
        for r in relationships:
            related_nodes.add(r.get("entity_a") or r.get("source"))
            related_nodes.add(r.get("entity_b") or r.get("target"))

        orphans = sum(1 for e in entities if e.get("name") not in related_nodes)
        avg_rels = round(len(relationships) / len(entities), 2) if entities else 0.0

        # Stale knowledge: not updated in > 90 days
        cutoff = datetime.now(timezone.utc) - timedelta(days=90)
        stale_count = 0
        for m in memories:
            up_str = m.get("updated_at")
            if up_str:
                try:
                    dt = datetime.fromisoformat(up_str)
                    if dt < cutoff:
                        stale_count += 1
                except Exception:
                    pass

        return {
            "total_knowledge_items": total,
            "verified_count": verified,
            "draft_count": draft,
            "needs_review_count": needs_review,
            "archived_count": archived,
            "duplicate_merge_count": duplicate_merge_count,
            "orphan_entities_count": orphans,
            "avg_relationships_per_entity": avg_rels,
            "stale_knowledge_count": stale_count,
            "repository_size_kb": self.repo.get_index().get("count", 0)
        }


global_health_service = HealthService()
