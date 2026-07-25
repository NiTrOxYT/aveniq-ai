"""
Unit tests for Brain Loader Markdown Parser.
"""

import unittest
from brain.parser.markdown_parser import MarkdownParser

class TestMarkdownParser(unittest.TestCase):
    def setUp(self):
        self.parser = MarkdownParser()

    def test_parse_simple_markdown(self):
        md_text = """---
id: service_test
name: Test Service
---

# Test Service

## Overview

This is an overview of the test service.

- Feature 1
- Feature 2

## Technical Details

Paragraph explaining technical details.
"""
        frontmatter, sections, title = self.parser.parse(md_text)

        self.assertEqual(title, "Test Service")
        self.assertEqual(frontmatter.get("id"), "service_test")
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].title, "Overview")
        self.assertEqual(sections[1].title, "Technical Details")
        self.assertIn("Feature 1", sections[0].lists[0])

if __name__ == "__main__":
    unittest.main()
