"""
REST API Router & Lightweight HTTP Server for AVENIQ Strategy Department.
Exposes JSON endpoints for AI agents, n8n workflows, and external systems.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from strategy.reports.generator import StrategyReportGenerator
from strategy.utils.analytics import StrategyAnalyticsTracker

generator = StrategyReportGenerator()

class StrategyAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/strategy/today":
            report = generator.generate_daily_report()
            self._send_json(200, report)
        elif path == "/strategy/weekly":
            report = generator.generate_weekly_report()
            self._send_json(200, report)
        elif path == "/strategy/monthly":
            report = generator.generate_monthly_report()
            self._send_json(200, report)
        elif path == "/strategy/opportunities":
            report = generator.generate_daily_report()
            self._send_json(200, {
                "opportunities": [
                    {
                        "topic": report["content"]["suggested_title"],
                        "priority": report["priority"],
                        "category": report["content"]["category"]
                    }
                ]
            })
        elif path == "/strategy/campaigns":
            report = generator.generate_weekly_report()
            self._send_json(200, {
                "top_campaign": report["top_campaign"],
                "content_mix": report["content_mix"]
            })
        elif path == "/strategy/audience":
            report = generator.generate_daily_report()
            self._send_json(200, report["audience"])
        elif path == "/strategy/seo":
            report = generator.generate_daily_report()
            self._send_json(200, report["seo"])
        elif path == "/strategy/health":
            analytics = StrategyAnalyticsTracker.calculate_analytics()
            self._send_json(200, {
                "status": "healthy",
                "department": "Strategy Department (AI CMO)",
                "version": "1.0.0",
                "analytics": analytics
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, StrategyAPIHandler)
    print(f"Strategy REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
