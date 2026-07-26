"""
Unified CampaignMetrics Data Models for Performance Analytics.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class ReachMetrics:
    impressions: int = 0
    views: int = 0
    unique_users: int = 0

@dataclass
class EngagementMetrics:
    reactions: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    reposts: int = 0

@dataclass
class WebsiteMetrics:
    visits: int = 0
    bounce_rate_pct: float = 0.0
    avg_session_duration_sec: float = 0.0
    cta_clicks: int = 0

@dataclass
class BusinessConversionMetrics:
    leads: int = 0
    signups: int = 0
    demo_requests: int = 0
    conversions: int = 0

@dataclass
class CampaignMetrics:
    campaign_id: str
    execution_id: str
    session_id: str
    publication_id: str
    platform: str
    publication_time: str
    reach: ReachMetrics = field(default_factory=ReachMetrics)
    engagement: EngagementMetrics = field(default_factory=EngagementMetrics)
    website: WebsiteMetrics = field(default_factory=WebsiteMetrics)
    business: BusinessConversionMetrics = field(default_factory=BusinessConversionMetrics)
    created_at: str = field(default_factory=_get_utc_now)
