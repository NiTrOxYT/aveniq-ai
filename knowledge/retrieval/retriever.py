"""
Evidence Citation Builder and Department Knowledge Retriever.
Automatically auto-indexes knowledge base files if vector store is empty.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import os
from knowledge.search.staged_pipeline import StagedRetrievalPipeline
from knowledge.vectorstore.repository import global_vector_store
from knowledge.ingestion.markdown import MarkdownIngestionConnector

@dataclass
class EvidenceCitation:
    citation_id: str
    source_document: str
    section_heading: str
    collection: str
    confidence_score: float
    excerpt: str

class DepartmentKnowledgeRetriever:
    @staticmethod
    def _ensure_indexed():
        if not global_vector_store.list_documents():
            conn = MarkdownIngestionConnector()
            default_paths = [
                "knowledge/company/company.md",
                "knowledge/brand/brand.md"
            ]
            for p in default_paths:
                if os.path.exists(p):
                    doc = conn.ingest_path(p, collection="Company Brain")
                    global_vector_store.index_document(doc)

    @classmethod
    def retrieve_knowledge(cls, query: str, department: str = "general", workspace_id: str = "ws_default", collection: str = None) -> Dict[str, Any]:
        cls._ensure_indexed()

        raw_passages = StagedRetrievalPipeline.search(
            query=query,
            top_k=4,
            workspace_id=workspace_id,
            collection=collection
        )

        citations = []
        passages_text = []

        for i, item in enumerate(raw_passages):
            cit_id = f"cit_{department[:3]}_{i+1:02d}"
            citations.append(EvidenceCitation(
                citation_id=cit_id,
                source_document=item["document_title"],
                section_heading=item["heading"],
                collection=item["collection"],
                confidence_score=item["confidence_score"],
                excerpt=item["content"][:120] + "..."
            ))
            passages_text.append(f"[{cit_id} | Doc: {item['document_title']} | Heading: {item['heading']}]\n{item['content']}")

        return {
            "query": query,
            "department": department,
            "passages_count": len(raw_passages),
            "context_block": "\n\n".join(passages_text),
            "citations": citations
        }
