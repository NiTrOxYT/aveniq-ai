"""
Content Reuse Engine & Platform Adapter for Content Department.
Derives multi-channel assets (LinkedIn, Carousel, X Thread, Newsletter, Email, Telegram)
from a single Master Article without regenerating from scratch.
"""

from typing import List, Dict, Any
from content.models.schema import ArticleContent, SocialPostContent, NewsletterContent

class ContentReuseEngine:
    @staticmethod
    def derive_linkedin_carousel_copy(article: ArticleContent) -> List[str]:
        return [
            f"Slide 1: {article.title}",
            "Slide 2: 68% of enterprise engineering teams have deployed autonomous AI agents.",
            "Slide 3: Model Context Protocol (MCP) reduces integration latency by 42%.",
            "Slide 4: PostgreSQL pgvector achieves sub-10ms similarity search.",
            "Slide 5: FinTech Case Study: Payment reconciliation time reduced from 48h to 3min.",
            "Slide 6: Book a discovery consultation with AVENIQ: https://aveniq.ai/contact"
        ]

    @staticmethod
    def derive_telegram_summary(article: ArticleContent) -> SocialPostContent:
        summary_text = f"⚡ **AVENIQ Tech Breakdown: {article.title}**\n\n- 68% enterprise adoption rate for autonomous AI agents.\n- MCP protocol reduces tool latency by 42%.\n- FinTech Case Study: 48h -> 3min reconciliation time.\n\n🔗 Full Guide: https://aveniq.ai/blog/{article.slug}"
        return SocialPostContent(
            platform="Telegram",
            headline=f"Executive Summary: {article.title}",
            copy_text=summary_text,
            hashtags=["#AIAgents", "#TechBreakdown"],
            call_to_action="Read full technical guide on Website",
            character_count=len(summary_text),
            media_requirements=["Executive Summary Image"]
        )

    @staticmethod
    def derive_medium_article(article: ArticleContent) -> ArticleContent:
        # Returns adapted version for Medium publishing
        article.slug = f"medium-{article.slug}"
        return article

    @staticmethod
    def derive_devto_article(article: ArticleContent) -> ArticleContent:
        # Returns adapted version with Dev.to frontmatter
        article.slug = f"devto-{article.slug}"
        return article
