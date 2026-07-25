"""
Asset, CTA, Funnel, Workflow, and Distribution Planners.
"""

from typing import List, Dict, Any
from planning.models.schema import (
    AssetChecklist, CTAPlan, FunnelPlan, DistributionPlan, WorkflowDiagram, PlanningContext
)

class AssetPlanner:
    @staticmethod
    def plan_assets(context: PlanningContext) -> AssetChecklist:
        topic = context.strategy_report.get("content", {}).get("suggested_title", "AI Operations")
        return AssetChecklist(
            hero_image=f"hero_dark_glassmorphism_{topic.lower().replace(' ', '_')}.png",
            infographics=["ai_agent_mcp_architecture_infographic.png"],
            architecture_diagrams=["mcp_agent_tool_execution_flow.mermaid"],
            charts=["latency_comparison_mcp_vs_rest.png"],
            screenshots=["n8n_workflow_canvas_screenshot.png"],
            code_snippets=["mcp_server_definition.ts", "pgvector_hnsw_query.sql"],
            demo_gifs=["agent_execution_demo.gif"],
            required_logos_icons=["aveniq_logo.svg", "nextjs_logo.svg", "postgres_logo.svg"]
        )

class CTAPlaner:
    @staticmethod
    def plan_cta(context: PlanningContext) -> CTAPlan:
        return CTAPlan(
            primary_cta="Schedule a custom discovery consultation with AVENIQ engineers",
            secondary_cta="Download the Enterprise AI Agent Architecture Blueprint",
            lead_magnet_url="https://aveniq.ai/resources/ai-agent-blueprint.pdf",
            newsletter_signup_url="https://aveniq.ai/newsletter",
            discovery_consultation_url="https://aveniq.ai/contact",
            github_repo_url="https://github.com/aveniq-ai/aveniq-brain"
        )

class FunnelPlanner:
    @staticmethod
    def plan_funnel(context: PlanningContext) -> FunnelPlan:
        return FunnelPlan(
            awareness_deliverables=["LinkedIn Architecture Carousel", "X Engineering Thread"],
            consideration_deliverables=["Master Technical Guide", "Benchmark Case Study"],
            decision_deliverables=["Custom Discovery Consultation Call", "Architecture Audit Proposal"],
            retention_deliverables=["Weekly AI Engineering Newsletter"],
            expansion_deliverables=["Custom Module Integration Sprint"]
        )

class DistributionPlanner:
    @staticmethod
    def plan_distribution(context: PlanningContext) -> DistributionPlan:
        return DistributionPlan(
            channels=["Website", "LinkedIn", "X", "GitHub", "Newsletter", "Dev.to"],
            platform_schedules={
                "Website": "Day 1 08:00 EST",
                "LinkedIn": "Day 1 08:30 EST",
                "X": "Day 1 09:15 EST",
                "Newsletter": "Day 3 10:00 EST",
                "Dev.to": "Day 4 11:00 EST"
            },
            cross_posting_sequence=["Website -> LinkedIn -> X -> Newsletter -> Dev.to"],
            timezone_optimal_hours=["08:30 EST", "13:30 UTC"]
        )

class WorkflowPlanner:
    @staticmethod
    def plan_workflow(context: PlanningContext) -> WorkflowDiagram:
        return WorkflowDiagram(
            current_state="Approved",
            sequential_steps=[
                "1. Research Complete",
                "2. Strategy & Planning Package Approved",
                "3. Creative Assets Produced",
                "4. Technical Article Written",
                "5. Internal Peer Review",
                "6. Publishing & Distribution Executed",
                "7. Analytics Tracking & Lead Capture Monitored"
            ],
            step_owners={
                "Research": "Research Department",
                "Planning": "Planning Department (COO)",
                "Creative": "Creative Department",
                "Writing": "Content Department",
                "Publishing": "Publishing Department"
            }
        )
