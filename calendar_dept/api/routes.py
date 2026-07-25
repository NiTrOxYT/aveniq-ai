"""
REST API Router & Lightweight HTTP Server for AVENIQ Calendar & Campaign Management.
Exposes JSON endpoints for publishing schedulers, campaign dashboards, and operations tools.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from calendar_dept.reports.generator import CalendarReportGenerator

generator = CalendarReportGenerator()

class CalendarAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/calendar/package" or path == "/calendar/month":
            report = generator.generate_calendar_report()
            self._send_json(200, report)
        elif path == "/calendar/week":
            report = generator.generate_calendar_report()
            self._send_json(200, {"weekly_themes": report["weekly_themes"]})
        elif path == "/calendar/day":
            report = generator.generate_calendar_report()
            self._send_json(200, {"30day_summary": report["30day_calendar"]})
        elif path == "/calendar/campaigns":
            report = generator.generate_calendar_report()
            self._send_json(200, {
                "campaigns": report["campaigns"],
                "roadmap_90day": report["90day_roadmap"]
            })
        elif path == "/calendar/events":
            report = generator.generate_calendar_report()
            self._send_json(200, {"events": report["events"]})
        elif path == "/calendar/health":
            self._send_json(200, {
                "status": "healthy",
                "department": "Calendar & Campaign Management",
                "version": "1.0.0",
                "quality_gate_status": "Active (10 Gates Enforced)"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8090):
    server_address = ("", port)
    httpd = HTTPServer(server_address, CalendarAPIHandler)
    print(f"Calendar REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
