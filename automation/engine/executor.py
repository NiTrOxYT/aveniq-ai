"""
Executor Abstraction for AVENIQ AI v2 Native Workflow Engine.
Decouples parallel execution model (ThreadPool, ProcessPool, Distributed) from workflow logic.
"""

from abc import ABC, abstractmethod
from typing import Callable, Any
from concurrent.futures import ThreadPoolExecutor, Future

class BaseExecutor(ABC):
    @abstractmethod
    def submit(self, fn: Callable, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def shutdown(self, wait: bool = True):
        pass

class ThreadExecutor(BaseExecutor):
    def __init__(self, max_workers: int = 4):
        self._pool = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="WorkflowExecutor")

    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        return self._pool.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True):
        self._pool.shutdown(wait=wait)
