"""
Typed Configuration System for AVENIQ AI Runtime v1.
Centralized, validated configuration reading environment variables, config files, and runtime overrides.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class RuntimeConfig:
    env: str = field(default_factory=lambda: os.getenv("AVENIQ_ENV", "production"))
    debug: bool = field(default_factory=lambda: os.getenv("AVENIQ_DEBUG", "false").lower() in ("true", "1"))
    port: int = field(default_factory=lambda: int(os.getenv("PORT", "8097")))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    
    # Provider keys
    github_token: Optional[str] = field(default_factory=lambda: os.getenv("GITHUB_TOKEN"))
    reddit_client_id: Optional[str] = field(default_factory=lambda: os.getenv("REDDIT_CLIENT_ID"))
    reddit_client_secret: Optional[str] = field(default_factory=lambda: os.getenv("REDDIT_CLIENT_SECRET"))
    reddit_user_agent: str = field(default_factory=lambda: os.getenv("REDDIT_USER_AGENT", "AVENIQ Research Engine/1.0"))
    
    # Overrides map
    overrides: Dict[str, Any] = field(default_factory=dict)

    def set_override(self, key: str, value: Any):
        self.overrides[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        if key in self.overrides:
            return self.overrides[key]
        return getattr(self, key, default)


global_runtime_config = RuntimeConfig()
