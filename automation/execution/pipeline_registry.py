"""
Per-department pipeline stage registry.
Each department registers an ordered list of stages.
The scheduler consumes this to drive stage-by-stage execution.
"""

from typing import Dict, List

_STAGE = lambda name, icon: {"name": name, "icon": icon}

_DEFAULT_PIPELINES: Dict[str, List[dict]] = {
    "Creative": [
        _STAGE("Prompt Expansion",   "📝"),
        _STAGE("Image Generation",   "🖼️"),
        _STAGE("Quality Review",     "🔍"),
        _STAGE("Asset Packaging",    "📦"),
    ],
    "Research": [
        _STAGE("Signal Collection",  "📡"),
        _STAGE("Market Analysis",    "📊"),
        _STAGE("Trend Extraction",   "🔬"),
        _STAGE("Report Generation",  "📋"),
    ],
    "Content": [
        _STAGE("Hook Generation",    "✍️"),
        _STAGE("Body Copy",          "📄"),
        _STAGE("CTA Attachment",     "🎯"),
        _STAGE("Editorial Review",   "✅"),
    ],
    "Editorial": [
        _STAGE("Brand Check",        "🏷️"),
        _STAGE("Compliance Audit",   "⚖️"),
        _STAGE("Version Stamp",      "🔖"),
    ],
    "Delivery": [
        _STAGE("Payload Validation", "🔒"),
        _STAGE("Telegram Dispatch",  "📤"),
        _STAGE("Archive",            "🗄️"),
        _STAGE("Version Bump",       "🔢"),
    ],
    "Analytics": [
        _STAGE("Provider Health Check", "🩺"),
        _STAGE("Metric Aggregation",    "📈"),
        _STAGE("Report Persist",        "💾"),
    ],
    "Strategy": [
        _STAGE("Opportunity Scan",   "🔭"),
        _STAGE("Priority Scoring",   "🏆"),
        _STAGE("Brief Generation",   "📝"),
    ],
    "General": [
        _STAGE("Job Initialization", "⚙️"),
        _STAGE("Execution",          "▶️"),
        _STAGE("Completion",         "✅"),
    ],
}


class PipelineRegistry:
    """Registry mapping department names to ordered pipeline stage lists."""

    def __init__(self):
        self._pipelines: Dict[str, List[dict]] = dict(_DEFAULT_PIPELINES)

    def register(self, department: str, stages: List[dict]):
        """Override or add a department's pipeline. Each stage: {name, icon}."""
        self._pipelines[department] = stages

    def get_stages(self, department: str) -> List[dict]:
        """Return ordered stage list for department. Falls back to General."""
        return list(self._pipelines.get(department, self._pipelines["General"]))

    def list_departments(self) -> List[str]:
        return list(self._pipelines.keys())


global_pipeline_registry = PipelineRegistry()
