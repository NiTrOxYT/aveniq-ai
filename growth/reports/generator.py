"""
Growth Report Generator for Brand Growth Intelligence.
Formats growth packages into structured JSON optimization reports.
"""

from typing import Dict, Any
from growth.engine.growth_engine import GrowthEngine
from growth.storage.manager import GrowthStorageManager

class GrowthReportGenerator:
    def __init__(self):
        self.engine = GrowthEngine()
        self.storage = GrowthStorageManager()

    def generate_growth_report(self, topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        pkg = self.engine.generate_growth_package(topic)
        self.storage.save_package(pkg)

        return {
            "report_type": "growth_package",
            "growth_id": pkg.id,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "overall_growth_score": f"{pkg.metrics.overall_growth_score}/100",
            "version": pkg.version,
            "goals": [
                {
                    "id": g.goal_id,
                    "title": g.title,
                    "target": f"{g.target_value} {g.target_metric}",
                    "current": f"{g.current_value}",
                    "deadline": g.deadline,
                    "priority": g.priority
                } for g in pkg.goals
            ],
            "objective_tree": {
                "annual": pkg.objective_tree.annual_goal,
                "quarterly": pkg.objective_tree.quarterly_objectives,
                "monthly": pkg.objective_tree.monthly_campaign_goals
            },
            "forecast": {
                "expected_leads": pkg.kpi_forecast.expected_leads,
                "expected_reach": pkg.kpi_forecast.expected_reach,
                "expected_subscribers": pkg.kpi_forecast.expected_newsletter_subscribers,
                "confidence": f"{int(pkg.kpi_forecast.confidence_score * 100)}%"
            },
            "scenarios": [
                {
                    "name": s.scenario_name,
                    "projected_leads": s.projected_leads,
                    "projected_reach": s.projected_reach,
                    "campaigns_required": s.required_campaigns_count
                } for s in pkg.scenarios
            ],
            "portfolio": [
                {
                    "id": p.portfolio_id,
                    "name": p.campaign_name,
                    "type": p.campaign_type,
                    "stage": p.funnel_stage,
                    "kpi": p.target_kpi,
                    "weight": f"{p.allocated_weight_pct}%"
                } for p in pkg.portfolio
            ],
            "funnel_allocation": {
                "awareness": f"{pkg.funnel_allocation.awareness_pct}%",
                "interest": f"{pkg.funnel_allocation.interest_pct}%",
                "consideration": f"{pkg.funnel_allocation.consideration_pct}%",
                "evaluation": f"{pkg.funnel_allocation.evaluation_pct}%",
                "decision": f"{pkg.funnel_allocation.decision_pct}%",
                "retention": f"{pkg.funnel_allocation.retention_pct}%",
                "advocacy": f"{pkg.funnel_allocation.advocacy_pct}%"
            },
            "content_mix": {
                "educational": f"{pkg.content_mix.educational_pct}%",
                "thought_leadership": f"{pkg.content_mix.thought_leadership_pct}%",
                "case_studies": f"{pkg.content_mix.case_study_pct}%",
                "product": f"{pkg.content_mix.product_pct}%",
                "community": f"{pkg.content_mix.community_pct}%"
            },
            "metrics": {
                "kpi_coverage": f"{pkg.metrics.kpi_coverage_score}%",
                "funnel_balance": f"{pkg.metrics.funnel_balance_score}%",
                "diversity_score": f"{pkg.metrics.portfolio_diversity_score}%",
                "capacity_alignment": f"{pkg.metrics.capacity_alignment_score}%"
            },
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": f"{pkg.quality_gate.score}%",
                "checklist": pkg.quality_gate.checklist
            }
        }
