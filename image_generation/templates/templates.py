"""
Layout Templates Engine for Platform Visual Assets.
Defines aspect ratios, safe zones, composition rules, and layout dimensions for 11 platform asset types.
"""

from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class LayoutTemplateConfig:
    template_type: str
    platform: str
    width: int
    height: int
    aspect_ratio: str
    safe_zone_margin_px: int
    max_text_lines: int

TEMPLATES_MAP: Dict[str, LayoutTemplateConfig] = {
    "hero": LayoutTemplateConfig("hero", "website", 1920, 1080, "16:9", 80, 2),
    "carousel": LayoutTemplateConfig("carousel", "instagram", 1080, 1080, "1:1", 60, 4),
    "infographic": LayoutTemplateConfig("infographic", "pinterest", 1080, 1920, "9:16", 100, 8),
    "thumbnail": LayoutTemplateConfig("thumbnail", "youtube", 1280, 720, "16:9", 50, 2),
    "reel_cover": LayoutTemplateConfig("reel_cover", "instagram", 1080, 1920, "9:16", 120, 2),
    "story": LayoutTemplateConfig("story", "instagram", 1080, 1920, "9:16", 120, 3),
    "banner": LayoutTemplateConfig("banner", "blog", 1200, 630, "1.91:1", 40, 2),
    "linkedin": LayoutTemplateConfig("linkedin", "linkedin", 1200, 627, "1.91:1", 40, 3),
    "square_post": LayoutTemplateConfig("square_post", "facebook", 1080, 1080, "1:1", 50, 3),
    "email_header": LayoutTemplateConfig("email_header", "email", 600, 200, "3:1", 20, 1)
}

class TemplateEngine:
    @staticmethod
    def get_template(template_type: str) -> LayoutTemplateConfig:
        return TEMPLATES_MAP.get(template_type.lower(), TEMPLATES_MAP["hero"])

    @staticmethod
    def list_templates() -> List[Dict[str, Any]]:
        return [
            {
                "type": cfg.template_type,
                "platform": cfg.platform,
                "resolution": f"{cfg.width}x{cfg.height}",
                "aspect_ratio": cfg.aspect_ratio
            }
            for cfg in TEMPLATES_MAP.values()
        ]
