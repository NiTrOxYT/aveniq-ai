"""
Metrics Persistence Store and Time-Series Snapshots Storage for Performance Analytics.
"""

import os
import json
from typing import Dict, Any, List, Optional
from analytics.models.campaign_metrics import CampaignMetrics

class MetricsStoreManager:
    def __init__(self, base_dir: str = "analytics/storage"):
        self.base_dir = base_dir
        self.metrics_dir = os.path.join(base_dir, "metrics")
        self.snapshots_dir = os.path.join(base_dir, "snapshots")
        
        for d in [self.metrics_dir, self.snapshots_dir]:
            os.makedirs(d, exist_ok=True)

    def save_metrics(self, metrics: CampaignMetrics) -> str:
        filepath = os.path.join(self.metrics_dir, f"met_{metrics.campaign_id}_{metrics.platform}.json")
        data = {
            "campaign_id": metrics.campaign_id,
            "execution_id": metrics.execution_id,
            "session_id": metrics.session_id,
            "publication_id": metrics.publication_id,
            "platform": metrics.platform,
            "publication_time": metrics.publication_time,
            "impressions": metrics.reach.impressions,
            "views": metrics.reach.views,
            "reactions": metrics.engagement.reactions,
            "likes": metrics.engagement.likes,
            "comments": metrics.engagement.comments,
            "shares": metrics.engagement.shares,
            "visits": metrics.website.visits,
            "cta_clicks": metrics.website.cta_clicks,
            "leads": metrics.business.leads,
            "signups": metrics.business.signups,
            "created_at": metrics.created_at
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return filepath

    def save_time_series_snapshot(self, timeframe: str, snapshot_data: Dict[str, Any]) -> str:
        filepath = os.path.join(self.snapshots_dir, f"snap_{timeframe}_{snapshot_data.get('date', '2026-07-26')}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(snapshot_data, f, indent=2)
        return filepath
