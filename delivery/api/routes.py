"""
REST API Router & Lightweight HTTP Server for AVENIQ Delivery Department.
Exposes JSON endpoints for downstream automated publishing platforms, social schedulers, and CMS integrations.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from delivery.reports.generator import DeliveryReportGenerator

generator = DeliveryReportGenerator()

class DeliveryAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/delivery/package" or path == "/delivery/report":
            report = generator.generate_delivery_report()
            self._send_json(200, report)
        elif path == "/delivery/attachments":
            report = generator.generate_delivery_report()
            self._send_json(200, {
                "attachments": report["attachments"],
                "checksums": report["manifest"]["checksums"]
            })
        elif path == "/delivery/export":
            report = generator.generate_delivery_report()
            self._send_json(200, report["exports"])
        elif path == "/delivery/validate":
            report = generator.generate_delivery_report()
            self._send_json(200, {
                "quality_gate": report["quality_gate"],
                "status": report["manifest"]["status"],
                "scores": report["scores"]
            })
        elif path == "/delivery/health":
            self._send_json(200, {
                "status": "healthy",
                "department": "Delivery Department (AI Delivery Manager)",
                "version": "1.0.0",
                "quality_gate_status": "Active (11 Gates Enforced)"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8086):
    server_address = ("", port)
    httpd = HTTPServer(server_address, DeliveryAPIHandler)
    print(f"Delivery REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
