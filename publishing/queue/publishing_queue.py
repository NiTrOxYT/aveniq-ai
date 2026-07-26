"""
Async Publishing Queue with Dead-Letter Queue (DLQ) & Publication History Store.
"""

import os
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from publishing.models.publication import Publication, PublicationState

@dataclass
class QueueItem:
    publication: Publication
    payload: Dict[str, Any]
    priority: int = 1
    attempts: int = 0
    status: str = "QUEUED"

class PublishingQueue:
    def __init__(self):
        self.queue: List[QueueItem] = []
        self.dead_letter_queue: List[QueueItem] = []

    def enqueue(self, publication: Publication, payload: Dict[str, Any], priority: int = 1):
        item = QueueItem(publication=publication, payload=payload, priority=priority)
        self.queue.append(item)
        self.queue.sort(key=lambda x: x.priority)

    def process(self, publisher_func) -> int:
        processed = 0
        while self.queue:
            item = self.queue.pop(0)
            item.attempts += 1
            try:
                pub = publisher_func(item.publication.campaign_id, item.publication.channel, item.payload)
                if pub.status in [PublicationState.PUBLISHED, PublicationState.VERIFIED]:
                    item.status = "SUCCESS"
                    processed += 1
                else:
                    item.status = "FAILED"
                    self.dead_letter_queue.append(item)
            except Exception as e:
                item.status = "FAILED"
                self.dead_letter_queue.append(item)
        return processed

class PublicationStore:
    def __init__(self, storage_dir: str = "publishing/storage/publications"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_publication(self, pub: Publication) -> str:
        filepath = os.path.join(self.storage_dir, f"{pub.publication_id}.json")
        data = {
            "publication_id": pub.publication_id,
            "campaign_id": pub.campaign_id,
            "execution_id": pub.execution_id,
            "workspace_id": pub.workspace_id,
            "channel": pub.channel.value,
            "status": pub.status.value,
            "publication_url": pub.publication_url,
            "provider_response": pub.provider_response,
            "published_time": pub.published_time,
            "created_at": pub.created_at
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return filepath
