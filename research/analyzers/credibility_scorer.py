"""
Source Validator and Credibility Scorer for Research Department.
"""

from typing import Tuple, List, Dict, Any
from research.models.schema import CitationItem

EVIDENCE_LEVEL_WEIGHTS = {
    "Peer-Reviewed": 1.0,
    "Industry Report": 0.90,
    "Official Documentation": 0.95,
    "Company Blog": 0.70,
    "Community": 0.50
}

class SourceValidator:
    @staticmethod
    def validate_citation(citation: CitationItem) -> Tuple[bool, List[str]]:
        violations = []
        if not citation.url or not citation.url.startswith("http"):
            violations.append(f"Invalid URL: {citation.url}")
        if not citation.publication:
            violations.append("Missing publication name")
        if not citation.publication_date:
            violations.append("Missing publication date")
        return len(violations) == 0, violations

class CredibilityScorer:
    @staticmethod
    def calculate_score(citation: CitationItem) -> float:
        base = EVIDENCE_LEVEL_WEIGHTS.get(citation.evidence_level, 0.70)
        # Adjust slightly for recency
        if "2026" in citation.publication_date or "2025" in citation.publication_date:
            base = min(1.0, base + 0.05)
        return round(base, 2)
