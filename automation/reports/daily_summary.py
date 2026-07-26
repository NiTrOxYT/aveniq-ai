"""
Daily Summary Report Generator for Autonomous Execution & Human Approval Platform.
Exports daily summary reports in JSON and Markdown formats.
"""

import json
from typing import Dict, Any

class DailySummaryReportGenerator:
    @staticmethod
    def generate_report(run_result: Dict[str, Any], format_type: str = "json") -> str:
        data = {
            "report_type": "automation_daily_summary",
            "session_id": run_result.get("session_id"),
            "success": run_result.get("success"),
            "state": run_result.get("state"),
            "duration": f"{run_result.get('duration', 0.0)}s",
            "packages_count": run_result.get("packages_count", 0),
            "briefing": run_result.get("briefing", "")
        }

        if format_type.lower() in ["markdown", "md"]:
            lines = [
                f"# AVENIQ Autonomous Daily Summary Report",
                f"**Session ID**: `{data['session_id']}`",
                f"**Status State**: `{data['state']}`",
                f"**Execution Duration**: {data['duration']}",
                f"**Packages Produced**: {data['packages_count']}",
                "\n## Briefing Preview",
                data['briefing']
            ]
            return "\n".join(lines)

        return json.dumps(data, indent=2)
