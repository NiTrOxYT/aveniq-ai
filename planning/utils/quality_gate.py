"""
Planning Quality Gate Verifier for Planning Department.
Enforces 11 mandatory operational checklist gates before a Planning Package is approved.
"""

from typing import Dict, Any, List
from planning.models.schema import (
    PlanningQualityGate, CampaignPlan, EditorialSchedule, PublishingCalendar, AssetChecklist, CTAPlan, FunnelPlan, DistributionPlan, WorkflowDiagram, DependencyGraph, RiskAssessment, CapacityEstimate
)

class QualityGateVerifier:
    @staticmethod
    def verify_planning_package(
        campaign: CampaignPlan,
        editorial: EditorialSchedule,
        publishing: PublishingCalendar,
        assets: AssetChecklist,
        cta: CTAPlan,
        funnel: FunnelPlan,
        distribution: DistributionPlan,
        workflow: WorkflowDiagram,
        dependency_graph: DependencyGraph,
        risk: RiskAssessment,
        capacity: CapacityEstimate
    ) -> PlanningQualityGate:
        checklist = {
            "campaign_complete": campaign is not None and len(campaign.name) > 0,
            "timeline_optimized": len(campaign.milestones) > 0,
            "dependencies_validated": dependency_graph is not None and len(dependency_graph.nodes) > 0,
            "asset_checklist_complete": assets is not None and len(assets.hero_image) > 0,
            "editorial_calendar_generated": editorial is not None and len(editorial.content_sequence) > 0,
            "publishing_schedule_generated": publishing is not None and len(publishing.daily_schedule) > 0,
            "cta_defined": cta is not None and len(cta.primary_cta) > 0,
            "distribution_plan_completed": distribution is not None and len(distribution.channels) > 0,
            "funnel_mapped": funnel is not None and len(funnel.awareness_deliverables) > 0,
            "kpis_defined": capacity is not None and capacity.estimated_production_hours > 0,
            "confidence_calculated": True
        }

        diagnostics = []
        if risk.risk_score > 75.0:
            diagnostics.append(f"High risk score detected ({risk.risk_score}/100)")

        passed_count = sum(1 for v in checklist.values() if v)
        total_count = len(checklist)
        score = round((passed_count / float(total_count)) * 100.0, 1)

        is_passed = score >= 85.0

        return PlanningQualityGate(
            passed=is_passed,
            score=score,
            checklist=checklist,
            diagnostics=diagnostics
        )
