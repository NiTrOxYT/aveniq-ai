"""
Knowledge Lifecycle & Trust Domain Service for Company Brain.
Manages state transitions: Draft, Verified, Trusted, Needs Review, Deprecated, Archived.
Derives trust levels and trust scores based on source metadata.
"""

from typing import Dict, Any

VALID_STATUSES = {"Draft", "Verified", "Trusted", "Needs Review", "Deprecated", "Archived"}

TRUST_SCORES = {
    "Official Documentation": 1.0,
    "Research Paper": 0.95,
    "Internal Knowledge": 0.90,
    "Manual Entry": 0.90,
    "Automation Output": 0.85,
    "LLM Reflection": 0.80,
    "GitHub": 0.85,
    "Product Hunt": 0.75,
    "Hacker News": 0.70,
    "Reddit": 0.65,
    "News": 0.60
}


class LifecycleService:
    def assign_trust_metadata(self, item: Dict[str, Any]) -> Dict[str, Any]:
        source = item.get("source", "").lower()
        created_by = item.get("created_by", "").lower()

        if "knowledge/" in source or "documentation" in source:
            trust_level = "Official Documentation"
            trust_reason = "Indexed core Markdown documentation"
        elif "research" in source or "github" in source:
            trust_level = "GitHub" if "github" in source else "Research Paper"
            trust_reason = "Collected from Research Engine pipeline"
        elif "automation" in created_by or "pipeline" in created_by:
            trust_level = "Automation Output"
            trust_reason = "Ingested from completed automation execution"
        elif "reflection" in source:
            trust_level = "LLM Reflection"
            trust_reason = "Synthesized strategic observation"
        else:
            trust_level = "Manual Entry"
            trust_reason = "Manually created knowledge memory"

        item["trust_level"] = trust_level
        item["trust_reason"] = trust_reason
        item["trust_score"] = TRUST_SCORES.get(trust_level, 0.80)
        item["verified"] = item.get("status") in ("Verified", "Trusted") or trust_level in ("Official Documentation", "Internal Knowledge")
        
        if "status" not in item or item["status"] not in VALID_STATUSES:
            item["status"] = "Verified" if item["verified"] else "Draft"

        return item

    def transition_status(self, item: Dict[str, Any], new_status: str) -> Dict[str, Any]:
        if new_status in VALID_STATUSES:
            item["status"] = new_status
        return item


global_lifecycle_service = LifecycleService()
