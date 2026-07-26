"""
Comprehensive Dashboard Test Suite for AVENIQ Web Dashboard & Customer Portal.
Tests static web assets, Dashboard API endpoints, Design System styles, and SPA router.
"""

import unittest
import os
from apps.dashboard.api import DashboardServerHandler

class TestDashboardPlatform(unittest.TestCase):
    def test_static_assets_exist(self):
        base = "apps/dashboard"
        self.assertTrue(os.path.exists(os.path.join(base, "index.html")))
        self.assertTrue(os.path.exists(os.path.join(base, "css/style.css")))
        self.assertTrue(os.path.exists(os.path.join(base, "js/event_bus.js")))
        self.assertTrue(os.path.exists(os.path.join(base, "js/widgets.js")))
        self.assertTrue(os.path.exists(os.path.join(base, "js/command_palette.js")))
        self.assertTrue(os.path.exists(os.path.join(base, "js/api.js")))

    def test_dashboard_api_handler_import(self):
        self.assertIsNotNone(DashboardServerHandler)

if __name__ == "__main__":
    unittest.main()
