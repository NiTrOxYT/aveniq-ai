"""
REST API Router & Lightweight HTTP Server for AVENIQ Archive Department.
Exposes JSON endpoints for downstream audit systems, time-travel queries, and historical analytics tools.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from archive.reports.generator import ArchiveReportGenerator
from archive.repository.manager import ArchiveRepositoryManager
from archive.search.archive_search import ArchiveSearchEngine

generator = ArchiveReportGenerator()
repository = ArchiveRepositoryManager()

class ArchiveAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        query_params = parse_qs(parsed.query)

        if path == "/archive/package" or path == "/archive/campaign":
            report = generator.generate_archive_report()
            self._send_json(200, report)
        elif path == "/archive/search":
            q = query_params.get("q", ["AI"])[0]
            pkgs = repository.list_archived_packages()
            results = ArchiveSearchEngine.search(q, pkgs)
            self._send_json(200, {
                "query": q,
                "total_results": len(results),
                "results": [
                    {
                        "archive_id": r.archive_id,
                        "campaign_id": r.campaign_id,
                        "topic": r.topic,
                        "score": r.score,
                        "matched_field": r.matched_field,
                        "created_at": r.created_at
                    } for r in results
                ]
            })
        elif path == "/archive/assets":
            report = generator.generate_archive_report()
            self._send_json(200, {
                "archive_id": report["archive_id"],
                "asset_count": report["manifest"]["asset_count"],
                "checksums": report["manifest"]["checksums"]
            })
        elif path == "/archive/version":
            report = generator.generate_archive_report()
            self._send_json(200, {
                "version": report["version"],
                "snapshots": report["snapshots"],
                "events": report["events_log"]
            })
        elif path == "/archive/health":
            self._send_json(200, {
                "status": "healthy",
                "department": "Archive Department (AI Archivist)",
                "version": "1.0.0",
                "quality_gate_status": "Active (11 Gates Enforced)"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8087):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ArchiveAPIHandler)
    print(f"Archive REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
