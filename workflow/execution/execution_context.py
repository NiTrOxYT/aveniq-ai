"""
Expanded ExecutionContext and DependencyManager for Workflow Engine.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from workflow.execution.package_registry import PackageRegistry
from workflow.events.event_bus import EventBus

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class ExecutionContext:
    execution_id: str
    workflow_id: str = "aveniq_master_workflow"
    started_at: str = field(default_factory=_get_utc_now)
    configuration: Dict[str, Any] = field(default_factory=dict)
    logger: Any = None
    package_registry: PackageRegistry = field(default_factory=PackageRegistry)
    metrics_collector: Any = None
    event_bus: EventBus = field(default_factory=EventBus)
    workflow_state: str = "PENDING"
    shared_memory: Dict[str, Any] = field(default_factory=dict)
    environment: str = "production"
    user_context: Dict[str, Any] = field(default_factory=dict)

class DependencyManager:
    DEPENDENCIES = {
        "company_brain": [],
        "market": [],
        "growth": [],
        "strategy": ["company_brain"],
        "calendar": ["strategy"],
        "planning": ["strategy", "calendar"],
        "content": ["planning"],
        "creative": ["planning", "content"],
        "editorial": ["content", "creative"],
        "delivery": ["editorial", "creative"],
        "approval": ["delivery"],
        "archive": ["delivery", "approval"],
        "learning": ["archive"]
    }

    @staticmethod
    def is_ready(department: str, registry: PackageRegistry) -> bool:
        required_deps = DependencyManager.DEPENDENCIES.get(department, [])
        for dep in required_deps:
            if not registry.exists(dep):
                return False
        return True

    @staticmethod
    def get_missing_dependencies(department: str, registry: PackageRegistry) -> List[str]:
        required_deps = DependencyManager.DEPENDENCIES.get(department, [])
        return [dep for dep in required_deps if not registry.exists(dep)]
