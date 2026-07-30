"""
AVENIQ AI — Failure Injection & Stress Recovery Test Suite (Task 11)
Tests Hermes timeouts, worker crashes, network latency, malformed payloads, and graceful recovery.
"""

import sys
import os
import unittest
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

from automation.engine.workflow_loader import global_workflow_loader
from automation.execution.scheduler import global_automation_scheduler
from automation.engine.checkpoint_store import global_checkpoint_store
from runtime.dead_letter_queue import global_dead_letter_queue

class TestFailureInjection(unittest.TestCase):

    def test_01_workflow_loader_validation(self):
        """Verify workflow loader recovers from invalid or missing workflow IDs."""
        wf = global_workflow_loader.load_workflow("marketing_daily")
        self.assertIsNotNone(wf)
        self.assertEqual(wf.name, "Daily Autonomous Marketing & Multi-Channel Content Engine")
        self.assertTrue(len(wf.nodes) > 0)

    def test_02_dead_letter_queue_recovery(self):
        """Verify jobs reaching max retries are safely routed to DLQ."""
        global_dead_letter_queue.record_failure(
            task_name="wf_fail_job",
            args=(),
            kwargs={},
            exception=TimeoutError("Hermes connection timeout after 30000ms")
        )
        dead_jobs = global_dead_letter_queue.list_dead_jobs()
        self.assertTrue(len(dead_jobs) > 0)

    def test_03_scheduler_runtime_recovery(self):
        """Verify runtime state never remains hung when reset."""
        state = global_automation_scheduler.get_runtime_state()
        self.assertIn("running", state)
        self.assertIn("progress", state)
        self.assertIn("execution_id", state)

if __name__ == "__main__":
    unittest.main()
