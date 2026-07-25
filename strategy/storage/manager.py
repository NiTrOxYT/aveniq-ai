"""
Strategy Storage Manager for AVENIQ Strategy Department.
Persists daily, weekly, and monthly reports into structured file storage.
"""

import os, json
from typing import Dict, Any, Optional
from strategy.models.schema import MarketingPlan, StrategyReport
from brain.utils.logger import get_logger

logger = get_logger("aveniq.strategy.storage")

class StrategyStorageManager:
    def __init__(self, base_dir: str = "strategy/storage"):
        self.base_dir = base_dir
        self.daily_dir = os.path.join(base_dir, "daily")
        self.weekly_dir = os.path.join(base_dir, "weekly")
        self.monthly_dir = os.path.join(base_dir, "monthly")
        self.campaigns_dir = os.path.join(base_dir, "campaigns")
        self.opportunities_dir = os.path.join(base_dir, "opportunities")
        self.history_dir = os.path.join(base_dir, "history")

        for d in [self.daily_dir, self.weekly_dir, self.monthly_dir, self.campaigns_dir, self.opportunities_dir, self.history_dir]:
            os.makedirs(d, exist_ok=True)

    def save_daily_plan(self, plan: MarketingPlan) -> str:
        filepath = os.path.join(self.daily_dir, f"{plan.date}.json")
        data = {
            "id": plan.id,
            "date": plan.date,
            "primary_goal": plan.primary_goal,
            "business_objective": plan.business_objective,
            "publish_today": plan.publish_today,
            "priority_score": plan.priority_score,
            "confidence_percentage": plan.confidence_percentage,
            "audience": {
                "primary_audience": plan.audience.primary_audience,
                "secondary_audience": plan.audience.secondary_audience,
                "buying_intent": plan.audience.buying_intent,
                "awareness_stage": plan.audience.awareness_stage,
                "industry": plan.audience.industry,
                "persona": plan.audience.customer_persona
            },
            "content": {
                "category": plan.content.category,
                "format": plan.content.content_format,
                "suggested_title": plan.content.suggested_title,
                "unique_angle": plan.content.unique_angle,
                "target_platforms": plan.content.target_platforms,
                "call_to_action": plan.content.call_to_action
            },
            "seo": {
                "primary_keyword": plan.seo.primary_keyword,
                "secondary_keywords": plan.seo.secondary_keywords,
                "search_intent": plan.seo.search_intent,
                "content_cluster": plan.seo.content_cluster
            },
            "decision_reasoning": {
                "primary_reason": plan.decision_reasoning.primary_reason,
                "supporting_evidence": plan.decision_reasoning.supporting_evidence,
                "confidence_score": plan.decision_reasoning.confidence_score,
                "expected_impact": plan.decision_reasoning.expected_impact
            },
            "expected_result": plan.expected_result
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Also persist to historical memory
        hist_path = os.path.join(self.history_dir, f"history_{plan.date}_{plan.id}.json")
        with open(hist_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved daily marketing plan to {filepath}")
        return filepath

    def get_latest_daily_plan(self) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.daily_dir) if f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.daily_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
