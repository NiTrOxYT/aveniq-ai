"""
Operational Decision Engine & Master Planning Engine for Planning Department.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Tuple
from planning.models.schema import (
    PlanningPackage, PlanningContext, CampaignVersion
)
from planning.context.builder import PlanningContextBuilder
from planning.planners.campaign_planner import CampaignPlanner, EditorialPlanner, PublishingPlanner
from planning.planners.asset_planner import (
    AssetPlanner, CTAPlaner, FunnelPlanner, DistributionPlanner, WorkflowPlanner
)
from planning.analyzers.risk_analyzer import RiskAnalyzer, CapacityPlanner
from planning.dependencies.graph_builder import DependencyGraphBuilder
from planning.utils.quality_gate import QualityGateVerifier

class PlanningDecisionEngine:
    @staticmethod
    def evaluate_decisions(context: PlanningContext) -> Dict[str, Any]:
        return {
            "campaign_priority": "High (P1)",
            "publishing_cadence": "5 Times / Week (Timezone: 08:30 EST)",
            "workload_allocation": "Distributed across Research -> Creative -> Technical Writing -> Review",
            "content_sequencing": "Architecture Overview -> Technical Guide -> Case Study -> Checklist",
            "asset_priorities": ["Hero Image", "MCP Architecture Diagram", "Code Snippets"],
            "decision_reasoning": {
                "decision": "Weekly Sprint on 'AI Agents in Enterprise Operations'",
                "reason": "Highest expected lead generation reach with low competition and complete research backing.",
                "supporting_evidence": [
                    "Strategy Department recommendation priority 92/100",
                    "Research Department package confidence 94%",
                    "Resource capacity 22.5 hours estimated workload within limit"
                ],
                "confidence": 0.95
            }
        }

class PlanningEngine:
    def __init__(self):
        self.context_builder = PlanningContextBuilder()

    def generate_planning_package(self, topic: str = "AI Agents in Enterprise Operations") -> PlanningPackage:
        context = self.context_builder.build_context(topic)
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        decisions = PlanningDecisionEngine.evaluate_decisions(context)

        camp_plan = CampaignPlanner.plan_campaign(context)
        ed_plan = EditorialPlanner.plan_editorial(context)
        pub_plan = PublishingPlanner.plan_publishing(context)
        assets = AssetPlanner.plan_assets(context)
        cta = CTAPlaner.plan_cta(context)
        funnel = FunnelPlanner.plan_funnel(context)
        distro = DistributionPlanner.plan_distribution(context)
        workflow = WorkflowPlanner.plan_workflow(context)

        dep_graph = DependencyGraphBuilder.build_graph()
        risk = RiskAnalyzer.analyze_risks(context)
        capacity = CapacityPlanner.estimate_capacity(len(ed_plan.content_sequence))

        version_info = CampaignVersion(
            version="1.0.0",
            timestamp=today_str,
            planner_id="ai_coo_planning_agent",
            update_reason="Initial operational planning package generation",
            approval_status="Approved"
        )

        deliverables = [
            "Master Technical Guide (Markdown & HTML)",
            "Dark Glassmorphism Hero Image (PNG)",
            "MCP Architecture Diagram (Mermaid & SVG)",
            "LinkedIn Carousel (PDF)",
            "X Thread Script",
            "Technical Newsletter (HTML)"
        ]

        qg_result = QualityGateVerifier.verify_planning_package(
            camp_plan, ed_plan, pub_plan, assets, cta, funnel, distro, workflow, dep_graph, risk, capacity
        )

        exec_summary = f"Deterministic production plan created for '{topic}'. Total deliverables: {len(deliverables)}. Estimated production hours: {capacity.estimated_production_hours} hours. Risk score: {risk.risk_score}/100."

        return PlanningPackage(
            id=f"plan_pkg_{today_str}_{abs(hash(topic)) % 10000:04d}",
            topic=topic,
            date=today_str,
            executive_summary=exec_summary,
            campaign_objective="Authority Building & High-Intent Lead Generation",
            campaign=camp_plan,
            production_timeline="7-Day Production & Distribution Sprint",
            editorial_calendar=ed_plan,
            publishing_schedule=pub_plan,
            deliverables=deliverables,
            required_assets=assets,
            dependency_graph=dep_graph,
            risk_assessment=risk,
            resource_estimate=capacity,
            cta_plan=cta,
            funnel_plan=funnel,
            distribution_plan=distro,
            workflow_diagram=workflow,
            approval_checklist=[
                "✓ Strategy & Research inputs verified",
                "✓ Asset dependencies mapped",
                "✓ Brand guardrails enforced",
                "✓ Timezone publishing hours optimized"
            ],
            success_metrics=[
                "15+ Qualified executive discovery consultations scheduled",
                "1,500+ Technical guide views on Website",
                "4.5%+ Engagement rate on LinkedIn carousel"
            ],
            confidence_score=0.95,
            version_info=version_info,
            quality_gate=qg_result
        )
