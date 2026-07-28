"""
Dataclass schema definitions for WorkflowDefinition, WorkflowNode, and RetryPolicy.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from automation.engine.node_state import NodeState

@dataclass
class RetryPolicy:
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: float = 30.0
    exponential_backoff: bool = True
    fallback_strategy: str = "default"

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> "RetryPolicy":
        if not data:
            return cls()
        return cls(
            max_retries=int(data.get("max_retries", 3)),
            retry_delay=float(data.get("retry_delay", 1.0)),
            timeout=float(data.get("timeout", 30.0)),
            exponential_backoff=bool(data.get("exponential_backoff", True)),
            fallback_strategy=str(data.get("fallback_strategy", "default"))
        )

@dataclass
class WorkflowNode:
    id: str
    type: str = "agent"
    agent: str = ""
    depends_on: List[str] = field(default_factory=list)
    timeout: float = 30.0
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    enabled: bool = True
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: List[str] = field(default_factory=list)
    condition: Optional[str] = None
    state: NodeState = NodeState.WAITING

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowNode":
        return cls(
            id=str(data.get("id", "")),
            type=str(data.get("type", "agent")),
            agent=str(data.get("agent") or data.get("id") or ""),
            depends_on=list(data.get("depends_on", [])),
            timeout=float(data.get("timeout", 30.0)),
            retry_policy=RetryPolicy.from_dict(data.get("retry_policy") or data.get("retry")),
            enabled=bool(data.get("enabled", True)),
            inputs=dict(data.get("inputs", {})),
            outputs=list(data.get("outputs", [])),
            condition=data.get("condition"),
            state=NodeState(data.get("state", NodeState.WAITING.value))
        )

@dataclass
class WorkflowDefinition:
    workflow_id: str
    name: str
    version: str = "1.0.0"
    trigger: Dict[str, Any] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)
    outputs: List[str] = field(default_factory=list)
    nodes: List[WorkflowNode] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowDefinition":
        nodes_raw = data.get("nodes") or data.get("graph") or []
        nodes = [WorkflowNode.from_dict(n) for n in nodes_raw]
        return cls(
            workflow_id=str(data.get("workflow_id") or data.get("id") or "unnamed_workflow"),
            name=str(data.get("name") or "Unnamed Workflow"),
            version=str(data.get("version") or "1.0.0"),
            trigger=dict(data.get("trigger", {})),
            variables=dict(data.get("variables", {})),
            outputs=list(data.get("outputs", [])),
            nodes=nodes
        )
