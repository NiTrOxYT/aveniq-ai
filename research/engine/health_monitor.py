"""
Source Health Monitor for AVENIQ Research Engine.
Tracks and persists provider status, auth states, rate limits, and latency in research/storage/source_status.json.
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
        last_error: Optional[str] = None
    ) -> Dict[str, Any]:
        data = self.load_status()
        sources = data.setdefault("sources", {})
        
        sources[provider] = {
            "provider": provider,
            "status": status,
            "configured": configured,
            "authenticated": authenticated,
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "latency_ms": round(latency_ms, 2),
            "remaining_quota": remaining_quota,
            "last_error": last_error
        }
        data["updated_at"] = datetime.now(timezone.utc).isoformat()

        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        return sources[provider]

    def get_sources_summary(self) -> Dict[str, Any]:
        data = self.load_status()
        sources = data.get("sources", {})
        
        configured_count = sum(1 for s in sources.values() if s.get("configured"))
        connected_count = sum(1 for s in sources.values() if s.get("status") in ("Connected", "Healthy"))
        failed_count = sum(1 for s in sources.values() if s.get("status") in ("Authentication Failed", "Offline", "Error", "Failed"))
        
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
