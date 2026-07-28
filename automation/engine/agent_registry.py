"""
Central Agent Registry for AVENIQ AI v2 Native Workflow Engine.
Provides auto-registration, plugin extension, and dynamic worker resolution.
"""

import logging
from typing import Dict, Any, Callable, Optional, List

logger = logging.getLogger("AgentRegistry")

class AgentRegistry:
    _agents: Dict[str, Callable] = {}
    _metadata: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register(cls, name: str, agent_fn_or_class: Any, capabilities: Optional[List[str]] = None):
        clean_name = name.strip().lower()
        cls._agents[clean_name] = agent_fn_or_class
        cls._metadata[clean_name] = {
            "name": name,
            "capabilities": capabilities or [],
            "class_name": getattr(agent_fn_or_class, "__name__", str(agent_fn_or_class))
        }
        logger.debug(f"[AgentRegistry] Registered agent '{clean_name}' -> {agent_fn_or_class}")

    @classmethod
    def get(cls, name: str) -> Optional[Any]:
        clean_name = name.strip().lower()
        if clean_name in cls._agents:
            return cls._agents[clean_name]
        # Fallback aliases
        aliases = {
            "research": "researchworker",
            "trend_research": "researchworker",
            "competitor_intelligence": "strategyworker",
            "seo": "plannerworker",
            "content_planner": "plannerworker",
            "blog_writer": "campaignworker",
            "linkedin_writer": "campaignworker",
            "instagram_writer": "creativeadapter",
            "facebook_writer": "campaignworker",
            "x_writer": "campaignworker",
            "hashtag_generator": "campaignworker",
            "cta_generator": "campaignworker",
            "image_generator": "creativeadapter",
            "carousel_generator": "creativeadapter",
            "quality_checker": "approvalworker",
            "supabase_store": "deliveryadapter",
            "telegram_bot": "publishingworker"
        }
        target = aliases.get(clean_name)
        if target and target in cls._agents:
            return cls._agents[target]
        return None

    @classmethod
    def list_agents(cls) -> List[Dict[str, Any]]:
        return list(cls._metadata.values())

def register_agent(name: str, capabilities: Optional[List[str]] = None):
    def decorator(cls_or_fn):
        AgentRegistry.register(name, cls_or_fn, capabilities)
        return cls_or_fn
    return decorator

# Register existing workers & department adapters by default
def _register_builtin_agents():
    try:
        from ai_workers.research_worker import ResearchWorker
        AgentRegistry.register("ResearchWorker", ResearchWorker, ["research", "trend_analysis"])
        AgentRegistry.register("researchworker", ResearchWorker)
    except Exception:
        pass

    try:
        from ai_workers.strategy_worker import StrategyWorker
        AgentRegistry.register("StrategyWorker", StrategyWorker, ["strategy", "competitors"])
        AgentRegistry.register("strategyworker", StrategyWorker)
    except Exception:
        pass

    try:
        from ai_workers.planner_worker import PlannerWorker
        AgentRegistry.register("PlannerWorker", PlannerWorker, ["planning", "seo"])
        AgentRegistry.register("plannerworker", PlannerWorker)
    except Exception:
        pass

    try:
        from ai_workers.campaign_worker import CampaignWorker
        AgentRegistry.register("CampaignWorker", CampaignWorker, ["campaign", "copywriting"])
        AgentRegistry.register("campaignworker", CampaignWorker)
    except Exception:
        pass

    try:
        from ai_workers.approval_worker import ApprovalWorker
        AgentRegistry.register("ApprovalWorker", ApprovalWorker, ["quality", "approval"])
        AgentRegistry.register("approvalworker", ApprovalWorker)
    except Exception:
        pass

    try:
        from ai_workers.publishing_worker import PublishingWorker
        AgentRegistry.register("PublishingWorker", PublishingWorker, ["publishing", "telegram"])
        AgentRegistry.register("publishingworker", PublishingWorker)
    except Exception:
        pass

    try:
        from ai_workers.regenerate_worker import RegenerateWorker
        AgentRegistry.register("RegenerateWorker", RegenerateWorker, ["regeneration", "refinement"])
        AgentRegistry.register("regenerateworker", RegenerateWorker)
        AgentRegistry.register("regenerate", RegenerateWorker)
    except Exception:
        pass

    try:
        from workflow.adapters.base import ADAPTER_REGISTRY
        for key, adapter in ADAPTER_REGISTRY.items():
            AgentRegistry.register(f"{key}adapter", adapter, [key])
    except Exception:
        pass

_register_builtin_agents()
