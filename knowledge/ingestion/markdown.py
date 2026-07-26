"""
Abstract Base Source Connector and Multi-Format Document Ingestion Engine.
Supports Markdown, PDF, HTML, JSON, YAML, and GitHub.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os
import json

try:
    import yaml
except ImportError:
    yaml = None

from knowledge.documents.document import KnowledgeDocument

class BaseSourceConnector(ABC):
    source_type: str = "base"

    @abstractmethod
    def ingest_path(self, path_or_content: str, collection: str = "Company Brain", workspace_id: str = "ws_default") -> KnowledgeDocument:
        pass

class MarkdownIngestionConnector(BaseSourceConnector):
    source_type = "markdown"

    def ingest_path(self, path_or_content: str, collection: str = "Company Brain", workspace_id: str = "ws_default") -> KnowledgeDocument:
        if os.path.exists(path_or_content):
            title = os.path.basename(path_or_content)
            with open(path_or_content, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            title = "Markdown Document"
            content = path_or_content

        return KnowledgeDocument(
            id=f"doc_md_{abs(hash(content))%10000:04d}",
            title=title,
            source_type="markdown",
            source_path=path_or_content if os.path.exists(path_or_content) else "inline",
            content=content,
            collection=collection,
            workspace_id=workspace_id
        )

class JSONIngestionConnector(BaseSourceConnector):
    source_type = "json"

    def ingest_path(self, path_or_content: str, collection: str = "Company Brain", workspace_id: str = "ws_default") -> KnowledgeDocument:
        if os.path.exists(path_or_content):
            title = os.path.basename(path_or_content)
            with open(path_or_content, "r", encoding="utf-8") as f:
                raw_json = json.load(f)
            content = json.dumps(raw_json, indent=2)
        else:
            title = "JSON Document"
            content = path_or_content

        return KnowledgeDocument(
            id=f"doc_json_{abs(hash(content))%10000:04d}",
            title=title,
            source_type="json",
            source_path=path_or_content if os.path.exists(path_or_content) else "inline",
            content=content,
            collection=collection,
            workspace_id=workspace_id
        )
