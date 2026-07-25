"""
REST API Router & Lightweight HTTP Server for AVENIQ Editorial Department.
Exposes JSON endpoints for downstream AI departments, publishing queues, and external audit tools.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from editorial.reports.generator import EditorialReportGenerator

generator = EditorialReportGenerator()

class EditorialAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/editorial/report" or path == "/editorial/approve":
            report = generator.generate_editorial_report()
            self._send_json(200, report)
        elif path == "/editorial/review":
            report = generator.generate_editorial_report()
            self._send_json(200, {
                "decision": report["approval_decision"],
                "scorecard": report["scorecard"],
                "quality_gate": report["quality_gate"]
            })
        elif path == "/editorial/grammar":
            report = generator.generate_editorial_report()
            self._send_json(200, {
                "grammar_score": report["scorecard"]["grammar"],
                "grammar_issues": [i for i in report["issues"] if i["category"] == "Grammar"]
            })
        elif path == "/editorial/seo":
            report = generator.generate_editorial_report()
            self._send_json(200, {
                "seo_score": report["scorecard"]["seo"],
                "seo_issues": [i for i in report["issues"] if i["category"] == "SEO"]
            })
        elif path == "/editorial/claims":
            report = generator.generate_editorial_report()
            self._send_json(200, {
                "claims": report["claims_verification"],
                "evidence_map": report["evidence_map"]
            })
        elif path == "/editorial/health":
            self._send_json(200, {
                "status": "healthy",
                "department": "Editorial Department (AI Editor-in-Chief)",
                "version": "1.0.0",
                "quality_gate_status": "Active (11 Gates Enforced)"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8085):
    server_address = ("", port)
    httpd = HTTPServer(server_address, EditorialAPIHandler)
    print(f"Editorial REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
