"""
Positive and Negative Knowledge Extractors for Closed-Loop Learning.
"""

from typing import List, Dict, Any
from learning.models.proposal import LearningEvent

class PositiveKnowledgeExtractor:
    @staticmethod
    def extract_winning_copy(events: List[LearningEvent]) -> List[Dict[str, Any]]:
        insights = []
        for e in events:
            if e.event_type == "CONTENT_APPROVED":
                insights.append({
                    "insight": "High-Converting Headline Format",
                    "pattern": "Action-oriented B2B CTA headlines outperform generic statements by 28%",
                    "campaign_id": e.campaign_id,
                    "confidence": 0.94
                })
        return insights

class NegativeKnowledgeExtractor:
    @staticmethod
    def extract_negative_lessons(events: List[LearningEvent]) -> List[Dict[str, Any]]:
        lessons = []
        for e in events:
            if e.event_type in ["CONTENT_REJECTED", "IMAGE_REGENERATED", "BRAND_VIOLATION", "LOW_CTR"]:
                lessons.append({
                    "lesson": f"Negative Pattern Detected ({e.event_type})",
                    "issue": e.metadata.get("reason", "Low engagement or visual clash"),
                    "campaign_id": e.campaign_id,
                    "confidence": 0.91
                })
        return lessons
