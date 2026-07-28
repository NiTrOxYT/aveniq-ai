"""
Centralized Company Brain Orchestrator Facade for AVENIQ AI.
Lightweight orchestrator coordinating Repository, Domain Services, Reflection Policy, and Event Bus.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional

from company_brain.repository.knowledge_repository import global_knowledge_repository
from company_brain.services.extraction_service import global_extraction_service
from company_brain.services.relationship_service import global_relationship_service
from company_brain.services.reflection_service import global_reflection_service
from company_brain.services.graph_service import global_graph_service
from company_brain.services.health_service import global_health_service
from company_brain.services.lifecycle_service import global_lifecycle_service
from runtime.event_bus import global_event_bus
from runtime.queue import global_background_queue
from runtime.search_service import global_unified_search_service


class CompanyBrainService:
    def __init__(self):
        self.repo = global_knowledge_repository
        self.extractor = global_extraction_service
        self.relationship_service = global_relationship_service
        self.reflection_service = global_reflection_service
        self.graph_service = global_graph_service
        self.health_service = global_health_service
        self.lifecycle_service = global_lifecycle_service
        self.event_bus = global_event_bus
        self.queue = global_background_queue
        self.search_service = global_unified_search_service

        # Register search provider with unified runtime search
        self.search_service.register_provider(self._search_provider_adapter)

    def _search_provider_adapter(self, query: str, limit: int) -> List[Dict[str, Any]]:
        return self.search(query=query, limit=limit)

    def rebuild_persistent_index(self) -> Dict[str, Any]:
        """Delegate index rebuilding to repository."""
        # Index scan logic via extraction
        index_data = self.repo.get_index()
        return index_data

    def ingest_item(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest item, assign trust metadata, extract relationships, check dependencies, and reflect."""
        payload = self.lifecycle_service.assign_trust_metadata(payload)
        
        # Save or update memory
        item_id = payload.get("id") or payload.get("title", "").lower().replace(" ", "_")
        memories = self.repo.get_all_memories()
        existing = next((m for m in memories if m.get("id") == item_id or m.get("title", "").lower() == payload.get("title", "").lower()), None)

        if existing:
            existing["ref_count"] = existing.get("ref_count", 1) + 1
            existing["revision"] = existing.get("revision", 1) + 1
            existing["summary"] = payload.get("summary") or existing.get("summary")
            existing["body"] = payload.get("body") or existing.get("body")
            existing["depends_on"] = list(set(existing.get("depends_on", []) + payload.get("depends_on", [])))
            if "status" in payload:
                existing["status"] = payload["status"]
            
            # Merge tags
            existing_tags = set(existing.get("tags", []))
            existing_tags.update(payload.get("tags", []))
            existing["tags"] = sorted(list(existing_tags))
            
            self.lifecycle_service.assign_trust_metadata(existing)
            self.repo.save_memory_item(existing)
            self.repo.save_revision(existing["id"], existing["revision"], existing)
            
            target_item = existing
        else:
            payload["id"] = item_id
            payload["revision"] = 1
            payload["ref_count"] = 1
            payload["depends_on"] = payload.get("depends_on", [])
            self.lifecycle_service.assign_trust_metadata(payload)
            self.repo.save_memory_item(payload)
            self.repo.save_revision(item_id, 1, payload)
            target_item = payload

        # Extract entities & relationships
        extracted = self.extractor.extract_entities(target_item.get("body", "") + " " + target_item.get("title", ""))
        self.relationship_service.process_item_relationships(target_item, extracted)

        # Dependency check: if upstream changes, mark dependent items as Needs Review
        self.relationship_service.check_dependencies_and_mark_review(target_item)

        # Reflection policy evaluation
        self.reflection_service.evaluate_and_reflect(target_item)

        # Publish runtime event
        self.event_bus.publish("KnowledgeAdded", {"id": target_item["id"], "title": target_item["title"]})
        self.repo.log_activity(f"Knowledge ingested: '{target_item['title']}' ({target_item.get('type')})")
        return target_item

    def get_all_items(self) -> List[Dict[str, Any]]:
        memories = self.repo.get_all_memories()
        index_data = self.repo.get_index()
        indexed = index_data.get("items", [])

        seen = set()
        combined = []
        for item in memories + indexed:
            if item.get("id") not in seen:
                seen.add(item.get("id"))
                item = self.lifecycle_service.assign_trust_metadata(item)
                combined.append(item)
        combined.sort(key=lambda x: x.get("updated_at") or "", reverse=True)
        return combined

    def search_ranked(self, query: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        """Rank memories by similarity, trust level, freshness, and ref_count."""
        items = self.search(query=query, limit=100)
        if not query or not items:
            return items[:limit]

        q_lower = query.lower().strip()
        scored_items = []

        for item in items:
            title = (item.get("title") or "").lower()
            body = (item.get("body") or "").lower()
            tags = " ".join(item.get("tags") or []).lower()

            # Base relevance score
            rel_score = 0.0
            if q_lower in title: rel_score += 3.0
            if q_lower in tags: rel_score += 2.0
            if q_lower in body: rel_score += 1.0

            # Trust multiplier
            trust_level = item.get("trust_level", "Draft")
            trust_mult = 1.5 if trust_level == "Official Documentation" else (1.2 if trust_level == "Automation Output" else 1.0)

            # Historical success (ref_count)
            ref_boost = min(2.0, 1.0 + (item.get("ref_count", 1) * 0.1))

            total_score = rel_score * trust_mult * ref_boost
            item["_rank_score"] = round(total_score, 2)
            scored_items.append(item)

        scored_items.sort(key=lambda x: x.get("_rank_score", 0), reverse=True)
        return scored_items[:limit]

    def search(self, query: str = "", item_type: str = "", source: str = "", limit: int = 50) -> List[Dict[str, Any]]:
        all_items = self.get_all_items()
        if not query and not item_type and not source:
            return all_items[:limit]

        q_lower = query.lower().strip()
        results = []

        for item in all_items:
            if item_type and item.get("type", "").lower() != item_type.lower():
                continue
            if source and source.lower() not in item.get("source", "").lower():
                continue
            if q_lower:
                title = (item.get("title") or "").lower()
                summary = (item.get("summary") or "").lower()
                body = (item.get("body") or "").lower()
                tags = " ".join(item.get("tags") or []).lower()
                src = (item.get("source") or "").lower()

                if q_lower not in title and q_lower not in summary and q_lower not in body and q_lower not in tags and q_lower not in src:
                    continue
            results.append(item)
            if len(results) >= limit:
                break

        return results

    def get_statistics(self) -> Dict[str, Any]:
        items = self.get_all_items()
        data = self.repo.get_entities_and_relationships()
        health = self.health_service.calculate_health()

        return {
            "total_knowledge_items": len(items),
            "categories_count": len(set(i.get("category") for i in items if i.get("category"))),
            "entities_count": len(data.get("entities", [])),
            "relationships_count": len(data.get("relationships", [])),
            "sources_count": len(set(i.get("source") for i in items if i.get("source"))),
            "unique_tags_count": len(set(t for i in items for t in i.get("tags", []))),
            "storage_size_kb": health.get("repository_size_kb", 0),
            "verified_count": health.get("verified_count", 0),
            "needs_review_count": health.get("needs_review_count", 0),
            "last_updated": self.repo.get_index().get("updated_at")
        }

    def get_graph(self) -> Dict[str, Any]:
        return self.graph_service.get_graph_payload()

    def get_reflections(self) -> List[Dict[str, Any]]:
        return self.reflection_service.get_all_reflections()

    def get_overview(self) -> Dict[str, Any]:
        stats = self.get_statistics()
        items = self.get_all_items()
        entities_data = self.repo.get_entities_and_relationships()
        activity = self.repo.get_activity()
        reflections = self.get_reflections()
        health = self.health_service.calculate_health()

        return {
            "statistics": stats,
            "health": health,
            "recent_items": items[:10],
            "entities": entities_data.get("entities", [])[:15],
            "relationships": entities_data.get("relationships", [])[:15],
            "reflections": reflections[:10],
            "activity_timeline": activity[:15]
        }


global_company_brain_service = CompanyBrainService()
