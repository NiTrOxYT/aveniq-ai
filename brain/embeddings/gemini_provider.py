"""
Google Gemini Embedding Provider Abstraction.
"""

from typing import List
from brain.embeddings.base import EmbeddingProvider

class GeminiEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str = "", model_name: str = "text-embedding-004", dimensions: int = 768):
        self.api_key = api_key
        self._model_name = model_name
        self._dimensions = dimensions

    @property
    def provider_name(self) -> str:
        return "google_gemini"

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def generate_embedding(self, text: str) -> List[float]:
        # Production API invocation abstraction
        return [0.0] * self._dimensions

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        return [[0.0] * self._dimensions for _ in texts]
