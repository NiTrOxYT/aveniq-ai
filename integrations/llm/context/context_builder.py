"""
Context Builder and Window Budgeting Engine for Real LLM Router.
Assembles prompt templates, workspace metadata, knowledge packages, and previous workflow outputs.
"""

import os
from typing import Dict, Any, Optional

class ContextBuilder:
    @staticmethod
    def build_context(department: str, variables: Dict[str, Any] = None) -> str:
        variables = variables or {}
        template_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
        template_path = os.path.join(template_dir, f"{department.lower()}.md")

        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as f:
                template_text = f.read()
        else:
            template_text = f"# {department.capitalize()} System Prompt\nProcess input for {department}."

        # Variable injection
        for k, v in variables.items():
            template_text = template_text.replace(f"{{{{{k}}}}}", str(v))

        return template_text
