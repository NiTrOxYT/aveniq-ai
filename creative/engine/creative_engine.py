"""
Master Creative Engine & Media Package Synthesizer for Creative Department.
Orchestrates context building, art direction, asset specifications, prompt adapters, and quality verification.
"""

from datetime import datetime, timezone
from typing import Dict, Any
from creative.models.schema import MediaPackage, CreativeVersion
from creative.context.builder import CreativeContextBuilder
from creative.directors.art_director import ArtDirector
from creative.generators.hero_generator import (
    HeroGenerator, InfographicGenerator, CarouselGenerator, ThumbnailGenerator, StoryboardGenerator
)
from creative.transformers.aspect_ratio_adapter import AspectRatioAdapter, AccessibilityAdapter
from creative.analyzers.scoring_engine import CreativeScoringEngine
from creative.workflow.review_workflow import ReviewWorkflowEngine
from creative.utils.quality_gate import QualityGateVerifier

class CreativeEngine:
    def __init__(self):
        self.context_builder = CreativeContextBuilder()

    def generate_media_package(self, topic: str = "AI Agents in Enterprise Operations") -> MediaPackage:
        context = self.context_builder.build_context(topic)
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # 1. Art & Brand Direction
        style_guide = ArtDirector.define_visual_style(context)

        # 2. Generate Creative Deliverable Specifications & AI Prompts
        hero_brief = HeroGenerator.generate_hero(context)
        infographic = InfographicGenerator.generate_infographic(context)
        carousel = CarouselGenerator.generate_carousel(context)
        thumbnail = ThumbnailGenerator.generate_thumbnail(context)
        storyboard = StoryboardGenerator.generate_storyboard(context)

        diagram_spec = {
            "diagram_type": "System Architecture Flow",
            "mermaid_code": "graph TD;\n  A[Client Request] --> B[MCP Agent Core];\n  B --> C[PostgreSQL pgvector];\n  B --> D[n8n Workflow Engine];",
            "visual_style": "Dark background with cyan glowing nodes"
        }

        # 3. Apply Transformers & Accessibility
        export_specs = AspectRatioAdapter.get_export_specifications()
        captions_alt = AccessibilityAdapter.generate_captions_and_alt_text(topic)

        # 4. Compute Creative Scores & Versioning
        scores = CreativeScoringEngine.calculate_scores(context)
        review_state = ReviewWorkflowEngine.initialize_review_state()

        version_info = CreativeVersion(
            version="1.0.0",
            timestamp=today_str,
            director_id="ai_creative_director",
            content_version="1.0.0",
            planning_version="1.0.0"
        )

        qg_result = QualityGateVerifier.verify_media_package(
            hero_brief, infographic, carousel, thumbnail, storyboard, scores
        )

        exec_summary = f"Complete media package and AI prompt specifications compiled for '{topic}'. Visual theme: {style_guide.style_name}. Overall creative score: {scores.overall_score}/100. Quality gate pass status: {qg_result.passed}."

        return MediaPackage(
            id=f"med_pkg_{today_str}_{abs(hash(topic)) % 10000:04d}",
            topic=topic,
            date=today_str,
            executive_summary=exec_summary,
            visual_theme=style_guide.style_name,
            style_guide=style_guide,
            hero_brief=hero_brief,
            infographic=infographic,
            carousel_design=carousel,
            architecture_diagram_spec=diagram_spec,
            thumbnail=thumbnail,
            video_storyboard=storyboard,
            captions_and_alt_text=captions_alt,
            export_specifications=export_specs,
            scores=scores,
            version_info=version_info,
            quality_gate=qg_result
        )
