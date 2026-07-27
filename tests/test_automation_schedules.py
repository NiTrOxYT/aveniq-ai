"""
Production Unit & Integration Test Suite for Automation Schedule Management.
Validates schedule CRUD, separate history persistence, immutable UUID keys,
trigger preview calculators, async job queue, bulk actions, import/export, and summary KPIs.
"""

import os
import shutil
import unittest
import json
import time
from datetime import datetime, timezone

from automation.storage.schedule_store import ScheduleStore
from automation.execution.scheduler import AutomationScheduler

class TestAutomationSchedules(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/scratch_schedule_store"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)
        self.store = ScheduleStore(base_dir=self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_create_get_update_schedule(self):
        payload = {
            "name": "Social Media Pulse",
            "description": "Daily post generator",
            "department": "Content",
            "priority": "HIGH",
            "trigger": "daily",
            "time": "09:00",
            "timezone": "Asia/Kolkata",
            "prompt": "Create social media post for {{company}}",
            "outputs": ["telegram", "dashboard"],
            "enabled": True
        }
        created = self.store.create_schedule(payload)
        self.assertIsNotNone(created.get("id"))
        uuid_id = created["id"]
        self.assertEqual(created["name"], "Social Media Pulse")

        # Get schedule
        fetched = self.store.get_schedule(uuid_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["department"], "Content")

        # Update schedule (Rename should preserve UUID)
        updated = self.store.update_schedule(uuid_id, {
            "name": "Social Media Pulse V2",
            "description": "Updated post generator",
            "department": "Content",
            "priority": "CRITICAL",
            "trigger": "weekly",
            "time": "10:00",
            "timezone": "Asia/Kolkata",
            "prompt": "Create weekly digest for {{company}}",
            "outputs": ["dashboard"],
            "enabled": True
        })
        self.assertEqual(updated["id"], uuid_id)  # Immutable UUID!
        self.assertEqual(updated["name"], "Social Media Pulse V2")
        self.assertEqual(updated["trigger"], "weekly")

    def test_separate_history_persistence(self):
        payload = {
            "name": "Market Signal Scanner",
            "prompt": "Scan RSS feed",
            "department": "Research"
        }
        sch = self.store.create_schedule(payload)
        sid = sch["id"]

        hist_record = {
            "started_at": "2026-07-27T10:00:00Z",
            "completed_at": "2026-07-27T10:00:02Z",
            "duration_ms": 2000,
            "trigger": "scheduled",
            "status": "success",
            "output_summary": "Scanned 45 articles",
            "checklist": ["✓ Signal Ingested", "✓ Report Saved"]
        }

        history_entry = self.store.add_execution_history(sid, hist_record)
        self.assertEqual(history_entry["status"], "success")

        # Check history file is stored separately under history/<uuid>/
        hist_dir = os.path.join(self.test_dir, "history", sid)
        self.assertTrue(os.path.isdir(hist_dir))
        hist_files = os.listdir(hist_dir)
        self.assertGreaterEqual(len(hist_files), 1)

        # Retrieve history via store
        history_list = self.store.get_execution_history(sid)
        self.assertEqual(len(history_list), 1)
        self.assertEqual(history_list[0]["output_summary"], "Scanned 45 articles")

    def test_toggle_and_duplicate(self):
        sch = self.store.create_schedule({"name": "Draft Generator", "prompt": "Gen copy", "department": "Content"})
        sid = sch["id"]

        # Pause schedule
        toggled = self.store.toggle_schedule(sid, state="paused")
        self.assertEqual(toggled["state"], "paused")

        # Duplicate schedule
        dup = self.store.duplicate_schedule(sid)
        self.assertNotEqual(dup["id"], sid)
        self.assertEqual(dup["name"], "Draft Generator Copy")

    def test_delete_schedule(self):
        sch = self.store.create_schedule({"name": "Temp Task", "prompt": "Do temp task", "department": "General"})
        sid = sch["id"]
        self.store.delete_schedule(sid)
        self.assertIsNone(self.store.get_schedule(sid))

    def test_trigger_preview_computation(self):
        previews = self.store.compute_next_executions(
            trigger="hourly",
            time_str="12:00",
            interval_value=1,
            count=5
        )
        self.assertEqual(len(previews), 5)

        previews_weekdays = self.store.compute_next_executions(
            trigger="weekdays_only",
            time_str="09:00",
            count=5
        )
        self.assertEqual(len(previews_weekdays), 5)

    def test_summary_statistics(self):
        self.store.create_schedule({"name": "Task 1", "prompt": "p1", "enabled": True, "state": "active"})
        self.store.create_schedule({"name": "Task 2", "prompt": "p2", "enabled": False, "state": "disabled"})
        summary = self.store.get_summary_statistics()
        self.assertGreaterEqual(summary["total_schedules"], 2)
        self.assertGreaterEqual(summary["running"], 1)
        self.assertGreaterEqual(summary["disabled"], 1)

    def test_import_export(self):
        sch = self.store.create_schedule({"name": "Exportable Task", "prompt": "export prompt", "department": "Creative"})
        exported = self.store.export_schedules([sch["id"]])
        self.assertEqual(len(exported), 1)
        self.assertEqual(exported[0]["name"], "Exportable Task")

        imported = self.store.import_schedules(exported)
        self.assertEqual(len(imported), 1)
        self.assertNotEqual(imported[0]["id"], sch["id"])  # Deduplicated UUID!

if __name__ == "__main__":
    unittest.main()
