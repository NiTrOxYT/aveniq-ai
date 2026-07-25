"""
Editorial Layer for Content Department.
Polishes, refines flow, improves readability, and enforces brand/technical precision without generating content from scratch.
"""

from typing import Dict, Any, Tuple, List
from content.models.schema import ArticleContent, SocialPostContent

class TechnicalEditor:
    @staticmethod
    def edit_article(article: ArticleContent) -> ArticleContent:
        # Refine technical precision and section headers
        polished_body = article.body_markdown.replace("very good", "high-performance").replace("really fast", "sub-10ms latency")
        article.body_markdown = polished_body
        return article

class ComplianceEditor:
    @staticmethod
    def validate_brand_compliance(text: str, forbidden_words: List[str]) -> Tuple[bool, List[str]]:
        violations = []
        text_lower = text.lower()
        for fw in forbidden_words:
            if fw in text_lower:
                violations.append(f"Forbidden marketing hype word detected: '{fw}'")
        return len(violations) == 0, violations
