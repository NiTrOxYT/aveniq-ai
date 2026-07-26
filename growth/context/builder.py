"""
Growth Context Loader & Builder for AVENIQ Brand Growth Intelligence.
Normalizes StrategyPackage, CalendarPackage, and Archive History into CalendarContextRef.
"""

from typing import Dict, Any, List
from strategy.reports.generator import StrategyReportGenerator
from calendar_dept.reports.generator import CalendarReportGenerator
from archive.repository.manager import ArchiveRepositoryManager
from growth.models.schema import CalendarContextRef

class ContextLoader:
    @staticmethod
    def load_strategy_package() -> Dict[str, Any]:
        return StrategyReportGenerator().generate_daily_report()

    @staticmethod
    def load_calendar_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return CalendarReportGenerator().generate_calendar_report(topic)

    @staticmethod
    def load_archive_history() -> List[Dict[str, Any]]:
        return ArchiveRepositoryManager().list_archived_packages()

class GrowthContextBuilder:
    @staticmethod
    def build_context(topic: str = "AI Agents in Enterprise Operations") -> CalendarContextRef:
        strat_pkg = ContextLoader.load_strategy_package()
        cal_pkg = ContextLoader.load_calendar_package(topic)
        arc_history = ContextLoader.load_archive_history()

        return CalendarContextRef(
            strategy_package=strat_pkg,
            calendar_package=cal_pkg,
            archive_history=arc_history
        )
