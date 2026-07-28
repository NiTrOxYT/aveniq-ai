"""
Worker Registry & Capability-Based Locator for AVENIQ AI Workers v2.1.
Registers AI Workers, resolves workers by capability, and aggregates workforce health telemetry.
"""

import logging
from typing import Dict, Any, List, Optional
from ai_workers.base_worker import BaseWorker

logger = logging.getLogger("aveniq.ai_workers.registry")


class WorkerRegistry:
    def __init__(self):
        self._workers: Dict[str, BaseWorker] = {}
        self._initialized = False

    def _ensure_default_workers(self):
        if self._initialized:
            return
        self._initialized = True
        try:
            from ai_workers.planner_worker import global_planner_worker
            from ai_workers.research_worker import global_research_worker
            from ai_workers.strategy_worker import global_strategy_worker
            from ai_workers.campaign_worker import global_campaign_worker
            from ai_workers.approval_worker import global_approval_worker
            from ai_workers.publishing_worker import global_publishing_worker
            from ai_workers.learning_worker import global_learning_worker

            for w in [
                global_planner_worker, global_research_worker, global_strategy_worker,
                global_campaign_worker, global_approval_worker, global_publishing_worker,
                global_learning_worker
            ]:
                self.register_worker(w)
        except Exception as e:
            logger.error(f"[WorkerRegistry] Error registering default workers: {e}")

    def register_worker(self, worker: BaseWorker):
        self._workers[worker.name] = worker
        logger.info(f"[WorkerRegistry] Registered AI Worker '{worker.name}' with capabilities: {list(worker.capabilities)}")

    def find_worker_by_capability(self, capability: str) -> Optional[BaseWorker]:
        """Resolve an active worker that advertises the required capability."""
        self._ensure_default_workers()
        for worker in self._workers.values():
            if worker.state != "disabled" and worker.can_handle(capability):
                return worker
        return None

    def get_worker(self, name: str) -> Optional[BaseWorker]:
        self._ensure_default_workers()
        return self._workers.get(name)

    def list_workers(self) -> List[Dict[str, Any]]:
        self._ensure_default_workers()
        return [w.health() for w in self._workers.values()]


global_worker_registry = WorkerRegistry()
