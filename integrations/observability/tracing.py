"""
Observability Tracing, Audit Logging, and System Diagnostics.
Generates traces for every provider request (request_id, provider, operation, latency, retries, status).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class IntegrationTrace:
    request_id: str
    provider: str
    operation: str
    latency: float
    retries: int = 0
    cache_used: bool = False
    status: str = "SUCCESS"
    error_classification: Optional[str] = None
    timestamp: str = field(default_factory=_get_utc_now)

class ObservabilityTracer:
    def __init__(self):
        self.traces: List[IntegrationTrace] = []

    def record_trace(self, trace: IntegrationTrace) -> None:
        self.traces.append(trace)

    def get_traces_for_provider(self, provider_name: str) -> List[IntegrationTrace]:
        return [t for t in self.traces if t.provider == provider_name]

class AuditLogger:
    @staticmethod
    def log(request_id: str, provider: str, operation: str, status: str):
        print(f"[{_get_utc_now()}] [AUDIT] [{provider}] Request '{request_id}' ({operation}) -> {status}")

class SystemDiagnostics:
    @staticmethod
    def inspect(tracer: ObservabilityTracer) -> Dict[str, Any]:
        total_requests = len(tracer.traces)
        successful = sum(1 for t in tracer.traces if t.status == "SUCCESS")
        cache_hits = sum(1 for t in tracer.traces if t.cache_used)
        retries = sum(t.retries for t in tracer.traces)
        
        return {
            "total_requests": total_requests,
            "success_rate": f"{round((successful / total_requests) * 100.0, 1)}%" if total_requests else "100.0%",
            "cache_hits": cache_hits,
            "total_retries": retries
        }

global_tracer = ObservabilityTracer()
