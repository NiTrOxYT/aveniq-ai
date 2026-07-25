"""
Unit tests for Brain Loader Discovery Engine.
"""

import unittest
import os
from brain.loader.discovery import DiscoveryEngine

class TestDiscoveryEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DiscoveryEngine()

    def test_load_manifest_content(self):
        content = self.engine.load_manifest_content()
        self.assertIn("modules:", content)
        self.assertIn("AVENIQ", content)

    def test_discover_modules(self):
        modules = self.engine.discover_modules()
        self.assertIsInstance(modules, list)
        self.assertGreater(len(modules), 0)

        # Check for company and web-development modules
        mod_ids = [m["id"] for m in modules]
        self.assertIn("company", mod_ids)
        self.assertIn("services", mod_ids)

if __name__ == "__main__":
    unittest.main()
