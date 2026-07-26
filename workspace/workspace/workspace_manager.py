"""
Workspace Data Model and Workspace Manager for multi-tenant isolation.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class Workspace:
    workspace_id: str
    organization_id: str
    name: str
    template: str = "SaaS Startup"
    active: bool = True
    config: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_get_utc_now)

class WorkspaceManager:
    def __init__(self):
        self._workspaces: Dict[str, Workspace] = {}

    def create_workspace(self, organization_id: str, name: str, template: str = "SaaS Startup") -> Workspace:
        ws_id = f"ws_{int(datetime.now().timestamp())}_{abs(hash(name))%1000:03d}"
        ws = Workspace(workspace_id=ws_id, organization_id=organization_id, name=name, template=template)
        self._workspaces[ws_id] = ws
        return ws

    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        return self._workspaces.get(workspace_id)

    def list_workspaces(self, organization_id: Optional[str] = None) -> List[Workspace]:
        if organization_id:
            return [w for w in self._workspaces.values() if w.organization_id == organization_id]
        return list(self._workspaces.values())
