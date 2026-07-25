"""
Campaign, Editorial, and Publishing Planners for Planning Department.
"""

from typing import List, Dict, Any
from planning.models.schema import (
    CampaignPlan, EditorialSchedule, PublishingCalendar, PlanningContext
)

class CampaignPlanner:
    @staticmethod
    def plan_campaign(context: PlanningContext) -> CampaignPlan:
        topic = context.strategy_report.get("content", {}).get("suggested_title", "Enterprise AI Operations")
        return CampaignPlan(
            id="camp_ops_001",
            name="Enterprise AI Systems Operational Sprint",
            theme=f"Scaling {topic}",
            duration_days=7,
            milestones=[
                "Day 1: Technical Research & Architecture Spec Signed Off",
                "Day 3: Hero Image & Architecture Diagrams Approved",
                "Day 5: Master Technical Guide Written & Reviewed",
                "Day 7: Multi-Channel Publishing & Analytics Tracking Active"
            ],
            stages=["Preparation", "Asset Production", "Content Review", "Distribution", "Analytics"]
        )

class EditorialPlanner:
    @staticmethod
    def plan_editorial(context: PlanningContext) -> EditorialSchedule:
        return EditorialSchedule(
            content_sequence=[
                "1. High-Level Architecture Overview",
                "2. Step-by-Step Technical Guide",
                "3. Benchmark Case Study Results",
                "4. Executive Checklist & Cheat-Sheet"
            ],
            publishing_order=["Technical Guide", "LinkedIn Carousel", "X Thread", "Newsletter"],
            topic_progression=[
                "Awareness: What are autonomous AI agents?",
                "Consideration: How does MCP protocol secure agent tool calls?",
                "Decision: Why choose AVENIQ custom software engineering?"
            ],
            internal_linking_strategy=[
                "Link Technical Guide to knowledge/services/ai-automation.md",
                "Link Case Study to knowledge/services/saas-development.md"
            ],
            user_journey_map=["Social Discovery -> Website Guide -> Book Discovery Consultation"]
        )

class PublishingPlanner:
    @staticmethod
    def plan_publishing(context: PlanningContext) -> PublishingCalendar:
        return PublishingCalendar(
            daily_schedule={
                "Monday": "Publish Technical Guide on Website & Blog",
                "Tuesday": "Post Architecture Breakdown Carousel on LinkedIn",
                "Wednesday": "Publish Engineering Thread on X",
                "Thursday": "Send Technical Deep-Dive Newsletter",
                "Friday": "Share Case Study Results Summary"
            },
            weekly_schedule={
                "Week 1": ["Technical Guide", "LinkedIn Carousel", "X Thread", "Newsletter"]
            },
            monthly_calendar={
                "July 2026": ["AI Automation Week", "SaaS Scalability Sprint"]
            },
            timezone_aware_plan="Publish at 08:30 EST (13:30 UTC) for optimal US/European executive engagement."
        )
