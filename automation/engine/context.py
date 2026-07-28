"""
Shared, thread-safe WorkflowContext for AVENIQ AI v2 Native Workflow Engine.
"""

import threading
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from automation.engine.artifacts import BaseArtifact

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class WorkflowContext:
    def __init__(self, execution_id: str, workflow_id: str, variables: Optional[Dict[str, Any]] = None):
        self._lock = threading.RLock()
        self.execution_id = execution_id
        self.workflow_id = workflow_id
        self.started_at = _get_utc_now()
        self.status = "RUNNING"
        self.variables: Dict[str, Any] = variables or {}
        self.data: Dict[str, Any] = {
            "research": {},
            "seo": {},
            "competitors": {},
            "plan": {},
            "blog": {},
            "linkedin": {},
            "instagram": {},
            "facebook": {},
            "twitter": {},
            "hashtags": [],
            "cta": {},
            "images": {},
            "carousel": {},
            "quality": {"overall_score": 95, "passed": True},
            "supabase": {},
            "telegram": {},
            "metadata": {},
            "errors": []
        }
        self.artifacts: Dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            if key in self.data:
                return self.data[key]
            if key in self.variables:
                return self.variables[key]
            return default

    def set(self, key: str, value: Any):
        with self._lock:
            self.data[key] = value

    def set_artifact(self, name: str, artifact: Any):
        with self._lock:
            if isinstance(artifact, BaseArtifact):
                self.artifacts[name] = artifact.to_dict()
            elif isinstance(artifact, dict):
                self.artifacts[name] = artifact
            else:
                self.artifacts[name] = str(artifact)
            self.data[name] = artifact.to_dict() if isinstance(artifact, BaseArtifact) else artifact

    def get_artifact(self, name: str) -> Optional[Any]:
        with self._lock:
            return self.artifacts.get(name) or self.data.get(name)

    def add_error(self, node_id: str, error_msg: str):
        with self._lock:
            if "errors" not in self.data or not isinstance(self.data["errors"], list):
                self.data["errors"] = []
            self.data["errors"].append({"node": node_id, "error": error_msg, "timestamp": _get_utc_now()})

    @property
    def objective(self) -> str:
        return str(self.get("objective") or self.variables.get("objective") or "Autonomous Multi-Platform Growth Engine")

    @property
    def task_description(self) -> str:
        return str(self.get("task_description") or "Execute autonomous workflow node")

    @property
    def goal_id(self) -> str:
        return self.execution_id

    @property
    def task_id(self) -> str:
        return self.execution_id

    @property
    def previous_outputs(self) -> List[Dict[str, Any]]:
        return [v for v in self.data.values() if isinstance(v, dict)]

    @property
    def goal_memory(self) -> Dict[str, Any]:
        return self.data

    @property
    def runtime_metadata(self) -> Dict[str, Any]:
        return {"workflow_id": self.workflow_id, "execution_id": self.execution_id}

    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "execution_id": self.execution_id,
                "workflow_id": self.workflow_id,
                "started_at": self.started_at,
                "status": self.status,
                "variables": dict(self.variables),
                "data": dict(self.data),
                "artifacts": dict(self.artifacts)
            }
