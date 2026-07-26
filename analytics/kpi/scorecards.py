"""
Centralized KPI Definitions, Calculator Engine, and 0-100 Scorecard Normalizer.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class KPIDefinition:
    name: str
    category: str  # Reach, Engagement, Conversion, SEO, Financial
    unit: str  # percentage, ratio, currency, count
    description: str

class KPICalculator:
    @staticmethod
    def calculate_ctr(clicks: int, impressions: int) -> float:
        if impressions <= 0:
            return 0.0
        return round((clicks / float(impressions)) * 100.0, 2)

    @staticmethod
    def calculate_engagement_rate(interactions: int, reach: int) -> float:
        if reach <= 0:
            return 0.0
        return round((interactions / float(reach)) * 100.0, 2)

    @staticmethod
    def calculate_conversion_rate(conversions: int, visits: int) -> float:
        if visits <= 0:
            return 0.0
        return round((conversions / float(visits)) * 100.0, 2)

class KPIScorecardNormalizer:
    @staticmethod
    def normalize_to_score(metric_val: float, baseline: float, target: float) -> float:
        if target <= baseline:
            return 50.0
        ratio = (metric_val - baseline) / (target - baseline)
        score = 50.0 + (ratio * 50.0)
        return max(0.0, min(100.0, round(score, 1)))
