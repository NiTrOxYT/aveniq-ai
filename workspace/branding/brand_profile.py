"""
Workspace Brand Profile & Workspace Credentials Isolation Manager.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class BrandProfile:
    workspace_id: str
    brand_name: str
    logo_url: str = ""
    primary_color: str = "#4F46E5"
    secondary_color: str = "#10B981"
    font_family: str = "Inter, sans-serif"
    tone_of_voice: str = "Authoritative, Visionary, Modern"
    target_audience: str = "Enterprise CTOs & AI Engineers"
    writing_style_guidelines: str = "Clear, concise, evidence-backed with code snippets."

class WorkspaceCredentialsManager:
    def __init__(self):
        self._credentials: Dict[str, Dict[str, str]] = {}

    def set_api_key(self, workspace_id: str, provider: str, api_key: str):
        if workspace_id not in self._credentials:
            self._credentials[workspace_id] = {}
        self._credentials[workspace_id][provider] = api_key

    def get_api_key(self, workspace_id: str, provider: str) -> Optional[str]:
        return self._credentials.get(workspace_id, {}).get(provider)
