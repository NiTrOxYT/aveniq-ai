"""
Dead Letter Queue (DLQ) Manager for AVENIQ AI Runtime v1.
Captures failed background tasks with exception tracebacks and supports dashboard inspection, retry, and purge.
"""

import time
import traceback
from typing import Dict, Any, List, Optional, Callable


class DeadLetterQueue:
    def __init__(self):
        self._dead_jobs: List[Dict[str, Any]] = []

    def record_failure(self, task_name: str, args: tuple, kwargs: dict, exception: Exception, retry_fn: Optional[Callable] = None):
        """Record a failed task in the Dead Letter Queue."""
        job_id = f"dlq_{int(time.time()*1000)}"
        job = {
            "job_id": job_id,
            "task_name": task_name,
            "failed_at": time.time(),
            "exception": str(exception),
            "traceback": traceback.format_exc(),
            "retry_count": 0,
            "status": "failed",
            "_retry_fn": retry_fn
        }
        self._dead_jobs.insert(0, job)
        self._dead_jobs = self._dead_jobs[:100]

    def list_dead_jobs(self) -> List[Dict[str, Any]]:
        """Return clean list of dead letter jobs (excluding non-serializable callables)."""
        clean_jobs = []
        for j in self._dead_jobs:
            c = dict(j)
            c.pop("_retry_fn", None)
            clean_jobs.append(c)
        return clean_jobs

    def retry_job(self, job_id: str) -> bool:
        """Attempt to re-execute a dead job."""
        job = next((j for j in self._dead_jobs if j.get("job_id") == job_id), None)
        if not job:
            return False
        
        retry_fn = job.get("_retry_fn")
        if not retry_fn:
            job["status"] = "retry_failed_no_fn"
            return False
        
        try:
            retry_fn()
            job["status"] = "retried_successfully"
            job["retry_count"] += 1
            return True
        except Exception as e:
            job["status"] = f"retry_failed: {str(e)}"
            job["retry_count"] += 1
            return False

    def purge(self):
        self._dead_jobs.clear()


global_dead_letter_queue = DeadLetterQueue()
