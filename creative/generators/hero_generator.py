"""
Hero, Infographic, Carousel, Thumbnail, Storyboard, and Caption Generators.
"""

from typing import List, Dict, Any
from creative.models.schema import (
    HeroBrief, InfographicSpec, CarouselDesign, ThumbnailSpec, VideoStoryboard, CreativeContext
)
from creative.specifications.visual_spec import VisualSpecificationBuilder

class HeroGenerator:
    @staticmethod
    def generate_hero(context: CreativeContext) -> HeroBrief:
        topic = context.planning_report.get("topic", "AI Operations")
        spec = VisualSpecificationBuilder.build_visual_spec(topic)

        return HeroBrief(
            title=f"Hero Visual: {topic}",
            concept_summary=f"Dark glassmorphism isometric 3D visualization showcasing an autonomous AI agent core executing MCP tools connected to PostgreSQL vector storage.",
            spec=spec,
            aspect_ratios={
                "16:9": "1920x1080 (Website Banner & YouTube)",
                "1:1": "1080x1080 (LinkedIn & Instagram Post)",
                "4:5": "1080x1350 (LinkedIn Mobile & Instagram Feed)",
                "9:16": "1080x1920 (Reels & Stories)"
            }
        )

class InfographicGenerator:
    @staticmethod
    def generate_infographic(context: CreativeContext) -> InfographicSpec:
        topic = context.planning_report.get("topic", "AI Operations")
        spec = VisualSpecificationBuilder.build_visual_spec(topic)

        return InfographicSpec(
            title=f"Process Infographic: {topic} Architecture",
            process_steps=[
                {"step": "1. Strategy Decision", "desc": "Opportunity ranking & goal mapping"},
                {"step": "2. Research Package", "desc": "Verified statistics & MCP benchmarks"},
                {"step": "3. Planning Package", "desc": "Dependency graph & publishing schedule"},
                {"step": "4. Execution & Analytics", "desc": "Multi-channel distribution & lead tracking"}
            ],
            spec=spec
        )

class CarouselGenerator:
    @staticmethod
    def generate_carousel(context: CreativeContext) -> CarouselDesign:
        topic = context.planning_report.get("topic", "AI Operations")
        return CarouselDesign(
            title=f"LinkedIn Carousel Design: {topic}",
            slides=[
                {"slide_number": 1, "header": topic, "visual": "Dark glassmorphism hero core"},
                {"slide_number": 2, "header": "68% Enterprise AI Adoption", "visual": "Stat counter graphic"},
                {"slide_number": 3, "header": "MCP Tool Execution", "visual": "Protocol flow diagram"},
                {"slide_number": 4, "header": "PostgreSQL pgvector Latency", "visual": "Sub-10ms latency benchmark chart"},
                {"slide_number": 5, "header": "FinTech Case Study", "visual": "Before/After metric card (48h -> 3min)"},
                {"slide_number": 6, "header": "Book Discovery Call", "visual": "AVENIQ CTA Card with QR Code"}
            ],
            total_slides=6,
            cta_slide={"text": "Book your free consultation", "url": "https://aveniq.ai/contact"}
        )

class ThumbnailGenerator:
    @staticmethod
    def generate_thumbnail(context: CreativeContext) -> ThumbnailSpec:
        topic = context.planning_report.get("topic", "AI Operations")
        return ThumbnailSpec(
            headline_text=f"AI AGENTS IN PRODUCTION: 42% FASTER",
            contrast_focal_point="Glowing cyan AI core against ultra-dark obsidian background with high text contrast",
            thumbnail_prompt=f"YouTube thumbnail, bold high-contrast text 'AI AGENTS IN PRODUCTION', glowing cyan 3D AI agent core, dark background, octane render, 16:9"
        )

class StoryboardGenerator:
    @staticmethod
    def generate_storyboard(context: CreativeContext) -> VideoStoryboard:
        topic = context.planning_report.get("topic", "AI Operations")
        return VideoStoryboard(
            video_title=f"How {topic} Is Built",
            duration_seconds=45,
            scenes=[
                {"scene": 1, "duration": 5, "description": "Isometric shot of glowing cyan AI core", "audio": "68% of engineering teams run AI agents in production."},
                {"scene": 2, "duration": 15, "description": "Animation of MCP tool request payload passing into database", "audio": "MCP protocol reduces software integration latency by 42%."},
                {"scene": 3, "duration": 15, "description": "FinTech SaaS case study metrics transforming from 48h to 3min", "audio": "Real-world result: 48-hour invoice reconciliation reduced to 3 minutes."},
                {"scene": 4, "duration": 10, "description": "AVENIQ logo reveal with discovery CTA button", "audio": "Book a custom discovery consultation with AVENIQ engineers today."}
            ],
            voiceover_script="68% of engineering teams run AI agents in production. MCP protocol reduces tool execution latency by 42%. Book a custom consultation with AVENIQ today.",
            subtitle_script="[Subtitles: High contrast white text with cyan highlight]",
            video_prompt=f"Sora 4k video, smooth camera dolly shot through glowing dark glassmorphism server vault processing {topic}"
        )
