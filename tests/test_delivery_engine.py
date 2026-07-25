"""
Unit tests for Delivery Department Context, Bundles, Manifest, Exporters, and Engine.
"""

import unittest
from delivery.context.builder import DeliveryContextBuilder
from delivery.platforms.linkedin import DedicatedBundleBuilder
from delivery.manifest.manifest_builder import DeliveryManifestBuilder
from delivery.engine.delivery_engine import DeliveryEngine

class TestDeliveryDepartment(unittest.TestCase):
    def test_context_builder(self):
        ctx = DeliveryContextBuilder.build_context("AI Agents")
        self.assertIsNotNone(ctx.approved_content_package)
        self.assertIsNotNone(ctx.media_package)
        self.assertIsNotNone(ctx.research_package)

    def test_bundle_builder(self):
        ctx = DeliveryContextBuilder.build_context("AI Agents")
        bundles = DedicatedBundleBuilder.build_all_bundles(ctx)
        self.assertIn("linkedin", bundles)
        self.assertIn("instagram", bundles)
        self.assertEqual(len(bundles), 8)

    def test_manifest_builder(self):
        ctx = DeliveryContextBuilder.build_context("AI Agents")
        bundles = DedicatedBundleBuilder.build_all_bundles(ctx)
        manifest = DeliveryManifestBuilder.build_manifest("del_test_001", "AI Agents", bundles, ctx)
        self.assertEqual(manifest.delivery_status, "READY")
        self.assertIn("hero.webp", manifest.checksums)

    def test_delivery_engine(self):
        engine = DeliveryEngine()
        pkg = engine.assemble_delivery_package("AI Agents in Enterprise Operations")
        self.assertIsNotNone(pkg)
        self.assertEqual(pkg.topic, "AI Agents in Enterprise Operations")
        self.assertEqual(pkg.manifest.delivery_status, "READY")
        self.assertGreater(pkg.scores.overall_delivery_score, 85.0)
        self.assertTrue(pkg.quality_gate.passed)

if __name__ == "__main__":
    unittest.main()
