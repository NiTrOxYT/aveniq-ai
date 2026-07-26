"""
Provider Abstract Base Class with Lifecycle methods for all integrations.
Every provider must implement initialize(), authenticate(), health(), execute(), and shutdown().
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from integrations.base.capability import ProviderCapability
from integrations.base.request import IntegrationRequest, IntegrationResponse, ProviderHealth

class Provider(ABC):
    name: str = ""
    version: str = "1.0.0"
    capabilities: List[ProviderCapability] = []

    def __init__(self):
        self._is_initialized = False
        self._is_authenticated = False

    def initialize(self) -> None:
        """Initialize provider resources."""
        self._is_initialized = True

    def authenticate(self) -> bool:
        """Authenticate credentials."""
        self._is_authenticated = True
        return True

    @abstractmethod
    def health(self) -> ProviderHealth:
        """Inspect provider health status."""
        pass

    @abstractmethod
    def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        """Execute request and return standardized response."""
        pass

    def shutdown(self) -> None:
        """Clean up provider resources."""
        self._is_initialized = False
        self._is_authenticated = False
