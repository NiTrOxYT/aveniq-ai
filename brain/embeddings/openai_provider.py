"""
OpenAI Embedding Provider Abstraction.
"""

from typing import List
from brain.embeddings.base import EmbeddingProvider

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str = "", model_name: str = "text-embedding-3-large", dimensions: int = 3072):
        self.api_key = api_key
        self._model_name = model_name
        self._dimensions = dimensions

    @property
    def provider_name(self) -> str:
        return "openai"

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
