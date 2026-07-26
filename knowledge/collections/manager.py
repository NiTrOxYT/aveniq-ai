"""
Knowledge Collections Manager for AVENIQ Platform.
Organizes indexed documents into scoped collections.
"""

from typing import List, Dict, Any, Optional

KNOWLEDGE_COLLECTIONS = [
    "Company Brain",
    "Brand Guidelines",
    "Product Documentation",
    "Marketing Assets",
    "Competitor Research",
    "Historical Campaigns",
    "Analytics Reports",
    "SOPs",
    "Customer Documentation"
]

class KnowledgeCollectionsManager:
    @staticmethod
    def list_collections() -> List[str]:
        return KNOWLEDGE_COLLECTIONS

    @staticmethod
    def validate_collection(collection_name: str) -> str:
        for c in KNOWLEDGE_COLLECTIONS:
            if c.lower() == collection_name.lower():
                return c
        return "Company Brain"
