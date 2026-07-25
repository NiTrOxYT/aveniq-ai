"""
Approval Context Loader & Builder for AVENIQ Human Approval System.
Normalizes DeliveryPackage, EditorialReport, MediaPackage, and ResearchPackage into ApprovalContext.
"""

from typing import Dict, Any
from delivery.reports.generator import DeliveryReportGenerator
from editorial.reports.generator import EditorialReportGenerator
from creative.reports.generator import CreativeReportGenerator
from research.reports.generator import ResearchReportGenerator
from approval.models.schema import ApprovalContext

class ContextLoader:
    @staticmethod
    def load_delivery_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return DeliveryReportGenerator().generate_delivery_report(topic)

    @staticmethod
    def load_editorial_report(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return EditorialReportGenerator().generate_editorial_report(topic)

    @staticmethod
    def load_media_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return CreativeReportGenerator().generate_media_report(topic)

    @staticmethod
    def load_research_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return ResearchReportGenerator().generate_package_report(topic)

class ApprovalContextBuilder:
    @staticmethod
    def build_context(topic: str = "AI Agents in Enterprise Operations") -> ApprovalContext:
        del_pkg = ContextLoader.load_delivery_package(topic)
        edt_report = ContextLoader.load_editorial_report(topic)
        media_pkg = ContextLoader.load_media_package(topic)
        res_pkg = ContextLoader.load_research_package(topic)

        return ApprovalContext(
            delivery_package=del_pkg,
            editorial_report=edt_report,
            media_package=media_pkg,
            research_package=res_pkg
        )
