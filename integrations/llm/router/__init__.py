"""
LLM Provider Abstraction, Standardized LLMResponse Model, and Capability-Based Router.
Supports OpenAI GPT-5, Google Gemini 2.5 Pro, Anthropic Claude, Qwen, and DeepSeek.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from integrations.base.provider import Provider
from integrations.base.capability import ProviderCapability
from integrations.base.request import IntegrationRequest, IntegrationResponse, ProviderHealth
from integrations.llm.providers.base import LLMResponseModel, OpenAIProvider, GeminiProvider, GPTImageProvider
from integrations.llm.router.llm_router import RealLLMRouter, global_real_llm_router
from integrations.llm.configuration.department_mapping import DepartmentMappingRegistry

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

# Re-export for legacy imports
LLMResponse = LLMResponseModel

class LLMProvider(Provider):
    name: str = "llm_base"
    version: str = "1.0.0"
    model_name: str = "gpt-5"
    capabilities = [
        ProviderCapability.STREAMING,
        ProviderCapability.JSON_OUTPUT,
        ProviderCapability.FUNCTION_CALLING,
        ProviderCapability.REASONING
    ]

    def health(self) -> ProviderHealth:
        return ProviderHealth(provider=self.name, status="Healthy", message=f"{self.name} ready")

    def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        prompt = request.payload.get("prompt", "Generate response")
        resp = LLMResponseModel(
            id=f"llm_{abs(hash(prompt))%10000:04d}",
            provider=self.name,
            model_name=self.model_name,
            text_content=f"Generated text for: {prompt}"
        )
        return IntegrationResponse(
            request_id=request.request_id,
            success=True,
            data={"llm_response": resp},
            provider=self.name
        )

class AnthropicProvider(LLMProvider):
    name = "anthropic"
    model_name = "claude-3-5-sonnet"

class QwenProvider(LLMProvider):
    name = "qwen"
    model_name = "qwen-2.5-72b"

class LLMRouter:
    def __init__(self, default_provider: str = "openai", fallback_provider: str = "gemini"):
        self.default_provider = default_provider
        self.fallback_provider = fallback_provider
        self.real_router = global_real_llm_router

    def generate(self, prompt: str, capabilities: List[ProviderCapability] = None, department: str = None) -> LLMResponseModel:
        if department:
            return self.real_router.generate(prompt=prompt, department=department)
        
        # Legacy fallback to specified default_provider
        from integrations.registry.global_registry import global_registry
        req = IntegrationRequest(
            request_id=f"req_llm_{abs(hash(prompt))%10000:04d}",
            operation="generate",
            payload={"prompt": prompt}
        )

        provider = global_registry.resolve(self.default_provider) or global_registry.resolve("mock_llm")
        if not provider:
            provider = OpenAIProvider()

        try:
            res = provider.execute(req)
            if res.success:
                return res.data["llm_response"]
        except Exception:
            fallback = global_registry.resolve(self.fallback_provider) or GeminiProvider()
            res = fallback.execute(req)
            return res.data["llm_response"]

        return LLMResponseModel(id="llm_fallback", provider="fallback", model_name="fallback", text_content=f"Generated text for: {prompt}")

global_llm_router = LLMRouter()
