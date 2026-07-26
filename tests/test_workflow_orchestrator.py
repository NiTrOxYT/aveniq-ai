"""
Unit tests for Workflow Engine Orchestrator, Adapters, PackageRegistry, EventBus, and Exporters.
"""

import unittest
from workflow.engine.orchestrator import Orchestrator
from workflow.execution.package_registry import PackageRegistry
from workflow.execution.dependency_manager import DependencyManager
from workflow.events.event_bus import EventBus, WorkflowStarted, WorkflowCompleted
from workflow.reliability.retry import RetryEngine, ErrorClassifier
from workflow.reports.report_generator import WorkflowReportGenerator
from workflow.adapters.base import ADAPTER_REGISTRY

class TestWorkflowEngine(unittest.TestCase):
    def test_package_registry(self):
        reg = PackageRegistry()
        reg.register("strategy", {"plan": "daily"}, "strategy_type")
        self.assertTrue(reg.exists("strategy"))
        self.assertEqual(reg.get("strategy"), {"plan": "daily"})
        self.assertEqual(len(reg.get_by_type("strategy_type")), 1)
        self.assertEqual(len(reg.history("strategy")), 1)

    def test_dependency_manager(self):
        reg = PackageRegistry()
        self.assertTrue(DependencyManager.is_ready("company_brain", reg))
        self.assertFalse(DependencyManager.is_ready("strategy", reg))
        
        reg.register("company_brain", {"status": "ok"})
        self.assertTrue(DependencyManager.is_ready("strategy", reg))

    def test_event_bus(self):
        bus = EventBus()
        received = []
        bus.subscribe(WorkflowStarted, lambda e: received.append(e.event_type))
        bus.publish(WorkflowStarted(execution_id="exec_001", workflow_name="test"))
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0], "WorkflowStarted")

    def test_error_classifier_and_retry(self):
        self.assertTrue(ErrorClassifier.is_retryable(TimeoutError("LLM timeout")))
        self.assertFalse(ErrorClassifier.is_retryable(ValueError("Invalid schema")))

        calls = 0
        def flappy():
            nonlocal calls
            calls += 1
            if calls < 2:
                raise TimeoutError("Temporary glitch")
            return "success"

        ok, val, retries, err = RetryEngine.execute_with_retry(flappy, max_retries=3)
        self.assertTrue(ok)
        self.assertEqual(val, "success")
        self.assertEqual(retries, 1)

    def test_orchestrator_execution(self):
        orchestrator = Orchestrator()
        result = orchestrator.execute_workflow(workflow_name="unit_test_run")
        self.assertTrue(result.success)
        self.assertEqual(len(result.packages), 13)
        self.assertGreater(len(result.timeline), 10)

    def test_report_exporters(self):
        orchestrator = Orchestrator()
        result = orchestrator.execute_workflow()
        
        json_report = WorkflowReportGenerator.generate_report(result, "json")
        md_report = WorkflowReportGenerator.generate_report(result, "markdown")
        html_report = WorkflowReportGenerator.generate_report(result, "html")

        self.assertIn('"success": true', json_report.lower())
        self.assertIn("# AVENIQ Workflow Execution Report", md_report)
        self.assertIn("<!DOCTYPE html>", html_report)

if __name__ == "__main__":
    unittest.main()
