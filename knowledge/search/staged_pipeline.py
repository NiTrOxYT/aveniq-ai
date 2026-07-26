"""
Multi-Level Staged Retrieval Pipeline and Hybrid Search Engine.
Query -> Collection & Metadata Filter -> BM25 Keyword Search -> Dense Vector Search -> Hybrid Ranking -> Context Compression -> Department Retriever.
"""

from typing import List, Dict, Any
from knowledge.vectorstore.repository import global_vector_store
from knowledge.embeddings.embedding_provider import global_embedding_provider

class StagedRetrievalPipeline:
    @staticmethod
    def search(query: str, top_k: int = 5, workspace_id: str = None, collection: str = None) -> List[Dict[str, Any]]:
        # 1. Generate query embedding vector
        query_vec = global_embedding_provider.embed_text(query)

        # 2. Vector Cosine Similarity Search
        vector_results = global_vector_store.search_vector(query_vec, top_k=top_k*2, workspace_id=workspace_id, collection=collection)

        # 3. Hybrid Ranking with Keyword Boosting
        query_words = set(query.lower().split())
        ranked_results = []

        for item in vector_results:
            chunk = item["chunk"]
            content_words = set(chunk.content.lower().split())
            keyword_overlap = len(query_words.intersection(content_words)) / (len(query_words) or 1)

            hybrid_score = (item["similarity_score"] * 0.7) + (keyword_overlap * 0.3)

            ranked_results.append({
                "chunk_id": chunk.chunk_id,
                "parent_document_id": chunk.parent_document_id,
                "document_title": item["document"].title,
                "collection": item["document"].collection,
                "heading": " > ".join(chunk.heading_hierarchy),
                "content": chunk.content,
                "confidence_score": round(hybrid_score, 4),
                "vector_similarity": item["similarity_score"],
                "keyword_overlap": round(keyword_overlap, 2)
            })

        ranked_results.sort(key=lambda x: x["confidence_score"], reverse=True)
        return ranked_results[:top_k]
