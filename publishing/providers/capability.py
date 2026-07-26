"""
Publishing Provider Capabilities and Capability Registry.
"""

from enum import Enum
from typing import Set, Dict

class PublishingCapability(str, Enum):
    SCHEDULING = "SCHEDULING"
    ROLLBACK = "ROLLBACK"
    CAROUSEL = "CAROUSEL"
    VIDEO = "VIDEO"
    DRAFT = "DRAFT"
    ANALYTICS = "ANALYTICS"
    THREADING = "THREADING"

class CapabilityRegistry:
    CAPABILITIES = {
        "LinkedIn": {PublishingCapability.SCHEDULING, PublishingCapability.ROLLBACK, PublishingCapability.CAROUSEL, PublishingCapability.VIDEO},
        "X": {PublishingCapability.THREADING, PublishingCapability.ROLLBACK, PublishingCapability.SCHEDULING},
        "WordPress": {PublishingCapability.DRAFT, PublishingCapability.ROLLBACK, PublishingCapability.SCHEDULING},
        "Medium": {PublishingCapability.DRAFT, PublishingCapability.ROLLBACK},
        "Ghost": {PublishingCapability.DRAFT, PublishingCapability.ROLLBACK, PublishingCapability.SCHEDULING},
        "Dev.to": {PublishingCapability.DRAFT, PublishingCapability.ROLLBACK},
        "Hashnode": {PublishingCapability.DRAFT, PublishingCapability.ROLLBACK},
        "Webhook": {PublishingCapability.SCHEDULING}
    }

    @staticmethod
    def get_capabilities(channel_name: str) -> Set[PublishingCapability]:
        return CapabilityRegistry.CAPABILITIES.get(channel_name, {PublishingCapability.SCHEDULING})
