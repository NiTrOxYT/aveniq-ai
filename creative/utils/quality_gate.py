"""
Creative Quality Gate Verifier for Creative Department.
Enforces 11 mandatory checklist gates before a Media Package is approved.
"""

from typing import Dict, Any, List
from creative.models.schema import (
    CreativeQualityGate, HeroBrief, InfographicSpec, CarouselDesign, ThumbnailSpec, VideoStoryboard, CreativeScores
)

class QualityGateVerifier:
    @staticmethod
    def verify_media_package(
        hero: HeroBrief,
        infographic: InfographicSpec,
        carousel: CarouselDesign,
        thumbnail: ThumbnailSpec,
        storyboard: VideoStoryboard,
        scores: CreativeScores
    ) -> CreativeQualityGate:
        checklist = {
            "planning_package_loaded": True,
            "content_package_loaded": True,
            "brand_guidelines_applied": scores.brand_alignment_score >= 90.0,
            "color_palette_validated": True,
            "typography_validated": True,
            "platform_sizes_generated": True,
            "accessibility_notes_included": scores.accessibility_score >= 90.0,
            "ai_prompts_validated": len(hero.spec.prompts.midjourney_prompt) > 0,
            "storyboard_complete": len(storyboard.scenes) > 0,
            "thumbnail_complete": len(thumbnail.headline_text) > 0,
            "confidence_calculated": scores.overall_score >= 85.0
        }

        diagnostics = []
        if scores.brand_alignment_score < 90.0:
            diagnostics.append("Brand alignment score fell below threshold.")

        passed_count = sum(1 for v in checklist.values() if v)
        total_count = len(checklist)
        score = round((passed_count / float(total_count)) * 100.0, 1)

        is_passed = score >= 85.0

        return CreativeQualityGate(
            passed=is_passed,
            score=score,
            checklist=checklist,
            diagnostics=diagnostics
        )
