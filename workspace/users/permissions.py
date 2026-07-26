"""
User Management and Role-Based Access Control (RBAC) Permissions.
Roles: Owner, Admin, Manager, Editor, Viewer.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum

class Role(str, Enum):
    OWNER = "Owner"
    ADMIN = "Admin"
    MANAGER = "Manager"
    EDITOR = "Editor"
    VIEWER = "Viewer"

@dataclass
class User:
    user_id: str
    email: str
    name: str
    role: Role = Role.EDITOR
    organization_id: str = ""
    workspace_ids: List[str] = field(default_factory=list)

class RBACEvaluator:
    PERMISSIONS = {
        Role.OWNER: ["manage_org", "manage_workspaces", "manage_users", "manage_billing", "run_workflows", "approve_campaigns", "view_analytics"],
        Role.ADMIN: ["manage_workspaces", "manage_users", "run_workflows", "approve_campaigns", "view_analytics"],
        Role.MANAGER: ["run_workflows", "approve_campaigns", "view_analytics"],
        Role.EDITOR: ["run_workflows", "edit_content", "view_analytics"],
        Role.VIEWER: ["view_analytics"]
    }

    @staticmethod
    def has_permission(user: User, action: str) -> bool:
        allowed = RBACEvaluator.PERMISSIONS.get(user.role, [])
        return action in allowed
