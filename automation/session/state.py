"""
Automation State Enumeration for Automation Sessions.
"""

from enum import Enum

class AutomationState(str, Enum):
    CREATED = "CREATED"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    REGENERATING = "REGENERATING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
    LEARNING = "LEARNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
