"""
Embedding Provider Interface for AVENIQ Brain Loader.
Abstract base class supporting dependency injection for LLM embedding providers.
"""

from abc import ABC, abstractmethod
from typing import List

class EmbeddingProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    @property
    @abstractmethod
    def dimensions(self) -> int:
        pass

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Generate a single text embedding vector."""
        pass

    @abstractmethod
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate a batch of text embedding vectors."""
        pass
