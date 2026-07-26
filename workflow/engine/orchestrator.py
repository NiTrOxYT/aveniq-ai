"""
Lightweight Master Workflow Orchestrator for AVENIQ AI.
Coordinates execution across department adapters without containing business logic.
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from workflow.models.status import WorkflowStatus
from workflow.models.step import WorkflowStep
from workflow.models.execution import WorkflowExecution
from workflow.models.result import WorkflowResult
from workflow.execution.execution_context import ExecutionContext, DependencyManager
from workflow.execution.package_registry import PackageRegistry
from workflow.adapters.base import ADAPTER_REGISTRY
from workflow.engine.pipeline import Pipeline, WorkflowConfig
from workflow.events.event_bus import (
    EventBus, WorkflowStarted, WorkflowCompleted, WorkflowFailed,
    DepartmentStarted, DepartmentCompleted, DepartmentFailed, PackageRegistered
)
from workflow.monitoring.timeline import TimelineRecorder, MetricsCollector, WorkflowStructuredLogger
from workflow.reliability.retry import RetryEngine

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class Orchestrator:
    def __init__(self, pipeline: Optional[Pipeline] = None, event_bus: Optional[EventBus] = None):
        self.pipeline = pipeline or Pipeline()
        self.event_bus = event_bus or EventBus()
        self.timeline_recorder = TimelineRecorder(self.event_bus)

    def execute_workflow(
        self,
        execution_id: Optional[str] = None,
        workflow_name: str = "aveniq_master_workflow",
        config: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        start_time = time.time()
        exec_id = execution_id or f"exec_{int(start_time)}_{abs(hash(workflow_name))%1000:03d}"
        
        registry = PackageRegistry()
        logger = WorkflowStructuredLogger(exec_id)
        metrics_collector = MetricsCollector()

        context = ExecutionContext(
            execution_id=exec_id,
            workflow_id=workflow_name,
            started_at=_get_utc_now(),
            configuration=config or {},
            logger=logger,
            package_registry=registry,
            metrics_collector=metrics_collector,
            event_bus=self.event_bus,
            workflow_state=WorkflowStatus.RUNNING.value
        )

        steps_list = [
            WorkflowStep(name=dept, department=dept, status=WorkflowStatus.PENDING)
            for dept in self.pipeline.get_steps()
        ]

        execution = WorkflowExecution(
            execution_id=exec_id,
            workflow_name=workflow_name,
            started_at=_get_utc_now(),
            status=WorkflowStatus.RUNNING,
            steps=steps_list
        )

        self.event_bus.publish(WorkflowStarted(execution_id=exec_id, workflow_name=workflow_name))

        success = True
        failed_dept = ""
        error_msg = ""

        for step in execution.steps:
            dept = step.department
            execution.current_step = dept
            step.status = WorkflowStatus.RUNNING
            step.started_at = _get_utc_now()

            # Check dependencies
            if not DependencyManager.is_ready(dept, registry):
                missing = DependencyManager.get_missing_dependencies(dept, registry)
                step.status = WorkflowStatus.FAILED
                step.error = f"Missing required dependencies: {missing}"
                execution.status = WorkflowStatus.FAILED
                execution.errors.append(step.error)
                success = False
                failed_dept = dept
                error_msg = step.error
                self.event_bus.publish(DepartmentFailed(execution_id=exec_id, department=dept, error=step.error))
                break

            self.event_bus.publish(DepartmentStarted(execution_id=exec_id, department=dept))
            adapter = ADAPTER_REGISTRY.get(dept)

            if not adapter:
                step.status = WorkflowStatus.FAILED
                step.error = f"Adapter for department '{dept}' not registered"
                execution.status = WorkflowStatus.FAILED
                execution.errors.append(step.error)
                success = False
                failed_dept = dept
                error_msg = step.error
                self.event_bus.publish(DepartmentFailed(execution_id=exec_id, department=dept, error=step.error))
                break

            step_start = time.time()

            # Execute with Retry Engine
            ok, output_pkg, retries, err = RetryEngine.execute_with_retry(
                lambda: adapter.execute(context),
                max_retries=3
            )

            step_duration = round(time.time() - step_start, 3)
            step.duration = step_duration
            step.retry_count = retries
            step.finished_at = _get_utc_now()

            if ok and output_pkg:
                step.status = WorkflowStatus.COMPLETED
                step.output_package = output_pkg
                registry.register(adapter.output_package, output_pkg)
                metrics_collector.record_step(dept, step_duration, retries)
                self.event_bus.publish(PackageRegistered(execution_id=exec_id, package_name=adapter.output_package, package_type=dept))
                self.event_bus.publish(DepartmentCompleted(execution_id=exec_id, department=dept, duration=step_duration))
            else:
                step.status = WorkflowStatus.FAILED
                step.error = err
                execution.errors.append(f"Department {dept} failed: {err}")
                execution.status = WorkflowStatus.FAILED
                success = False
                failed_dept = dept
                error_msg = err
                self.event_bus.publish(DepartmentFailed(execution_id=exec_id, department=dept, error=err))
                break

        total_duration = round(time.time() - start_time, 3)
        metrics_collector.total_duration = total_duration
        execution.finished_at = _get_utc_now()

        if success:
            execution.status = WorkflowStatus.COMPLETED
            self.event_bus.publish(WorkflowCompleted(execution_id=exec_id, duration=total_duration, packages_count=len(registry.get_all())))
        else:
            self.event_bus.publish(WorkflowFailed(execution_id=exec_id, error=error_msg, failed_step=failed_dept))

        return WorkflowResult(
            success=success,
            packages=registry.get_all(),
            metrics=metrics_collector.get_metrics_summary(),
            errors=execution.errors,
            timeline=self.timeline_recorder.events
        )
