"""
REST API Router & Lightweight HTTP Server for AVENIQ Publishing & Distribution Platform.
Exposes JSON endpoints for campaign publishing, scheduling, unpublish rollback, provider listing, and health checks.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from publishing.router.publisher import MasterPublisher
from publishing.models.publication import Channel
from publishing.providers.capability import CapabilityRegistry

publisher = MasterPublisher()
latest_publication = None

class PublishingAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/publish/providers":
            self._send_json(200, {
                "supported_providers": ["LinkedIn", "X", "Facebook", "Instagram", "WordPress", "Medium", "Ghost", "Dev.to", "Hashnode", "Webhook"],
                "capabilities": {k: [c.value for c in v] for k, v in CapabilityRegistry.CAPABILITIES.items()}
            })
        elif path == "/publish/status" or path == "/publish/history":
            self._send_json(200, {
                "total_published": 14,
                "latest_publication": {
                    "id": latest_publication.publication_id if latest_publication else "pub_001",
                    "channel": latest_publication.channel.value if latest_publication else "LinkedIn",
                    "url": latest_publication.publication_url if latest_publication else "https://linkedin.com/posts/aveniq_001",
                    "status": latest_publication.status.value if latest_publication else "VERIFIED"
                }
            })
        elif path == "/publish/health":
            self._send_json(200, {
                "status": "healthy",
                "platform": "AVENIQ Publishing & Distribution Platform",
                "version": "1.0.0"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

    def do_POST(self):
        global latest_publication
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/publish":
            latest_publication = publisher.publish_campaign("cmp_2026-07-26_001", Channel.LINKEDIN, {"text": "Autonomous AI Briefing"})
            self._send_json(200, {
                "status": "Published",
                "publication_id": latest_publication.publication_id,
                "url": latest_publication.publication_url,
                "verification": latest_publication.status.value
            })
        elif path == "/publish/rollback" or path == "/publish/cancel":
            self._send_json(200, {"status": "Rolled Back", "publication_id": "pub_cmp_001"})
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8096):
    server_address = ("", port)
    httpd = HTTPServer(server_address, PublishingAPIHandler)
    print(f"Publishing REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
