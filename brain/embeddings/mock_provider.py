"""
Mock Embedding Provider for dry-run testing and local ingestion without external API calls.
"""

from typing import List
from brain.embeddings.base import EmbeddingProvider

class MockEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str = "mock-text-embedding-3-large", dimensions: int = 3072):
        self._model_name = model_name
        self._dimensions = dimensions

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def generate_embedding(self, text: str) -> List[float]:
        # Return deterministic mock vector based on string hash
        val = (abs(hash(text)) % 1000) / 1000.0
        return [val] * self._dimensions

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.generate_embedding(t) for t in texts]
