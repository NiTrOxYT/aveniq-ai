"""
Data models for the AVENIQ Brain Loader.
Represents Documents, Chunks, Embeddings, Relationships, Taxonomy, Metadata, and Versions.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class SectionNode:
    title: str
    level: int
    content: str
    subsections: List['SectionNode'] = field(default_factory=list)
    paragraphs: List[str] = field(default_factory=list)
    lists: List[List[str]] = field(default_factory=list)

@dataclass
class DocumentModel:
    id: str
    title: str
    file_path: str
    content_type: str  # markdown, yaml, json
    priority: int
    embedding_enabled: bool
    raw_content: str
    frontmatter: Dict[str, Any] = field(default_factory=dict)
    merged_metadata: Dict[str, Any] = field(default_factory=dict)
    sections: List[SectionNode] = field(default_factory=list)
    created_at: str = field(default_factory=_get_utc_now)
    version: str = "1.0.0"

@dataclass
class ChunkModel:
    id: str
    document_id: str
    document_title: str
    section_title: str
    heading_hierarchy: List[str]
    text: str
    token_estimate: int
    keywords: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class EmbeddingModel:
    id: str
    chunk_id: str
    provider: str
    model_name: str
    vector: List[float]
    dimensions: int
    created_at: str = field(default_factory=_get_utc_now)

@dataclass
class RelationshipEdge:
    source_id: str
    target_id: str
    relationship_type: str  # dependency, enhancement, cross_link
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TaxonomyNode:
    category: str
    values: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VersionModel:
    version: str
    applied_at: str
    description: str
