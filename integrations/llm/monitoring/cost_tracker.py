"""
Cost Tracker and Token Usage Collector for Real LLM Router.
Tracks prompt tokens, completion tokens, latency, and estimated cost across workspaces and departments.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class LLMUsageMetric:
    execution_id: str
    department: str
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_sec: float
    estimated_cost_usd: float
    timestamp: str = field(default_factory=_get_utc_now)

class CostTracker:
    # Model pricing per 1K tokens ($)
    PRICING = {
        "gpt-5": {"prompt": 0.005, "completion": 0.015},
        "gpt-image": {"prompt": 0.02, "completion": 0.04},
        "gemini-2.5-pro": {"prompt": 0.00125, "completion": 0.00375},
        "gemini-3.6-flash": {"prompt": 0.00015, "completion": 0.0006},
        "gemini-flash-latest": {"prompt": 0.00015, "completion": 0.0006},
        "gemini-2.0-flash": {"prompt": 0.0001, "completion": 0.0004},
        "gemini-1.5-flash": {"prompt": 0.000075, "completion": 0.0003},
        "claude-3-5-sonnet": {"prompt": 0.003, "completion": 0.015}
    }

    def __init__(self):
        self._metrics: List[LLMUsageMetric] = []

    def record_usage(self, execution_id: str, department: str, provider: str, model: str, prompt_tokens: int, completion_tokens: int, latency_sec: float) -> LLMUsageMetric:
        prices = self.PRICING.get(model, {"prompt": 0.002, "completion": 0.005})
        cost = (prompt_tokens / 1000.0 * prices["prompt"]) + (completion_tokens / 1000.0 * prices["completion"])

        metric = LLMUsageMetric(
            execution_id=execution_id,
            department=department,
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            latency_sec=round(latency_sec, 3),
            estimated_cost_usd=round(cost, 6)
        )
        self._metrics.append(metric)
        return metric

    def get_summary(self) -> Dict[str, Any]:
        total_tokens = sum(m.total_tokens for m in self._metrics)
        total_cost = sum(m.estimated_cost_usd for m in self._metrics)
        return {
            "total_requests": len(self._metrics),
            "total_tokens": total_tokens,
            "total_estimated_cost_usd": round(total_cost, 4),
            "records": len(self._metrics)
        }

    def get_aggregate_metrics(self) -> Dict[str, Any]:
        res = self.get_summary()
        res["total_cost"] = res["total_estimated_cost_usd"]
        return res

global_cost_tracker = CostTracker()
