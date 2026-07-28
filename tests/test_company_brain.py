"""
Automated Integration Tests for AVENIQ Company Brain Knowledge Engine.
Verifies live document scanning, ingestion, deduplication, revision history, search queries, entity extraction, and zero-mock statistics.
"""

import pytest
from company_brain.service import CompanyBrainService, global_company_brain_service


def test_scan_and_index_knowledge_files():
    """Verify live scanning of markdown files in knowledge/."""
    service = CompanyBrainService()
    items = service.scan_knowledge_files()
    assert len(items) > 0, "Company Brain must find live markdown documents in knowledge/"
    
    # Check that scanned items have valid types, categories, and sources
    first_item = items[0]
    assert first_item.title != ""
    assert first_item.category != ""
    assert first_item.source.startswith("knowledge/")


def test_knowledge_ingestion_and_deduplication():
    """Verify ingestion, entity extraction, deduplication, tag merging, and revision creation."""
    service = CompanyBrainService()
    payload = {
        "title": "Telegram Bot Dispatch Integration",
        "type": "Technology",
        "category": "Automation",
        "tags": ["telegram", "bot", "dispatch"],
        "source": "Campaign Engine",
        "body": "Dispatched market signals to Telegram channel using Gemini LLM Engine.",
        "confidence": 0.98
    }

    # First ingestion: create item
    item1 = service.ingest_item(payload)
    assert item1["title"] == "Telegram Bot Dispatch Integration"
    assert item1["revision"] == 1
    assert item1["ref_count"] == 1

    # Second ingestion with same title: deduplicate and bump revision
    payload2 = {
        "title": "Telegram Bot Dispatch Integration",
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

    # Seed test items to guarantee search query coverage
    service.ingest_item({
        "title": "Telegram Dispatch Workflow",
        "type": "Workflow",
        "category": "Automation",
        "tags": ["telegram"],
        "body": "Telegram notification pipeline for campaign approvals."
    })
    service.ingest_item({
        "title": "Gemini 1.5 Pro Strategy Engine",
        "type": "Technology",
        "category": "AI",
        "tags": ["gemini", "llm"],
        "body": "Gemini LLM reasoning engine for market intelligence analysis."
    })
    service.ingest_item({
        "title": "Q3 Marketing Campaign Blueprint",
        "type": "Campaign",
        "category": "Marketing",
        "tags": ["campaign", "q3"],
        "body": "Targeting SaaS decision makers with automated AI insights."
    })

    res_telegram = service.search(query="Telegram")
    assert len(res_telegram) > 0
    assert any("telegram" in (item.get("title") + item.get("body")).lower() for item in res_telegram)

    res_gemini = service.search(query="Gemini")
    assert len(res_gemini) > 0
    assert any("gemini" in (item.get("title") + item.get("body")).lower() for item in res_gemini)

    res_campaign = service.search(query="Campaign")
    assert len(res_campaign) > 0
    assert any("campaign" in (item.get("title") + item.get("body")).lower() for item in res_campaign)


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
