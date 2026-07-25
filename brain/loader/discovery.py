"""
Discovery Engine for AVENIQ Brain Loader.
Reads knowledge/manifest.yaml and dynamically discovers all registered knowledge modules.
"""

import os
import re
from typing import List, Dict, Any
from brain.utils.logger import get_logger

logger = get_logger("aveniq.brain.discovery")

class DiscoveryEngine:
    def __init__(self, manifest_path: str = "knowledge/manifest.yaml", root_dir: str = "."):
        self.manifest_path = os.path.join(root_dir, manifest_path)
        self.root_dir = root_dir

    def load_manifest_content(self) -> str:
        if not os.path.exists(self.manifest_path):
            logger.error(f"Manifest file not found: {self.manifest_path}")
            raise FileNotFoundError(f"Manifest missing at {self.manifest_path}")
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            return f.read()

    def discover_modules(self) -> List[Dict[str, Any]]:
        manifest_raw = self.load_manifest_content()
        modules: List[Dict[str, Any]] = []

        # Parse YAML modules block cleanly using regex patterns for dependency-free parsing
        # (or standard PyYAML if available)
        try:
            import yaml
            parsed = yaml.safe_load(manifest_raw)
            if isinstance(parsed, dict) and "modules" in parsed:
                raw_modules = parsed["modules"]
            else:
                raw_modules = []
        except Exception:
            # Fallback regex parser for basic YAML structure
            raw_modules = self._parse_manifest_regex(manifest_raw)

        for mod in raw_modules:
            mod_path = mod.get("path")
            if not mod_path:
                continue

            full_path = os.path.join(self.root_dir, mod_path)
            mod_type = mod.get("type", "document")
            priority = mod.get("priority", 3)
            embedding_enabled = mod.get("embedding_enabled", True)
            module_id = mod.get("id", os.path.basename(mod_path).replace(".", "_"))

            discovered_files = []
            if os.path.isdir(full_path):
                # Search directory for files
                for root, _, files in os.walk(full_path):
                    for file in files:
                        if file.endswith((".md", ".yaml", ".yml", ".json")):
                            file_full_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_full_path, self.root_dir)
                            discovered_files.append({
                                "file_path": rel_path,
                                "file_name": file,
                                "extension": os.path.splitext(file)[1].lstrip(".")
                            })
            elif os.path.isfile(full_path):
                discovered_files.append({
                    "file_path": mod_path,
                    "file_name": os.path.basename(mod_path),
                    "extension": os.path.splitext(mod_path)[1].lstrip(".")
                })

            modules.append({
                "id": module_id,
                "name": mod.get("name", module_id),
                "declared_path": mod_path,
                "type": mod_type,
                "priority": priority,
                "embedding_enabled": embedding_enabled,
                "description": mod.get("description", ""),
                "files": discovered_files
            })

        logger.info(f"Discovered {len(modules)} modules containing total file targets.")
        return modules

    def _parse_manifest_regex(self, content: str) -> List[Dict[str, Any]]:
        modules = []
        blocks = content.split("- id:")
        for block in blocks[1:]:
            lines = block.strip().split("\n")
            mod_dict = {}
            for line in lines:
                if ":" in line:
                    parts = line.split(":", 1)
                    k = parts[0].strip()
                    v = parts[1].strip().strip('"').strip("'")
                    if v == "true":
                        v = True
                    elif v == "false":
                        v = False
                    elif v.isdigit():
                        v = int(v)
                    mod_dict[k] = v
            if "path" in mod_dict:
                mod_dict["id"] = lines[0].strip()
                modules.append(mod_dict)
        return modules
