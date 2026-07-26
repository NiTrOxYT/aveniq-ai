"""
Production-Ready Capability-Based Real LLM Router.
Transparently routes inference requests to assigned providers (GPT-5, Gemini 2.5 Pro) based on department mappings,
supports prompt context building, fallback failovers, and cost tracking.
"""

from typing import Dict, Any, List, Optional
from integrations.llm.configuration.department_mapping import DepartmentMappingRegistry
from integrations.llm.context.context_builder import ContextBuilder
from integrations.llm.fallback.fallback_manager import FallbackManager
from integrations.llm.registry.provider_registry import global_llm_registry
from integrations.llm.providers.base import LLMResponseModel
from integrations.llm.monitoring.cost_tracker import global_cost_tracker

class RealLLMRouter:
    def __init__(self):
        self.fallback_manager = FallbackManager()

    def generate(self, prompt: str, department: str = "general", variables: Dict[str, Any] = None) -> LLMResponseModel:
        # 1. Resolve department assignment
        mapping = DepartmentMappingRegistry.get_config(department)
        target_provider = mapping.provider if mapping else "openai"

        # 2. Build context from prompt template
        full_context = ContextBuilder.build_context(department, variables) + f"\n\nUser Prompt:\n{prompt}"

        # 3. Execute inference with fallback
        response = self.fallback_manager.execute_with_fallback(
            department=department,
            prompt=full_context,
            target_provider=target_provider
        )

        return response

    def generate_department_inference(self, department: str, payload: Dict[str, Any] = None) -> LLMResponseModel:
        payload = payload or {}
        prompt = payload.get("prompt", f"Generate output for department {department}")
        return self.generate(prompt=prompt, department=department, variables=payload)

global_real_llm_router = RealLLMRouter()
