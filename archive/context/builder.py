"""
Archive Context Loader & Builder for AVENIQ Archive Department.
Normalizes DeliveryPackage, ApprovedContentPackage, MediaPackage, ResearchPackage, and PlanningReport.
"""

from typing import Dict, Any
from delivery.reports.generator import DeliveryReportGenerator
from editorial.reports.generator import EditorialReportGenerator
from creative.reports.generator import CreativeReportGenerator
from research.reports.generator import ResearchReportGenerator
from planning.reports.generator import PlanningReportGenerator
from archive.models.schema import ArchiveContext

class ContextLoader:
    @staticmethod
    def load_delivery_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return DeliveryReportGenerator().generate_delivery_report(topic)

    @staticmethod
    def load_approved_content(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return EditorialReportGenerator().generate_editorial_report(topic)

    @staticmethod
    def load_media_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return CreativeReportGenerator().generate_media_report(topic)

    @staticmethod
    def load_research_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return ResearchReportGenerator().generate_package_report(topic)

    @staticmethod
    def load_planning_report() -> Dict[str, Any]:
        return PlanningReportGenerator().generate_planning_report()

class ArchiveContextBuilder:
    @staticmethod
    def build_context(topic: str = "AI Agents in Enterprise Operations") -> ArchiveContext:
        del_pkg = ContextLoader.load_delivery_package(topic)
        app_content = ContextLoader.load_approved_content(topic)
        media_pkg = ContextLoader.load_media_package(topic)
        res_pkg = ContextLoader.load_research_package(topic)
        plan_report = ContextLoader.load_planning_report()

        return ArchiveContext(
            delivery_package=del_pkg,
            approved_content_package=app_content,
            media_package=media_pkg,
            research_package=res_pkg,
            planning_report=plan_report
        )
