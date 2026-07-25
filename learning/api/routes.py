"""
REST API Router & Lightweight HTTP Server for AVENIQ Learning Department.
Exposes JSON endpoints for downstream optimization tools, dashboard visualizers, and Company Brain curators.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from learning.reports.generator import LearningReportGenerator

generator = LearningReportGenerator()

class LearningAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/learning/package" or path == "/learning/report":
            report = generator.generate_learning_report()
            self._send_json(200, report)
        elif path == "/learning/recommendations":
            report = generator.generate_learning_report()
            self._send_json(200, {
                "recommendations": report["recommendations"],
                "knowledge_proposals": report["knowledge_proposals"]
            })
        elif path == "/learning/trends":
            report = generator.generate_learning_report()
            self._send_json(200, {
                "topics": report["topic_summary"],
                "brand_evolution": report["brand_evolution"],
                "learning_metrics": report["learning_metrics"]
            })
        elif path == "/learning/duplicates":
            report = generator.generate_learning_report()
            self._send_json(200, report["duplicate_report"])
        elif path == "/learning/health":
            self._send_json(200, {
                "status": "healthy",
                "department": "Learning Department (AI Learning Manager)",
                "version": "1.0.0",
                "quality_gate_status": "Active (11 Gates Enforced)"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8088):
    server_address = ("", port)
    httpd = HTTPServer(server_address, LearningAPIHandler)
    print(f"Learning REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
