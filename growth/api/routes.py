"""
REST API Router & Lightweight HTTP Server for AVENIQ Brand Growth Intelligence.
Exposes JSON endpoints for strategic planners, executive dashboards, and marketing operations tools.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from growth.reports.generator import GrowthReportGenerator

generator = GrowthReportGenerator()

class GrowthAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/growth/package" or path == "/growth/report":
            report = generator.generate_growth_report()
            self._send_json(200, report)
        elif path == "/growth/goals":
            report = generator.generate_growth_report()
            self._send_json(200, {
                "goals": report["goals"],
                "objective_tree": report["objective_tree"]
            })
        elif path == "/growth/portfolio":
            report = generator.generate_growth_report()
            self._send_json(200, {
                "portfolio": report["portfolio"],
                "content_mix": report["content_mix"]
            })
        elif path == "/growth/funnel":
            report = generator.generate_growth_report()
            self._send_json(200, {
                "funnel_allocation": report["funnel_allocation"],
                "forecast": report["forecast"],
                "scenarios": report["scenarios"]
            })
        elif path == "/growth/health":
            self._send_json(200, {
                "status": "healthy",
                "department": "Brand Growth Intelligence",
                "version": "1.0.0",
                "quality_gate_status": "Active (8 Gates Enforced)"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8091):
    server_address = ("", port)
    httpd = HTTPServer(server_address, GrowthAPIHandler)
    print(f"Growth REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
