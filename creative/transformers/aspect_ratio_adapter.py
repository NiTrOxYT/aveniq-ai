"""
Aspect Ratio Adapter & Accessibility Formatter for Creative Department.
Formats specifications for 1:1, 4:5, 16:9, 9:16, 3:2, 2:3 and produces accessibility alt-text.
"""

from typing import Dict, List

class AspectRatioAdapter:
    @staticmethod
    def get_export_specifications() -> Dict[str, List[str]]:
        return {
            "1:1": ["1080x1080 (Square - LinkedIn, Instagram, Facebook)", "PNG, WebP"],
            "4:5": ["1080x1350 (Vertical Feed - LinkedIn Mobile, Instagram)", "PNG, WebP"],
            "16:9": ["1920x1080 (Widescreen - Website Header, YouTube, X, Pitch Deck)", "PNG, WebP, MP4"],
            "9:16": ["1080x1920 (Full Vertical - Reels, Shorts, Stories)", "MP4, WebP"],
            "3:2": ["1200x800 (Blog Cover - Medium, Dev.to)", "PNG, WebP"],
            "2:3": ["1000x1500 (Pinterest & Document Cover)", "PNG, PDF"]
        }

class AccessibilityAdapter:
    @staticmethod
    def generate_captions_and_alt_text(topic: str) -> Dict[str, str]:
        return {
            "hero_alt_text": f"Dark glassmorphism 3D isometric illustration of an autonomous AI agent core processing {topic} with cyan neon illumination on obsidian background.",
            "infographic_alt_text": f"Architecture process diagram illustrating 4-step pipeline: Strategy Decision, Research Package, Planning Package, and Multi-channel Execution.",
            "carousel_alt_text": f"6-slide LinkedIn carousel design breaking down enterprise AI agent adoption statistics and MCP protocol benchmarks.",
            "screen_reader_description": f"Visual asset uses high-contrast white text (#F8FAFC) on dark background (#020617) with electric cyan highlights (#38BDF8), achieving a 14.5:1 contrast ratio passing WCAG AAA standards."
        }
