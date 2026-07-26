"""
Reliability modules: StateMachine, ErrorClassifier, and RetryEngine.
"""

import time
from typing import Callable, Any, Tuple
from workflow.models.status import WorkflowStatus

class WorkflowStateMachine:
    VALID_TRANSITIONS = {
        WorkflowStatus.PENDING: [WorkflowStatus.READY, WorkflowStatus.SKIPPED, WorkflowStatus.CANCELLED],
        WorkflowStatus.READY: [WorkflowStatus.RUNNING, WorkflowStatus.SKIPPED, WorkflowStatus.CANCELLED],
        WorkflowStatus.RUNNING: [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.RETRYING],
        WorkflowStatus.RETRYING: [WorkflowStatus.RUNNING, WorkflowStatus.FAILED],
        WorkflowStatus.COMPLETED: [],
        WorkflowStatus.FAILED: [WorkflowStatus.RETRYING],
        WorkflowStatus.SKIPPED: [],
        WorkflowStatus.CANCELLED: []
    }

    @staticmethod
    def can_transition(current: WorkflowStatus, target: WorkflowStatus) -> bool:
        allowed = WorkflowStateMachine.VALID_TRANSITIONS.get(current, [])
        return target in allowed

class ErrorClassifier:
    RETRYABLE_EXCEPTIONS = (
        TimeoutError, ConnectionError, OSError, RuntimeWarning
    )

    @staticmethod
    def is_retryable(exception: Exception) -> bool:
        if isinstance(exception, ErrorClassifier.RETRYABLE_EXCEPTIONS):
            return True
        err_msg = str(exception).lower()
        retryable_keywords = ["timeout", "connection", "rate limit", "temporary", "busy", "503", "504"]
        return any(k in err_msg for k in retryable_keywords)

class RetryEngine:
    @staticmethod
    def execute_with_retry(
        func: Callable[[], Any],
        max_retries: int = 3,
        initial_backoff: float = 0.1,
        backoff_factor: float = 2.0,
        on_retry: Callable[[int, Exception], None] = None
    ) -> Tuple[bool, Any, int, str]:
        attempt = 0
        backoff = initial_backoff

        while attempt <= max_retries:
            try:
                result = func()
                return True, result, attempt, ""
            except Exception as e:
                attempt += 1
                if attempt > max_retries or not ErrorClassifier.is_retryable(e):
                    return False, None, attempt - 1, str(e)
                if on_retry:
                    on_retry(attempt, e)
                time.sleep(backoff)
                backoff *= backoff_factor

        return False, None, max_retries, "Exhausted retries"
