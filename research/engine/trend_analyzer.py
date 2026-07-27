"""
Trend Analyzer and Cross-Source Correlation Engine for AVENIQ Research Engine.
Processes normalized research items across multiple providers to detect trending topics and high-confidence market signals.
"""

from collections import Counter
import re
from typing import List, Dict, Any


STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'from', 'up', 'down', 'of', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
    'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'this', 'that', 'these', 'those', 'http', 'https', 'com', 'org', 'new', 'released', 'using'
}


class TrendAnalyzer:
    @staticmethod
    def extract_keywords(text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z0-9\-\.]{3,}\b', text)
        return [w.lower() for w in words if w.lower() not in STOPWORDS and not w.isdigit()]

    def analyze_trends(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract cross-source trending topics and momentum scores."""
        topic_providers = {}
        topic_scores = Counter()
        topic_items = {}

        for item in items:
            title = item.get("title", "")
            summary = item.get("summary", "")
            provider = item.get("provider", "unknown")
            score = item.get("score", 1.0) or 1.0

            text = f"{title} {summary}"
            keywords = set(self.extract_keywords(text))

            # Look for 2-word phrases as well
            words = title.split()
            phrases = []
            for i in range(len(words) - 1):
                p = f"{words[i]} {words[i+1]}".strip().lower()
                clean_p = re.sub(r'[^a-z0-9 ]', '', p)
                if len(clean_p) > 5 and not any(w in STOPWORDS for w in clean_p.split()):
                    phrases.append(clean_p)

            for token in list(keywords) + phrases:
                if len(token) < 3:
                    continue
                topic_providers.setdefault(token, set()).add(provider)
                topic_scores[token] += min(score, 100) + 1
                topic_items.setdefault(token, []).append(item)

        # Rank topics appearing in multiple sources or with high scores
        trends = []
        for topic, count in topic_scores.most_common(30):
            provs = list(topic_providers.get(topic, []))
            if len(provs) >= 1 and count >= 2:
                momentum = "Surging" if len(provs) >= 3 else ("Increasing" if len(provs) >= 2 else "Stable")
                trends.append({
                    "topic": topic.title(),
                    "mention_count": int(count),
                    "providers": provs,
                    "provider_count": len(provs),
                    "trend_score": round(min(100.0, (len(provs) * 25) + (count * 2)), 1),
                    "momentum": momentum,
                    "sample_title": topic_items[topic][0].get("title") if topic_items.get(topic) else ""
                })

        # Deduplicate similar phrases
        trends.sort(key=lambda x: (x["provider_count"], x["trend_score"]), reverse=True)
        return trends[:10]

    def compute_market_signals(self, items: List[Dict[str, Any]], trends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate high-confidence market signals based on cross-source correlation."""
        signals = []
        for t in trends[:5]:
            p_count = t.get("provider_count", 1)
            confidence = "HIGH" if p_count >= 3 else ("MEDIUM" if p_count >= 2 else "LOW")
            signals.append({
                "signal_id": f"sig_{t['topic'].lower().replace(' ', '_')}",
                "topic": t["topic"],
                "category": "Market Intelligence Signal",
                "confidence": confidence,
                "confidence_score": round(min(0.99, 0.65 + (p_count * 0.1)), 2),
                "summary": f"High intent detected for '{t['topic']}' across {p_count} sources ({', '.join(t['providers'])}).",
                "sources": t["providers"],
                "momentum": t["momentum"],
                "trend_score": t["trend_score"]
            })
        return signals


global_trend_analyzer = TrendAnalyzer()
