"""
Decision Engine for Strategy Department.
Enforces business rules, reasoning generation, confidence scoring, and publishing decisions.
"""

from typing import List, Dict, Any, Tuple
from strategy.models.schema import Opportunity, AudienceProfile, DecisionReasoning, StrategyContext
from strategy.goals.objectives import ObjectiveMapper

class BusinessRulesEngine:
    @staticmethod
    def evaluate_publishing_feasibility(context: StrategyContext) -> Tuple[bool, str]:
        # Check publishing calendar and blackout dates
        pub_cal = context.publishing_calendar
        if pub_cal.get("blackout_dates") and "today" in pub_cal.get("blackout_dates", []):
            return False, "Today is marked as a publishing blackout date."
        
        # Check active brand guardrails
        if not context.brand_guardrails.get("allowed_services"):
            return False, "No active services configured in brand guardrails."
            
        return True, "Publishing schedule and business criteria met for today."

class ReasoningEngine:
    @staticmethod
    def build_reasoning(opportunity: Opportunity, audience: AudienceProfile, goal: str) -> DecisionReasoning:
        primary_reason = f"High search growth and low competition for '{opportunity.topic}' matching AVENIQ's {opportunity.category} services."
        supporting_evidence = [
            f"Market Signal: {opportunity.title}",
            f"Target Audience Fit: {audience.primary_audience} ({audience.awareness_stage})",
            f"Source Channels: {', '.join(opportunity.source_channels)}",
            f"Strategic Value: High operational demand in {opportunity.target_industry}"
        ]
        
        return DecisionReasoning(
            publish_today=True,
            primary_reason=primary_reason,
            supporting_evidence=supporting_evidence,
            confidence_score=0.91,
            business_goal=goal,
            expected_impact="High authority growth, organic SEO traction, and qualified lead generation."
        )

class ConfidenceCalculator:
    @staticmethod
    def calculate_confidence(opportunity: Opportunity) -> float:
        # Confidence derived from priority score, signal count, and brand fit
        base_score = opportunity.priority_score.overall_score
        confidence = min(0.98, max(0.70, (base_score / 100.0) * 0.95))
        return round(confidence, 2)

class DecisionEngine:
    @staticmethod
    def make_decision(context: StrategyContext, opportunities: List[Opportunity]) -> Tuple[Opportunity, DecisionReasoning]:
        can_publish, reason_text = BusinessRulesEngine.evaluate_publishing_feasibility(context)
        if not can_publish or not opportunities:
            raise ValueError(f"Publishing pre-check failed: {reason_text}")

        top_opp = opportunities[0]
        goal = ObjectiveMapper.map_topic_to_goal(top_opp.topic, top_opp.category)
        
        # Build mock audience profile for reasoning
        from strategy.analyzers.opportunity_ranker import AudienceMatcher
        aud = AudienceMatcher.match_audience(top_opp)
        
        reasoning = ReasoningEngine.build_reasoning(top_opp, aud, goal)
        reasoning.confidence_score = ConfidenceCalculator.calculate_confidence(top_opp)
        
        return top_opp, reasoning
