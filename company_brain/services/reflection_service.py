"""
Reflection Domain Service for Company Brain.
Synthesizes market signals & workflow events into first-class Reflection knowledge items.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from company_brain.reflection_policy import global_reflection_policy
from company_brain.repository.knowledge_repository import global_knowledge_repository


class ReflectionService:
    def __init__(self, repository=global_knowledge_repository, policy=global_reflection_policy):
        self.repo = repository
        self.policy = policy

    def evaluate_and_reflect(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Evaluate item via reflection policy and generate reflection item if significant."""
        if not self.policy.should_reflect(payload):
            return None

        title = payload.get("title", "Observation")
        body = payload.get("body") or payload.get("summary", "")
        category = payload.get("category", "Market Opportunity")

        reflection_item = {
            "id": f"ref_{payload.get('id', 'gen')}",
            "title": f"Strategic Reflection: {title}",
            "observation": f"Observed activity/signal regarding '{title}'. Context: {body[:300]}",
            "recommendation": f"Evaluate integration of findings from '{title}' into strategic campaign workflows.",
            "category": category,
            "tags": list(set(payload.get("tags", []) + ["reflection", "strategic"])),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source_item": payload.get("title")
        }

        self.repo.save_reflection(reflection_item)
        self.repo.log_activity(f"Strategic reflection synthesized: '{reflection_item['title']}'")
        return reflection_item

    def get_all_reflections(self) -> List[Dict[str, Any]]:
        return self.repo.get_reflections()


global_reflection_service = ReflectionService()
