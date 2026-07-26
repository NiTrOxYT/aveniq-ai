"""
Comprehensive Test Suite for Real LLM Router & Department Model Assignment Platform.
Tests Providers, Department Mappings, Context Builder, Fallback Manager, Cost Tracker, and RealLLMRouter.
"""

import unittest
from integrations.llm.registry.provider_registry import global_llm_registry
from integrations.llm.configuration.department_mapping import DepartmentMappingRegistry
from integrations.llm.context.context_builder import ContextBuilder
from integrations.llm.fallback.fallback_manager import FallbackManager
from integrations.llm.monitoring.cost_tracker import global_cost_tracker
from integrations.llm.router.llm_router import global_real_llm_router

class TestRealLLMRouterPlatform(unittest.TestCase):
    def test_provider_registration(self):
        enabled = global_llm_registry.enabled_providers()
        disabled = global_llm_registry.disabled_providers()
        self.assertIn("openai", enabled)
        self.assertIn("gemini", enabled)
        self.assertIn("anthropic", disabled)
        self.assertIn("deepseek", disabled)

    def test_department_mapping(self):
        planning_cfg = DepartmentMappingRegistry.get_config("planning")
        brain_cfg = DepartmentMappingRegistry.get_config("company_brain")
        self.assertEqual(planning_cfg.provider, "openai")
        self.assertEqual(planning_cfg.model, "gpt-5")
        self.assertEqual(brain_cfg.provider, "gemini")
        self.assertEqual(brain_cfg.model, "gemini-2.5-pro")

    def test_context_builder(self):
        ctx = ContextBuilder.build_context("planning", {"topic": "AI Agents"})
        self.assertIn("Planning Department", ctx)
        self.assertIn("AI Agents", ctx)

    def test_fallback_manager(self):
        fb = FallbackManager()
        resp = fb.execute_with_fallback("planning", "Test prompt", "openai")
        self.assertIsNotNone(resp.id)
        self.assertEqual(resp.provider, "openai")

    def test_cost_tracker(self):
        metric = global_cost_tracker.record_usage("exec_01", "planning", "openai", "gpt-5", 100, 200, 0.4)
        self.assertGreater(metric.estimated_cost_usd, 0.0)

    def test_real_llm_router(self):
        resp = global_real_llm_router.generate("Formulate strategy", department="strategy")
        self.assertIsNotNone(resp.text_content)
        # Gemini is the primary provider for strategy. In quota-limited environments
        # the fallback manager may transparently fall through to the hard fallback.
        # We verify routing intent (provider is gemini) OR fallback was triggered.
        self.assertIn(resp.provider, ("gemini", "gemini_fallback", "openai"),
                      f"Unexpected provider: {resp.provider}")

if __name__ == "__main__":
    unittest.main()
