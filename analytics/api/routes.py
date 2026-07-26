"""
REST API Router & Lightweight HTTP Server for AVENIQ Performance Analytics Platform.
Exposes JSON endpoints for performance metrics, benchmarks, trends, recommendations, and executive summaries.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from analytics.reports.performance_report import PerformanceReportGenerator
from analytics.optimization.scoring import CampaignScorer, BenchmarkEngine
from analytics.collectors.linkedin import LinkedInCollector
from analytics.optimization.recommendation_engine import OptimizationEngine

class AnalyticsAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/analytics/reports" or path == "/analytics/report":
            rep = json.loads(PerformanceReportGenerator.generate_report("cmp_2026-07-26_001", "json"))
            self._send_json(200, rep)
        elif path == "/analytics/trends":
            self._send_json(200, {
                "improving_topics": ["Model Context Protocol", "Autonomous AI Agents", "pgvector Architecture"],
                "declining_topics": ["Generic Prompt Engineering"],
                "top_formats": ["Visual Carousel", "Technical Architecture Deep Dive"],
                "best_posting_time": "09:00 UTC Tuesday & Thursday"
            })
        elif path == "/analytics/recommendations":
            collector = LinkedInCollector()
            metrics = collector.collect("cmp_001", "pub_001")
            scores = CampaignScorer.calculate_scores(metrics)
            recs = OptimizationEngine.generate_recommendations(scores, {})
            self._send_json(200, [
                {
                    "id": r.id,
                    "target_department": r.target_department,
                    "recommendation": r.recommendation_text,
                    "confidence_score": r.confidence_score,
                    "expected_impact": r.expected_impact
                } for r in recs
            ])
        elif path == "/analytics/status" or path == "/analytics/campaigns":
            self._send_json(200, {
                "active_campaigns_tracked": 12,
                "latest_campaign_id": "cmp_2026-07-26_001",
                "overall_health": "Outperforming (+10.2% vs Benchmark)"
            })
        elif path == "/analytics/health":
            self._send_json(200, {
                "status": "healthy",
                "platform": "AVENIQ Performance Analytics & Continuous Optimization Platform",
                "version": "1.0.0"
            })
        else:
            self._send_json(404, {"error": "Endpoint not found", "path": path})

def start_server(port: int = 8094):
    server_address = ("", port)
    httpd = HTTPServer(server_address, AnalyticsAPIHandler)
    print(f"Analytics REST API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    start_server()
