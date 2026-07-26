"""
Embedding Provider Abstraction and Vector Generator.
Generates deterministic 384-dimensional dense vector embeddings for text chunks.
"""

from typing import List
import math

class EmbeddingProvider:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def embed_text(self, text: str) -> List[float]:
        # Fast, deterministic pseudo-embedding vector for RAG similarity calculation
        vector = [0.0] * self.dimension
        text_bytes = text.encode("utf-8")

        for i, b in enumerate(text_bytes):
            idx = (i + b) % self.dimension
            vector[idx] += math.sin(b * (i + 1)) * 0.1

        # Normalize vector to unit length
        norm = math.sqrt(sum(x * x for x in vector)) or 1.0
        return [round(x / norm, 5) for x in vector]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]

global_embedding_provider = EmbeddingProvider()
