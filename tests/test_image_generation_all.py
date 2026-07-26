"""
Comprehensive Test Suite for Image Generation Platform (Phase 10).
Tests Models, Templates, Gemini Provider, Prompt Orchestrator, Brand Validator, Image Router, and Asset Store.
"""

import unittest
from image_generation.models.asset import VisualAsset, GenerationJob, AssetApprovalStatus
from image_generation.templates.templates import TemplateEngine
from image_generation.providers.gemini_image import GeminiImageProvider
from image_generation.branding.consistency_engine import VisualConsistencyEngine, BrandStyleGuide, BrandValidator
from image_generation.router.image_router import InternalPromptOrchestrator, CampaignImageRouter
from image_generation.storage.asset_store import AssetLibraryStore

class TestImageGenerationPlatform(unittest.TestCase):
    def test_templates_engine(self):
        hero_tpl = TemplateEngine.get_template("hero")
        self.assertEqual(hero_tpl.aspect_ratio, "16:9")
        self.assertEqual(hero_tpl.width, 1920)

        carousel_tpl = TemplateEngine.get_template("carousel")
        self.assertEqual(carousel_tpl.aspect_ratio, "1:1")

    def test_gemini_image_provider(self):
        prov = GeminiImageProvider()
        health = prov.health()
        self.assertEqual(health["status"], "Healthy")

        res = prov.generate_image("Modern AI Banner", width=1920, height=1080)
        self.assertTrue(res.success)
        self.assertIn("assets", res.image_url_or_path)

    def test_prompt_orchestrator(self):
        prompt = InternalPromptOrchestrator.translate_intent_to_prompt(
            "thumbnail",
            {"topic": "AI Agents", "visual_theme": "High Tech"}
        )
        self.assertIn("THUMBNAIL", prompt)
        self.assertIn("AI Agents", prompt)

    def test_brand_validator(self):
        asset = VisualAsset(
            asset_id="ast_01",
            campaign_id="cmp_01",
            template_type="hero",
            platform="website",
            file_path="assets/test.png",
            width=1920,
            height=1080,
            aspect_ratio="16:9"
        )
        style = BrandStyleGuide(workspace_id="ws_01")
        res = BrandValidator.validate_asset(asset, style)
        self.assertTrue(res["passed"])
        self.assertGreater(res["brand_score"], 90.0)

    def test_campaign_image_router(self):
        router = CampaignImageRouter()
        job = router.generate_campaign_assets(
            campaign_id="cmp_100",
            creative_package_data={"topic": "AI Agents"},
            requested_templates=["hero", "thumbnail", "linkedin"]
        )
        self.assertEqual(job.status, "COMPLETED")
        self.assertEqual(len(job.generated_assets), 3)

    def test_asset_library_store(self):
        store = AssetLibraryStore()
        asset = VisualAsset(
            asset_id="ast_10",
            campaign_id="cmp_100",
            template_type="hero",
            platform="website",
            file_path="assets/hero.png",
            width=1920,
            height=1080,
            aspect_ratio="16:9"
        )
        store.save_asset(asset)
        retrieved = store.get_asset("ast_10")
        self.assertIsNotNone(retrieved)

        updated = store.update_feedback("ast_10", "More Premium")
        self.assertEqual(updated.version, 2)
        self.assertEqual(updated.feedback_tag, "More Premium")

if __name__ == "__main__":
    unittest.main()
