"""
Validation Engine for AVENIQ Brain Loader.
Checks schema integrity, missing files, duplicate IDs, and broken references.
"""

import os
from typing import List, Dict, Any
from brain.utils.logger import get_logger
from brain.loader.discovery import DiscoveryEngine

logger = get_logger("aveniq.brain.validator")

class ValidationError:
    def __init__(self, code: str, message: str, file_path: str = "", severity: str = "ERROR"):
        self.code = code
        self.message = message
        self.file_path = file_path
        self.severity = severity

    def to_dict(self) -> Dict[str, str]:
        return {
            "code": self.code,
            "severity": self.severity,
            "file_path": self.file_path,
            "message": self.message
        }

    def __str__(self) -> str:
        return f"[{self.severity}] [{self.code}] {self.file_path}: {self.message}"

class ValidationEngine:
    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir
        self.discovery = DiscoveryEngine(root_dir=root_dir)

    def validate_all(self) -> List[ValidationError]:
        errors: List[ValidationError] = []
        logger.info("Starting Company Brain validation sweep...")

        # 1. Manifest file existence
        manifest_path = os.path.join(self.root_dir, "knowledge/manifest.yaml")
        if not os.path.exists(manifest_path):
            errors.append(ValidationError("ERR_MISSING_MANIFEST", "Master manifest.yaml is missing", manifest_path))
            return errors

        # 2. Discover modules
        try:
            modules = self.discovery.discover_modules()
        except Exception as e:
            errors.append(ValidationError("ERR_MANIFEST_CORRUPT", f"Failed to parse manifest: {e}", manifest_path))
            return errors

        # 3. Check for Duplicate Module IDs and missing paths
        seen_ids = set()
        for mod in modules:
            mod_id = mod["id"]
            if mod_id in seen_ids:
                errors.append(ValidationError("ERR_DUPLICATE_MODULE_ID", f"Duplicate module ID found: {mod_id}", manifest_path))
            seen_ids.add(mod_id)

            declared_path = os.path.join(self.root_dir, mod["declared_path"])
            if not os.path.exists(declared_path):
                errors.append(ValidationError("ERR_MISSING_PATH", f"Declared path does not exist: {mod['declared_path']}", manifest_path))
            else:
                if len(mod["files"]) == 0 and os.path.isdir(declared_path):
                    errors.append(ValidationError("WARN_EMPTY_DIRECTORY", f"Directory path is empty: {mod['declared_path']}", manifest_path, severity="WARNING"))

        # 4. Service Index & Metadata Verification
        services_index_path = os.path.join(self.root_dir, "knowledge/services/index.yaml")
        if os.path.exists(services_index_path):
            with open(services_index_path, "r", encoding="utf-8") as f:
                idx_raw = f.read()

            services = [
                "web-development", "saas-development", "custom-software-development",
                "ai-automation", "ai-agents", "mobile-app-development",
                "ui-ux-design", "api-integration", "cloud-deployment", "maintenance-support"
            ]

            for s in services:
                md_path = os.path.join(self.root_dir, f"knowledge/services/{s}.md")
                meta_path = os.path.join(self.root_dir, f"knowledge/services/{s}.metadata.yaml")

                if not os.path.exists(md_path):
                    errors.append(ValidationError("ERR_MISSING_SERVICE_MD", f"Service Markdown missing: {md_path}", md_path))
                if not os.path.exists(meta_path):
                    errors.append(ValidationError("ERR_MISSING_SERVICE_META", f"Service Metadata missing: {meta_path}", meta_path))
                if f"service_{s.replace('-', '_')}" not in idx_raw:
                    errors.append(ValidationError("ERR_INDEX_MISSING_REF", f"services/index.yaml missing reference to service_{s.replace('-', '_')}", services_index_path))

        logger.info(f"Validation sweep complete. Found {len(errors)} issues.")
        return errors
