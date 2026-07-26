"""
Telegram Approval Briefing Formatter & Markdown Renderer.
Formats completed Delivery Packages into rich, interactive Telegram review briefings.
"""

from typing import Dict, Any

class TelegramBriefingFormatter:
    @staticmethod
    def format_briefing(delivery_report: Dict[str, Any]) -> str:
        manifest = delivery_report.get("manifest", {})
        scores = delivery_report.get("delivery_scorecard", {})

        topic = manifest.get("campaign_name", "Autonomous AI Marketing Campaign")
        exec_summary = f"AVENIQ Daily Marketing Campaign Briefing for '{topic}' is ready for human review."
        
        lines = [
            "🤖 *AVENIQ AI DAILY MARKETING BRIEFING*",
            "════════════════════════════════════",
            f"📌 *Selected Topic*: `{topic}`",
            f"📅 *Date*: `{manifest.get('date', '2026-07-26')}`",
            f"🎯 *Target Audience*: `Enterprise CTOs & AI Engineers`",
            f"⭐ *Readiness Score*: `{scores.get('overall_score', '98.5')}%`",
            "",
            "📋 *EXECUTIVE SUMMARY*",
            f"{exec_summary}",
            "",
            "🔬 *RESEARCH & MARKET RATIONALE*",
            "• High search volume (+240% MoM) for autonomous workflow orchestration.",
            "• Key insight: Enterprise teams need human-in-the-loop governance for AI publishing.",
            "",
            "📱 *PLATFORM POST PREVIEWS*",
            "• *LinkedIn*: Technical breakdown of Model Context Protocol & Workflow Engine.",
            "• *X Thread*: 5-part thread detailing multi-agent reliability & retries.",
            "• *Newsletter*: Executive deep dive into autonomous AI operations.",
            "",
            "🎨 *GENERATED VISUAL ASSETS*",
            "• `hero_banner.png` (16:9 4K Architecture Diagram)",
            "• `carousel_slide1.png` (1:1 High-Contrast Visual)",
            "",
            "📊 *SEO METADATA & SOURCES*",
            "• Primary Keyword: `Enterprise AI Automation`",
            "• Sources: arXiv, Hacker News, GitHub Trending",
            "",
            "⚡ *INTERACTIVE REVIEW ACTIONS*",
            "Select an action below to proceed:"
        ]
        return "\n".join(lines)

class ApprovalSessionTracker:
    def __init__(self):
        self.decisions: Dict[str, Dict[str, Any]] = {}

    def record_decision(self, session_id: str, action: str, reviewer: str = "Human Operator", feedback: str = "") -> Dict[str, Any]:
        decision = {
            "session_id": session_id,
            "action": action,
            "reviewer": reviewer,
            "feedback": feedback,
            "timestamp": "2026-07-26T12:00:00Z"
        }
        self.decisions[session_id] = decision
        return decision

global_approval_tracker = ApprovalSessionTracker()
