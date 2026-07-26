"""
Mock Provider Framework for testing environments without requiring external API credentials.
Provides MockLLMProvider, MockImageProvider, MockResearchProvider, and MockCompanyBrainProvider.
"""

from integrations.base.provider import Provider
from integrations.base.capability import ProviderCapability
from integrations.base.request import IntegrationRequest, IntegrationResponse, ProviderHealth
from integrations.company_brain.document import CompanyBrainDocument
from integrations.research.document import ResearchDocument
from integrations.llm.router import LLMResponse
from integrations.image.router import ImageAsset

class MockLLMProvider(Provider):
    name = "mock_llm"
    version = "1.0.0"
    capabilities = [
        ProviderCapability.STREAMING,
        ProviderCapability.JSON_OUTPUT,
        ProviderCapability.FUNCTION_CALLING,
        ProviderCapability.REASONING
    ]

    def health(self) -> ProviderHealth:
        return ProviderHealth(provider=self.name, status="Healthy", message="Mock LLM ready")

    def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        prompt = request.payload.get("prompt", "")
        resp = LLMResponse(
            id="mock_llm_001",
            provider=self.name,
            model_name="mock-model-v1",
            text_content=f"[Mock LLM Output] Generated text for: '{prompt}'"
        )
        return IntegrationResponse(
            request_id=request.request_id,
            success=True,
            data={"llm_response": resp},
            provider=self.name
        )

class MockImageProvider(Provider):
    name = "mock_image"
    version = "1.0.0"
    capabilities = [ProviderCapability.IMAGE_GENERATION]

    def health(self) -> ProviderHealth:
        return ProviderHealth(provider=self.name, status="Healthy", message="Mock Image ready")

    def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        prompt = request.payload.get("prompt", "")
        asset = ImageAsset(
            id="mock_img_001",
            filename="mock_hero.png",
            provider=self.name,
            prompt=prompt,
            url_or_path="assets/mock_generated.png"
        )
        return IntegrationResponse(
            request_id=request.request_id,
            success=True,
            data={"image_asset": asset},
            provider=self.name
        )

class MockResearchProvider(Provider):
    name = "mock_research"
    version = "1.0.0"
    capabilities = [ProviderCapability.RESEARCH_FETCH]

    def health(self) -> ProviderHealth:
        return ProviderHealth(provider=self.name, status="Healthy", message="Mock Research ready")

    def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        topic = request.payload.get("topic", "")
        doc = ResearchDocument(
            id="mock_res_001",
            source_name="Mock Research",
            topic=topic,
            summary=f"Mock research document for topic: '{topic}'",
            url="https://example.com/mock-research"
        )
        return IntegrationResponse(
            request_id=request.request_id,
            success=True,
            data={"document": doc},
            provider=self.name
        )

class MockCompanyBrainProvider(Provider):
    name = "mock_brain"
    version = "1.0.0"
    capabilities = [ProviderCapability.DOCUMENT_LOAD]

    def health(self) -> ProviderHealth:
        return ProviderHealth(provider=self.name, status="Healthy", message="Mock Brain ready")

    def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        doc = CompanyBrainDocument(
            id="mock_brain_001",
            title="Mock Company Brain Document",
            content="Mock Company Brain knowledge content.",
            source_type="mock",
            file_path_or_uri="knowledge/mock.md"
        )
        return IntegrationResponse(
            request_id=request.request_id,
            success=True,
            data={"document": doc},
            provider=self.name
        )
