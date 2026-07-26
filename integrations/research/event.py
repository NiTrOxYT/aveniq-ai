"""
Normalized MarketEvent Schema for Production Market Intelligence Data Collectors.
Provides a standardized event structure across all data sources (Reddit, GitHub, RSS, Google News, Product Hunt, Website Crawler).
Bridges seamlessly with ResearchDocument for backwards compatibility.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import hashlib

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def generate_event_id(source: str, url: str, title: str) -> str:
    """Generate deterministic SHA-256 event ID based on source, URL, and title."""
    raw = f"{source.lower()}:{url.strip().lower()}:{title.strip().lower()}"
    return f"evt_{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]}"

@dataclass
class MarketEvent:
    id: str
    source: str          # 'reddit', 'github', 'rss', 'google_news', 'product_hunt', 'website'
    category: str        # 'trends', 'launches', 'funding', 'discussions', 'competitors', 'general'
    title: str
    content: str
    url: str
    published_at: str = field(default_factory=_get_utc_now)
    author: str = "Anonymous"
    collected_at: str = field(default_factory=_get_utc_now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    freshness_score: float = 100.0
    credibility_score: float = 85.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "category": self.category,
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "published_at": self.published_at,
            "author": self.author,
            "collected_at": self.collected_at,
            "metadata": self.metadata,
            "confidence": self.confidence,
            "freshness_score": self.freshness_score,
            "credibility_score": self.credibility_score
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarketEvent":
        return cls(
            id=data.get("id", ""),
            source=data.get("source", "unknown"),
            category=data.get("category", "general"),
            title=data.get("title", ""),
            content=data.get("content", ""),
            url=data.get("url", ""),
            published_at=data.get("published_at", _get_utc_now()),
            author=data.get("author", "Anonymous"),
            collected_at=data.get("collected_at", _get_utc_now()),
            metadata=data.get("metadata", {}),
            confidence=float(data.get("confidence", 1.0)),
            freshness_score=float(data.get("freshness_score", 100.0)),
            credibility_score=float(data.get("credibility_score", 85.0))
        )

    def to_document(self):
        """Bridge convert to legacy ResearchDocument."""
        from integrations.research.document import ResearchDocument
        return ResearchDocument(
            id=self.id,
            source=self.source,
            title=self.title,
            url=self.url,
            author=self.author,
            published_at=self.published_at,
            collected_at=self.collected_at,
            tags=[self.source, self.category],
            summary=self.content[:300],
            content=self.content,
            engagement_metrics=self.metadata,
            metadata=self.metadata,
            freshness_score=self.freshness_score,
            credibility_score=self.credibility_score
        )
