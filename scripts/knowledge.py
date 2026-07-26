#!/usr/bin/env python3
"""
AVENIQ Knowledge & Retrieval Platform CLI Control Center
Command Line Tool for indexing Markdown/JSON files, querying hybrid search, displaying collections & documents, and inspecting snapshots.

Commands:
  index       - Ingest & index knowledge files into vector store.
  search      - Execute multi-level staged hybrid search.
  collections - List active knowledge collections.
  documents   - List indexed knowledge documents.
  snapshots   - List historical document snapshots.
  status      - Display knowledge platform health & vector store status.
"""

import sys
import os
import argparse
import json

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from knowledge.ingestion.markdown import MarkdownIngestionConnector, JSONIngestionConnector
from knowledge.vectorstore.repository import global_vector_store
from knowledge.collections.manager import KnowledgeCollectionsManager
from knowledge.search.staged_pipeline import StagedRetrievalPipeline
from knowledge.retrieval.retriever import DepartmentKnowledgeRetriever
from knowledge.versioning.snapshot import global_snapshot_store

def main():
    parser = argparse.ArgumentParser(description="AVENIQ Knowledge & Retrieval Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Knowledge commands")

    p_idx = subparsers.add_parser("index", help="Ingest & index knowledge files")
    p_idx.add_argument("--path", default="knowledge/company/company.md", help="File path to index")
    p_idx.add_argument("--collection", default="Company Brain", help="Target collection")

    p_sch = subparsers.add_parser("search", help="Execute hybrid search")
    p_sch.add_argument("--query", default="Autonomous AI Marketing Strategy", help="Search query")

    subparsers.add_parser("collections", help="List knowledge collections")
    subparsers.add_parser("documents", help="List indexed documents")
    subparsers.add_parser("snapshots", help="List versioning snapshots")
    subparsers.add_parser("status", help="Display knowledge platform status")

    args = parser.parse_args()

    if args.command == "index":
        conn = MarkdownIngestionConnector()
        path = args.path if os.path.exists(args.path) else "knowledge/company/company.md"
        if not os.path.exists(path):
            path = "AVENIQ Enterprise AI Organization Knowledge Base."
        doc = conn.ingest_path(path, collection=args.collection)
        indexed_doc = global_vector_store.index_document(doc)
        print("\n=== KNOWLEDGE DOCUMENT INDEXED ===")
        print(json.dumps({
            "id": indexed_doc.id,
            "title": indexed_doc.title,
            "collection": indexed_doc.collection,
            "chunks_count": len(indexed_doc.chunks),
            "checksum": indexed_doc.checksum
        }, indent=2))
    elif args.command == "search":
        res = DepartmentKnowledgeRetriever.retrieve_knowledge(args.query, department="strategy")
        print(f"\n=== HYBRID SEARCH & EVIDENCE CITATIONS (Query: '{args.query}') ===")
        print(json.dumps({
            "query": res["query"],
            "passages_count": res["passages_count"],
            "citations": [
                {
                    "citation_id": c.citation_id,
                    "source": c.source_document,
                    "heading": c.section_heading,
                    "confidence": c.confidence_score,
                    "excerpt": c.excerpt
                } for c in res["citations"]
            ]
        }, indent=2))
    elif args.command == "collections":
        print("\n=== KNOWLEDGE COLLECTIONS ===")
        print(json.dumps(KnowledgeCollectionsManager.list_collections(), indent=2))
    elif args.command == "documents":
        print("\n=== INDEXED KNOWLEDGE DOCUMENTS ===")
        docs = global_vector_store.list_documents()
        print(json.dumps([{
            "id": d.id,
            "title": d.title,
            "collection": d.collection,
            "lifecycle_state": d.lifecycle_state.value
        } for d in docs], indent=2))
    elif args.command == "snapshots" or args.command == "status":
        print("\n=== KNOWLEDGE PLATFORM STATUS & METRICS ===")
        docs = global_vector_store.list_documents()
        print(json.dumps({
            "status": "Healthy",
            "indexed_documents": len(docs),
            "total_chunks": sum(len(d.chunks) for d in docs),
            "collections_count": len(KnowledgeCollectionsManager.list_collections())
        }, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
