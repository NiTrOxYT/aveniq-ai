"""
Art Director & Visual Style Guide Engine for Creative Department.
Defines visual style, composition rules, lighting, typography, and mood.
"""

from typing import Dict, Any
from creative.models.schema import VisualStyle, CreativeContext

class ArtDirector:
    @staticmethod
    def define_visual_style(context: CreativeContext) -> VisualStyle:
        colors = context.design_system.get("colors", {})
        return VisualStyle(
            style_name="AVENIQ Dark Glassmorphism AI Architecture",
            color_palette=colors,
            typography_primary="Inter, sans-serif",
            typography_secondary="Fira Code, monospace",
            mood="Authoritative, High-Tech, Premium, Scalable",
            lighting="Dark ambient environment with neon cyan (#38BDF8) edge rim lighting",
            camera_angle="Isometric 35° perspective with slight focal blur",
            composition_rule="Rule of thirds with centered primary focal point"
        )
