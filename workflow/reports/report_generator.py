"""
Multi-Format Report Exporters for Workflow Engine (JSON, Markdown, HTML).
"""

import json
from typing import Dict, Any
from workflow.models.result import WorkflowResult

class JSONReportExporter:
    @staticmethod
    def export(result: WorkflowResult) -> str:
        data = {
            "success": result.success,
            "metrics": result.metrics,
            "errors": result.errors,
            "packages_count": len(result.packages),
            "timeline": [
                {
                    "timestamp": e.timestamp,
                    "event_type": e.data.get("event_type", "Event"),
                    "department": e.department,
                    "level": e.level,
                    "duration": e.duration
                } for e in result.timeline
            ]
        }
        return json.dumps(data, indent=2)

class MarkdownReportExporter:
    @staticmethod
    def export(result: WorkflowResult) -> str:
        status_str = "SUCCESS ✅" if result.success else "FAILED ❌"
        lines = [
            f"# AVENIQ Workflow Execution Report",
            f"**Status**: {status_str}",
            f"**Total Duration**: {result.metrics.get('total_duration', 0.0)}s",
            f"**Total Steps**: {result.metrics.get('total_steps', 0)}",
            f"**Total Retries**: {result.metrics.get('total_retries', 0)}",
            f"**Packages Produced**: {len(result.packages)}",
            "\n## Department Execution Durations",
        ]
        for dept, dur in result.metrics.get("step_durations", {}).items():
            lines.append(f"- **{dept}**: {dur}s")

        if result.errors:
            lines.append("\n## Failures & Errors")
            for err in result.errors:
                lines.append(f"- ❌ {err}")

        lines.append("\n## Timeline Events")
        for e in result.timeline:
            lines.append(f"- `{e.timestamp}` [{e.department}] {e.data.get('event_type', 'Event')} (Duration: {e.duration}s)")

        return "\n".join(lines)

class HTMLReportExporter:
    @staticmethod
    def export(result: WorkflowResult) -> str:
        status_color = "#10B981" if result.success else "#EF4444"
        status_str = "SUCCESS" if result.success else "FAILED"
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>AVENIQ Workflow Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; background: #0F172A; color: #F8FAFC; }}
        .header {{ padding: 20px; background: #1E293B; border-radius: 8px; border-left: 6px solid {status_color}; }}
        .metric {{ margin: 10px 0; font-size: 16px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ background: #1E293B; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>AVENIQ Workflow Execution: <span style="color:{status_color};">{status_str}</span></h1>
        <div class="metric">Total Duration: <strong>{result.metrics.get('total_duration', 0.0)}s</strong></div>
        <div class="metric">Packages Produced: <strong>{len(result.packages)}</strong></div>
    </div>
    <h2>Department Durations</h2>
    <table>
        <tr><th>Department</th><th>Duration (s)</th><th>Retries</th></tr>
        {"".join([f"<tr><td>{dept}</td><td>{dur}</td><td>{result.metrics.get('retry_counts', {}).get(dept, 0)}</td></tr>" for dept, dur in result.metrics.get("step_durations", {}).items()])}
    </table>
</body>
</html>"""

class WorkflowReportGenerator:
    @staticmethod
    def generate_report(result: WorkflowResult, format_type: str = "json") -> str:
        fmt = format_type.lower()
        if fmt == "markdown" or fmt == "md":
            return MarkdownReportExporter.export(result)
        elif fmt == "html":
            return HTMLReportExporter.export(result)
        else:
            return JSONReportExporter.export(result)
