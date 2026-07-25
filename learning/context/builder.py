"""
Learning Context Loader & Builder for AVENIQ Learning Department.
Normalizes ArchivePackage, DeliveryPackage, and Historical Learning Memory into LearningContext.
"""

from typing import Dict, Any
from archive.reports.generator import ArchiveReportGenerator
from delivery.reports.generator import DeliveryReportGenerator
from learning.models.schema import LearningContext

class ContextLoader:
    @staticmethod
    def load_archive_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return ArchiveReportGenerator().generate_archive_report(topic)

    @staticmethod
    def load_delivery_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return DeliveryReportGenerator().generate_delivery_report(topic)

class LearningContextBuilder:
    @staticmethod
    def build_context(topic: str = "AI Agents in Enterprise Operations") -> LearningContext:
        arc_pkg = ContextLoader.load_archive_package(topic)
        del_pkg = ContextLoader.load_delivery_package(topic)

        mock_learning_memory = {
            "total_past_recommendations": 12,
            "approved_recommendations": 10,
            "implemented_proposals": 8
        }

        return LearningContext(
            archive_package=arc_pkg,
            delivery_package=del_pkg,
            historical_learning_memory=mock_learning_memory
        )
