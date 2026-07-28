"""
Service Registry & Dependency Injection Container for AVENIQ AI Runtime v1.
Modules register themselves and resolve services from the registry without direct import dependencies.
"""

import logging
from typing import Dict, Any, Optional, Type

logger = logging.getLogger("aveniq.runtime.service_registry")


class ServiceRegistry:
    def __init__(self):
        self._services: Dict[str, Any] = {}

    def register(self, service_name: str, instance: Any):
        """Register a service instance under a unique name."""
        self._services[service_name] = instance
        logger.info(f"[ServiceRegistry] Registered service '{service_name}'")

    def resolve(self, service_name: str) -> Any:
        """Resolve a registered service instance."""
        if service_name not in self._services:
            raise KeyError(f"Service '{service_name}' is not registered in ServiceRegistry.")
        return self._services[service_name]

    def has(self, service_name: str) -> bool:
        return service_name in self._services

    def list_services(self) -> Dict[str, str]:
        """Return dict of registered service names and their class names."""
        return {name: type(inst).__name__ for name, inst in self._services.items()}


global_service_registry = ServiceRegistry()
