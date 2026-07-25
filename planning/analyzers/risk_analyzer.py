"""
Risk Analyzer & Capacity Estimator for Planning Department.
"""

from typing import List, Dict, Any, Tuple
from planning.models.schema import RiskAssessment, CapacityEstimate, PlanningContext

class RiskAnalyzer:
    @staticmethod
    def analyze_risks(context: PlanningContext) -> RiskAssessment:
        conflicts = []
        overload = []
        missing_deps = []
        mitigation = []

        # Check if research package has knowledge gaps
        gaps = context.research_package.get("knowledge_gaps", [])
        if gaps:
            missing_deps.append(f"Research package has unresolved gaps: {', '.join(gaps)}")
            mitigation.append("Resolve technical research gaps before starting creative production.")

        # Check publishing cadence
        if context.publishing_history.get("cadence") == "Daily":
            overload.append("Daily publishing cadence risks bottlenecking code review cycles.")
            mitigation.append("Batch asset production 48 hours ahead of publishing window.")

        risk_score = round(20.0 + (len(conflicts) + len(overload) + len(missing_deps)) * 10.0, 1)

        return RiskAssessment(
            risk_score=min(100.0, risk_score),
            schedule_conflicts=conflicts,
            resource_overload=overload,
            missing_dependencies=missing_deps,
            mitigation_plan=mitigation if mitigation else ["Proceed with standard production timeline."]
        )

class CapacityPlanner:
    @staticmethod
    def estimate_capacity(deliverables_count: int = 5) -> CapacityEstimate:
        prod_hours = deliverables_count * 3.5
        review_hours = deliverables_count * 1.0
        creative_score = round(deliverables_count * 12.5, 1)
        pub_score = round(deliverables_count * 8.0, 1)

        return CapacityEstimate(
            deliverable_count=deliverables_count,
            estimated_production_hours=prod_hours,
            estimated_review_hours=review_hours,
            creative_workload_score=creative_score,
            publishing_workload_score=pub_score
        )
