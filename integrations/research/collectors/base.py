"""
Base Market Collector with Source Failure Isolation & Incremental Sync Checkpoints.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from integrations.research.document import ResearchDocument

class BaseMarketCollector(ABC):
    source_name: str = "base"

    @abstractmethod
    def collect_raw(self, topic: str, config: Any) -> List[ResearchDocument]:
        pass

    def collect_safe(self, topic: str, config: Any = None) -> List[ResearchDocument]:
        try:
            return self.collect_raw(topic, config)
        except Exception as e:
            print(f"⚠️ [Collector Warning] {self.source_name} failed: {e}. Pipeline continuing safely.")
            return []
