"""
Comprehensive Publishing Test Suite for AVENIQ Publishing & Distribution Platform.
Tests Publication models, State Machine, ContentAdapter, MasterPublisher, DeliveryVerifier, RollbackManager, and Queue.
"""

import unittest
from publishing.models.publication import Publication, PublicationState, Channel
from publishing.adaptation.content_adapter import ContentAdapter
from publishing.providers.capability import CapabilityRegistry, PublishingCapability
from publishing.router.publisher import MasterPublisher, DeliveryVerifier, RollbackManager
from publishing.providers.linkedin import LinkedInProvider
from publishing.queue.publishing_queue import PublishingQueue

class TestPublishingPlatform(unittest.TestCase):
    def test_content_adapter(self):
        text = "A" * 600
        x_payload = ContentAdapter.adapt_for_channel("X", {"text": text})
        self.assertEqual(x_payload["format"], "thread")
        self.assertGreater(len(x_payload["tweets"]), 1)

        li_payload = ContentAdapter.adapt_for_channel("LinkedIn", {"text": "Briefing text"})
        self.assertEqual(li_payload["format"], "longform")
        self.assertIn("#EnterpriseAI", li_payload["text"])

    def test_capability_registry(self):
        caps = CapabilityRegistry.get_capabilities("LinkedIn")
        self.assertIn(PublishingCapability.ROLLBACK, caps)
        self.assertIn(PublishingCapability.CAROUSEL, caps)

    def test_master_publisher_and_verification(self):
        publisher = MasterPublisher()
        pub = publisher.publish_campaign("cmp_001", Channel.LINKEDIN, {"text": "AI Briefing"})
        self.assertEqual(pub.status, PublicationState.VERIFIED)
        self.assertTrue(pub.publication_url.startswith("https://linkedin.com"))

    def test_rollback_manager(self):
        pub = Publication("pub_001", "cmp_001", "exec_001", "ws_001", Channel.LINKEDIN, status=PublicationState.PUBLISHED)
        provider = LinkedInProvider()
        rollback_mgr = RollbackManager()

        ok = rollback_mgr.rollback_publication(pub, provider)
        self.assertTrue(ok)
        self.assertEqual(pub.status, PublicationState.ROLLED_BACK)

    def test_publishing_queue(self):
        queue = PublishingQueue()
        pub = Publication("pub_001", "cmp_001", "exec_001", "ws_001", Channel.LINKEDIN)
        queue.enqueue(pub, {"text": "Hello"})
        self.assertEqual(len(queue.queue), 1)

        publisher = MasterPublisher()
        processed = queue.process(publisher.publish_campaign)
        self.assertEqual(processed, 1)
        self.assertEqual(len(queue.queue), 0)

if __name__ == "__main__":
    unittest.main()
