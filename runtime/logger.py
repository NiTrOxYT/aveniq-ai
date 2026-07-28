"""
Structured JSON Logger for AVENIQ AI Runtime v1.
Outputs correlation-traced log records with timestamp, module, event, request_id, job_id, level, duration_ms.
"""

import json
import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional


class StructuredLogger:
    def __init__(self, module_name: str = "runtime"):
        self.module_name = module_name
        self._logger = logging.getLogger(f"aveniq.{module_name}")

    def log(
        self,
        level: str,
        event: str,
        message: str = "",
        request_id: Optional[str] = None,
        job_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        duration_ms: Optional[float] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "module": self.module_name,
            "level": level.upper(),
            "event": event,
            "message": message,
            "request_id": request_id,
            "job_id": job_id,
            "correlation_id": correlation_id,
            "duration_ms": round(duration_ms, 2) if duration_ms is not None else None,
            "extra": extra or {}
        }
        
        # Clean null values
        clean_record = {k: v for k, v in record.items() if v is not None}
        log_str = json.dumps(clean_record)
        
        lvl = level.upper()
        if lvl == "DEBUG":
            self._logger.debug(log_str)
        elif lvl == "WARNING":
            self._logger.warning(log_str)
        elif lvl == "ERROR":
            self._logger.error(log_str)
        else:
            self._logger.info(log_str)

    def info(self, event: str, message: str = "", **kwargs):
        self.log("INFO", event, message, **kwargs)

    def error(self, event: str, message: str = "", **kwargs):
        self.log("ERROR", event, message, **kwargs)

    def warning(self, event: str, message: str = "", **kwargs):
        self.log("WARNING", event, message, **kwargs)


def get_structured_logger(module_name: str) -> StructuredLogger:
    return StructuredLogger(module_name)
