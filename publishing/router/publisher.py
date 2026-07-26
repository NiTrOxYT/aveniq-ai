"""
Master Publishing Router, Delivery Verifier, and Unpublish Rollback Manager.
"""

from typing import Dict, Any, List, Optional
from publishing.models.publication import Publication, PublicationState, Channel
from publishing.providers.linkedin import LinkedInProvider, XProvider, WordPressProvider
from publishing.adaptation.content_adapter import ContentAdapter
from publishing.providers.capability import CapabilityRegistry, PublishingCapability

class DeliveryVerifier:
    @staticmethod
    def verify_delivery(publication: Publication) -> bool:
        if publication.status == PublicationState.PUBLISHED and publication.publication_url:
            publication.status = PublicationState.VERIFIED
            return True
        return False

class RollbackManager:
    def __init__(self):
        self.rollback_history: List[Dict[str, Any]] = []

    def rollback_publication(self, publication: Publication, provider_instance: Any) -> bool:
        caps = CapabilityRegistry.get_capabilities(publication.channel.value)
        if PublishingCapability.ROLLBACK not in caps:
            return False

        ok = provider_instance.unpublish(publication.publication_id)
        if ok:
            publication.status = PublicationState.ROLLED_BACK
            self.rollback_history.append({
                "publication_id": publication.publication_id,
                "channel": publication.channel.value,
                "action": "ROLLED_BACK",
                "timestamp": "2026-07-26T13:00:00Z"
            })
            return True
        return False

class MasterPublisher:
    def __init__(self):
        self.providers = {
            Channel.LINKEDIN: LinkedInProvider(),
            Channel.X: XProvider(),
            Channel.WORDPRESS: WordPressProvider()
        }
        self.verifier = DeliveryVerifier()
        self.rollback_mgr = RollbackManager()

    def publish_campaign(self, campaign_id: str, channel: Channel, delivery_payload: Dict[str, Any]) -> Publication:
        pub_id = f"pub_{campaign_id}_{channel.value.lower()}"
        pub = Publication(
            publication_id=pub_id,
            campaign_id=campaign_id,
            execution_id=f"exec_{campaign_id}",
            workspace_id="ws_001",
            channel=channel
        )

        # 1. Adapt Content
        adapted = ContentAdapter.adapt_for_channel(channel.value, delivery_payload)

        # 2. Get Provider & Publish
        provider = self.providers.get(channel, self.providers[Channel.LINKEDIN])
        pub.status = PublicationState.PUBLISHING
        pub = provider.publish(pub, adapted)

        # 3. Verify Delivery
        self.verifier.verify_delivery(pub)

        return pub
