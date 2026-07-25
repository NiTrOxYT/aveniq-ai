"""
Structured Markdown AST Parser for AVENIQ Brain Loader.
Parses YAML frontmatter, headings, sections, lists, tables, and paragraphs.
"""

import re
from typing import List, Dict, Any, Tuple
from brain.models.schema import SectionNode

class MarkdownParser:
    def parse(self, raw_content: str) -> Tuple[Dict[str, Any], List[SectionNode], str]:
        frontmatter, content_body = self._extract_frontmatter(raw_content)
        title = self._extract_document_title(content_body, frontmatter)
        sections = self._parse_sections(content_body, title)
        return frontmatter, sections, title

    def _extract_frontmatter(self, raw_content: str) -> Tuple[Dict[str, Any], str]:
        frontmatter = {}
        content_body = raw_content

        if raw_content.startswith("---"):
            parts = raw_content.split("---", 2)
            if len(parts) >= 3:
                fm_raw = parts[1].strip()
                content_body = parts[2].strip()
                frontmatter = self._parse_yaml_basic(fm_raw)

        return frontmatter, content_body

    def _parse_yaml_basic(self, fm_raw: str) -> Dict[str, Any]:
        try:
            import yaml
            return yaml.safe_load(fm_raw) or {}
        except Exception:
            fm = {}
            for line in fm_raw.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    fm[k] = v
            return fm

    def _extract_document_title(self, body: str, frontmatter: Dict[str, Any]) -> str:
        if "name" in frontmatter:
            return frontmatter["name"]
        if "title" in frontmatter:
            return frontmatter["title"]

        match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return "Untitled Document"

    def _parse_sections(self, body: str, doc_title: str) -> List[SectionNode]:
        sections: List[SectionNode] = []
        lines = body.splitlines()

        current_title = "Overview"
        current_level = 2
        current_lines: List[str] = []

        for line in lines:
            header_match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if header_match:
                level = len(header_match.group(1))
                h_title = header_match.group(2).strip()

                # If this is the main document H1 title and has no body content before it, skip as a section header
                if level == 1 and h_title.lower() == doc_title.lower():
                    if current_lines:
                        sec_node = self._build_section_node(current_title, current_level, current_lines)
                        if sec_node.content or sec_node.paragraphs:
                            sections.append(sec_node)
                        current_lines = []
                    continue

                if current_lines:
                    sec_node = self._build_section_node(current_title, current_level, current_lines)
                    if sec_node.content or sec_node.paragraphs or sec_node.lists:
                        sections.append(sec_node)
                    current_lines = []

                current_level = level
                current_title = h_title
            else:
                current_lines.append(line)

        # Flush final section
        if current_lines:
            sec_node = self._build_section_node(current_title, current_level, current_lines)
            if sec_node.content or sec_node.paragraphs or sec_node.lists:
                sections.append(sec_node)

        return sections

    def _build_section_node(self, title: str, level: int, lines: List[str]) -> SectionNode:
        content = "\n".join(lines).strip()
        paragraphs = []
        lists = []
        current_list = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith(("- ", "* ", "1. ", "2. ", "3. ")):
                item = re.sub(r"^([-*]|\d+\.)\s+", "", stripped)
                current_list.append(item)
            else:
                if current_list:
                    lists.append(current_list)
                    current_list = []
                if stripped and not stripped.startswith("#"):
                    paragraphs.append(stripped)

        if current_list:
            lists.append(current_list)

        return SectionNode(
            title=title,
            level=level,
            content=content,
            paragraphs=paragraphs,
            lists=lists
        )
