"""
Design Token Loader & Context Builder for AVENIQ Creative Department.
Loads Brand Design System Tokens and builds unified CreativeContext.
"""

from typing import Dict, Any
from planning.reports.generator import PlanningReportGenerator
from research.reports.generator import ResearchReportGenerator
from content.reports.generator import ContentReportGenerator
from creative.models.schema import CreativeContext

class DesignTokenLoader:
    @staticmethod
    def load_design_tokens() -> Dict[str, Any]:
        return {
            "colors": {
                "primary": "#0F172A",      # Deep Slate / Dark Navy
                "accent": "#38BDF8",       # Electric Cyan / Neon Blue
                "secondary_accent": "#818CF8", # Indigo / Violet
                "background": "#020617",   # Ultra-Dark Obsidian
                "surface": "#1E293B",      # Glassmorphism Dark Card
                "text_primary": "#F8FAFC", # Crisp White
                "text_secondary": "#94A3B8"
            },
            "typography": {
                "font_family_primary": "Inter, sans-serif",
                "font_family_code": "Fira Code, monospace",
                "font_weight_bold": 700,
                "font_weight_medium": 500
            },
            "glassmorphism": {
                "background_opacity": 0.6,
                "backdrop_blur": "16px",
                "border": "1px solid rgba(255, 255, 255, 0.1)",
                "border_radius": "12px",
                "box_shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
            }
        }

class CreativeContextBuilder:
    @staticmethod
    def build_context(topic: str = "AI Agents in Enterprise Operations") -> CreativeContext:
        plan_report = PlanningReportGenerator().generate_planning_report()
        res_package = ResearchReportGenerator().generate_package_report(topic)
        cnt_package = ContentReportGenerator().generate_content_report(topic)

        design_tokens = DesignTokenLoader.load_design_tokens()

        brand_guidelines = {
            "brand_name": "AVENIQ",
            "tagline": "Premium Software Engineering & AI Automation",
            "logo_url": "https://aveniq.ai/assets/logo.svg"
        }

        return CreativeContext(
            planning_report=plan_report,
            research_package=res_package,
            content_package=cnt_package,
            brand_guidelines=brand_guidelines,
            design_system=design_tokens
        )
