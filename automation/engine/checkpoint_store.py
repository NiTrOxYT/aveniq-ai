"""
Per-Execution Checkpoint Persistence Store for AVENIQ AI v2 Native Workflow Engine.
Stores node completion state in automation/storage/checkpoints/<execution_id>/<node_id>.json.
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("CheckpointStore")

class CheckpointStore:
    def __init__(self, base_dir: str = "automation/storage/checkpoints"):
        self.base_dir = base_dir

    def _get_exec_dir(self, execution_id: str) -> str:
        d = os.path.join(self.base_dir, execution_id)
        os.makedirs(d, exist_ok=True)
        return d

    def save_node_checkpoint(self, execution_id: str, node_id: str, data: Dict[str, Any]):
        try:
            d = self._get_exec_dir(execution_id)
            filepath = os.path.join(d, f"{node_id}.json")
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.debug(f"[Checkpoint] Saved node '{node_id}' checkpoint for exec '{execution_id}'")
        except Exception as e:
            logger.warning(f"[Checkpoint] Failed to save node checkpoint: {e}")

    def load_node_checkpoint(self, execution_id: str, node_id: str) -> Optional[Dict[str, Any]]:
        try:
            filepath = os.path.join(self.base_dir, execution_id, f"{node_id}.json")
            if os.path.isfile(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"[Checkpoint] Failed to load checkpoint for '{node_id}': {e}")
        return None

    def load_all_checkpoints(self, execution_id: str) -> Dict[str, Dict[str, Any]]:
        res = {}
        d = os.path.join(self.base_dir, execution_id)
        if not os.path.isdir(d):
            return res
        try:
            for fname in os.listdir(d):
                if fname.endswith(".json"):
                    node_id = fname[:-5]
                    with open(os.path.join(d, fname), "r", encoding="utf-8") as f:
                        res[node_id] = json.load(f)
        except Exception as e:
            logger.warning(f"[Checkpoint] Error loading all checkpoints: {e}")
        return res

global_checkpoint_store = CheckpointStore()
