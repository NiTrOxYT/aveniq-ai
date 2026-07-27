"""
Internal Prompt Orchestrator and Campaign-Level Multi-Asset Image Router.
Translates CreativePackage design intent into provider prompts internally and executes GenerationJob batches.
"""

from typing import List, Dict, Any, Optional
from image_generation.models.asset import VisualAsset, CarouselAsset, GenerationJob, AssetApprovalStatus
from image_generation.templates.templates import TemplateEngine
from image_generation.branding.consistency_engine import VisualConsistencyEngine, BrandStyleGuide, BrandValidator
from image_generation.providers.gemini_image import GeminiImageProvider

class InternalPromptOrchestrator:
    @staticmethod
    def translate_intent_to_prompt(template_type: str, creative_package_data: Dict[str, Any]) -> str:
        topic = creative_package_data.get("topic", "Autonomous AI Marketing")
        theme = creative_package_data.get("visual_theme", "High Tech Glassmorphic 3D Vector")
        audience = creative_package_data.get("target_audience", "Enterprise CTOs")
        cta = creative_package_data.get("call_to_action", "Explore AVENIQ AI")

        return f"Professional {template_type.upper()} graphic for '{topic}'. Visual Theme: {theme}. Audience: {audience}. CTA: '{cta}'."

class CampaignImageRouter:
    def __init__(self, provider=None):
        self.provider = provider or get_image_provider()

    def generate_campaign_assets(self, campaign_id: str, creative_package_data: Dict[str, Any], requested_templates: List[str] = None, workspace_id: str = "ws_default") -> GenerationJob:
        requested = requested_templates or ["hero", "carousel", "infographic", "thumbnail", "linkedin"]
        style_guide = BrandStyleGuide(workspace_id=workspace_id)
        job = GenerationJob(job_id=f"job_{campaign_id}", campaign_id=campaign_id, workspace_id=workspace_id, requested_templates=requested)

        generated_assets: List[VisualAsset] = []

        for i, t_type in enumerate(requested):
            tpl = TemplateEngine.get_template(t_type)
            raw_prompt = InternalPromptOrchestrator.translate_intent_to_prompt(t_type, creative_package_data)
            locked_prompt = VisualConsistencyEngine.apply_style_lock(raw_prompt, style_guide)

            res = self.provider.generate_image(locked_prompt, width=tpl.width, height=tpl.height)

            asset = VisualAsset(
                asset_id=f"ast_{campaign_id}_{t_type}_{i+1:02d}",
                campaign_id=campaign_id,
                template_type=t_type,
                platform=tpl.platform,
                file_path=res.image_url_or_path,
                width=tpl.width,
                height=tpl.height,
                aspect_ratio=tpl.aspect_ratio,
                prompt_used=locked_prompt,
                provider_used=self.provider.provider_name
            )
            # Perform Brand Validation
            BrandValidator.validate_asset(asset, style_guide)
            generated_assets.append(asset)

        job.generated_assets = generated_assets
        job.status = "COMPLETED"
        return job

global_campaign_image_router = CampaignImageRouter()
