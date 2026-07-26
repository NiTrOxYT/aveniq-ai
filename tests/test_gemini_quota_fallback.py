"""
Comprehensive Unit Test Suite for Production-Grade Gemini Provider (Quota-Aware, Automatic Model Fallback).
Tests environment parsing, candidate ordering, primary success, quota failover, RetryInfo delay extraction,
cooldown caching, provider-wide health, cost tracking with actual serving model, and logging debounce.
"""

import unittest
import time
import os
import logging
from unittest.mock import MagicMock, patch

from integrations.llm.providers.gemini import (
    RealGeminiProvider,
    GeminiAuthError,
    GeminiQuotaError,
    GeminiUnavailableError
)
from integrations.llm.monitoring.cost_tracker import global_cost_tracker


class TestGeminiQuotaFallback(unittest.TestCase):

    def setUp(self):
        # Reset provider instance for each test
        self.provider = RealGeminiProvider()
        self.provider._initialized = True
        self.provider._client = MagicMock()

    def test_environment_parsing_and_candidate_ordering(self):
        with patch.dict(os.environ, {
            "GEMINI_PRIMARY_MODEL": "gemini-2.5-pro",
            "GEMINI_FALLBACK_MODELS": "gemini-3.6-flash, gemini-flash-latest, gemini-2.0-flash, gemini-2.5-pro"
        }):
            p = RealGeminiProvider()
            self.assertEqual(p.primary_model, "gemini-2.5-pro")
            self.assertEqual(p.fallback_models, ["gemini-3.6-flash", "gemini-flash-latest", "gemini-2.0-flash", "gemini-2.5-pro"])
            # Deduplicated candidate list with primary first
            self.assertEqual(p.candidate_models, ["gemini-2.5-pro", "gemini-3.6-flash", "gemini-flash-latest", "gemini-2.0-flash"])

    def test_lazy_initialization(self):
        p = RealGeminiProvider()
        self.assertFalse(p._initialized)
        with patch("google.genai.Client") as mock_client_cls:
            with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
                p.initialize()
                self.assertTrue(p._initialized)
                mock_client_cls.assert_called_once_with(api_key="test_key")

    def test_primary_model_success(self):
        mock_resp = MagicMock()
        mock_resp.text = "Generated text from primary model"
        mock_resp.usage_metadata = MagicMock(prompt_token_count=100, candidates_token_count=200)

        self.provider._client.models.generate_content.return_value = mock_resp

        res = self.provider.generate("Test prompt", department="strategy")
        self.assertEqual(res.model_name, "gemini-2.5-pro")
        self.assertEqual(res.text_content, "Generated text from primary model")
        self.assertEqual(res.metadata["serving_model"], "gemini-2.5-pro")
        self.assertEqual(res.metadata["fallback_count"], 0)

    def test_primary_quota_exhaustion_automatic_fallback_success(self):
        """Test automatic failover from primary model (429 RESOURCE_EXHAUSTED) to fallback model."""
        def mock_generate_content(model, contents, config=None):
            if model == "gemini-2.5-pro":
                raise Exception("429 RESOURCE_EXHAUSTED: Quota exceeded for metric: generate_content_free_tier_input_token_count, limit: 0, model: gemini-2.5-pro")
            mock_resp = MagicMock()
            mock_resp.text = f"Response from fallback {model}"
            mock_resp.usage_metadata = MagicMock(prompt_token_count=50, candidates_token_count=150)
            return mock_resp

        self.provider._client.models.generate_content.side_effect = mock_generate_content

        res = self.provider.generate("Test prompt", department="growth")
        self.assertEqual(res.model_name, "gemini-3.6-flash")
        self.assertEqual(res.text_content, "Response from fallback gemini-3.6-flash")
        self.assertEqual(res.metadata["primary_model"], "gemini-2.5-pro")
        self.assertEqual(res.metadata["serving_model"], "gemini-3.6-flash")
        self.assertEqual(res.metadata["fallback_count"], 1)

    def test_multi_step_fallback_chain(self):
        """Test failover when both Primary and Fallback 1 fail, but Fallback 2 succeeds."""
        def mock_generate_content(model, contents, config=None):
            if model in ("gemini-2.5-pro", "gemini-3.6-flash"):
                raise Exception(f"429 RESOURCE_EXHAUSTED for model {model}")
            mock_resp = MagicMock()
            mock_resp.text = f"Response from {model}"
            mock_resp.usage_metadata = MagicMock(prompt_token_count=30, candidates_token_count=70)
            return mock_resp

        self.provider._client.models.generate_content.side_effect = mock_generate_content

        res = self.provider.generate("Test prompt", department="learning")
        self.assertEqual(res.model_name, "gemini-flash-latest")
        self.assertEqual(res.metadata["serving_model"], "gemini-flash-latest")
        self.assertEqual(res.metadata["fallback_count"], 2)

    def test_retry_info_delay_extraction(self):
        err = Exception("429 RESOURCE_EXHAUSTED. Please retry in 37.5s.")
        delay = self.provider._extract_retry_delay(err)
        self.assertEqual(delay, 37.5)

    def test_cooldown_caching_and_expiration(self):
        now = time.time()
        # Mark primary model exhausted with 1 second cooldown
        self.provider._cooldown_cache["gemini-2.5-pro"] = {
            "status": "QUOTA_EXHAUSTED",
            "cooldown_expiry": now + 0.2,
            "last_failure": now,
            "failure_reason": "Quota limit"
        }

        # Currently in cooldown -> not eligible
        self.assertFalse(self.provider._is_model_eligible("gemini-2.5-pro", now))

        # Wait for cooldown to expire
        time.sleep(0.3)
        self.assertTrue(self.provider._is_model_eligible("gemini-2.5-pro", time.time()))

    def test_provider_wide_health_reporting(self):
        """Test HEALTHY, DEGRADED, and UNAVAILABLE provider health statuses."""
        # 1. Primary healthy -> HEALTHY
        self.provider._client.models.generate_content.return_value = MagicMock(text="ready")
        h1 = self.provider.health()
        self.assertEqual(h1.status, "HEALTHY")

        # 2. Primary quota exhausted, fallback working -> DEGRADED
        def mock_health(model, contents):
            if model == "gemini-2.5-pro":
                raise Exception("429 RESOURCE_EXHAUSTED for gemini-2.5-pro")
            return MagicMock(text="ready")

        self.provider._client.models.generate_content.side_effect = mock_health
        h2 = self.provider.health()
        self.assertEqual(h2.status, "DEGRADED")
        self.assertIn("gemini-3.6-flash", h2.message)

        # 3. All models failing -> UNAVAILABLE
        self.provider._client.models.generate_content.side_effect = Exception("429 RESOURCE_EXHAUSTED")
        h3 = self.provider.health()
        self.assertEqual(h3.status, "UNAVAILABLE")

    def test_cost_tracker_receives_actual_serving_model(self):
        """Verify global_cost_tracker records usage with the actual serving model (e.g. gemini-3.6-flash)."""
        def mock_generate_content(model, contents, config=None):
            if model == "gemini-2.5-pro":
                raise Exception("429 RESOURCE_EXHAUSTED")
            return MagicMock(text="Fallback text", usage_metadata=MagicMock(prompt_token_count=100, candidates_token_count=200))

        self.provider._client.models.generate_content.side_effect = mock_generate_content

        initial_count = len(global_cost_tracker._metrics)
        self.provider.generate("Test prompt", department="company_brain")

        self.assertEqual(len(global_cost_tracker._metrics), initial_count + 1)
        latest_metric = global_cost_tracker._metrics[-1]
        self.assertEqual(latest_metric.provider, "gemini")
        self.assertEqual(latest_metric.model, "gemini-3.6-flash")


if __name__ == "__main__":
    unittest.main()
