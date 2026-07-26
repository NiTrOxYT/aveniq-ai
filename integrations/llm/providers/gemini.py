"""
Production-Grade Google Gemini LLM Provider.
Quota-Aware, Configuration-Driven Automatic Model Fallback using official google-genai SDK.

Configuration (Environment Variables):
    GEMINI_API_KEY         - Google AI Studio API key (required)
    GEMINI_PRIMARY_MODEL   - Primary model name (default: gemini-2.5-pro)
    GEMINI_FALLBACK_MODELS- Comma-separated fallback models (default: gemini-3.6-flash,gemini-flash-latest,gemini-2.0-flash)
    GEMINI_IMAGE_MODEL     - Image model name (default: gemini-2.5-flash-image-preview)

No hardcoded model assumptions. Candidate models are evaluated in order; fallback occurs automatically on quota limits.
"""

import os
import re
import time
import logging
import uuid
import json
from typing import Dict, Any, List, Iterator, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone

from integrations.llm.providers.base import BaseLLMProvider, LLMResponseModel
from integrations.llm.monitoring.cost_tracker import global_cost_tracker
from integrations.base.request import IntegrationRequest, IntegrationResponse, ProviderHealth

log = logging.getLogger("aveniq.gemini.provider")


# --------------------------------------------------------------------------- #
#  Streaming response wrapper                                                  #
# --------------------------------------------------------------------------- #

@dataclass
class GeminiStreamChunk:
    text: str
    is_final: bool = False


# --------------------------------------------------------------------------- #
#  Exceptions                                                                  #
# --------------------------------------------------------------------------- #

class GeminiAuthError(RuntimeError):
    """Raised when the API key is invalid or missing."""

class GeminiQuotaError(RuntimeError):
    """Raised when all configured Gemini models have exceeded quota."""

class GeminiRateLimitError(RuntimeError):
    """Raised when temporary rate limit is encountered."""

class GeminiUnavailableError(RuntimeError):
    """Raised when the Gemini service or all candidate models are unavailable."""


# --------------------------------------------------------------------------- #
#  Production Gemini Provider                                                  #
# --------------------------------------------------------------------------- #

