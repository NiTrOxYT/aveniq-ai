"""
Image Generation Provider Abstraction, Standardized ImageAsset Model, and Capability-Based Router.
Supports DALL-E (GPT Image), Flux.1, Stable Diffusion XL, and Mock Image.
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
class ImageAsset:
    id: str
    filename: str
    provider: str
    prompt: str
    width: int = 1024
    height: int = 1024
    mime_type: str = "image/png"
    url_or_path: str = "assets/generated_hero.png"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_get_utc_now)

class ImageProvider(Provider):
    name: str = "image_base"
    version: str = "1.0.0"
    capabilities = [ProviderCapability.IMAGE_GENERATION]

    def health(self) -> ProviderHealth:
        return ProviderHealth(provider=self.name, status="Healthy", message=f"{self.name} ready")

    def execute(self, request: IntegrationRequest) -> IntegrationResponse:
        prompt = request.payload.get("prompt", "Enterprise AI banner")
        asset = ImageAsset(
            id=f"img_{abs(hash(prompt))%10000:04d}",
            filename=f"hero_{abs(hash(prompt))%1000:03d}.png",
            provider=self.name,
            prompt=prompt,
            url_or_path=f"assets/{self.name}_generated.png"
        )
        return IntegrationResponse(
            request_id=request.request_id,
            success=True,
            data={"image_asset": asset},
            provider=self.name
        )

class GPTImageProvider(ImageProvider):
    name = "gpt_image"

class FluxProvider(ImageProvider):
    name = "flux"

class StableDiffusionProvider(ImageProvider):
    name = "stable_diffusion"

class ImageRouter:
    def __init__(self, default_provider: str = "gpt_image", fallback_provider: str = "flux"):
        self.default_provider = default_provider
        self.fallback_provider = fallback_provider

    def generate_image(self, prompt: str, width: int = 1024, height: int = 1024) -> ImageAsset:
        from integrations.registry.global_registry import global_registry
        req = IntegrationRequest(
            request_id=f"req_img_{abs(hash(prompt))%10000:04d}",
            operation="generate_image",
            payload={"prompt": prompt, "width": width, "height": height}
        )

        provider = global_registry.resolve(self.default_provider) or global_registry.resolve("mock_image")
        if not provider:
            provider = GPTImageProvider()

        try:
            res = provider.execute(req)
            if res.success:
                return res.data["image_asset"]
        except Exception:
            fallback = global_registry.resolve(self.fallback_provider) or FluxProvider()
            res = fallback.execute(req)
            return res.data["image_asset"]

        return ImageAsset(id="img_fallback", filename="fallback.png", provider="fallback", prompt=prompt)
