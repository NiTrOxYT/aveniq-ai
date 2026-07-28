"""
Knowledge Repository Abstraction Layer for AVENIQ Company Brain.
Sole point of access for persistent JSON storage files. Zero direct file manipulation outside this layer.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = WORKSPACE_ROOT / "knowledge"
STORAGE_DIR = KNOWLEDGE_DIR / "storage"

MEMORIES_FILE = STORAGE_DIR / "memories.json"
ENTITIES_FILE = STORAGE_DIR / "entities.json"
ACTIVITY_FILE = STORAGE_DIR / "activity.json"
INDEX_FILE = STORAGE_DIR / "index.json"
REFLECTIONS_FILE = STORAGE_DIR / "reflections.json"
REVISIONS_DIR = STORAGE_DIR / "revisions"


class KnowledgeRepository:
    def __init__(self, storage_dir: Path = STORAGE_DIR):
        self.storage_dir = storage_dir
        self.revisions_dir = REVISIONS_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.revisions_dir.mkdir(parents=True, exist_ok=True)

    def _read_json(self, path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default

    def _write_json(self, path: Path, data: Any):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # --- Memories ---
    def get_all_memories(self) -> List[Dict[str, Any]]:
        return self._read_json(MEMORIES_FILE, [])

    def save_memories(self, memories: List[Dict[str, Any]]):
        self._write_json(MEMORIES_FILE, memories)

    def save_memory_item(self, item: Dict[str, Any]):
        memories = self.get_all_memories()
        idx = next((i for i, m in enumerate(memories) if m.get("id") == item.get("id")), None)
        if idx is not None:
            memories[idx] = item
        else:
            memories.append(item)
        self.save_memories(memories)

    # --- Index ---
    def get_index(self) -> Dict[str, Any]:
        return self._read_json(INDEX_FILE, {"updated_at": None, "count": 0, "items": []})

    def save_index(self, index_data: Dict[str, Any]):
        self._write_json(INDEX_FILE, index_data)

    # --- Entities & Relationships ---
    def get_entities_and_relationships(self) -> Dict[str, Any]:
        return self._read_json(ENTITIES_FILE, {"entities": [], "relationships": []})

    def save_entities_and_relationships(self, data: Dict[str, Any]):
        self._write_json(ENTITIES_FILE, data)

    # --- Reflections ---
    def get_reflections(self) -> List[Dict[str, Any]]:
        return self._read_json(REFLECTIONS_FILE, [])

    def save_reflection(self, reflection: Dict[str, Any]):
        reflections = self.get_reflections()
        reflections.insert(0, reflection)
        self._write_json(REFLECTIONS_FILE, reflections[:100])

    # --- Activity ---
    def get_activity(self) -> List[Dict[str, Any]]:
        return self._read_json(ACTIVITY_FILE, [])

    def log_activity(self, message: str):
        activity = self.get_activity()
        activity.insert(0, {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": message
        })
        self._write_json(ACTIVITY_FILE, activity[:100])

    # --- Revisions ---
    def save_revision(self, item_id: str, revision_no: int, payload: Dict[str, Any]):
        rev_file = self.revisions_dir / f"{item_id}_rev_{revision_no}.json"
        self._write_json(rev_file, payload)


global_knowledge_repository = KnowledgeRepository()
