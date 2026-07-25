"""
REST API Router & Lightweight HTTP Server for AVENIQ Planning Department.
Exposes JSON endpoints for downstream AI departments, n8n workflows, and external systems.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from planning.reports.generator import PlanningReportGenerator

generator = PlanningReportGenerator()

class PlanningAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/planning/report":
            report = generator.generate_planning_report()
            self._send_json(200, report)
        elif path == "/planning/campaign":
            report = generator.generate_planning_report()
            self._send_json(200, report["campaign"])
        elif path == "/planning/calendar":
            report = generator.generate_planning_report()
            self._send_json(200, report["editorial_calendar"])
        elif path == "/planning/schedule":
            report = generator.generate_planning_report()
            self._send_json(200, report["publishing_schedule"])
        elif path == "/planning/assets":
            report = generator.generate_planning_report()
            self._send_json(200, report["required_assets"])
        elif path == "/planning/workflow":
            report = generator.generate_planning_report()
            self._send_json(200, report["workflow_diagram"])
        elif path == "/planning/dependencies":
            report = generator.generate_planning_report()
            self._send_json(200, report["dependency_graph"])
        elif path == "/planning/health":
            self._send_json(200, {
                "status": "healthy",
                "department": "Planning Department (AI Chief Operations Officer)",
                "version": "1.0.0",
                "quality_gate_status": "Active (11 Gates Enforced)"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8082):
    server_address = ("", port)
    httpd = HTTPServer(server_address, PlanningAPIHandler)
    print(f"Planning REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
