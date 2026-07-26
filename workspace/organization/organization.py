"""
Organization Data Model and Organization Manager.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class Organization:
    organization_id: str
    name: str
    industry: str = "Technology"
    timezone_str: str = "UTC"
    website: str = ""
    settings: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=_get_utc_now)

class OrganizationManager:
    def __init__(self):
        self._orgs: Dict[str, Organization] = {}

    def create_organization(self, name: str, industry: str = "Technology", website: str = "") -> Organization:
        org_id = f"org_{int(datetime.now().timestamp())}_{abs(hash(name))%1000:03d}"
        org = Organization(organization_id=org_id, name=name, industry=industry, website=website)
        self._orgs[org_id] = org
        return org

    def get_organization(self, org_id: str) -> Optional[Organization]:
        return self._orgs.get(org_id)

    def list_organizations(self) -> List[Organization]:
        return list(self._orgs.values())
