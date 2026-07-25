"""
Storage Provider Interface for AVENIQ Brain Loader.
Abstract base class for storage implementations using dependency injection.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from brain.models.schema import DocumentModel, ChunkModel, EmbeddingModel

class StorageProvider(ABC):
    @abstractmethod
    def save_document(self, document: DocumentModel) -> bool:
        pass

    @abstractmethod
    def get_document(self, doc_id: str) -> Optional[DocumentModel]:
        pass

    @abstractmethod
    def save_chunks(self, chunks: List[ChunkModel]) -> bool:
        pass

    @abstractmethod
    def get_chunks_for_document(self, doc_id: str) -> List[ChunkModel]:
        pass

    @abstractmethod
    def clear_all(self) -> bool:
        pass
