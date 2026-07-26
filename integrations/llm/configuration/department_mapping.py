"""
Department-to-Model Mapping Registry for AVENIQ AI Organization.
Configures default provider and model assignments for all 13 departments.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class DepartmentModelConfig:
    department: str
    provider: str
    model: str
    requires_llm: bool = True
    capabilities: list = None

DEPARTMENT_MODEL_MAP: Dict[str, DepartmentModelConfig] = {
    "company_brain": DepartmentModelConfig("company_brain", "gemini", "gemini-2.5-pro"),
    "market_intelligence": DepartmentModelConfig("market_intelligence", "gemini", "gemini-2.5-pro"),
    "growth": DepartmentModelConfig("growth", "gemini", "gemini-2.5-pro"),
    "strategy": DepartmentModelConfig("strategy", "gemini", "gemini-2.5-pro"),
    "planning": DepartmentModelConfig("planning", "openai", "gpt-5"),
    "content": DepartmentModelConfig("content", "openai", "gpt-5"),
    "creative": DepartmentModelConfig("creative", "openai", "gpt-5"),
    "creative_images": DepartmentModelConfig("creative_images", "openai", "gpt-image"),
    "editorial": DepartmentModelConfig("editorial", "openai", "gpt-5"),
    "learning": DepartmentModelConfig("learning", "gemini", "gemini-2.5-pro"),
    "calendar": DepartmentModelConfig("calendar", "none", "none", requires_llm=False),
    "delivery": DepartmentModelConfig("delivery", "none", "none", requires_llm=False),
    "archive": DepartmentModelConfig("archive", "none", "none", requires_llm=False),
    "approval": DepartmentModelConfig("approval", "human", "human-in-the-loop", requires_llm=False)
}

class DepartmentMappingRegistry:
    @staticmethod
    def get_config(department_name: str) -> Optional[DepartmentModelConfig]:
        return DEPARTMENT_MODEL_MAP.get(department_name.lower().replace(" ", "_"))

    @staticmethod
    def list_mappings() -> Dict[str, Dict[str, str]]:
        return {
            dept: {"provider": cfg.provider, "model": cfg.model, "requires_llm": cfg.requires_llm}
            for dept, cfg in DEPARTMENT_MODEL_MAP.items()
        }
