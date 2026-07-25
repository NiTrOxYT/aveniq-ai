"""
Unit tests for Creative Department Context, Engine, Prompt Adapters, and Quality Gate.
"""

import unittest
from creative.context.builder import CreativeContextBuilder
from creative.directors.art_director import ArtDirector
from creative.specifications.visual_spec import VisualSpecificationBuilder
from creative.engine.creative_engine import CreativeEngine
from creative.utils.quality_gate import QualityGateVerifier

class TestCreativeDepartment(unittest.TestCase):
    def test_context_builder(self):
        ctx = CreativeContextBuilder.build_context("AI Agents")
        self.assertIsNotNone(ctx.planning_report)
        self.assertIsNotNone(ctx.content_package)
        self.assertEqual(ctx.brand_guidelines["brand_name"], "AVENIQ")

    def test_art_director(self):
        ctx = CreativeContextBuilder.build_context("AI Agents")
        style = ArtDirector.define_visual_style(ctx)
        self.assertIn("Dark Glassmorphism", style.style_name)
        self.assertIn("primary", style.color_palette)

    def test_visual_spec_and_prompts(self):
        spec = VisualSpecificationBuilder.build_visual_spec("AI Agents")
        self.assertIsNotNone(spec.prompts.midjourney_prompt)
        self.assertIsNotNone(spec.prompts.dalle3_prompt)
        self.assertIn("--ar 16:9", spec.prompts.midjourney_prompt)

    def test_creative_engine(self):
        engine = CreativeEngine()
        pkg = engine.generate_media_package("AI Agents in Enterprise Operations")
        self.assertIsNotNone(pkg)
        self.assertEqual(pkg.topic, "AI Agents in Enterprise Operations")
        self.assertGreater(pkg.scores.overall_score, 85.0)
        self.assertTrue(pkg.quality_gate.passed)

if __name__ == "__main__":
    unittest.main()
