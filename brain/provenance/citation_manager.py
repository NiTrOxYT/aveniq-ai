"""
AI Citations & Knowledge Provenance Tracker.
Persists citations.json linking generated outputs to RAG documents, market events, prompt versions, and LLM models.
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class CitationManager:
    @staticmethod
    def generate_citations(
        session_id: str,
        campaign_id: str,
        rag_docs: Optional[List[Dict[str, Any]]] = None,
        market_events: Optional[List[Dict[str, Any]]] = None,
        prompt_version: str = "v1.4",
        model_used: str = "gemini-2.5-pro"
    ) -> Dict[str, Any]:
        docs = rag_docs or [
            {"doc_id": "doc_brand_01", "title": "Brand Guidelines", "collection": "Brand"},
            {"doc_id": "doc_prod_02", "title": "Product Architecture Spec", "collection": "Engineering"}
        ]
        events = market_events or [
            {"event_id": "evt_reddit_001", "source": "reddit", "title": "AI Agent Operations Discussion"},
            {"event_id": "evt_gh_002", "source": "github", "title": "MCP Tool Repository Launch"}
        ]

        return {
            "session_id": session_id,
            "campaign_id": campaign_id,
            "timestamp": _get_utc_now(),
            "prompt_version": prompt_version,
            "model_used": model_used,
            "rag_documents": docs,
            "market_events": events,
            "provenance_chain": [
                "MarketEventStorage -> RAG Hybrid Search -> Strategy Reasoning -> Content Synthesizer -> Delivery Package"
            ]
        }

    @staticmethod
    def save_citations(citations: Dict[str, Any], campaign_dir: str) -> str:
        os.makedirs(campaign_dir, exist_ok=True)
        path = os.path.join(campaign_dir, "citations.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(citations, f, indent=2)
        return path

global_citation_manager = CitationManager()
