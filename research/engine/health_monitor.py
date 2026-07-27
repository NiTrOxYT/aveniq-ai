"""
Source Health Monitor for AVENIQ Research Engine.
Tracks and persists provider status, auth states, rate limits, configuration checklist, and latency in research/storage/source_status.json.
Single source of truth for dashboard and drawer telemetry.
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
STATUS_FILE = WORKSPACE_ROOT / "research" / "storage" / "source_status.json"


class SourceHealthMonitor:
    def __init__(self, status_file: Optional[Path] = None):
        self.status_file = status_file or STATUS_FILE
        self.status_file.parent.mkdir(parents=True, exist_ok=True)

    def load_status(self) -> Dict[str, Any]:
        if not self.status_file.exists():
            return {"updated_at": None, "sources": {}}
        try:
            with open(self.status_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"updated_at": None, "sources": {}}

    def update_source_status(
        self,
        provider: str,
        status: str,
        configured: bool,
        authenticated: bool,
        latency_ms: float = 0.0,
        remaining_quota: Optional[Any] = None,
        last_error: Optional[str] = None,
        grant_type: Optional[str] = None,
        config: Optional[Dict[str, bool]] = None,
        diagnostics: Optional[Dict[str, Any]] = None,
        sample_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        data = self.load_status()
        sources = data.setdefault("sources", {})

        entry = {
            "provider": provider,
            "status": status,
            "configured": configured,
            "authenticated": authenticated,
            "grant_type": grant_type or (diagnostics.get("grant_type") if diagnostics else None),
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "latency_ms": round(latency_ms, 2),
            "remaining_quota": remaining_quota,
            "rate_limit": remaining_quota,
            "last_error": last_error,
            "config": config or (diagnostics.get("config") if diagnostics else {}),
            "diagnostics": diagnostics or {},
            "sample_data": sample_data or []
        }
        
        sources[provider] = entry
        data["updated_at"] = datetime.now(timezone.utc).isoformat()

        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return entry

    def get_provider_status(self, provider: str) -> Dict[str, Any]:
        data = self.load_status()
        sources = data.get("sources", {})
        if provider in sources:
            return sources[provider]
        return {
            "provider": provider,
            "status": "NOT CONFIG",
            "configured": False,
            "authenticated": False,
            "last_sync": None,
            "latency_ms": 0.0,
            "last_error": "Provider not tested yet",
            "config": {},
            "diagnostics": {}
        }

    def get_sources_summary(self) -> Dict[str, Any]:
        data = self.load_status()
        sources = data.get("sources", {})
        
        configured_count = sum(1 for s in sources.values() if s.get("configured"))
        connected_count = sum(1 for s in sources.values() if s.get("status") in ("Connected", "Healthy", "CONNECTED"))
        failed_count = sum(1 for s in sources.values() if s.get("status") in ("Authentication Failed", "Offline", "Error", "Failed", "FORBIDDEN", "UNAUTHORIZED"))
        
        latencies = [s.get("latency_ms", 0) for s in sources.values() if s.get("latency_ms", 0) > 0]
        avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else 0.0

        return {
            "total_configured": configured_count,
            "total_connected": connected_count,
            "total_failed": failed_count,
            "avg_latency_ms": avg_latency,
            "last_sync": data.get("updated_at"),
            "sources": sources
        }


global_health_monitor = SourceHealthMonitor()
