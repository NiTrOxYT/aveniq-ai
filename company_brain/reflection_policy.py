"""
Reflection Policy Engine for AVENIQ Company Brain.
Evaluates whether an ingestion item or event warrants a strategic reflection.
"""

from typing import Dict, Any

SIGNIFICANT_CATEGORIES = {"Competitor", "Market", "Technology", "Campaign", "Incident", "Decision", "Research"}
SIGNIFICANT_TAGS = {"competitor", "market_trend", "failure", "strategic", "breakthrough", "integration"}


class ReflectionPolicyEngine:
    def should_reflect(self, payload: Dict[str, Any]) -> bool:
        """Determine if an ingested item or event should trigger reflection."""
        item_type = payload.get("type", "")
        category = payload.get("category", "")
        tags = set(payload.get("tags", []))
        title = payload.get("title", "").lower()

        if item_type in ("Competitor", "Market", "Incident", "Decision"):
            return True
        if category in SIGNIFICANT_CATEGORIES:
            return True
        if any(t in SIGNIFICANT_TAGS for t in tags):
            return True
        if "failure" in title or "competitor" in title or "trend" in title:
            return True

        return False


global_reflection_policy = ReflectionPolicyEngine()
