"""
Company Brain Input Normalizer for Strategy Department.
"""

import os, json
from typing import Dict, Any, List

class CompanyInputNormalizer:
    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir

    def load_company_context(self) -> Dict[str, Any]:
        company_file = os.path.join(self.root_dir, "knowledge/company/company.md")
        brand_file = os.path.join(self.root_dir, "knowledge/brand/brand.md")

        company_raw = ""
        brand_raw = ""

        if os.path.exists(company_file):
            with open(company_file, "r", encoding="utf-8") as f:
                company_raw = f.read()

        if os.path.exists(brand_file):
            with open(brand_file, "r", encoding="utf-8") as f:
                brand_raw = f.read()

        services = [
            "web-development", "saas-development", "custom-software-development",
            "ai-automation", "ai-agents", "mobile-app-development",
            "ui-ux-design", "api-integration", "cloud-deployment", "maintenance-support"
        ]

        return {
            "company_name": "AVENIQ",
            "mission": "Empower businesses with intelligent software that simplifies operations and accelerates growth.",
            "target_industries": ["Hospitality", "Healthcare", "Education", "Retail", "E-commerce", "SaaS", "Enterprise"],
            "core_services": services,
            "tech_stack": ["React", "Next.js", "TypeScript", "Node.js", "PostgreSQL", "Supabase", "Docker", "n8n", "OpenAI", "Claude", "Gemini"],
            "has_brand_guide": len(brand_raw) > 0,
            "has_company_profile": len(company_raw) > 0
        }
