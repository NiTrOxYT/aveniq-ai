"""
AVENIQ AI Runtime Kernel v1.
Coordinates service discovery, dependency injection, startup/shutdown hooks, health monitoring, and diagnostics.
"""

import time
import logging
from typing import Dict, Any, List, Optional

from runtime.config import global_runtime_config
from runtime.logger import get_structured_logger
from runtime.security import global_security_manager
from runtime.telemetry import global_telemetry_collector
from runtime.service_registry import global_service_registry
from runtime.event_bus import global_event_bus
from runtime.queue import global_background_queue
from runtime.dead_letter_queue import global_dead_letter_queue
from runtime.event_store import global_event_store
from runtime.search_service import global_unified_search_service

logger = get_structured_logger("kernel")


class RuntimeKernel:
    def __init__(self):
        self.config = global_runtime_config
        self.registry = global_service_registry
        self.event_bus = global_event_bus
        self.queue = global_background_queue
        self.dead_letter_queue = global_dead_letter_queue
        self.event_store = global_event_store
        self.telemetry = global_telemetry_collector
        self.security = global_security_manager
        self.search_service = global_unified_search_service
        self._is_initialized = False

    def initialize(self):
        """Bootstraps and registers core runtime services."""
        if self._is_initialized:
            return
        
        logger.info("kernel_bootstrap", "Initializing AVENIQ AI Runtime Kernel...")

        # Register core runtime infrastructure services
        self.registry.register("Config", self.config)
        self.registry.register("EventBus", self.event_bus)
        self.registry.register("Queue", self.queue)
        self.registry.register("Telemetry", self.telemetry)
        self.registry.register("Security", self.security)
        self.registry.register("SearchService", self.search_service)

        # Lazy register CompanyBrainService
        try:
            from company_brain import global_company_brain_service
            self.registry.register("CompanyBrain", global_company_brain_service)
        except Exception as e:
            logger.error("module_register_error", f"Failed to register CompanyBrain: {e}")

        # Lazy register ResearchProviderManager
        try:
            from research.engine.provider_manager import global_research_manager
            self.registry.register("ResearchEngine", global_research_manager)
        except Exception as e:
            logger.error("module_register_error", f"Failed to register ResearchEngine: {e}")

        # Lazy register AutomationScheduler
        try:
            from automation.execution.scheduler import global_automation_scheduler
            self.registry.register("AutomationScheduler", global_automation_scheduler)
        except Exception as e:
            logger.error("module_register_error", f"Failed to register AutomationScheduler: {e}")

        self._is_initialized = True
        logger.info("kernel_started", "AVENIQ AI Runtime Kernel initialized successfully.")

    def get_diagnostics(self) -> Dict[str, Any]:
        """Synthesize complete live runtime diagnostics snapshot."""
        metrics = self.telemetry.get_metrics()
        services = self.registry.list_services()
        dead_jobs_count = len(self.dead_letter_queue.list_dead_jobs())
        queue_depth = self.queue.get_queue_size()

        return {
            "kernel_status": "active" if self._is_initialized else "bootstrap",
            "environment": self.config.env,
            "metrics": metrics,
            "registered_services": services,
            "queue_depth": queue_depth,
            "dead_jobs_count": dead_jobs_count,
            "recent_events_count": len(self.event_store.get_events(50))
        }

    def shutdown(self):
        """Perform graceful shutdown: drain queue, stop workers, flush telemetry."""
        logger.info("kernel_shutdown", "Shutting down AVENIQ AI Runtime Kernel...")
        self.queue.stop()
        self._is_initialized = False
        logger.info("kernel_stopped", "Runtime Kernel stopped cleanly.")


global_runtime_kernel = RuntimeKernel()
