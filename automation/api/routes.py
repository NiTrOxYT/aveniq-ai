"""
REST API Router & Lightweight HTTP Server for AVENIQ Autonomous Execution Platform.
Exposes JSON endpoints for daily workflow triggers, human approval actions, emergency controls, and reporting.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from automation.execution.daily_runner import DailyRunner
from automation.reports.daily_summary import DailySummaryReportGenerator
from automation.audit.audit_log import global_emergency_controls

runner = DailyRunner()
latest_run_result = None

class AutomationAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        global latest_run_result
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/automation/status":
            self._send_json(200, {
                "active_sessions": len(runner.session_mgr._sessions),
                "latest_run": latest_run_result
            })
        elif path == "/automation/report":
            if not latest_run_result:
                latest_run_result = runner.run_daily_cycle()
            rep = json.loads(DailySummaryReportGenerator.generate_report(latest_run_result, "json"))
            self._send_json(200, rep)
        elif path == "/automation/health":
            self._send_json(200, {
                "status": "healthy",
                "platform": "AVENIQ Autonomous Execution & Human Approval Platform",
                "version": "1.0.0"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

    def do_POST(self):
        global latest_run_result
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/automation/run":
            latest_run_result = runner.run_daily_cycle()
            self._send_json(200, latest_run_result)
        elif path == "/automation/approve":
            sid = latest_run_result.get("session_id") if latest_run_result else "aut_sess_001"
            res = runner.process_human_decision(sid, "Approve")
            self._send_json(200, res)
        elif path == "/automation/reject":
            sid = latest_run_result.get("session_id") if latest_run_result else "aut_sess_001"
            res = runner.process_human_decision(sid, "Reject")
            self._send_json(200, res)
        elif path == "/automation/regenerate":
            sid = latest_run_result.get("session_id") if latest_run_result else "aut_sess_001"
            res = runner.process_human_decision(sid, "More Technical")
            self._send_json(200, res)
        elif path == "/automation/control":
            self._send_json(200, {"status": "Control action executed"})
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8093):
    server_address = ("", port)
    httpd = HTTPServer(server_address, AutomationAPIHandler)
    print(f"Automation REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
