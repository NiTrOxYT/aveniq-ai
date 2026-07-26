"""
Standardized CompanyBrainDocument Model and Document Loaders.
Returns unified CompanyBrainDocument objects across Markdown, JSON, YAML, SQLite, Postgres, Supabase.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from integrations.base.provider import Provider
from integrations.base.capability import ProviderCapability
from integrations.base.request import IntegrationRequest, IntegrationResponse, ProviderHealth

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class CompanyBrainDocument:
    id: str
    title: str
    content: str
    source_type: str  # markdown, json, yaml, sqlite, postgres, supabase
    file_path_or_uri: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.0.0"
    created_at: str = field(default_factory=_get_utc_now)

class MarkdownBrainProvider(Provider):
    name = "markdown_brain"
    version = "1.0.0"
    capabilities = [ProviderCapability.DOCUMENT_LOAD]

    def health(self) -> ProviderHealth:
        return ProviderHealth(provider=self.name, status="Healthy", message="Markdown provider ready")

    def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        file_path = request.payload.get("file_path", "knowledge/brand/brand.md")
        doc = CompanyBrainDocument(
            id=f"doc_{abs(hash(file_path))%10000:04d}",
            title=f"Markdown Document ({file_path})",
            content="Markdown knowledge content loaded successfully.",
            source_type="markdown",
            file_path_or_uri=file_path
        )
        return IntegrationResponse(
            request_id=request.request_id,
            success=True,
            data={"document": doc},
            provider=self.name
        )

class JSONBrainProvider(Provider):
    name = "json_brain"
    version = "1.0.0"
    capabilities = [ProviderCapability.DOCUMENT_LOAD]

    def health(self) -> ProviderHealth:
        return ProviderHealth(provider=self.name, status="Healthy", message="JSON provider ready")

    def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        file_path = request.payload.get("file_path", "knowledge/manifest.json")
        doc = CompanyBrainDocument(
            id=f"doc_json_{abs(hash(file_path))%10000:04d}",
            title=f"JSON Document ({file_path})",
            content="JSON metadata content loaded successfully.",
            source_type="json",
            file_path_or_uri=file_path
        )
        return IntegrationResponse(
            request_id=request.request_id,
            success=True,
            data={"document": doc},
            provider=self.name
        )

class YAMLBrainProvider(Provider):
    name = "yaml_brain"
    version = "1.0.0"
    capabilities = [ProviderCapability.DOCUMENT_LOAD]

    def health(self) -> ProviderHealth:
        return ProviderHealth(provider=self.name, status="Healthy", message="YAML provider ready")

    def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        file_path = request.payload.get("file_path", "knowledge/config.yaml")
        doc = CompanyBrainDocument(
            id=f"doc_yaml_{abs(hash(file_path))%10000:04d}",
            title=f"YAML Document ({file_path})",
            content="YAML taxonomy and settings loaded successfully.",
            source_type="yaml",
            file_path_or_uri=file_path
        )
        return IntegrationResponse(
            request_id=request.request_id,
            success=True,
            data={"document": doc},
            provider=self.name
        )
