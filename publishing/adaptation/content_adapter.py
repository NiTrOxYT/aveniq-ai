"""
Channel Content Adaptation Layer.
Optimizes Delivery Packages for each specific publishing channel (X thread splitting, LinkedIn hashtags, WordPress HTML).
"""

from typing import Dict, Any, List

class ContentAdapter:
    @staticmethod
    def adapt_for_channel(channel_name: str, delivery_payload: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = delivery_payload.get("text", "Autonomous AI Marketing Campaign Briefing")
        topic = delivery_payload.get("topic", "AI Automation")

        if channel_name == "X":
            # X Thread Splitting
            chunks = [raw_text[i:i+260] for i in range(0, len(raw_text), 260)]
            if not chunks:
                chunks = [raw_text]
            formatted_thread = [f"🧵 {i+1}/{len(chunks)} {chunk}" for i, chunk in enumerate(chunks)]
            return {
                "channel": "X",
                "format": "thread",
                "tweets": formatted_thread,
                "hashtags": ["#AI", "#Automation"]
            }
        elif channel_name == "LinkedIn":
            # LinkedIn Long-Form
            return {
                "channel": "LinkedIn",
                "format": "longform",
                "text": f"{raw_text}\n\nKey Takeaways for CTOs:\n• Human-in-the-loop governance\n• Deterministic orchestration\n\n#EnterpriseAI #Automation #AI",
                "media_attached": True
            }
        elif channel_name == "WordPress":
            # WordPress HTML Article
            return {
                "channel": "WordPress",
                "format": "html_post",
                "title": f"Deep Dive: {topic}",
                "content_html": f"<h1>{topic}</h1><p>{raw_text}</p><p><em>Published via AVENIQ Publishing Platform.</em></p>",
                "tags": ["AI", "Architecture", "Orchestration"]
            }

        return {"channel": channel_name, "text": raw_text}
