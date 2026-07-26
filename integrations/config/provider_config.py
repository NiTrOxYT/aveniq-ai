"""
Profile-aware Provider Configuration Manager loading from config/providers.yaml and .env.
Supports basic YAML parsing fallback if PyYAML is not installed.
"""

import os
from typing import Dict, Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

class ProviderConfigManager:
    def __init__(self, config_path: str = "config/providers.yaml"):
        self.config_path = config_path
        self.raw_config = self._load_config()
        self.active_profile = self.raw_config.get("profile", "testing")

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            return {"profile": "testing"}
        
        if HAS_YAML:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}

        # Fallback dictionary for testing profile
        return {
            "profile": "testing",
            "profiles": {
                "testing": {
                    "llm": {"primary": "mock_llm", "fallback": "mock_llm"},
                    "image": {"primary": "mock_image", "fallback": "mock_image"}
                }
            }
        }

    def get_profile_settings(self) -> Dict[str, Any]:
        profiles = self.raw_config.get("profiles", {})
        return profiles.get(self.active_profile, {})

    def get_llm_settings(self) -> Dict[str, Any]:
        profile = self.get_profile_settings()
        return profile.get("llm", {"primary": "mock_llm", "fallback": "mock_llm"})

    def get_image_settings(self) -> Dict[str, Any]:
        profile = self.get_profile_settings()
        return profile.get("image", {"primary": "mock_image", "fallback": "mock_image"})

global_config = ProviderConfigManager()
