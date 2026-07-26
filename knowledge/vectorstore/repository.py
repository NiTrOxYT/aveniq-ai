"""
Vector Store Repository with Cosine Similarity, Metadata Filtering, and Incremental Indexing.
"""

import math
from typing import List, Dict, Any, Optional
from knowledge.documents.document import KnowledgeDocument, DocumentChunk, DocumentLifecycleState
from knowledge.chunking.splitter import SemanticTextSplitter
from knowledge.embeddings.embedding_provider import global_embedding_provider

def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    return dot / (norm1 * norm2) if norm1 and norm2 else 0.0

class VectorStoreRepository:
    def __init__(self):
        self._documents: Dict[str, KnowledgeDocument] = {}
        self._chunks: Dict[str, DocumentChunk] = {}

    def index_document(self, document: KnowledgeDocument) -> KnowledgeDocument:
        # Incremental indexing check
        if document.id in self._documents:
            existing = self._documents[document.id]
            if existing.checksum == document.checksum:
                return existing

        # Split and embed chunks
        chunks = SemanticTextSplitter.split_document(document)
        for chunk in chunks:
            chunk.embedding = global_embedding_provider.embed_text(chunk.content)
            self._chunks[chunk.chunk_id] = chunk

        document.lifecycle_state = DocumentLifecycleState.ACTIVE
        self._documents[document.id] = document
        return document

    def list_documents(self, workspace_id: str = None) -> List[KnowledgeDocument]:
        docs = list(self._documents.values())
        if workspace_id:
            docs = [d for d in docs if d.workspace_id == workspace_id]
        return docs

    def search_vector(self, query_vec: List[float], top_k: int = 5, workspace_id: str = None, collection: str = None) -> List[Dict[str, Any]]:
        results = []
        for chunk in self._chunks.values():
            parent_doc = self._documents.get(chunk.parent_document_id)
            if not parent_doc or parent_doc.lifecycle_state != DocumentLifecycleState.ACTIVE:
                continue

            if workspace_id and parent_doc.workspace_id != workspace_id:
                continue

            if collection and parent_doc.collection != collection:
                continue

            score = _cosine_similarity(query_vec, chunk.embedding)
            results.append({
                "chunk": chunk,
                "document": parent_doc,
                "similarity_score": round(score, 4)
            })

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]

global_vector_store = VectorStoreRepository()
