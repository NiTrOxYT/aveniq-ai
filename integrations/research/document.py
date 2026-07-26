"""
Extended ResearchDocument Schema with Freshness and Credibility Metadata.
Also exports legacy connectors and MarketPackage data model for backwards compatibility.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from integrations.base.provider import Provider
from integrations.base.capability import ProviderCapability
from integrations.base.request import IntegrationResponse, ProviderHealth

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class ResearchDocument:
    id: str
    source: str
    title: str
    url: str
    author: str = "Anonymous"
    published_at: str = field(default_factory=_get_utc_now)
    collected_at: str = field(default_factory=_get_utc_now)
    tags: List[str] = field(default_factory=list)
    summary: str = ""
    content: str = ""
    engagement_metrics: Dict[str, Any] = field(default_factory=dict)
    language: str = "en"
    metadata: Dict[str, Any] = field(default_factory=dict)
    freshness_score: float = 100.0  # 0 to 100
    credibility_score: float = 85.0  # 0 to 100
    expires_at: Optional[str] = None

@dataclass
class MarketPackage:
    id: str
    date: str
    summary: str
    signals: Dict[str, Any]
    trends: List[str]
    audience_insights: Dict[str, Any]
    competitor_notes: List[str]
    sources: List[str]
    opportunities: List[str]

class BaseConnectorProvider(Provider):
    name: str = "base_connector"
    capabilities: set = {ProviderCapability.WEB_SEARCH}

    def execute(self, request) -> IntegrationResponse:
        return IntegrationResponse(
            request_id=getattr(request, "request_id", "req_mock"),
            success=True,
            data={"document": {"title": "Mock Title", "url": "https://example.com"}},
            provider=self.name
        )

    def health(self) -> ProviderHealth:
        return ProviderHealth(provider=self.name, status="Healthy", message="Connector active")

class RedditConnector(BaseConnectorProvider):
    name = "reddit"

class HackerNewsConnector(BaseConnectorProvider):
    name = "hackernews"

class GitHubTrendingConnector(BaseConnectorProvider):
    name = "github"

def __getattr__(name: str):
    if name == "ResearchAggregator":
        from integrations.research.aggregation.aggregator import ResearchAggregator
        return ResearchAggregator
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
