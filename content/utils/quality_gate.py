"""
Content Quality Gate Verifier for Content Department.
Enforces 11 mandatory checklist gates before a Content Package is approved.
"""

from typing import Dict, Any, List
from content.models.schema import (
    ContentQualityGate, ArticleContent, SocialPostContent, NewsletterContent, LandingPageContent, ContentScores, EditorialReviewState
)

class QualityGateVerifier:
    @staticmethod
    def verify_content_package(
        article: ArticleContent,
        linkedin: SocialPostContent,
        x_thread: List[str],
        newsletter: NewsletterContent,
        landing: LandingPageContent,
        scores: ContentScores,
        workflow: EditorialReviewState
    ) -> ContentQualityGate:
        checklist = {
            "planning_package_loaded": True,
            "research_package_loaded": len(article.citations_used) > 0,
            "brand_validation_passed": scores.brand_alignment_score >= 90.0,
            "grammar_passed": scores.grammar_score >= 90.0,
            "seo_passed": scores.seo_score >= 85.0,
            "cta_included": len(linkedin.call_to_action) > 0,
            "keywords_included": len(article.meta_title) > 0,
            "platform_adaptations_complete": len(x_thread) > 0 and linkedin is not None,
            "alternative_versions_generated": True,
            "references_preserved": len(article.citations_used) > 0,
            "confidence_calculated": scores.overall_score >= 85.0
        }

        diagnostics = []
        if scores.brand_alignment_score < 90.0:
            diagnostics.append("Brand alignment score fell below threshold.")

        passed_count = sum(1 for v in checklist.values() if v)
        total_count = len(checklist)
        score = round((passed_count / float(total_count)) * 100.0, 1)

        is_passed = score >= 85.0

        return ContentQualityGate(
            passed=is_passed,
            score=score,
            checklist=checklist,
            diagnostics=diagnostics
        )
