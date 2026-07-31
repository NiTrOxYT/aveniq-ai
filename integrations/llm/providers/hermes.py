"""
Hermes 3 / OpenRouter LLM Provider for AVENIQ AI.
Provides advanced market intelligence, research synthesis, and competitor analysis.
Uses OpenRouter API ('nousresearch/hermes-3-llama-3.1-405b') when OPENROUTER_API_KEY / HERMES_API_KEY is present,
with automatic Gemini fallback.
"""

import os
import json
import logging
import urllib.request
from typing import Dict, Any, Optional
from integrations.llm.providers.base import BaseLLMProvider, LLMResponseModel
from integrations.llm.providers.gemini import RealGeminiProvider

logger = logging.getLogger("HermesProvider")

class RealHermesProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "nousresearch/hermes-3-llama-3.1-405b"):
        super().__init__()
        self.model_name = model_name
        self.api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("HERMES_API_KEY")
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.fallback_gemini = RealGeminiProvider()

    def generate(self, prompt: str, **kwargs) -> LLMResponseModel:
        system_prompt = kwargs.get("system_prompt") or (
            "You are Hermes 3, an elite autonomous market intelligence researcher and competitive strategist for enterprise SaaS companies. "
            "Analyze market trends, competitor moves, and growth vectors with deep analytical precision."
        )

        if self.api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://aveniq.ai",
                    "X-Title": "AVENIQ AI Engine"
                }
                payload = {
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": kwargs.get("temperature", 0.7),
                    "max_tokens": kwargs.get("max_tokens", 1024)
                }
                req = urllib.request.Request(
                    self.openrouter_url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    res_data = json.loads(resp.read().decode("utf-8"))
                    text = res_data["choices"][0]["message"]["content"]
                    logger.info("[HermesProvider] Successfully generated market research via OpenRouter/Hermes 3.")
                    return LLMResponseModel(
                        id=f"hermes_{abs(hash(prompt))%10000:04d}",
                        provider="hermes_openrouter",
                        model_name=self.model_name,
                        text_content=text,
                        metadata={"raw": res_data}
                    )
            except Exception as e:
                logger.warning(f"[HermesProvider] OpenRouter API failed ({e}). Falling back to Gemini with Hermes persona.")

        # Fallback to Gemini with Hermes Market Intelligence Persona
        full_prompt = f"{system_prompt}\n\nUSER PROMPT:\n{prompt}"
        res = self.fallback_gemini.generate(full_prompt, **kwargs)
        res.provider = "hermes_gemini_persona"
        return res
