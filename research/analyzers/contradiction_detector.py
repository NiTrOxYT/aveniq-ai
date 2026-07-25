"""
Contradiction Detector, Evidence Ranker, Citation Manager, and Gap Detector.
"""

from typing import List, Dict, Any
from research.models.schema import StatisticItem, CitationItem

class ContradictionDetector:
    @staticmethod
    def detect_contradictions(statistics: List[StatisticItem]) -> List[str]:
        # Scans collected statistics for conflicting values or statements
        contradictions = []
        seen_metrics = {}
        for stat in statistics:
            key = stat.metric_name.lower()
            if key in seen_metrics:
                if seen_metrics[key] != stat.value:
                    contradictions.append(
                        f"Discrepancy detected in '{stat.metric_name}': {seen_metrics[key]} vs {stat.value}"
                    )
            else:
                seen_metrics[key] = stat.value
        return contradictions

class EvidenceRanker:
    @staticmethod
    def rank_statistics(statistics: List[StatisticItem]) -> List[StatisticItem]:
        return sorted(statistics, key=lambda s: s.confidence_score, reverse=True)

class CitationManager:
    @staticmethod
    def format_citations(citations: List[CitationItem]) -> List[Dict[str, str]]:
        formatted = []
        for idx, c in enumerate(citations, 1):
            formatted.append({
                "index": f"[{idx}]",
                "id": c.id,
                "citation_text": f"{c.author} ({c.publication_date}). \"{c.source_title}\". {c.publication}. Available at: {c.url}",
                "evidence_level": c.evidence_level,
                "confidence": f"{int(c.confidence_score * 100)}%"
            })
        return formatted

class GapDetector:
    @staticmethod
    def detect_gaps(statistics: List[StatisticItem], technical_claims: List[Any]) -> List[str]:
        gaps = []
        if not statistics:
            gaps.append("Missing quantitative industry statistics for topic.")
        if not technical_claims:
            gaps.append("Missing technical architecture verification for implementation claims.")
        return gaps
