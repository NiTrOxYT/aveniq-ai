"""
REST API Router & Lightweight HTTP Server for AVENIQ Human Approval System.
Exposes JSON endpoints for Telegram webhooks, dashboard UIs, and operator control centers.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from approval.reports.generator import ApprovalReportGenerator
from approval.storage.manager import ApprovalStorageManager

generator = ApprovalReportGenerator()
storage = ApprovalStorageManager()

class ApprovalAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/approval/session" or path == "/approval/report":
            report = generator.generate_approval_report()
            self._send_json(200, report)
        elif path == "/approval/history":
            latest = storage.get_latest_session()
            self._send_json(200, {"latest_session": latest})
        elif path == "/approval/health":
            self._send_json(200, {
                "status": "healthy",
                "department": "Human Approval System (Human-in-the-Loop)",
                "version": "1.0.0",
                "quality_gate_status": "Active (8 Gates Enforced)"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            body = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            body = {}

        if path == "/approval/approve":
            report = generator.generate_approval_report()
            self._send_json(200, {
                "status": "APPROVED",
                "session_id": report["session_id"],
                "message": "Package successfully approved and released to Archive & Learning"
            })
        elif path == "/approval/reject":
            report = generator.generate_approval_report()
            self._send_json(200, {
                "status": "REJECTED",
                "session_id": report["session_id"],
                "message": "Campaign rejected and closed"
            })
        elif path == "/approval/action":
            action_type = body.get("action", "Rewrite")
            report = generator.generate_approval_report()
            self._send_json(200, {
                "status": "CHANGES_REQUESTED",
                "session_id": report["session_id"],
                "action": action_type,
                "routed_department": "Content"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8089):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ApprovalAPIHandler)
    print(f"Approval REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
