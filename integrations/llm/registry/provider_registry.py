"""
Centralized LLM Provider Registry.
Supports dynamic registration, resolution, provider capability checks, enabled/disabled filtering, and health summary.
"""

from typing import Dict, Any, List, Optional
from integrations.llm.providers.base import (
    OpenAIProvider, GPTImageProvider, GeminiProvider, AnthropicProvider, DeepSeekProvider, QwenProvider
)

class LLMProviderRegistry:
    def __init__(self):
        self._providers: Dict[str, Any] = {}

    def register(self, provider_instance: Any):
        self._providers[provider_instance.name] = provider_instance

    def unregister(self, name: str):
        self._providers.pop(name, None)

    def resolve(self, name: str) -> Optional[Any]:
        return self._providers.get(name)

    def enabled_providers(self) -> List[str]:
        return [name for name, p in self._providers.items() if getattr(p, "enabled", True)]

    def disabled_providers(self) -> List[str]:
        return [name for name, p in self._providers.items() if not getattr(p, "enabled", True)]

    def health_summary(self) -> Dict[str, Any]:
        summary = {}
        for name, p in self._providers.items():
            health = p.health()
            summary[name] = {
                "status": health.status,
                "model": getattr(p, "model_name", "unknown"),
                "enabled": getattr(p, "enabled", True),
                "message": health.message
            }
        return summary

global_llm_registry = LLMProviderRegistry()

# Register Production & Skeleton Providers
global_llm_registry.register(OpenAIProvider())
global_llm_registry.register(GPTImageProvider())
global_llm_registry.register(GeminiProvider())
global_llm_registry.register(AnthropicProvider())
global_llm_registry.register(DeepSeekProvider())
global_llm_registry.register(QwenProvider())
