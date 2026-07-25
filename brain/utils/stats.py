"""
Statistics Aggregator for AVENIQ Brain Loader.
Calculates document counts, chunk counts, token estimates, average chunk sizes,
and embedding cost estimates.
"""

from typing import List, Dict, Any
from brain.models.schema import DocumentModel, ChunkModel

class StatsAggregator:
    @staticmethod
    def calculate(documents: List[DocumentModel], chunks: List[ChunkModel]) -> Dict[str, Any]:
        doc_count = len(documents)
        chunk_count = len(chunks)
        total_tokens = sum(c.token_estimate for c in chunks)
        avg_chunk_tokens = int(total_tokens / chunk_count) if chunk_count > 0 else 0

        services_indexed = sum(1 for d in documents if "services/" in d.file_path and d.file_path.endswith(".md"))
        glossary_terms = 0
        taxonomy_categories = 0

        for d in documents:
            if "glossary.md" in d.file_path:
                glossary_terms = d.raw_content.count("#### ")
            if "taxonomy.yaml" in d.file_path:
                taxonomy_categories = d.raw_content.count(":")

        # OpenAI text-embedding-3-large cost: ~$0.00013 per 1,000 tokens
        estimated_embedding_cost_usd = round((total_tokens / 1000.0) * 0.00013, 6)

        return {
            "document_count": doc_count,
            "chunk_count": chunk_count,
            "total_token_count": total_tokens,
            "average_chunk_size_tokens": avg_chunk_tokens,
            "services_indexed": services_indexed,
            "glossary_terms_count": glossary_terms,
            "taxonomy_categories_count": taxonomy_categories,
            "estimated_embedding_cost_usd": f"${estimated_embedding_cost_usd:.6f}"
        }
