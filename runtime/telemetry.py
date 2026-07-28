"""
Observability & Telemetry Collector for AVENIQ AI Runtime v1.
Tracks process resource utilization, request latencies, throughput counters, and error rates.
Calculates mathematically derived metrics only.
"""

import time
import os
from typing import Dict, Any, List


class TelemetryCollector:
    def __init__(self):
        self._start_time = time.time()
        self._latencies: List[float] = []
        self._requests_count = 0
        self._errors_count = 0
        self._events_published_count = 0

    def record_request(self, duration_ms: float, is_error: bool = False):
        self._requests_count += 1
        if is_error:
            self._errors_count += 1
        self._latencies.append(duration_ms)
        if len(self._latencies) > 1000:
            self._latencies = self._latencies[-1000:]

    def record_event_published(self):
        self._events_published_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        uptime_seconds = int(time.time() - self._start_time)
        avg_latency = round(sum(self._latencies) / len(self._latencies), 2) if self._latencies else 0.0

        # Memory usage via psutil/resource if available, fallback to basic calculation
        mem_mb = 0.0
        try:
            import resource
            mem_mb = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024), 2)
        except Exception:
            pass

        return {
            "uptime_seconds": uptime_seconds,
            "total_requests": self._requests_count,
            "total_errors": self._errors_count,
            "error_rate": round(self._errors_count / max(self._requests_count, 1), 4),
            "events_published": self._events_published_count,
            "avg_latency_ms": avg_latency,
            "memory_usage_mb": mem_mb,
            "process_id": os.getpid()
        }


global_telemetry_collector = TelemetryCollector()
