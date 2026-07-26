"""
REST API Router & Lightweight HTTP Server for AVENIQ Workflow Engine.
Exposes JSON endpoints for execution triggers, status monitoring, timeline logs, and reports.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from workflow.engine.orchestrator import Orchestrator
from workflow.reports.report_generator import WorkflowReportGenerator

orchestrator = Orchestrator()

class WorkflowAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/workflow/status" or path == "/workflow/report":
            res = orchestrator.execute_workflow()
            report = json.loads(WorkflowReportGenerator.generate_report(res, "json"))
            self._send_json(200, report)
        elif path == "/workflow/timeline":
            res = orchestrator.execute_workflow()
            self._send_json(200, {
                "timeline": [
                    {
                        "timestamp": e.timestamp,
                        "department": e.department,
                        "event_type": e.data.get("event_type", "Event")
                    } for e in res.timeline
                ]
            })
        elif path == "/workflow/health":
            self._send_json(200, {
                "status": "healthy",
                "engine": "AVENIQ Workflow Engine (Operating System Orchestrator)",
                "version": "1.0.0",
                "departments_count": 13
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/workflow/run":
            res = orchestrator.execute_workflow()
            self._send_json(200, {
                "success": res.success,
                "metrics": res.metrics,
                "packages_count": len(res.packages)
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8092):
    server_address = ("", port)
    httpd = HTTPServer(server_address, WorkflowAPIHandler)
    print(f"Workflow REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
