"""
Centralized ProviderRegistry for discovery, registration, resolution, and health inspection.
Routers resolve providers through ProviderRegistry instead of hardcoded mappings.
"""

from typing import Dict, List, Optional
from integrations.base.provider import Provider
from integrations.base.capability import ProviderCapability
from integrations.base.request import ProviderHealth

class ProviderRegistry:
    def __init__(self):
        self._providers: Dict[str, Provider] = {}

    def register(self, provider: Provider) -> None:
        provider.initialize()
        provider.authenticate()
        self._providers[provider.name] = provider

    def unregister(self, provider_name: str) -> bool:
        if provider_name in self._providers:
            self._providers[provider_name].shutdown()
            del self._providers[provider_name]
            return True
        return False

    def resolve(self, provider_name: str) -> Optional[Provider]:
        return self._providers.get(provider_name)

    def resolve_by_capability(self, capability: ProviderCapability) -> List[Provider]:
        return [
            p for p in self._providers.values()
            if capability in p.capabilities
        ]

    def list_providers(self) -> List[str]:
        return list(self._providers.keys())

    def list_capabilities(self) -> Dict[str, List[str]]:
        res = {}
        for p in self._providers.values():
            res[p.name] = [c.value for c in p.capabilities]
        return res

    def health_summary(self) -> Dict[str, ProviderHealth]:
        return {name: p.health() for name, p in self._providers.items()}

# Global Registry Instance
global_registry = ProviderRegistry()
