"""
Immutable Decision Logger & Feedback Engine for Human Approval System.
"""

from typing import List, Dict, Any
from approval.models.schema import HumanDecision, FeedbackRecord, TimelineEvent

class DecisionLogger:
    @staticmethod
    def log_decision(session_id: str, decision_type: str, reviewer_id: str, rationale: str) -> HumanDecision:
        return HumanDecision(
            session_id=session_id,
            decision=decision_type,
            reviewer_id=reviewer_id,
            rationale=rationale
        )

    @staticmethod
    def create_timeline_event(event_type: str, actor: str, details: str) -> TimelineEvent:
        from datetime import datetime, timezone
        return TimelineEvent(
            event_id=f"evt_timeline_{abs(hash(details))%1000:03d}",
            event_type=event_type,
            actor=actor,
            timestamp=datetime.now(timezone.utc).isoformat(),
            details=details
        )
