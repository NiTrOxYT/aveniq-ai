"""
Master Content Engine & Packaging Synthesizer for Content Department.
Orchestrates context loading, platform generation, editorial polishing, reuse, scoring, and packaging.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any
from content.models.schema import ContentPackage, ContentVersion
from content.context.builder import ContentContextBuilder
from content.generators.article_generator import (
    ArticleGenerator, LinkedInGenerator, XGenerator, NewsletterGenerator, LandingPageGenerator
)
from content.editors.technical_editor import TechnicalEditor
from content.transformers.reuse_engine import ContentReuseEngine
from content.analyzers.scoring_engine import ContentScoringEngine
from content.workflow.review_workflow import ReviewWorkflowEngine
from content.engine.decision_engine import ContentVariationEngine, ContentDecisionEngine
from content.utils.quality_gate import QualityGateVerifier

class ContentEngine:
    def __init__(self):
        self.context_builder = ContentContextBuilder()

    def generate_content_package(self, topic: str = "AI Agents in Enterprise Operations") -> ContentPackage:
        context = self.context_builder.build_context(topic)
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # 1. Generate Master Written Assets
        master_article = ArticleGenerator.generate_article(context)
        master_article = TechnicalEditor.edit_article(master_article)

        linkedin_post = LinkedInGenerator.generate_post(context)
        x_thread = XGenerator.generate_thread(context)
        newsletter = NewsletterGenerator.generate_newsletter(context)
        landing_copy = LandingPageGenerator.generate_landing(context)

        # 2. Derive Multi-Channel Assets via Reuse Engine
        carousel_copy = ContentReuseEngine.derive_linkedin_carousel_copy(master_article)
        telegram_summary = ContentReuseEngine.derive_telegram_summary(master_article)
        medium_art = ContentReuseEngine.derive_medium_article(master_article)
        devto_art = ContentReuseEngine.derive_devto_article(master_article)

        # 3. Generate Variations & Decision Reasoning
        variations = ContentVariationEngine.generate_variations(topic)
        decisions = ContentDecisionEngine.evaluate_content_decisions(context, master_article)

        # 4. Compute Content Scores & Review Workflow State
        scores = ContentScoringEngine.calculate_scores(master_article, context)
        workflow_state = ReviewWorkflowEngine.initialize_review_state()

        version_info = ContentVersion(
            version="1.0.0",
            timestamp=today_str,
            author="ai_content_director",
            planning_version="1.0.0",
            research_version="1.0.0"
        )

        qg_result = QualityGateVerifier.verify_content_package(
            master_article, linkedin_post, x_thread, newsletter, landing_copy, scores, workflow_state
        )

        exec_summary = f"Complete platform-specific content package generated for '{topic}'. Master article: {master_article.word_count} words ({master_article.reading_time_minutes} min read). Overall content score: {scores.overall_score}/100. Quality gate pass status: {qg_result.passed}."

        return ContentPackage(
            id=f"cnt_pkg_{today_str}_{abs(hash(topic)) % 10000:04d}",
            topic=topic,
            date=today_str,
            executive_summary=exec_summary,
            master_article=master_article,
            linkedin_post=linkedin_post,
            linkedin_carousel_copy=carousel_copy,
            instagram_caption=linkedin_post,
            facebook_post=linkedin_post,
            x_thread=x_thread,
            threads_post=linkedin_post,
            telegram_summary=telegram_summary,
            newsletter=newsletter,
            medium_article=medium_art,
            devto_article=devto_art,
            landing_page_copy=landing_copy,
            email_campaign=newsletter,
            variations=variations,
            scores=scores,
            workflow_state=workflow_state,
            version_info=version_info,
            quality_gate=qg_result,
            decision_reasoning=decisions
        )
