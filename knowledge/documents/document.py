"""
KnowledgeDocument and DocumentChunk Data Models with Lifecycle States and Rich Metadata.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime, timezone
import hashlib

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class DocumentLifecycleState(str, Enum):
    DRAFT = "DRAFT"
    INDEXING = "INDEXING"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    SUPERSEDED = "SUPERSEDED"
    DELETED = "DELETED"

@dataclass
class DocumentChunk:
    chunk_id: str
    parent_document_id: str
    content: str
    heading_hierarchy: List[str] = field(default_factory=list)
    previous_chunk_id: Optional[str] = None
    next_chunk_id: Optional[str] = None
    embedding: List[float] = field(default_factory=list)
    token_count: int = 150
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class KnowledgeDocument:
    id: str
    title: str
    source_type: str  # markdown, pdf, html, json, yaml, github
    source_path: str
    content: str
    workspace_id: str = "ws_default"
    collection: str = "Company Brain"
    author: str = "AVENIQ System"
    lifecycle_state: DocumentLifecycleState = DocumentLifecycleState.ACTIVE
    tags: List[str] = field(default_factory=list)
    checksum: str = ""
    chunks: List[DocumentChunk] = field(default_factory=list)
    version: int = 1
    created_at: str = field(default_factory=_get_utc_now)
    updated_at: str = field(default_factory=_get_utc_now)

    def __post_init__(self):
        if not self.checksum and self.content:
            self.checksum = hashlib.sha256(self.content.encode("utf-8")).hexdigest()
