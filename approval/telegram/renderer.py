"""
Telegram Dashboard Card Renderer & Inline Keyboard Builder.
Generates rich Telegram Markdown formatting with interactive review action buttons.
"""

from typing import Dict, Any, List
from approval.models.schema import TelegramDashboardMarkup, ApprovalContext

class TelegramRenderer:
    @staticmethod
    def render_dashboard(context: ApprovalContext) -> TelegramDashboardMarkup:
        del_pkg = context.delivery_package
        topic = del_pkg.get("topic", "AI Operations")
        del_id = del_pkg.get("package_id", "del_001")
        overall_score = del_pkg.get("overall_delivery_score", "98.5/100")

        card_text = (
            f"🚀 **AVENIQ TODAY'S MARKETING PACKAGE**\n"
            f"────────────────────────────\n"
            f"📌 **Topic**: {topic}\n"
            f"🆔 **Delivery ID**: `{del_id}`\n"
            f"⭐ **Quality Score**: {overall_score}\n"
            f"────────────────────────────\n"
            f"📱 **Platform Coverage**: LinkedIn, Instagram, Facebook, X, Threads, Telegram, Website, Newsletter\n"
            f"🖼️ **Attached Assets**: hero.webp, carousel.pdf, reel.mp4, thumbnail.png\n"
            f"⏰ **Best Posting Window**: Tuesday 09:00 AM EST\n"
            f"🔗 **CTA**: https://aveniq.ai/contact\n"
            f"────────────────────────────\n"
            f"Please review the campaign and select an action below:"
        )

        keyboard = [
            [
                {"text": "✅ Approve", "callback_data": "action_Approve"},
                {"text": "❌ Reject", "callback_data": "action_Reject"}
            ],
            [
                {"text": "🔄 Regenerate", "callback_data": "action_Rewrite"},
                {"text": "📊 More Technical", "callback_data": "action_Technical"},
                {"text": "💡 Simpler", "callback_data": "action_Simplify"}
            ],
            [
                {"text": "🖼️ New Hero Image", "callback_data": "action_RegenerateHero"},
                {"text": "🎬 Generate Sora Video", "callback_data": "action_GenerateVideo"}
            ]
        ]

        return TelegramDashboardMarkup(
            card_text=card_text,
            inline_keyboard=keyboard
        )
