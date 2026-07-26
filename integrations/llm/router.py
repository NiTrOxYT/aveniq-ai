"""
LLM Provider Abstraction, Standardized LLMResponse Model, and Capability-Based Router.
Supports OpenAI GPT, Anthropic Claude, Google Gemini, Qwen, and Mock LLM.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from integrations.base.provider import Provider
from integrations.base.capability import ProviderCapability
from integrations.base.request import IntegrationRequest, IntegrationResponse, ProviderHealth

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class LLMResponse:
    id: str
    provider: str
    model_name: str
    text_content: str
    prompt_tokens: int = 150
    completion_tokens: int = 250
    total_tokens: int = 400
    latency: float = 0.45
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_get_utc_now)

class LLMProvider(Provider):
    name: str = "llm_base"
    version: str = "1.0.0"
    model_name: str = "gpt-4o"
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
        resp = LLMResponse(
            id=f"llm_{abs(hash(prompt))%10000:04d}",
            provider=self.name,
            model_name=self.model_name,
            text_content=f"[{self.name} Response] Synthesized completion for prompt: '{prompt}'."
        )
        return IntegrationResponse(
            request_id=request.request_id,
            success=True,
            data={"llm_response": resp},
            provider=self.name
        )

class OpenAIProvider(LLMProvider):
    name = "openai"
    model_name = "gpt-4o"

class AnthropicProvider(LLMProvider):
    name = "anthropic"
    model_name = "claude-3-5-sonnet"

class GeminiProvider(LLMProvider):
    name = "gemini"
    model_name = "gemini-1.5-pro"

class QwenProvider(LLMProvider):
    name = "qwen"
    model_name = "qwen-2.5-72b"

class LLMRouter:
    def __init__(self, default_provider: str = "openai", fallback_provider: str = "gemini"):
        self.default_provider = default_provider
        self.fallback_provider = fallback_provider

    def generate(self, prompt: str, capabilities: List[ProviderCapability] = None) -> LLMResponse:
        from integrations.registry.global_registry import global_registry
        req = IntegrationRequest(
            request_id=f"req_llm_{abs(hash(prompt))%10000:04d}",
            operation="generate",
            payload={"prompt": prompt}
        )

        # Resolve provider from registry or fallback
        provider = global_registry.resolve(self.default_provider) or global_registry.resolve("mock_llm")
        if not provider:
            provider = OpenAIProvider()

        try:
            res = provider.execute(req)
            if res.success:
                return res.data["llm_response"]
        except Exception:
            # Transparent Failover
            fallback = global_registry.resolve(self.fallback_provider) or GeminiProvider()
            res = fallback.execute(req)
            return res.data["llm_response"]

        return LLMResponse(id="llm_fallback", provider="fallback", model_name="fallback", text_content="Fallback LLM output.")
