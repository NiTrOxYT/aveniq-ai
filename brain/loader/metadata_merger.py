"""
Metadata Merger for AVENIQ Brain Loader.
Unifies frontmatter, .metadata.yaml sidecars, taxonomy.yaml, relationships.yaml, and manifest.yaml.
"""

import os
import re
from typing import Dict, Any, Optional

class MetadataMerger:
    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir
        self.taxonomy = self._load_yaml_file("knowledge/taxonomy.yaml")
        self.relationships = self._load_yaml_file("knowledge/relationships.yaml")
        self.manifest = self._load_yaml_file("knowledge/manifest.yaml")

    def _load_yaml_file(self, rel_path: str) -> Dict[str, Any]:
        full_path = os.path.join(self.root_dir, rel_path)
        if not os.path.exists(full_path):
            return {}
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                import yaml
                res = yaml.safe_load(f)
                if isinstance(res, dict):
                    return res
        except Exception:
            pass

        # Fallback simple parser for relationship keys if PyYAML is absent
        with open(full_path, "r", encoding="utf-8") as f:
            raw = f.read()

        result: Dict[str, Any] = {}
        if "service_relationships:" in raw:
            result["service_relationships"] = {}
            current_service = None
            for line in raw.splitlines():
                if line.startswith("  ") and line.endswith(":") and not line.startswith("    "):
                    current_service = line.strip().rstrip(":")
                    result["service_relationships"][current_service] = {"related": []}
                elif "primary_dependencies:" in line or "downstream_enhancements:" in line:
                    pass
                elif line.strip().startswith("- ") and current_service:
                    target = line.strip().lstrip("- ").strip()
                    result["service_relationships"][current_service]["related"].append(target)
        return result

    def merge(self, file_path: str, frontmatter: Dict[str, Any]) -> Dict[str, Any]:
        merged: Dict[str, Any] = {}

        # 1. Start with frontmatter
        merged.update(frontmatter)

        # 2. Look for matching .metadata.yaml sidecar
        base_no_ext = os.path.splitext(file_path)[0]
        meta_sidecar_path = f"{base_no_ext}.metadata.yaml"
        if os.path.exists(os.path.join(self.root_dir, meta_sidecar_path)):
            sidecar_data = self._load_yaml_file(meta_sidecar_path)
            for k, v in sidecar_data.items():
                if k not in merged or not merged[k]:
                    merged[k] = v

        # 3. Attach relevant graph relationships if available
        service_id = merged.get("id") or os.path.basename(base_no_ext)
        clean_service_id = service_id.replace("service_", "").replace("_", "-")
        
        service_rels = self.relationships.get("service_relationships", {}).get(clean_service_id)
        if service_rels:
            merged["graph_relationships"] = service_rels

        # 4. Attach system taxonomy context
        merged["taxonomy_ref"] = {
            "version": self.taxonomy.get("version", "1.0.0"),
            "categories": list(self.taxonomy.keys())
        }

        # 5. Attach manifest priority and module metadata
        merged["brain_version"] = self.manifest.get("version", "1.0.0")
        merged["company_name"] = self.manifest.get("company_name", "AVENIQ")

        return merged
