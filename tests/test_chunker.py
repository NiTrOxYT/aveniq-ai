"""
Unit tests for Brain Loader Heading-Based Semantic Chunker.
"""

import unittest
from brain.parser.markdown_parser import MarkdownParser
from brain.chunker.semantic_chunker import SemanticChunker
from brain.models.schema import DocumentModel

class TestSemanticChunker(unittest.TestCase):
    def setUp(self):
        self.parser = MarkdownParser()
        self.chunker = SemanticChunker(target_chunk_tokens=500, max_chunk_tokens=800)

    def test_chunk_document(self):
        md_text = """---
id: service_test
name: Test Service
---

# Test Service

## Overview

This is an overview of the test service. It provides modern software architecture solutions.

## Features

- Feature 1
- Feature 2
- Feature 3
"""
        fm, sections, title = self.parser.parse(md_text)
        doc = DocumentModel(
            id="test_doc",
            title=title,
            file_path="knowledge/test.md",
            content_type="md",
            priority=2,
            embedding_enabled=True,
            raw_content=md_text,
            frontmatter=fm,
            merged_metadata=fm,
            sections=sections
        )

        chunks = self.chunker.chunk_document(doc)
        self.assertGreater(len(chunks), 0)
        self.assertEqual(chunks[0].document_id, "test_doc")
        self.assertEqual(chunks[0].heading_hierarchy[0], "Test Service")
        self.assertGreater(chunks[0].token_estimate, 0)
        self.assertIsInstance(chunks[0].keywords, list)

if __name__ == "__main__":
    unittest.main()
