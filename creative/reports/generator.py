"""
Creative Report Generator for Creative Department.
Formats media packages into executable JSON specifications for AI image/video generators.
"""

from typing import Dict, Any
from creative.engine.creative_engine import CreativeEngine
from creative.storage.manager import CreativeStorageManager

class CreativeReportGenerator:
    def __init__(self):
        self.engine = CreativeEngine()
        self.storage = CreativeStorageManager()

    def generate_media_report(self, topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        pkg = self.engine.generate_media_package(topic)
        self.storage.save_package(pkg)

        return {
            "report_type": "media_package",
            "package_id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "overall_score": f"{pkg.scores.overall_score}/100",
            "version": pkg.version_info.version,
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": f"{pkg.quality_gate.score}%",
                "checklist": pkg.quality_gate.checklist
            },
            "style_guide": {
                "theme": pkg.visual_theme,
                "colors": pkg.style_guide.color_palette,
                "typography": f"{pkg.style_guide.typography_primary} / {pkg.style_guide.typography_secondary}",
                "mood": pkg.style_guide.mood,
                "lighting": pkg.style_guide.lighting,
                "camera_angle": pkg.style_guide.camera_angle
            },
            "hero_brief": {
                "title": pkg.hero_brief.title,
                "summary": pkg.hero_brief.concept_summary,
                "aspect_ratios": pkg.hero_brief.aspect_ratios,
                "ai_prompts": {
                    "midjourney": pkg.hero_brief.spec.prompts.midjourney_prompt,
                    "dalle3": pkg.hero_brief.spec.prompts.dalle3_prompt,
                    "flux": pkg.hero_brief.spec.prompts.flux_prompt,
                    "sdxl_positive": pkg.hero_brief.spec.prompts.sdxl_positive_prompt,
                    "sdxl_negative": pkg.hero_brief.spec.prompts.sdxl_negative_prompt
                }
            },
            "infographic_spec": {
                "title": pkg.infographic.title,
                "steps": pkg.infographic.process_steps
            },
            "carousel_design": {
                "title": pkg.carousel_design.title,
                "total_slides": pkg.carousel_design.total_slides,
                "slides": pkg.carousel_design.slides,
                "cta_slide": pkg.carousel_design.cta_slide
            },
            "thumbnail_spec": {
                "headline": pkg.thumbnail.headline_text,
                "focal_point": pkg.thumbnail.contrast_focal_point,
                "prompt": pkg.thumbnail.thumbnail_prompt
            },
            "video_storyboard": {
                "title": pkg.video_storyboard.video_title,
                "duration": f"{pkg.video_storyboard.duration_seconds}s",
                "scenes": pkg.video_storyboard.scenes,
                "voiceover": pkg.video_storyboard.voiceover_script,
                "sora_prompt": pkg.video_storyboard.video_prompt
            },
            "captions_and_accessibility": pkg.captions_and_alt_text,
            "export_specifications": pkg.export_specifications,
            "creative_scores": {
                "brand_alignment": pkg.scores.brand_alignment_score,
                "composition": pkg.scores.composition_score,
                "prompt_quality": pkg.scores.prompt_quality_score,
                "accessibility": pkg.scores.accessibility_score,
                "overall": pkg.scores.overall_score
            }
        }
