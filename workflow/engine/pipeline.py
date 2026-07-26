"""
Configurable Pipeline Definition and Default Workflow Configuration.
Pipeline defines department execution order dynamically.
"""

from typing import List, Dict, Any

class WorkflowConfig:
    DEFAULT_PIPELINE = [
        "company_brain",
        "market",
        "growth",
        "strategy",
        "calendar",
        "planning",
        "content",
        "creative",
        "editorial",
        "delivery",
        "approval",
        "archive",
        "learning"
    ]

    @staticmethod
    def load_pipeline_config(config_dict: Dict[str, Any] = None) -> List[str]:
        if config_dict and "pipeline" in config_dict:
            return config_dict["pipeline"]
        return WorkflowConfig.DEFAULT_PIPELINE

class Pipeline:
    def __init__(self, steps: List[str] = None):
        self.steps = steps or WorkflowConfig.DEFAULT_PIPELINE

    def get_steps(self) -> List[str]:
        return self.steps
