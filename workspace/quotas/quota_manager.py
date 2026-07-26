"""
Resource Quotas Tracker and Portable Workspace Export/Import Engine.
"""

import json
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class WorkspaceQuota:
    workspace_id: str
    monthly_workflows_limit: int = 500
    monthly_workflows_used: int = 0
    generated_images_limit: int = 1000
    generated_images_used: int = 0
    llm_requests_limit: int = 5000
    llm_requests_used: int = 0

class WorkspaceQuotaManager:
    def __init__(self):
        self._quotas: Dict[str, WorkspaceQuota] = {}

    def get_quota(self, workspace_id: str) -> WorkspaceQuota:
        if workspace_id not in self._quotas:
            self._quotas[workspace_id] = WorkspaceQuota(workspace_id=workspace_id)
        return self._quotas[workspace_id]

    def record_workflow_usage(self, workspace_id: str):
        q = self.get_quota(workspace_id)
        q.monthly_workflows_used += 1

class WorkspaceExporterImporter:
    @staticmethod
    def export_workspace(workspace_id: str, brand: Any) -> str:
        data = {
            "version": "1.0.0",
            "workspace_id": workspace_id,
            "brand": {
                "brand_name": getattr(brand, "brand_name", "Acme"),
                "primary_color": getattr(brand, "primary_color", "#4F46E5"),
                "tone_of_voice": getattr(brand, "tone_of_voice", "Technical")
            },
            "exported_at": "2026-07-26T13:00:00Z"
        }
        return json.dumps(data, indent=2)

    @staticmethod
    def import_workspace(json_str: str) -> Dict[str, Any]:
        data = json.loads(json_str)
        return {
            "status": "Imported",
            "workspace_id": data.get("workspace_id"),
            "version": data.get("version")
        }
