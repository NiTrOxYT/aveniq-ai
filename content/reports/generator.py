"""
Content Report Generator for Content Department.
Formats content packages into publication-ready JSON reports.
"""

from typing import Dict, Any
from content.engine.content_engine import ContentEngine
from content.storage.manager import ContentStorageManager

class ContentReportGenerator:
    def __init__(self):
        self.engine = ContentEngine()
        self.storage = ContentStorageManager()

    def generate_content_report(self, topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        pkg = self.engine.generate_content_package(topic)
        self.storage.save_package(pkg)

        return {
            "report_type": "content_package",
            "package_id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "overall_score": f"{pkg.scores.overall_score}/100",
            "version": pkg.version_info.version,
            "workflow_state": pkg.workflow_state.current_state,
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": f"{pkg.quality_gate.score}%",
                "checklist": pkg.quality_gate.checklist
            },
            "master_article": {
                "title": pkg.master_article.title,
                "slug": pkg.master_article.slug,
                "meta_title": pkg.master_article.meta_title,
                "meta_description": pkg.master_article.meta_description,
                "hook": pkg.master_article.hook,
                "word_count": pkg.master_article.word_count,
                "reading_time": f"{pkg.master_article.reading_time_minutes} min",
                "citations_count": len(pkg.master_article.citations_used),
                "internal_links": pkg.master_article.internal_links,
                "body_preview": pkg.master_article.body_markdown[:300] + "..."
            },
            "social_posts": {
                "linkedin": {
                    "headline": pkg.linkedin_post.headline,
                    "copy": pkg.linkedin_post.copy_text,
                    "hashtags": pkg.linkedin_post.hashtags,
                    "cta": pkg.linkedin_post.call_to_action
                },
                "x_thread": pkg.x_thread,
                "telegram": {
                    "headline": pkg.telegram_summary.headline,
                    "copy": pkg.telegram_summary.copy_text
                }
            },
            "carousel_copy": pkg.linkedin_carousel_copy,
            "newsletter": {
                "subject": pkg.newsletter.subject_line,
                "preview": pkg.newsletter.preview_text,
                "takeaways": pkg.newsletter.key_takeaways,
                "cta": pkg.newsletter.call_to_action
            },
            "landing_page": {
                "hero_headline": pkg.landing_page_copy.hero_headline,
                "hero_subheadline": pkg.landing_page_copy.hero_subheadline,
                "value_props": pkg.landing_page_copy.value_props,
                "button_text": pkg.landing_page_copy.button_text
            },
            "variations": {
                "alternative_titles": pkg.variations.alternative_titles,
                "alternative_hooks": pkg.variations.alternative_hooks,
                "cta_variations": pkg.variations.cta_variations,
                "emoji_version": pkg.variations.emoji_version,
                "short_version": pkg.variations.short_version
            },
            "content_scores": {
                "readability": pkg.scores.readability_score,
                "seo": pkg.scores.seo_score,
                "brand_alignment": pkg.scores.brand_alignment_score,
                "authority": pkg.scores.authority_score,
                "overall": pkg.scores.overall_score
            },
            "decision_reasoning": pkg.decision_reasoning
        }
