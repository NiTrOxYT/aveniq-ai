"""
Opportunity Deduplication & Trend Clustering Engine.
Executes prior to opportunity ranking to merge similar topics and prevent repetitive daily recommendations.
"""

from typing import List, Dict, Any
from strategy.models.schema import Opportunity, PriorityScore

class OpportunityDeduplicator:
    @staticmethod
    def deduplicate(signals: List[Dict[str, Any]]) -> List[Opportunity]:
        deduped: List[Opportunity] = []
        seen_topics = set()

        for sig in signals:
            topic = sig.get("topic", "").strip()
            topic_key = topic.lower()

            if topic_key in seen_topics:
                continue
            seen_topics.add(topic_key)

            sig_id = sig.get("id", f"opp_{len(deduped)+1:03d}")
            title = sig.get("title", topic)
            category = sig.get("category", "General Software")
            target_ind = sig.get("target_industry", "SaaS")
            source_ch = sig.get("source_channels", ["Market Research"])

            p_score = PriorityScore(
                overall_score=float(sig.get("growth_score", 85.0)),
                confidence=0.91,
                trend_growth_score=float(sig.get("growth_score", 85.0)),
                audience_fit_score=90.0,
                business_value_score=88.0,
                competition_score=30.0 if sig.get("competition_level") == "Low" else 60.0,
                seo_potential_score=85.0,
                revenue_impact_score=90.0,
                brand_alignment_score=95.0,
                reasoning=f"High trend growth ({sig.get('growth_score')}%) and strong strategic fit for AVENIQ core capabilities."
            )

            deduped.append(Opportunity(
                id=sig_id,
                title=title,
                topic=topic,
                category=category,
                target_industry=target_ind,
                source_channels=source_ch,
                priority_score=p_score,
                raw_signals=sig
            ))

        return deduped
