"""
Workflow History Persistence Store for AVENIQ AI v2 Native Workflow Engine.
Stores completed workflow executions in automation/storage/history/<execution_id>.json.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("WorkflowHistoryStore")

class WorkflowHistoryStore:
    def __init__(self, base_dir: str = "automation/storage/history"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_history(self, execution_id: str, record: Dict[str, Any]):
        try:
            filepath = os.path.join(self.base_dir, f"{execution_id}.json")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(record, f, indent=2)
            logger.debug(f"[WorkflowHistory] Saved record for '{execution_id}'")
        except Exception as e:
            logger.warning(f"[WorkflowHistory] Save failed for '{execution_id}': {e}")

    def get_history(self, execution_id: str) -> Optional[Dict[str, Any]]:
        try:
            filepath = os.path.join(self.base_dir, f"{execution_id}.json")
            if os.path.isfile(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    def list_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        records = []
        try:
            for fname in os.listdir(self.base_dir):
                if fname.endswith(".json"):
                    with open(os.path.join(self.base_dir, fname), "r", encoding="utf-8") as f:
                        records.append(json.load(f))
        except Exception as e:
            logger.warning(f"[WorkflowHistory] Error listing history: {e}")
        records.sort(key=lambda r: r.get("started_at") or "", reverse=True)
        return records[:limit]

global_workflow_history_store = WorkflowHistoryStore()
