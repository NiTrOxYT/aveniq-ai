"""
Comprehensive Integration Test Suite for AVENIQ External Integration Platform.
Tests ProviderRegistry, Capabilities, LLMRouter, ImageRouter, ResearchConnectors, CompanyBrainConnectors, Caching, and Observability.
"""

import unittest
from integrations.registry.global_registry import global_registry
from integrations.base.capability import ProviderCapability
from integrations.base.request import IntegrationRequest
from integrations.llm.router import LLMRouter
from integrations.image.router import ImageRouter
from integrations.company_brain.document import MarkdownBrainProvider, JSONBrainProvider
from integrations.research.document import RedditConnector, HackerNewsConnector, ResearchAggregator
from integrations.cache.memory import MemoryCacheProvider
from integrations.monitoring.metrics import global_metrics
from integrations.observability.tracing import global_tracer, IntegrationTrace, SystemDiagnostics

class TestIntegrationPlatform(unittest.TestCase):
    def test_provider_registry(self):
        providers = global_registry.list_providers()
        self.assertIn("mock_llm", providers)
        self.assertIn("openai", providers)
        self.assertIn("gpt_image", providers)

        cap_providers = global_registry.resolve_by_capability(ProviderCapability.STREAMING)
        self.assertGreater(len(cap_providers), 0)

    def test_llm_router(self):
        router = LLMRouter(default_provider="mock_llm")
        response = router.generate("Test LLM prompt")
        self.assertIsNotNone(response.id)
        self.assertEqual(response.provider, "mock_llm")
        self.assertIn("Generated text for", response.text_content)

    def test_image_router(self):
        router = ImageRouter(default_provider="mock_image")
        asset = router.generate_image("Enterprise AI Banner")
        self.assertIsNotNone(asset.id)
        self.assertEqual(asset.provider, "mock_image")
        self.assertTrue(asset.filename.endswith(".png"))

    def test_company_brain_connectors(self):
        md_provider = MarkdownBrainProvider()
        req = IntegrationRequest(request_id="req_md", operation="load", payload={"file_path": "knowledge/brand.md"})
        res = md_provider.execute(req)
        self.assertTrue(res.success)
        doc = res.data["document"]
        self.assertEqual(doc.source_type, "markdown")

    def test_research_connectors_and_aggregator(self):
        reddit = RedditConnector()
        hn = HackerNewsConnector()
        req = IntegrationRequest(request_id="req_res", operation="fetch", payload={"topic": "AI Agents"})
        
        doc1 = reddit.execute(req).data["document"]
        doc2 = hn.execute(req).data["document"]

        summary = ResearchAggregator.aggregate([doc1, doc2])
        self.assertEqual(summary["total_documents"], 2)
        self.assertIn("Reddit", summary["sources"])

    def test_cache_provider(self):
        cache = MemoryCacheProvider(ttl_seconds=10)
        cache.set("key1", {"data": 123})
        self.assertEqual(cache.get("key1"), {"data": 123})
        self.assertIsNone(cache.get("non_existent"))

    def test_observability_tracing(self):
        trace = IntegrationTrace(request_id="t_001", provider="mock_llm", operation="generate", latency=0.05)
        global_tracer.record_trace(trace)
        diags = SystemDiagnostics.inspect(global_tracer)
        self.assertGreater(diags["total_requests"], 0)

if __name__ == "__main__":
    unittest.main()
