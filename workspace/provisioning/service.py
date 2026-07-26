"""
Predefined Industry Workspace Templates Library and Provisioning Service.
"""

from typing import Dict, Any, List
from workspace.context.tenant_context import TenantContext

class TemplateLibrary:
    TEMPLATES = {
        "SaaS Startup": {
            "tone": "Technical, Visionary, Modern",
            "kpis": ["CTR", "Demo Requests", "Signups"],
            "schedule": "09:00 UTC",
            "primary_color": "#4F46E5"
        },
        "Digital Agency": {
            "tone": "Bold, Persuasive, Results-Driven",
            "kpis": ["Client Leads", "Engagement", "Shares"],
            "schedule": "10:00 UTC",
            "primary_color": "#EC4899"
        },
        "E-commerce": {
            "tone": "Energetic, Visual, Promotional",
            "kpis": ["Clicks", "Sales Conversions", "ROI"],
            "schedule": "14:00 UTC",
            "primary_color": "#10B981"
        },
        "Healthcare": {
            "tone": "Empathetic, Authoritative, Educational",
            "kpis": ["Trust Score", "Read Time", "Inquiries"],
            "schedule": "08:00 UTC",
            "primary_color": "#06B6D4"
        },
        "Education": {
            "tone": "Informative, Encouraging, Academic",
            "kpis": ["Enrollments", "Downloads", "Shares"],
            "schedule": "11:00 UTC",
            "primary_color": "#F59E0B"
        }
    }

    @staticmethod
    def get_template(name: str) -> Dict[str, Any]:
        return TemplateLibrary.TEMPLATES.get(name, TemplateLibrary.TEMPLATES["SaaS Startup"])

class ProvisioningService:
    @staticmethod
    def provision_workspace(tenant: TenantContext, template_name: str = "SaaS Startup") -> Dict[str, Any]:
        tpl = TemplateLibrary.get_template(template_name)
        return {
            "status": "Provisioned",
            "tenant": {
                "organization_id": tenant.organization_id,
                "workspace_id": tenant.workspace_id
            },
            "template": template_name,
            "preconfigured_settings": tpl,
            "components_initialized": [
                "Company Brain", "Archive", "Learning", "Calendar", "Automation", "Analytics", "Provider Config"
            ]
        }
