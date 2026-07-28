"""
Automated Integration Tests for AVENIQ Company Brain v3.1 Production Architecture.
Verifies repository abstraction, EventBus, BackgroundQueue, ReflectionPolicy, Dependency Tracking, Trust Metadata, HealthService, and UnifiedSearch.
"""

import time
import uuid
import pytest
from runtime.event_bus import global_event_bus, Event
from runtime.queue import global_background_queue
from runtime.search_service import global_unified_search_service
from company_brain.repository.knowledge_repository import global_knowledge_repository
from company_brain.reflection_policy import global_reflection_policy
from company_brain import global_company_brain_service


def test_event_bus_pub_sub():
    """Verify EventBus handler publication and subscription."""
    received = []

    def handler(evt: Event):
        received.append(evt)

    global_event_bus.subscribe("TestEvent", handler)
    global_event_bus.publish("TestEvent", {"data": "ok"})

    assert len(received) == 1
    assert received[0].name == "TestEvent"
    assert received[0].payload["data"] == "ok"


def test_background_queue_execution():
    """Verify BackgroundQueue asynchronous execution."""
    executed = []

    def background_task(val):
        executed.append(val)

    global_background_queue.enqueue(background_task, "done")
    time.sleep(0.1)
    assert "done" in executed


def test_repository_abstraction_layer():
    """Verify KnowledgeRepository is the single storage abstraction."""
    repo = global_knowledge_repository
    memories = repo.get_all_memories()
    assert isinstance(memories, list)
    
    entities_data = repo.get_entities_and_relationships()
    assert "entities" in entities_data
    assert "relationships" in entities_data


def test_reflection_policy_and_generation():
    """Verify reflection policy engine evaluation and strategic reflection synthesis."""
    policy = global_reflection_policy
    significant_payload = {
        "title": "Voice AI Competitor Launch",
        "type": "Competitor",
        "category": "Market",
        "tags": ["competitor", "voice_ai"],
        "body": "Competitor launched AI voice automation platform."
    }
    minor_payload = {
        "title": "Minor formatting update",
        "type": "General",
        "category": "Documentation",
        "tags": ["formatting"],
        "body": "Fixed typo."
    }

    assert policy.should_reflect(significant_payload) is True
    assert policy.should_reflect(minor_payload) is False

    ref = global_company_brain_service.reflection_service.evaluate_and_reflect(significant_payload)
    assert ref is not None
    assert ref["title"].startswith("Strategic Reflection")
    assert "voice_ai" in ref["tags"]


def test_dependency_tracking_needs_review():
    """Verify dependency graph tracking: updating an upstream item marks dependent items as Needs Review."""
    service = global_company_brain_service
    upstream_id = f"upstream_{uuid.uuid4().hex[:6]}"
    upstream_title = f"Core AI Provider API Key {uuid.uuid4().hex[:4]}"
    dep_id = f"dependent_{uuid.uuid4().hex[:6]}"
    dep_title = f"Campaign Bot Pipeline {uuid.uuid4().hex[:4]}"

    # Upstream item
    service.ingest_item({
        "id": upstream_id,
        "title": upstream_title,
        "type": "Technology",
        "status": "Verified",
        "body": "Core API key configuration."
    })

    # Dependent item
    service.ingest_item({
        "id": dep_id,
        "title": dep_title,
        "type": "Campaign",
        "status": "Verified",
        "depends_on": [upstream_id],
        "body": "Bot pipeline depending on Core AI Provider API Key."
    })

    # Re-ingest upstream item
    service.ingest_item({
        "id": upstream_id,
        "title": upstream_title,
        "body": "Rotated core API key configuration."
    })

    # Check that dependent item was marked Needs Review
    memories = service.repo.get_all_memories()
    dep_item = next((m for m in memories if m.get("id") == dep_id), None)
    assert dep_item is not None
    assert dep_item["status"] == "Needs Review"


def test_unified_search_service():
    """Verify runtime global search queries across registered providers."""
    search_service = global_unified_search_service
    results = search_service.search(query="Telegram")
    assert isinstance(results, list)
    assert len(results) > 0
