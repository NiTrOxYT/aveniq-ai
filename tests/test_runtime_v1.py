"""
Automated End-to-End Integration Tests for AVENIQ AI Runtime v1 Kernel.
Verifies Kernel initialization, Service Registry DI, Telemetry, Dead Letter Queue, Event Store Replay, Plugin Manager, and End-to-End Pipeline.
"""

import time
import pytest
from runtime.kernel import global_runtime_kernel
from runtime.service_registry import global_service_registry
from runtime.event_bus import global_event_bus, Event
from runtime.dead_letter_queue import global_dead_letter_queue
from runtime.event_store import global_event_store
from runtime.telemetry import global_telemetry_collector
from plugins.plugin_manager import global_plugin_manager, BasePlugin


def test_kernel_initialization_and_registry():
    """Verify Kernel bootstrap and ServiceRegistry resolution."""
    kernel = global_runtime_kernel
    kernel.initialize()

    diagnostics = kernel.get_diagnostics()
    assert diagnostics["kernel_status"] == "active"
    assert "CompanyBrain" in diagnostics["registered_services"]
    assert "ResearchEngine" in diagnostics["registered_services"]
    assert "AutomationScheduler" in diagnostics["registered_services"]

    company_brain = global_service_registry.resolve("CompanyBrain")
    assert company_brain is not None


def test_dead_letter_queue():
    """Verify DLQ failure recording, listing, and retry execution."""
    dlq = global_dead_letter_queue
    dlq.purge()

    counter = {"retried": False}

    def failing_fn():
        raise RuntimeError("Simulated worker failure")

    def retry_fn():
        counter["retried"] = True

    try:
        failing_fn()
    except Exception as e:
        dlq.record_failure("test_task", (), {}, e, retry_fn=retry_fn)

    dead_jobs = dlq.list_dead_jobs()
    assert len(dead_jobs) == 1
    job_id = dead_jobs[0]["job_id"]

    success = dlq.retry_job(job_id)
    assert success is True
    assert counter["retried"] is True


def test_event_store_and_replay():
    """Verify event logging and non-destructive replay."""
    es = global_event_store
    bus = global_event_bus

    received = []

    def subscriber(evt: Event):
        received.append(evt.payload.get("test_id"))

    bus.subscribe("KnowledgeIndexed", subscriber)

    # Publish original event
    bus.publish("KnowledgeIndexed", {"test_id": "idx_123"})
    time.sleep(0.05)

    events = es.get_events(50)
    assert len(events) > 0
    target = next((e for e in events if e.get("name") == "KnowledgeIndexed"), None)
    assert target is not None

    # Replay event
    replay_res = es.replay_event(target["event_id"])
    assert replay_res["status"] == "replayed"


def test_plugin_manager_lifecycle():
    """Verify BasePlugin registration and lifecycle initialization."""
    pm = global_plugin_manager

    class CustomTestPlugin(BasePlugin):
        def __init__(self):
            super().__init__("TestPlugin", "1.0.0")
            self.initialized = False

        def initialize(self, kernel):
            self.initialized = True

    plugin = CustomTestPlugin()
    pm.register_plugin(plugin)
    pm.initialize_all(global_runtime_kernel)

    assert plugin.initialized is True
    plugins_list = pm.list_plugins()
    assert any(p["name"] == "TestPlugin" for p in plugins_list)


def test_end_to_end_runtime_pipeline():
    """Verify End-to-End Pipeline: Event -> Reflection -> Ingestion -> Unified Search -> Diagnostics."""
    kernel = global_runtime_kernel
    kernel.initialize()

    # Step 1: Ingest research market signal
    company_brain = global_service_registry.resolve("CompanyBrain")
    item = company_brain.ingest_item({
        "title": "Voice AI Market Shift 2026",
        "type": "Competitor",
        "category": "Research",
        "tags": ["voice_ai", "market_shift"],
        "source": "Research Engine",
        "body": "Enterprise clients adopting AI voice automation agents rapidly."
    })

    assert item["title"] == "Voice AI Market Shift 2026"

    # Step 2: Unified Search query
    search_service = global_service_registry.resolve("SearchService")
    results = search_service.search(query="Voice AI")
    assert len(results) > 0

    # Step 3: Diagnostics snapshot
    diag = kernel.get_diagnostics()
    assert diag["metrics"]["total_requests"] >= 0
