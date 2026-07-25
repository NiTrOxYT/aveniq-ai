"""
Unit tests for Brain Loader Metadata Merger.
"""

import unittest
from brain.loader.metadata_merger import MetadataMerger

class TestMetadataMerger(unittest.TestCase):
    def setUp(self):
        self.merger = MetadataMerger()

    def test_merge_metadata(self):
        file_path = "knowledge/services/web-development.md"
        frontmatter = {"id": "service_web_development", "name": "Web Development"}

        merged = self.merger.merge(file_path, frontmatter)

        self.assertEqual(merged.get("id"), "service_web_development")
        self.assertIn("graph_relationships", merged)
        self.assertIn("taxonomy_ref", merged)
        self.assertEqual(merged.get("company_name"), "AVENIQ")

if __name__ == "__main__":
    unittest.main()
