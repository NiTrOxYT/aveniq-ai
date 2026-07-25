"""
Calendar Context Loader & Builder for AVENIQ Calendar & Campaign Management.
Normalizes StrategyPackage, PlanningPackage, and Archive History into CalendarContext.
"""

from typing import Dict, Any, List
from strategy.reports.generator import StrategyReportGenerator
from planning.reports.generator import PlanningReportGenerator
from archive.repository.manager import ArchiveRepositoryManager
from calendar_dept.models.schema import CalendarContext

class ContextLoader:
    @staticmethod
    def load_strategy_package() -> Dict[str, Any]:
        return StrategyReportGenerator().generate_daily_report()

    @staticmethod
    def load_planning_package(topic: str = "AI Agents in Enterprise Operations") -> Dict[str, Any]:
        return PlanningReportGenerator().generate_planning_report(topic)

    @staticmethod
    def load_archive_history() -> List[Dict[str, Any]]:
        return ArchiveRepositoryManager().list_archived_packages()

class CalendarContextBuilder:
    @staticmethod
    def build_context(topic: str = "AI Agents in Enterprise Operations") -> CalendarContext:
        strat_pkg = ContextLoader.load_strategy_package()
        plan_pkg = ContextLoader.load_planning_package(topic)
        arc_history = ContextLoader.load_archive_history()

        return CalendarContext(
            strategy_package=strat_pkg,
            planning_package=plan_pkg,
            archive_history=arc_history
        )
