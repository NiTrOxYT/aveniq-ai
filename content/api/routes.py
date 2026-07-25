"""
REST API Router & Lightweight HTTP Server for AVENIQ Content Department.
Exposes JSON endpoints for downstream AI departments, n8n workflows, and external publishing platforms.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from content.reports.generator import ContentReportGenerator

generator = ContentReportGenerator()

class ContentAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/content/package":
            report = generator.generate_content_report()
            self._send_json(200, report)
        elif path == "/content/article":
            report = generator.generate_content_report()
            self._send_json(200, report["master_article"])
        elif path == "/content/linkedin":
            report = generator.generate_content_report()
            self._send_json(200, {
                "linkedin": report["social_posts"]["linkedin"],
                "carousel": report["carousel_copy"]
            })
        elif path == "/content/newsletter":
            report = generator.generate_content_report()
            self._send_json(200, report["newsletter"])
        elif path == "/content/seo":
            report = generator.generate_content_report()
            self._send_json(200, {
                "slug": report["master_article"]["slug"],
                "meta_title": report["master_article"]["meta_title"],
                "meta_description": report["master_article"]["meta_description"],
                "internal_links": report["master_article"]["internal_links"]
            })
        elif path == "/content/review":
            report = generator.generate_content_report()
            self._send_json(200, {
                "scores": report["content_scores"],
                "workflow_state": report["workflow_state"],
                "quality_gate": report["quality_gate"]
            })
        elif path == "/content/health":
            self._send_json(200, {
                "status": "healthy",
                "department": "Content Department (AI Content Director)",
                "version": "1.0.0",
                "quality_gate_status": "Active (11 Gates Enforced)"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8083):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ContentAPIHandler)
    print(f"Content REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
