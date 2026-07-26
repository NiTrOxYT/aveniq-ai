"""
Enhanced PackageRegistry for AVENIQ Workflow Engine.
Single source of truth for storing and retrieving output packages across departments.
"""

from typing import Dict, Any, List, Optional

class PackageRegistry:
    def __init__(self):
        self._packages: Dict[str, Dict[str, Any]] = {}
        self._history: Dict[str, List[Dict[str, Any]]] = {}

    def register(self, package_name: str, package_data: Dict[str, Any], package_type: str = "generic") -> None:
        entry = {
            "name": package_name,
            "type": package_type,
            "data": package_data
        }
        self._packages[package_name] = entry
        if package_name not in self._history:
            self._history[package_name] = []
        self._history[package_name].append(entry)

    def get(self, package_name: str) -> Optional[Dict[str, Any]]:
        pkg = self._packages.get(package_name)
        return pkg["data"] if pkg else None

    def get_latest(self, package_name: str) -> Optional[Dict[str, Any]]:
        hist = self._history.get(package_name, [])
        return hist[-1]["data"] if hist else None

    def get_all(self) -> Dict[str, Dict[str, Any]]:
        return {k: v["data"] for k, v in self._packages.items()}

    def get_by_type(self, package_type: str) -> List[Dict[str, Any]]:
        return [v["data"] for v in self._packages.values() if v.get("type") == package_type]

    def exists(self, package_name: str) -> bool:
        return package_name in self._packages

    def history(self, package_name: str) -> List[Dict[str, Any]]:
        return [h["data"] for h in self._history.get(package_name, [])]

    def remove(self, package_name: str) -> bool:
        if package_name in self._packages:
            del self._packages[package_name]
            return True
        return False
