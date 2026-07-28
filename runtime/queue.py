"""
Asynchronous Background Worker Task Queue for AVENIQ AI Runtime.
Prevents heavy operations (extraction, indexing, reflection) from blocking HTTP handlers.
"""

import queue
import threading
import logging
from typing import Callable, Any, Dict

logger = logging.getLogger("aveniq.runtime.queue")


class BackgroundQueue:
    def __init__(self):
        self._work_queue: queue.Queue = queue.Queue()
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True, name="AVENIQ-BackgroundWorker")
        self._running = True
        self._worker_thread.start()

    def enqueue(self, func: Callable, *args, **kwargs):
        """Enqueue a background task for asynchronous execution."""
        self._work_queue.put((func, args, kwargs))

    def get_queue_size(self) -> int:
        return self._work_queue.qsize()

    def _worker_loop(self):
        while self._running:
            try:
                item = self._work_queue.get(timeout=1.0)
                if not item:
                    continue
                func, args, kwargs = item
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"[BackgroundQueue] Error executing task: {e}")
                finally:
                    self._work_queue.task_done()
            except queue.Empty:
                continue

    def stop(self):
        self._running = False


global_background_queue = BackgroundQueue()
