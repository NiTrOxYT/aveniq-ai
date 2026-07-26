"""
Immutable Campaign Version Manager & History Repository.
Manages version directories (v1, v2, v3) under storage/campaigns/{campaign_id}/ and preserves parent-child relationships.
"""

import os
import json
import shutil
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class CampaignVersionManager:
    def __init__(self, base_storage_dir: str = "storage/campaigns"):
        self.base_storage_dir = base_storage_dir
        os.makedirs(self.base_storage_dir, exist_ok=True)

    def create_version(
        self,
        campaign_id: str,
        artifacts: Dict[str, Any],
        parent_version: Optional[str] = None,
        trigger_action: str = "INITIAL_GENERATION"
    ) -> Dict[str, Any]:
        campaign_dir = os.path.join(self.base_storage_dir, campaign_id)
        os.makedirs(campaign_dir, exist_ok=True)

        existing = [d for d in os.listdir(campaign_dir) if d.startswith("v") and os.path.isdir(os.path.join(campaign_dir, d))]
        v_num = len(existing) + 1
        version_id = f"v{v_num}"
        version_dir = os.path.join(campaign_dir, version_id)
        os.makedirs(version_dir, exist_ok=True)
        os.makedirs(os.path.join(version_dir, "images"), exist_ok=True)

        # Write core payload files
        for filename, content in artifacts.items():
            filepath = os.path.join(version_dir, filename)
            if isinstance(content, (dict, list)):
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(content, f, indent=2)
            elif isinstance(content, str):
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

        manifest = {
            "campaign_id": campaign_id,
            "version_id": version_id,
            "parent_version": parent_version,
            "created_at": _get_utc_now(),
            "trigger_action": trigger_action,
            "artifacts_saved": list(artifacts.keys())
        }
        with open(os.path.join(version_dir, "campaign_manifest.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return {
            "campaign_id": campaign_id,
            "version_id": version_id,
            "version_dir": version_dir,
            "manifest": manifest
        }

    def list_versions(self, campaign_id: str) -> List[str]:
        campaign_dir = os.path.join(self.base_storage_dir, campaign_id)
        if not os.path.exists(campaign_dir):
            return []
        return sorted([d for d in os.listdir(campaign_dir) if os.path.isdir(os.path.join(campaign_dir, d))])

    def get_version(self, campaign_id: str, version_id: str) -> Optional[Dict[str, Any]]:
        v_dir = os.path.join(self.base_storage_dir, campaign_id, version_id)
        manifest_path = os.path.join(v_dir, "campaign_manifest.json")
        if not os.path.exists(manifest_path):
            return None
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)

global_version_manager = CampaignVersionManager()
