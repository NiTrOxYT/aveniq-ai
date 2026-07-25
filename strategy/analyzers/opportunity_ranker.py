"""
Opportunity Ranker & Audience Matcher & Positioning Engine.
"""

from typing import List, Dict, Any
from strategy.models.schema import Opportunity, AudienceProfile

class OpportunityRanker:
    @staticmethod
    def rank_opportunities(opportunities: List[Opportunity]) -> List[Opportunity]:
        return sorted(opportunities, key=lambda o: o.priority_score.overall_score, reverse=True)

class AudienceMatcher:
    @staticmethod
    def match_audience(opportunity: Opportunity) -> AudienceProfile:
        target_ind = opportunity.target_industry
        if target_ind == "SaaS":
            return AudienceProfile(
                primary_audience="SaaS Founders & CTOs",
                secondary_audience="Product Managers & Tech Lead Engineers",
                buying_intent="High",
                awareness_stage="Solution-Aware",
                business_size="11-50 employees",
                industry="SaaS",
                customer_persona="Tech Founder scaling recurring revenue platform needing custom multi-tenancy & AI tools",
                priority_score=94.0,
                reasoning="SaaS founders represent high-LTV clients seeking scalable React/Next.js/PostgreSQL architecture."
            )
        elif target_ind in ["Hospitality", "Food & Beverage"]:
            return AudienceProfile(
                primary_audience="Hospitality Group Executives & Restaurant Owners",
                secondary_audience="Operations Managers",
                buying_intent="High",
                awareness_stage="Problem-Aware",
                business_size="Small & Medium Business (SMB)",
                industry="Hospitality",
                customer_persona="Business Operator seeking order automation and custom digital reservation portals",
                priority_score=88.0,
                reasoning="Hospitality operators benefit immediately from order digitalization and workflow automation."
            )
        else:
            return AudienceProfile(
                primary_audience="SMB Business Leaders & Operations Directors",
                secondary_audience="Technical Department Managers",
                buying_intent="Medium",
                awareness_stage="Solution-Aware",
                business_size="SMB (11-100 employees)",
                industry=target_ind,
                customer_persona="Operations Leader automating manual spreadsheet workflows into custom software",
                priority_score=85.0,
                reasoning="Business leaders seeking operational efficiency and error reduction."
            )

class PositioningStrategist:
    @staticmethod
    def determine_positioning(opportunity: Opportunity) -> Dict[str, str]:
        return {
            "unique_angle": f"Building scalable, zero-lock-in software foundations tailored for {opportunity.target_industry}.",
            "market_positioning": "AVENIQ - Premium Software & AI Engineering Partner",
            "differentiator": "Focusing on clean software engineering fundamentals, type-safe code, and zero vendor lock-in.",
            "value_proposition": "Custom software and AI automation engineered for long-term scalability and operational performance."
        }
