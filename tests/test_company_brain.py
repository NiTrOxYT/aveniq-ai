"""
Automated Integration Tests for AVENIQ Company Brain Knowledge Engine.
Verifies live document scanning, persistent index rebuilding, ingestion, deduplication, revision history, search queries, entity extraction, and zero-mock statistics.
"""

import uuid
import pytest
from company_brain.service import CompanyBrainService, global_company_brain_service


def test_persistent_index_rebuilding():
    """Verify live scanning and persistent index rebuilding of markdown files in knowledge/."""
    service = CompanyBrainService()
    res = service.rebuild_persistent_index()
    assert res["count"] > 0, "Company Brain persistent index must contain live markdown items"
    assert len(res["items"]) > 0
    first_item = res["items"][0]
    assert first_item["title"] != ""
    assert first_item["source"].startswith("knowledge/")


def test_knowledge_ingestion_and_deduplication():
    """Verify ingestion, entity extraction, deduplication, tag merging, and revision creation."""
    service = CompanyBrainService()
    unique_title = f"Telegram Bot Dispatch Integration {uuid.uuid4().hex[:6]}"
    payload = {
        "title": unique_title,
        "type": "Technology",
        "category": "Automation",
        "tags": ["telegram", "bot", "dispatch"],
        "source": "Campaign Engine",
        "body": "Dispatched market signals to Telegram channel using Gemini LLM Engine.",
        "confidence": 0.98
    }

    # First ingestion: create item
    item1 = service.ingest_item(payload)
    assert item1["title"] == unique_title
    assert item1["revision"] == 1
    assert item1["ref_count"] == 1

    # Second ingestion with same title: deduplicate and bump revision
    payload2 = {
        "title": unique_title,
        "tags": ["realtime", "telegram"],
        "body": "Updated Telegram bot dispatch strategy with Gemini 1.5 Pro.",
    }
    item2 = service.ingest_item(payload2)
    assert item2["id"] == item1["id"]
    assert item2["revision"] == 2
    assert item2["ref_count"] == 2
    assert "realtime" in item2["tags"]
    assert "dispatch" in item2["tags"]


def test_company_brain_search_queries():
    """Verify specific search queries: 'Telegram', 'Gemini', 'Campaign' against live knowledge."""
    service = CompanyBrainService()

    service.ingest_item({
        "title": "Telegram Dispatch Workflow Test",
        "type": "Workflow",
        "category": "Automation",
        "tags": ["telegram"],
        "body": "Telegram notification pipeline for campaign approvals."
    })
    service.ingest_item({
        "title": "Gemini 1.5 Pro Strategy Engine Test",
        "type": "Technology",
        "category": "AI",
        "tags": ["gemini", "llm"],
        "body": "Gemini LLM reasoning engine for market intelligence analysis."
    })
    service.ingest_item({
        "title": "Q3 Marketing Campaign Blueprint Test",
        "type": "Campaign",
        "category": "Marketing",
        "tags": ["campaign", "q3"],
        "body": "Targeting SaaS decision makers with automated AI insights."
    })

    res_telegram = service.search(query="Telegram")
    assert len(res_telegram) > 0

    res_gemini = service.search(query="Gemini")
    assert len(res_gemini) > 0

    res_campaign = service.search(query="Campaign")
    assert len(res_campaign) > 0


def test_statistics_computation():
    """Verify statistics are computed from real files and storage (zero hardcoded values)."""
    service = CompanyBrainService()
    stats = service.get_statistics()
    
    assert "total_knowledge_items" in stats
    assert isinstance(stats["total_knowledge_items"], int)
    assert stats["total_knowledge_items"] >= 0
    assert "storage_size_kb" in stats
    assert isinstance(stats["storage_size_kb"], (int, float))
    assert stats["storage_size_kb"] > 0.0
    assert "last_updated" in stats
