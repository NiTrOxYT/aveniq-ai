"""
Brand Guardrails & Compliance Engine for Strategy Department.
Ensures every strategic recommendation adheres strictly to AVENIQ brand rules.
"""

from typing import Tuple, List, Dict, Any
from strategy.models.schema import ContentRecommendation, MarketingPlan

FORBIDDEN_WORDS = [
    "best company", "guaranteed", "cheapest", "magic", "overnight success",
    "mind-blowing", "revolutionary", "incredible", "buy now", "limited time offer"
]

class BrandGuardrails:
    @staticmethod
    def validate_content_recommendation(rec: ContentRecommendation) -> Tuple[bool, List[str]]:
        violations = []
        full_text = f"{rec.suggested_title} {rec.value_proposition} {rec.unique_angle} {rec.differentiator} {rec.call_to_action}".lower()

        for fw in FORBIDDEN_WORDS:
            if fw in full_text:
                violations.append(f"Contains forbidden word: '{fw}'")

        if not rec.call_to_action:
            violations.append("Call to Action cannot be empty")

        if not rec.target_platforms:
            violations.append("Target platforms list cannot be empty")

        is_valid = len(violations) == 0
        return is_valid, violations

    @staticmethod
    def validate_marketing_plan(plan: MarketingPlan) -> Tuple[bool, List[str]]:
        is_valid, violations = BrandGuardrails.validate_content_recommendation(plan.content)
        if not plan.primary_goal:
            violations.append("Marketing plan primary goal is missing")
        if not plan.audience:
            violations.append("Marketing plan audience profile is missing")
        return len(violations) == 0, violations
