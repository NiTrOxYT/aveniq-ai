"""
Planning Report Generator for Planning Department.
Formats planning packages into operational JSON blueprints.
"""

from typing import Dict, Any
from planning.engine.planning_engine import PlanningEngine
from planning.storage.manager import PlanningStorageManager

class PlanningReportGenerator:
    def __init__(self):
        self.engine = PlanningEngine()
        self.storage = PlanningStorageManager()

    def generate_planning_report(self, topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        pkg = self.engine.generate_planning_package(topic)
        self.storage.save_package(pkg)

        return {
            "report_type": "planning_package",
            "package_id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "campaign_objective": pkg.campaign_objective,
            "confidence_score": f"{int(pkg.confidence_score * 100)}%",
            "version": pkg.version_info.version,
            "approval_status": pkg.version_info.approval_status,
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": f"{pkg.quality_gate.score}%",
                "checklist": pkg.quality_gate.checklist
            },
            "campaign": {
                "name": pkg.campaign.name,
                "theme": pkg.campaign.theme,
                "duration_days": pkg.campaign.duration_days,
                "milestones": pkg.campaign.milestones,
                "stages": pkg.campaign.stages
            },
            "production_timeline": pkg.production_timeline,
            "deliverables": pkg.deliverables,
            "editorial_calendar": {
                "sequence": pkg.editorial_calendar.content_sequence,
                "publishing_order": pkg.editorial_calendar.publishing_order,
                "topic_progression": pkg.editorial_calendar.topic_progression,
                "user_journey": pkg.editorial_calendar.user_journey_map
            },
            "publishing_schedule": {
                "daily_schedule": pkg.publishing_schedule.daily_schedule,
                "timezone_aware_plan": pkg.publishing_schedule.timezone_aware_plan
            },
            "required_assets": {
                "hero_image": pkg.required_assets.hero_image,
                "infographics": pkg.required_assets.infographics,
                "diagrams": pkg.required_assets.architecture_diagrams,
                "charts": pkg.required_assets.charts,
                "code_snippets": pkg.required_assets.code_snippets
            },
            "dependency_graph": {
                "nodes": [
                    {
                        "id": n.deliverable_id,
                        "title": n.title,
                        "requires": n.requires,
                        "produces": n.produces,
                        "blocks": n.blocks
                    } for n in pkg.dependency_graph.nodes
                ],
                "critical_path": pkg.dependency_graph.critical_path,
                "max_depth": pkg.dependency_graph.max_dependency_depth
            },
            "risk_assessment": {
                "risk_score": f"{pkg.risk_assessment.risk_score}/100",
                "schedule_conflicts": pkg.risk_assessment.schedule_conflicts,
                "resource_overload": pkg.risk_assessment.resource_overload,
                "mitigation_plan": pkg.risk_assessment.mitigation_plan
            },
            "resource_estimate": {
                "deliverable_count": pkg.resource_estimate.deliverable_count,
                "estimated_production_hours": pkg.resource_estimate.estimated_production_hours,
                "estimated_review_hours": pkg.resource_estimate.estimated_review_hours
            },
            "cta_plan": {
                "primary": pkg.cta_plan.primary_cta,
                "secondary": pkg.cta_plan.secondary_cta,
                "lead_magnet": pkg.cta_plan.lead_magnet_url,
                "consultation_url": pkg.cta_plan.discovery_consultation_url
            },
            "funnel_plan": {
                "awareness": pkg.funnel_plan.awareness_deliverables,
                "consideration": pkg.funnel_plan.consideration_deliverables,
                "decision": pkg.funnel_plan.decision_deliverables
            },
            "distribution_plan": {
                "channels": pkg.distribution_plan.channels,
                "schedules": pkg.distribution_plan.platform_schedules,
                "sequence": pkg.distribution_plan.cross_posting_sequence
            },
            "workflow_diagram": {
                "current_state": pkg.workflow_diagram.current_state,
                "steps": pkg.workflow_diagram.sequential_steps,
                "step_owners": pkg.workflow_diagram.step_owners
            },
            "success_metrics": pkg.success_metrics
        }
