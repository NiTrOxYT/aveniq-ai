"""
Node State Machine definition for AVENIQ AI v2 Native Workflow Engine.
"""

from enum import Enum

class NodeState(str, Enum):
    WAITING = "WAITING"
    READY = "READY"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    SKIPPED = "SKIPPED"
    CANCELLED = "CANCELLED"
