"""
DependencyManager for Workflow Engine.
Declares department dependencies once and checks readiness before department execution.
"""

from typing import List, Dict, Any
from workflow.execution.package_registry import PackageRegistry

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
