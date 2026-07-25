"""
Filesystem Storage Provider for local JSON / JSONL caching.
"""

import os
import json
from typing import List, Optional, Dict, Any
from brain.storage.base import StorageProvider
from brain.models.schema import DocumentModel, ChunkModel
from brain.utils.logger import get_logger

logger = get_logger("aveniq.brain.storage.filesystem")

class FilesystemStorageProvider(StorageProvider):
    def __init__(self, output_dir: str = "brain_output"):
        self.output_dir = output_dir
        self.docs_dir = os.path.join(output_dir, "documents")
        self.chunks_dir = os.path.join(output_dir, "chunks")
        os.makedirs(self.docs_dir, exist_ok=True)
        os.makedirs(self.chunks_dir, exist_ok=True)

    def save_document(self, document: DocumentModel) -> bool:
        path = os.path.join(self.docs_dir, f"{document.id}.json")
        data = {
            "id": document.id,
            "title": document.title,
            "file_path": document.file_path,
            "content_type": document.content_type,
            "priority": document.priority,
            "embedding_enabled": document.embedding_enabled,
            "raw_content": document.raw_content,
            "frontmatter": document.frontmatter,
            "merged_metadata": document.merged_metadata,
            "created_at": document.created_at,
            "version": document.version
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True

    def get_document(self, doc_id: str) -> Optional[DocumentModel]:
        path = os.path.join(self.docs_dir, f"{doc_id}.json")
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
            return DocumentModel(
                id=d["id"],
                title=d["title"],
                file_path=d["file_path"],
                content_type=d["content_type"],
                priority=d["priority"],
                embedding_enabled=d["embedding_enabled"],
                raw_content=d["raw_content"],
                frontmatter=d.get("frontmatter", {}),
                merged_metadata=d.get("merged_metadata", {}),
                created_at=d.get("created_at", ""),
                version=d.get("version", "1.0.0")
            )

    def save_chunks(self, chunks: List[ChunkModel]) -> bool:
        for chunk in chunks:
            path = os.path.join(self.chunks_dir, f"{chunk.id}.json")
            data = {
                "id": chunk.id,
                "document_id": chunk.document_id,
                "document_title": chunk.document_title,
                "section_title": chunk.section_title,
                "heading_hierarchy": chunk.heading_hierarchy,
                "text": chunk.text,
                "token_estimate": chunk.token_estimate,
                "keywords": chunk.keywords,
                "metadata": chunk.metadata,
                "created_at": chunk.created_at
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        return True

    def get_chunks_for_document(self, doc_id: str) -> List[ChunkModel]:
        chunks = []
        if not os.path.exists(self.chunks_dir):
            return []
        for file in os.listdir(self.chunks_dir):
            if file.endswith(".json") and file.startswith(doc_id):
                with open(os.path.join(self.chunks_dir, file), "r", encoding="utf-8") as f:
                    c = json.load(f)
                    chunks.append(ChunkModel(
                        id=c["id"],
                        document_id=c["document_id"],
                        document_title=c["document_title"],
                        section_title=c["section_title"],
                        heading_hierarchy=c["heading_hierarchy"],
                        text=c["text"],
                        token_estimate=c["token_estimate"],
                        keywords=c["keywords"],
                        metadata=c.get("metadata", {}),
                        created_at=c.get("created_at", "")
                    ))
        return chunks

    def clear_all(self) -> bool:
        for folder in [self.docs_dir, self.chunks_dir]:
            if os.path.exists(folder):
                for f in os.listdir(folder):
                    os.remove(os.path.join(folder, f))
        logger.info("Cleared local filesystem storage.")
        return True
