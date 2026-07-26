"""
Publication State Enumeration, Channel Enum, and Publication Data Model.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class PublicationState(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    SCHEDULED = "SCHEDULED"
    PUBLISHING = "PUBLISHING"
    PUBLISHED = "PUBLISHED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    ROLLED_BACK = "ROLLED_BACK"
    CANCELLED = "CANCELLED"

class Channel(str, Enum):
    LINKEDIN = "LinkedIn"
    X = "X"
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"
    WORDPRESS = "WordPress"
    MEDIUM = "Medium"
    GHOST = "Ghost"
    DEVTO = "Dev.to"
    HASHNODE = "Hashnode"
    WEBHOOK = "Webhook"

@dataclass
class Publication:
    publication_id: str
    campaign_id: str
    execution_id: str
    workspace_id: str
    channel: Channel
    scheduled_time: Optional[str] = None
    published_time: Optional[str] = None
    status: PublicationState = PublicationState.CREATED
    publication_url: str = ""
    provider_response: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    created_at: str = field(default_factory=_get_utc_now)
