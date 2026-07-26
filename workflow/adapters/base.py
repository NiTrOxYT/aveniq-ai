"""
DepartmentAdapter Base Abstract Interface and Standardized Adapters.
The Workflow Orchestrator communicates exclusively with adapters and never directly invokes department internals.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from workflow.execution.execution_context import ExecutionContext

class DepartmentAdapter(ABC):
    name: str = ""
    version: str = "1.0.0"
    input_packages: List[str] = []
    output_package: str = ""

    @abstractmethod
    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        pass

# 1. Company Brain Adapter
class CompanyBrainAdapter(DepartmentAdapter):
    name = "company_brain"
    version = "1.0.0"
    input_packages = []
    output_package = "company_brain"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from brain.loader.discovery import DiscoveryEngine
        discovery = DiscoveryEngine()
        modules = discovery.discover_modules()
        return {
            "status": "Ingested",
            "modules_count": len(modules),
            "version": "1.0.0"
        }

# 2. Market Intelligence Adapter (backed by research department)
class MarketAdapter(DepartmentAdapter):
    name = "market"
    version = "1.0.0"
    input_packages = []
    output_package = "market"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from research.reports.generator import ResearchReportGenerator
        return ResearchReportGenerator().generate_package_report()

# 3. Brand Growth Intelligence Adapter
class GrowthAdapter(DepartmentAdapter):
    name = "growth"
    version = "1.0.0"
    input_packages = []
    output_package = "growth"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from growth.reports.generator import GrowthReportGenerator
        return GrowthReportGenerator().generate_growth_report()

# 4. Strategy Department Adapter
class StrategyAdapter(DepartmentAdapter):
    name = "strategy"
    version = "1.0.0"
    input_packages = ["company_brain"]
    output_package = "strategy"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from strategy.reports.generator import StrategyReportGenerator
        return StrategyReportGenerator().generate_daily_report()

# 5. Calendar Department Adapter
class CalendarAdapter(DepartmentAdapter):
    name = "calendar"
    version = "1.0.0"
    input_packages = ["strategy"]
    output_package = "calendar"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from calendar_dept.reports.generator import CalendarReportGenerator
        return CalendarReportGenerator().generate_calendar_report()

# 6. Planning Department Adapter
class PlanningAdapter(DepartmentAdapter):
    name = "planning"
    version = "1.0.0"
    input_packages = ["strategy", "calendar"]
    output_package = "planning"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from planning.reports.generator import PlanningReportGenerator
        return PlanningReportGenerator().generate_planning_report()

# 7. Content Department Adapter
class ContentAdapter(DepartmentAdapter):
    name = "content"
    version = "1.0.0"
    input_packages = ["planning"]
    output_package = "content"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from content.reports.generator import ContentReportGenerator
        return ContentReportGenerator().generate_content_report()

# 8. Creative Department Adapter
class CreativeAdapter(DepartmentAdapter):
    name = "creative"
    version = "1.0.0"
    input_packages = ["planning", "content"]
    output_package = "creative"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from creative.reports.generator import CreativeReportGenerator
        return CreativeReportGenerator().generate_media_report()

# 9. Editorial Department Adapter
class EditorialAdapter(DepartmentAdapter):
    name = "editorial"
    version = "1.0.0"
    input_packages = ["content", "creative"]
    output_package = "editorial"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from editorial.reports.generator import EditorialReportGenerator
        return EditorialReportGenerator().generate_editorial_report()

# 10. Delivery Department Adapter
class DeliveryAdapter(DepartmentAdapter):
    name = "delivery"
    version = "1.0.0"
    input_packages = ["editorial", "creative"]
    output_package = "delivery"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from delivery.reports.generator import DeliveryReportGenerator
        return DeliveryReportGenerator().generate_delivery_report()

# 11. Human Approval System Adapter
class ApprovalAdapter(DepartmentAdapter):
    name = "approval"
    version = "1.0.0"
    input_packages = ["delivery"]
    output_package = "approval"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from approval.reports.generator import ApprovalReportGenerator
        return ApprovalReportGenerator().generate_approval_report()

# 12. Archive Department Adapter
class ArchiveAdapter(DepartmentAdapter):
    name = "archive"
    version = "1.0.0"
    input_packages = ["delivery", "approval"]
    output_package = "archive"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from archive.reports.generator import ArchiveReportGenerator
        return ArchiveReportGenerator().generate_archive_report()

# 13. Learning Department Adapter
class LearningAdapter(DepartmentAdapter):
    name = "learning"
    version = "1.0.0"
    input_packages = ["archive"]
    output_package = "learning"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        from learning.reports.generator import LearningReportGenerator
        return LearningReportGenerator().generate_learning_report()

ADAPTER_REGISTRY = {
    "company_brain": CompanyBrainAdapter(),
    "market": MarketAdapter(),
    "growth": GrowthAdapter(),
    "strategy": StrategyAdapter(),
    "calendar": CalendarAdapter(),
    "planning": PlanningAdapter(),
    "content": ContentAdapter(),
    "creative": CreativeAdapter(),
    "editorial": EditorialAdapter(),
    "delivery": DeliveryAdapter(),
    "approval": ApprovalAdapter(),
    "archive": ArchiveAdapter(),
    "learning": LearningAdapter()
}
