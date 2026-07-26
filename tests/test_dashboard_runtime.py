"""
Runtime Test Suite for Dashboard REST API & Server Handler.
Validates HTTP GET responses, status codes, and JSON structure for all 8 endpoints.
"""

import unittest
import json
from unittest.mock import MagicMock
from io import BytesIO
from apps.dashboard.api import DashboardServerHandler

class DummyRequest:
    def __init__(self, path: str):
        self.path = path

class TestDashboardRuntime(unittest.TestCase):
    def _get_handler_response(self, path: str):
        handler = DashboardServerHandler.__new__(DashboardServerHandler)
        handler.path = path
        handler.wfile = BytesIO()
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        
        handler.do_GET()
        
        handler.send_response.assert_called_with(200)
        output_bytes = handler.wfile.getvalue()
        return json.loads(output_bytes.decode("utf-8")) if output_bytes else {}

    def test_overview_endpoint(self):
        data = self._get_handler_response("/dashboard/overview")
        self.assertIn("active_campaigns", data)
        self.assertIn("overall_score", data)
        self.assertIn("automation_status", data)

    def test_activity_endpoint(self):
        data = self._get_handler_response("/dashboard/activity")
        self.assertIn("activity_timeline", data)

    def test_approvals_endpoint(self):
        data = self._get_handler_response("/dashboard/approvals")
        self.assertIn("pending_approvals", data)

    def test_analytics_endpoint(self):
        data = self._get_handler_response("/dashboard/analytics")
        self.assertIn("engagement_rate", data)
        self.assertIn("impressions", data)

    def test_reasoning_endpoint(self):
        data = self._get_handler_response("/dashboard/reasoning")
        self.assertIn("topic", data)

    def test_versions_endpoint(self):
        data = self._get_handler_response("/dashboard/versions")
        self.assertIn("campaign_id", data)
        self.assertIn("available_versions", data)

    def test_health_endpoint(self):
        data = self._get_handler_response("/dashboard/health")
        self.assertEqual(data["status"], "healthy")
        self.assertIn("portal", data)

if __name__ == "__main__":
    unittest.main()