class RealGeminiProvider(BaseLLMProvider):
    """
    Quota-aware, configuration-driven Gemini Provider.
    Dynamically routes inference to the best available candidate model.
    """

    name = "gemini"
    enabled: bool = True

    _MAX_RETRIES_PER_MODEL = 2
    _DEFAULT_COOLDOWN_SEC = 60.0

    def __init__(self):
        self._client = None
        self._api_key: Optional[str] = None
        self._initialized = False

        # Cooldown & Status cache per model
        # model_name -> {"cooldown_expiry": float, "last_failure": float, "failure_reason": str, "status": str, "last_warned": float}
        self._cooldown_cache: Dict[str, Dict[str, Any]] = {}
        self._active_serving_model: Optional[str] = None
        self._last_fallback_reason: Optional[str] = None

    # ---------------------------------------------------------------------- #
    #  Configuration & Candidate Models                                        #
    # ---------------------------------------------------------------------- #

    @property
    def primary_model(self) -> str:
        return (
            os.environ.get("GEMINI_PRIMARY_MODEL")
            or os.environ.get("GEMINI_MODEL_TEXT")
            or "gemini-2.5-pro"
        ).strip()

    @property
    def fallback_models(self) -> List[str]:
        raw = os.environ.get("GEMINI_FALLBACK_MODELS", "gemini-3.6-flash,gemini-flash-latest,gemini-2.0-flash")
        models = [m.strip() for m in raw.split(",") if m.strip()]
        return models

    @property
    def candidate_models(self) -> List[str]:
        """Returns ordered, deduplicated candidate models [primary] + [fallbacks]."""
        models = [self.primary_model]
        for fb in self.fallback_models:
            if fb not in models:
                models.append(fb)
        return models

    @property
    def model_name(self) -> str:
        """Returns active serving model if set, else primary model."""
        return self._active_serving_model or self.primary_model

    @model_name.setter
    def model_name(self, value: str):
        self._active_serving_model = value

    # ---------------------------------------------------------------------- #
    #  Lazy Initialization (Zero Startup Probing)                              #
    # ---------------------------------------------------------------------- #

    def initialize(self):
        """Lazy initialization of the Gemini client. Does NOT make network calls."""
        if self._initialized:
            return

        self._api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not self._api_key:
            raise GeminiAuthError(
                "GEMINI_API_KEY environment variable is not set. Set it before starting AVENIQ."
            )

        try:
            from google import genai  # type: ignore
            self._client = genai.Client(api_key=self._api_key)
            self._initialized = True
            log.info(
                "[Gemini Provider] Initialized. Candidate models: %s",
                ", ".join(self.candidate_models)
            )
        except ImportError as e:
            raise RuntimeError(
                f"google-genai SDK import failed: {e}. Run: pip install google-genai"
            ) from e

    def shutdown(self):
        self._client = None
        self._initialized = False
        self._cooldown_cache.clear()
        self._active_serving_model = None
        log.info("[Gemini Provider] Shut down.")

    # ---------------------------------------------------------------------- #
    #  Quota & Delay Helpers                                                   #
    # ---------------------------------------------------------------------- #

    def _extract_retry_delay(self, err: Exception) -> float:
        """Extract retry delay from Google API RetryInfo or error text, defaulting to 60s."""
        err_str = str(err)
        # Regex match 'retryDelay': '37s' or 'retry in 37.7s'
        m = re.search(r"retry(?:Delay| in)[:\s]+'?" + r"(\d+(?:\.\d+)?)s?", err_str, re.IGNORECASE)
        if m:
            try:
                return max(float(m.group(1)), 5.0)
            except ValueError:
                pass
        return self._DEFAULT_COOLDOWN_SEC

    def _is_quota_exhaustion(self, err: Exception) -> bool:
        """Determines if the error represents quota exhaustion / resource limit."""
        err_str = str(err).lower()
        return any(
            k in err_str
            for k in (
                "resource_exhausted",
                "quotafailure",
                "quota exceeded",
                "limit: 0",
                "daily limit",
                "exceeded your current quota",
            )
        )

    def _is_non_retryable_auth_or_request(self, err: Exception) -> bool:
        """Determines if the error is unrecoverable for the API key / request format."""
        err_str = str(err).lower()
        return any(
            k in err_str
            for k in (
                "api_key",
                "invalid key",
                "unauthenticated",
                "permission_denied",
                "invalid argument",
            )
        )

    def _is_model_eligible(self, model: str, now: float) -> bool:
        """Check if model is eligible for traffic (not in active quota cooldown)."""
        cache = self._cooldown_cache.get(model)
        if not cache:
            return True
        expiry = cache.get("cooldown_expiry", 0)
        return now >= expiry

    def _mark_model_quota_exhausted(self, model: str, err: Exception, now: float):
        """Mark model as quota exhausted with calculated cooldown expiry and debounced warning."""
        delay = self._extract_retry_delay(err)
        expiry = now + delay

        cache = self._cooldown_cache.get(model, {})
        last_warned = cache.get("last_warned", 0)

        # Debounce log warning: at most 1 warning per cooldown window per model
        if now - last_warned > delay:
            next_model = next((m for m in self.candidate_models if m != model and self._is_model_eligible(m, now)), "None")
            log.warning(
                "[Gemini Provider] Quota exceeded for model '%s'. Primary: '%s'. Switching to: '%s'. Retry after: %.0f seconds. Error: %s",
                model, self.primary_model, next_model, delay, str(err)[:120]
            )
            last_warned = now

        self._cooldown_cache[model] = {
            "status": "QUOTA_EXHAUSTED",
            "cooldown_expiry": expiry,
            "last_failure": now,
            "failure_reason": str(err),
            "last_warned": last_warned,
            "retry_delay_sec": delay,
        }

    # ---------------------------------------------------------------------- #
    #  Health Check                                                            #
    # ---------------------------------------------------------------------- #

    def health(self) -> ProviderHealth:
        """
        Provider-wide health assessment.
        Returns HEALTHY if primary OR any fallback model is functioning.
        Returns DEGRADED if primary is unavailable but fallback is serving.
        Returns UNAVAILABLE only if ALL configured models fail or auth is invalid.
        """
        try:
            self.initialize()
        except GeminiAuthError as e:
            return ProviderHealth(
                provider=self.name,
                status="UNAVAILABLE",
                message=f"Auth failure: {e}"
            )
        except Exception as e:
            return ProviderHealth(
                provider=self.name,
                status="UNAVAILABLE",
                message=f"Initialization error: {e}"
            )

        now = time.time()
        candidates = self.candidate_models
        model_status_map: Dict[str, Dict[str, Any]] = {}
        working_model: Optional[str] = None
        first_error: Optional[str] = None

        for model in candidates:
            # Check cached cooldown first
            if not self._is_model_eligible(model, now):
                info = self._cooldown_cache.get(model, {})
                rem = max(0, int(info.get("cooldown_expiry", 0) - now))
                model_status_map[model] = {
                    "status": "QUOTA_EXHAUSTED",
                    "cooldown_remaining_sec": rem,
                    "failure_reason": info.get("failure_reason", "Quota exhausted")
                }
                continue

            try:
                # Probe model with 1-word generation
                self._client.models.generate_content(
                    model=model,
                    contents="ready"
                )
                model_status_map[model] = {"status": "READY"}
                if working_model is None:
                    working_model = model
            except Exception as e:
                first_error = first_error or str(e)
                if self._is_quota_exhaustion(e):
                    delay = self._extract_retry_delay(e)
                    model_status_map[model] = {
                        "status": "QUOTA_EXHAUSTED",
                        "cooldown_remaining_sec": int(delay),
                        "failure_reason": str(e)
                    }
                    self._mark_model_quota_exhausted(model, e, now)
                else:
                    model_status_map[model] = {
                        "status": "FAILED",
                        "failure_reason": str(e)
                    }

        if working_model == self.primary_model:
            self._active_serving_model = working_model
            self._last_fallback_reason = None
            msg_payload = {
                "status": "HEALTHY",
                "primary_model": self.primary_model,
                "active_model": working_model,
                "fallback_depth": 0,
                "reason": "Primary model functional",
                "models": model_status_map
            }
            return ProviderHealth(
                provider=self.name,
                status="HEALTHY",
                message=json.dumps(msg_payload)
            )
        elif working_model is not None:
            self._active_serving_model = working_model
            fallback_depth = candidates.index(working_model)
            reason = f"Primary model ({self.primary_model}) quota unavailable; serving via {working_model}"
            self._last_fallback_reason = reason
            msg_payload = {
                "status": "DEGRADED",
                "primary_model": self.primary_model,
                "active_model": working_model,
                "fallback_depth": fallback_depth,
                "reason": reason,
                "models": model_status_map
            }
            return ProviderHealth(
                provider=self.name,
                status="DEGRADED",
                message=json.dumps(msg_payload)
            )
        else:
            msg_payload = {
                "status": "UNAVAILABLE",
                "primary_model": self.primary_model,
                "active_model": "none",
                "fallback_depth": -1,
                "reason": f"All configured models failed: {first_error}",
                "models": model_status_map
            }
            return ProviderHealth(
                provider=self.name,
                status="UNAVAILABLE",
                message=json.dumps(msg_payload)
            )

    # ---------------------------------------------------------------------- #
    #  BaseLLMProvider Contract                                                #
    # ---------------------------------------------------------------------- #

    def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        prompt = request.payload.get("prompt", "")
        department = request.payload.get("department", "general")
        temperature = float(request.payload.get("temperature", 0.7))
        max_tokens = int(request.payload.get("max_tokens", 8192))

        response = self.generate(
            prompt=prompt,
            department=department,
            temperature=temperature,
            max_tokens=max_tokens,
            request_id=request.request_id,
        )

        return IntegrationResponse(
            request_id=request.request_id,
            success=True,
            data={"llm_response": response},
            provider=self.name
        )

    # ---------------------------------------------------------------------- #
    #  generate() with Automatic Model Fallback Loop                           #
    # ---------------------------------------------------------------------- #

    def generate(
        self,
        prompt: str,
        department: str = "general",
        temperature: float = 0.7,
        max_tokens: int = 8192,
        request_id: Optional[str] = None,
    ) -> LLMResponseModel:
        """
        Executes inference trying configured candidate models in priority order.
        Transparently recovers from quota limits by advancing to the next candidate.
        """
        self.initialize()
        request_id = request_id or f"gem_{uuid.uuid4().hex[:8]}"
        start_ts = time.monotonic()
        now = time.time()

        candidates = self.candidate_models
        # Filter eligible models, but if all are in cooldown, allow retrying the candidate with earliest expiry
        eligible = [m for m in candidates if self._is_model_eligible(m, now)]
        if not eligible:
            log.warning("[Gemini Provider] All candidate models in cooldown window. Forcing primary candidate retry.")
            eligible = candidates

        model_errors: Dict[str, str] = {}
        fallback_count = 0

        for candidate in eligible:
            # Attempt execution with retries for transient errors
            for attempt in range(1, self._MAX_RETRIES_PER_MODEL + 1):
                try:
                    response = self._call_api(candidate, prompt, temperature, max_tokens)
                    latency = round(time.monotonic() - start_ts, 3)

                    # Extract usage tokens
                    usage = getattr(response, "usage_metadata", None)
                    prompt_tokens = getattr(usage, "prompt_token_count", 0) or 0
                    completion_tokens = getattr(usage, "candidates_token_count", 0) or 0
                    if completion_tokens == 0:
                        completion_tokens = max(getattr(usage, "total_token_count", 0) - prompt_tokens, 0)

                    text = response.text or ""

                    # Successful candidate update
                    self._active_serving_model = candidate
                    if candidate != self.primary_model:
                        fallback_count = candidates.index(candidate)
                        self._last_fallback_reason = f"Primary model '{self.primary_model}' quota unavailable"
                    else:
                        self._last_fallback_reason = None

                    # Record cost using the ACTUAL serving model!
                    global_cost_tracker.record_usage(
                        execution_id=request_id,
                        department=department,
                        provider=self.name,
                        model=candidate,
                        prompt_tokens=max(prompt_tokens, 1),
                        completion_tokens=max(completion_tokens, 1),
                        latency_sec=latency,
                    )

                    log.info(
                        "[Gemini Provider] request_id=%s department=%s primary=%s serving=%s tokens=%d+%d latency=%.3fs status=OK",
                        request_id, department, self.primary_model, candidate,
                        prompt_tokens, completion_tokens, latency,
                    )

                    return LLMResponseModel(
                        id=request_id,
                        provider=self.name,
                        model_name=candidate,
                        text_content=text,
                        prompt_tokens=max(prompt_tokens, 1),
                        completion_tokens=max(completion_tokens, 1),
                        total_tokens=max(prompt_tokens + completion_tokens, 1),
                        latency=latency,
                        finish_reason="stop",
                        estimated_cost=0.0,
                        metadata={
                            "primary_model": self.primary_model,
                            "serving_model": candidate,
                            "fallback_count": fallback_count,
                            "fallback_reason": self._last_fallback_reason or "None",
                        }
                    )

                except Exception as e:
                    if self._is_non_retryable_auth_or_request(e):
                        log.error("[Gemini Provider] Unrecoverable error on model '%s': %s", candidate, e)
                        raise GeminiAuthError(f"Gemini authentication / request error: {e}") from e

                    if self._is_quota_exhaustion(e):
                        # Quota limit — set cooldown and break retry loop to move to NEXT candidate model
                        self._mark_model_quota_exhausted(candidate, e, time.time())
                        model_errors[candidate] = f"QUOTA_EXHAUSTED: {e}"
                        break  # Move to next candidate model in candidates list!

                    # Transient error — apply retry delay for current candidate
                    delay = self._extract_retry_delay(e)
                    log.warning(
                        "[Gemini Provider] Transient error on candidate '%s' (attempt %d/%d, delay=%.1fs): %s",
                        candidate, attempt, self._MAX_RETRIES_PER_MODEL, delay, e
                    )
                    if attempt < self._MAX_RETRIES_PER_MODEL:
                        time.sleep(min(delay, 2.0))
                    else:
                        model_errors[candidate] = f"FAILED: {e}"

        raise GeminiUnavailableError(
            f"All configured Gemini models failed. Primary: '{self.primary_model}'. Errors: {model_errors}"
        )

    # ---------------------------------------------------------------------- #
    #  stream()                                                                #
    # ---------------------------------------------------------------------- #

    def stream(
        self,
        prompt: str,
        department: str = "general",
        temperature: float = 0.7,
        max_tokens: int = 8192,
    ) -> Iterator[GeminiStreamChunk]:
        """
        Streams tokens from the active available Gemini model.
        """
        self.initialize()
        from google.genai import types as genai_types  # type: ignore

        config = genai_types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        now = time.time()
        candidates = [m for m in self.candidate_models if self._is_model_eligible(m, now)] or self.candidate_models

        for candidate in candidates:
            accumulated = []
            try:
                for chunk in self._client.models.generate_content_stream(
                    model=candidate,
                    contents=prompt,
                    config=config,
                ):
                    chunk_text = chunk.text or ""
                    accumulated.append(chunk_text)
                    yield GeminiStreamChunk(text=chunk_text, is_final=False)

                self._active_serving_model = candidate
                yield GeminiStreamChunk(text="".join(accumulated), is_final=True)
                return

            except Exception as e:
                if self._is_quota_exhaustion(e):
                    self._mark_model_quota_exhausted(candidate, e, time.time())
                    log.warning("[Gemini Stream] Quota limit on model '%s'. Retrying with next model.", candidate)
                    continue
                else:
                    log.error("[Gemini Stream] Streaming error on candidate '%s': %s", candidate, e)
                    raise

        raise GeminiUnavailableError("All configured Gemini models failed during stream request.")

    # ---------------------------------------------------------------------- #
    #  Private helpers                                                         #
    # ---------------------------------------------------------------------- #

    def _call_api(self, model: str, prompt: str, temperature: float, max_tokens: int):
        from google.genai import types as genai_types  # type: ignore

        config = genai_types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        return self._client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
