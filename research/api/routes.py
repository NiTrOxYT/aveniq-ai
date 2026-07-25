"""
REST API Router & Lightweight HTTP Server for AVENIQ Research Department.
Exposes JSON endpoints for downstream AI departments, n8n workflows, and external systems.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from research.reports.generator import ResearchReportGenerator

generator = ResearchReportGenerator()

class ResearchAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/research/package":
            report = generator.generate_package_report()
            self._send_json(200, report)
        elif path == "/research/topic":
            report = generator.generate_package_report()
            self._send_json(200, {
                "topic": report["topic"],
                "executive_summary": report["executive_summary"],
                "confidence_score": report["confidence_score"]
            })
        elif path == "/research/statistics":
            report = generator.generate_package_report()
            self._send_json(200, {"verified_statistics": report["verified_statistics"]})
        elif path == "/research/competitors":
            report = generator.generate_package_report()
            self._send_json(200, {"competitor_insights": report["competitor_insights"]})
        elif path == "/research/seo":
            report = generator.generate_package_report()
            self._send_json(200, {"seo_insights": report["seo_insights"]})
        elif path == "/research/sources":
            report = generator.generate_package_report()
            self._send_json(200, {"citations": report["citations"]})
        elif path == "/research/health":
            self._send_json(200, {
                "status": "healthy",
                "department": "Research Department (Senior Research Analyst)",
                "version": "1.0.0",
                "quality_gate_status": "Active (8 Gates Enforced)"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8081):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ResearchAPIHandler)
    print(f"Research REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
