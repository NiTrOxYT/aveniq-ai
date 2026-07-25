"""
Immutable Event Store & Knowledge Graph Builder for Archive Department.
"""

from typing import List, Dict, Any
from archive.models.schema import ArchiveEvent, RelationshipGraph, ArchiveContext

class EventStore:
    @staticmethod
    def generate_campaign_events(campaign_id: str, context: ArchiveContext) -> List[ArchiveEvent]:
        ts = context.created_at
        return [
            ArchiveEvent("evt_001", "StrategyFormulated", campaign_id, ts, {"status": "Complete"}),
            ArchiveEvent("evt_002", "ResearchCompleted", campaign_id, ts, {"citations_count": 3}),
            ArchiveEvent("evt_003", "PlanningCreated", campaign_id, ts, {"workload_items": 12}),
            ArchiveEvent("evt_004", "ContentGenerated", campaign_id, ts, {"channels_count": 8}),
            ArchiveEvent("evt_005", "CreativeApproved", campaign_id, ts, {"visual_theme": "Dark Glassmorphism"}),
            ArchiveEvent("evt_006", "EditorialPassed", campaign_id, ts, {"score": 96.7}),
            ArchiveEvent("evt_007", "DeliveryPackaged", campaign_id, ts, {"status": "READY"}),
            ArchiveEvent("evt_008", "ArchiveStored", campaign_id, ts, {"lifecycle_state": "ACTIVE"})
        ]

class KnowledgeGraphBuilder:
    @staticmethod
    def build_graph(campaign_id: str, topic: str) -> RelationshipGraph:
        nodes = [
            {"id": campaign_id, "type": "Campaign", "label": f"Campaign: {topic}"},
            {"id": f"top_{hash(topic)%1000}", "type": "Topic", "label": topic},
            {"id": f"res_{hash(topic)%1000}", "type": "Research", "label": "Research Package"},
            {"id": f"plan_{hash(topic)%1000}", "type": "Planning", "label": "Planning Package"},
            {"id": f"cnt_{hash(topic)%1000}", "type": "Content", "label": "Content Package"},
            {"id": f"crt_{hash(topic)%1000}", "type": "Creative", "label": "Media Package"},
            {"id": f"edt_{hash(topic)%1000}", "type": "Editorial", "label": "Approved Content"},
            {"id": f"del_{hash(topic)%1000}", "type": "Delivery", "label": "Delivery Package"},
            {"id": f"ast_hero", "type": "Asset", "label": "hero.webp"}
        ]

        edges = [
            {"source": campaign_id, "target": f"top_{hash(topic)%1000}", "relation": "HAS_TOPIC"},
            {"source": f"top_{hash(topic)%1000}", "target": f"res_{hash(topic)%1000}", "relation": "USES_RESEARCH"},
            {"source": f"res_{hash(topic)%1000}", "target": f"plan_{hash(topic)%1000}", "relation": "INFORMS_PLAN"},
            {"source": f"plan_{hash(topic)%1000}", "target": f"cnt_{hash(topic)%1000}", "relation": "DRIVES_CONTENT"},
            {"source": f"cnt_{hash(topic)%1000}", "target": f"crt_{hash(topic)%1000}", "relation": "INSPIRES_CREATIVE"},
            {"source": f"crt_{hash(topic)%1000}", "target": f"edt_{hash(topic)%1000}", "relation": "AUDITED_BY"},
            {"source": f"edt_{hash(topic)%1000}", "target": f"del_{hash(topic)%1000}", "relation": "PACKAGED_INTO"},
            {"source": f"del_{hash(topic)%1000}", "target": "ast_hero", "relation": "CONTAINS_ASSET"}
        ]

        return RelationshipGraph(nodes=nodes, edges=edges)
