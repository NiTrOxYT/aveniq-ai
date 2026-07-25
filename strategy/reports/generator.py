"""
Strategy Report Generator for AVENIQ Strategy Department.
Generates Daily Strategy Reports, Weekly Strategy Summaries, and Monthly Strategic Roadmaps.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List
from strategy.planners.marketing_planner import ChiefStrategyOfficer
from strategy.storage.manager import StrategyStorageManager

class StrategyReportGenerator:
    def __init__(self, root_dir: str = "."):
        self.cso = ChiefStrategyOfficer(root_dir)
        self.storage = StrategyStorageManager()

    def generate_daily_report(self) -> Dict[str, Any]:
        plan = self.cso.generate_daily_marketing_plan()
        self.storage.save_daily_plan(plan)

        return {
            "report_type": "daily",
            "date": plan.date,
            "primary_goal": plan.primary_goal,
            "business_objective": plan.business_objective,
            "publish_today": plan.publish_today,
            "priority": f"{plan.priority_score}/100",
            "confidence": f"{plan.confidence_percentage}%",
            "audience": {
                "primary_audience": plan.audience.primary_audience,
                "buying_intent": plan.audience.buying_intent,
                "awareness_stage": plan.audience.awareness_stage,
                "persona": plan.audience.customer_persona
            },
            "content": {
                "category": plan.content.category,
                "content_format": plan.content.content_format,
                "suggested_title": plan.content.suggested_title,
                "unique_angle": plan.content.unique_angle,
                "platforms": plan.content.target_platforms,
                "call_to_action": plan.content.call_to_action
            },
            "seo": {
                "primary_keyword": plan.seo.primary_keyword,
                "secondary_keywords": plan.seo.secondary_keywords,
                "search_intent": plan.seo.search_intent,
                "content_cluster": plan.seo.content_cluster
            },
            "reasoning": {
                "primary_reason": plan.decision_reasoning.primary_reason,
                "supporting_evidence": plan.decision_reasoning.supporting_evidence,
                "expected_impact": plan.decision_reasoning.expected_impact
            },
            "campaign": plan.campaign.name if plan.campaign else None
        }

    def generate_weekly_report(self) -> Dict[str, Any]:
        today_plan = self.cso.generate_daily_marketing_plan()
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        return {
            "report_type": "weekly",
            "date": today_str,
            "top_campaign": today_plan.campaign.name if today_plan.campaign else "Enterprise AI Automation Sprint",
            "publishing_frequency": "5 Times / Week (Mon-Fri)",
            "content_mix": [
                "2x Educational Guides (Next.js / TypeScript)",
                "1x Case Study (SaaS Multi-Tenancy & Postgres)",
                "1x Tutorial (n8n Workflow Automation)",
                "1x Authority Deep-Dive (Autonomous AI Agents)"
            ],
            "top_opportunities": [
                "Autonomous AI Agents for Business Operations",
                "n8n Open-Source Workflow Automation vs Proprietary SaaS",
                "Scaling SaaS Multi-Tenancy with PostgreSQL Row-Level Security"
            ],
            "seo_priorities": [
                "Primary Keyword: AI Business Automation",
                "Supporting Keywords: AI Agents, n8n Automation, SaaS Multi-Tenancy"
            ],
            "competitor_focus": "Differentiate via zero vendor lock-in, custom engineering, and self-hosted n8n workflows.",
            "business_goals": ["Lead Generation", "Brand Authority", "SEO Growth"]
        }

    def generate_monthly_report(self) -> Dict[str, Any]:
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        return {
            "report_type": "monthly",
            "month": datetime.now(timezone.utc).strftime("%B %Y"),
            "content_calendar": "20 Actionable Recommendations Scheduled Across 4 Sprints",
            "campaign_calendar": [
                "Week 1: AI Automation Week",
                "Week 2: Startup MVP Sprint",
                "Week 3: Restaurant & Hospitality Digitalization",
                "Week 4: Enterprise Custom Software Infrastructure"
            ],
            "keyword_roadmap": [
                "Phase 1: High-intent Commercial Keywords (custom saas development, ai agents company)",
                "Phase 2: Informational Search Keywords (how to build n8n workflows, postgres rls saas)"
            ],
            "authority_plan": "Publish 4 authoritative engineering case studies and 2 interactive architecture calculators.",
            "lead_generation_plan": "Drive 25+ executive discovery consultations through targeted LinkedIn and web CTAs.",
            "brand_growth_plan": "Establish AVENIQ as top-tier software and AI engineering partner in target markets."
        }
