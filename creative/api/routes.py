"""
REST API Router & Lightweight HTTP Server for AVENIQ Creative Department.
Exposes JSON endpoints for downstream AI departments, image generation queues, and external media platforms.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from creative.reports.generator import CreativeReportGenerator

generator = CreativeReportGenerator()

class CreativeAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/creative/package":
            report = generator.generate_media_report()
            self._send_json(200, report)
        elif path == "/creative/hero":
            report = generator.generate_media_report()
            self._send_json(200, report["hero_brief"])
        elif path == "/creative/carousel":
            report = generator.generate_media_report()
            self._send_json(200, report["carousel_design"])
        elif path == "/creative/video":
            report = generator.generate_media_report()
            self._send_json(200, report["video_storyboard"])
        elif path == "/creative/thumbnail":
            report = generator.generate_media_report()
            self._send_json(200, report["thumbnail_spec"])
        elif path == "/creative/review":
            report = generator.generate_media_report()
            self._send_json(200, {
                "scores": report["creative_scores"],
                "quality_gate": report["quality_gate"],
                "accessibility": report["captions_and_accessibility"]
            })
        elif path == "/creative/health":
            self._send_json(200, {
                "status": "healthy",
                "department": "Creative Department (AI Creative Director)",
                "version": "1.0.0",
                "quality_gate_status": "Active (11 Gates Enforced)"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8084):
    server_address = ("", port)
    httpd = HTTPServer(server_address, CreativeAPIHandler)
    print(f"Creative REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
