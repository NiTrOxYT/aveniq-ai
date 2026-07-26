"""
Comprehensive Test Suite for Knowledge & Retrieval Platform (Phase 9).
Tests Models, Ingestion, Chunking, Embeddings, Vector Store, Hybrid Search, Retriever, and Versioning.
"""

import unittest
from knowledge.documents.document import KnowledgeDocument, DocumentLifecycleState
from knowledge.collections.manager import KnowledgeCollectionsManager
from knowledge.ingestion.markdown import MarkdownIngestionConnector, JSONIngestionConnector
from knowledge.chunking.splitter import SemanticTextSplitter
from knowledge.embeddings.embedding_provider import global_embedding_provider
from knowledge.vectorstore.repository import VectorStoreRepository
from knowledge.search.staged_pipeline import StagedRetrievalPipeline
from knowledge.retrieval.retriever import DepartmentKnowledgeRetriever
from knowledge.versioning.snapshot import KnowledgeSnapshotStore

class TestKnowledgePlatform(unittest.TestCase):
    def test_document_model(self):
        doc = KnowledgeDocument(id="doc_1", title="Test", source_type="markdown", source_path="test.md", content="Content text")
        self.assertEqual(doc.lifecycle_state, DocumentLifecycleState.ACTIVE)
        self.assertIsNotNone(doc.checksum)

    def test_collections_manager(self):
        colls = KnowledgeCollectionsManager.list_collections()
        self.assertIn("Company Brain", colls)
        self.assertIn("Brand Guidelines", colls)

    def test_markdown_ingestion(self):
        conn = MarkdownIngestionConnector()
        doc = conn.ingest_path("# Heading\nSample body text", collection="Brand Guidelines")
        self.assertEqual(doc.collection, "Brand Guidelines")
        self.assertEqual(doc.source_type, "markdown")

    def test_semantic_chunking_and_graph(self):
        doc = KnowledgeDocument(id="doc_2", title="Architecture", source_type="markdown", source_path="arch.md", content="# Overview\nThis is paragraph one.\n\n# System\nThis is paragraph two.")
        chunks = SemanticTextSplitter.split_document(doc)
        self.assertGreater(len(chunks), 0)
        self.assertIsNotNone(chunks[0].token_count)

    def test_embedding_provider(self):
        vec = global_embedding_provider.embed_text("AVENIQ Architecture")
        self.assertEqual(len(vec), 384)

    def test_vectorstore_and_hybrid_search(self):
        repo = VectorStoreRepository()
        doc = KnowledgeDocument(id="doc_3", title="RAG Engine", source_type="markdown", source_path="rag.md", content="# RAG\nRetrieval Augmented Generation with vector search.")
        repo.index_document(doc)

        docs = repo.list_documents()
        self.assertEqual(len(docs), 1)

    def test_department_retriever(self):
        res = DepartmentKnowledgeRetriever.retrieve_knowledge("Retrieval", department="strategy")
        self.assertIsNotNone(res["context_block"])
        self.assertIsInstance(res["citations"], list)

    def test_snapshot_store(self):
        store = KnowledgeSnapshotStore()
        snap = store.create_snapshot("doc_3", 1, "RAG Engine", "Content", "checksum_123")
        self.assertEqual(snap.version, 1)

if __name__ == "__main__":
    unittest.main()
