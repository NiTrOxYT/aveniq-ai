"""
Shared TenantContext Data Model for Multi-Tenant Isolation.
Ensures every execution, request, and log strictly belongs to an Organization & Workspace.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class TenantContext:
    organization_id: str
    workspace_id: str
    user_id: str = "usr_system"
    role: str = "Admin"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_valid(self) -> bool:
        return bool(self.organization_id and self.workspace_id)
