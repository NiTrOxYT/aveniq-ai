"""
Approval State Machine & Centralized Action Router for Human Approval System.
"""

from typing import Dict, Any, Tuple
from approval.models.schema import ActionRequest

class ApprovalStateMachine:
    VALID_TRANSITIONS = {
        "CREATED": ["PENDING_REVIEW"],
        "PENDING_REVIEW": ["IN_REVIEW"],
        "IN_REVIEW": ["APPROVED", "REJECTED", "CHANGES_REQUESTED"],
        "CHANGES_REQUESTED": ["REGENERATING"],
        "REGENERATING": ["IN_REVIEW"],
        "APPROVED": ["ARCHIVED"],
        "REJECTED": ["ARCHIVED"],
        "ARCHIVED": []
    }

    @staticmethod
    def can_transition(current: str, target: str) -> bool:
        allowed = ApprovalStateMachine.VALID_TRANSITIONS.get(current, [])
        return target in allowed

class ActionRouter:
    MAPPER = {
        "Approve": ("Archive", "Approved & released for publication"),
        "Reject": ("SessionClosed", "Campaign rejected and terminated"),
        "Rewrite": ("Content", "Request article and post copy rewrite"),
        "Technical": ("Content", "Increase technical depth and benchmark detail"),
        "Simplify": ("Content", "Simplify language and improve readability"),
        "RegenerateHero": ("Creative", "Generate new 3D hero image concept"),
        "GenerateVideo": ("Creative", "Generate 4k Sora video storyboard"),
        "FixSources": ("Editorial", "Re-verify citations and research sources"),
        "ImproveHashtags": ("Delivery", "Refresh social hashtags and CTAs"),
        "DifferentAngle": ("Strategy", "Re-pivot campaign angle and positioning")
    }

    @staticmethod
    def route_action(action_type: str, reviewer_id: str, notes: str) -> Tuple[ActionRequest, str]:
        target_dept, desc = ActionRouter.MAPPER.get(action_type, ("Content", "General refinement request"))
        request = ActionRequest(
            action_id=f"act_{action_type.lower()[:4]}_{abs(hash(notes))%1000:03d}",
            action_type=action_type,
            target_department=target_dept,
            reviewer_id=reviewer_id,
            notes=notes
        )
        return request, desc
