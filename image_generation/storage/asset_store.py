"""
Asset Library Store with Versioning, Regeneration, and Human Approval Feedback Tags.
"""

from typing import Dict, Any, List, Optional
from image_generation.models.asset import VisualAsset, AssetApprovalStatus

class AssetLibraryStore:
    def __init__(self):
        self._assets: Dict[str, VisualAsset] = {}
        self._version_history: Dict[str, List[VisualAsset]] = {}

    def save_asset(self, asset: VisualAsset) -> VisualAsset:
        self._assets[asset.asset_id] = asset

        if asset.asset_id not in self._version_history:
            self._version_history[asset.asset_id] = []
        self._version_history[asset.asset_id].append(asset)
        return asset

    def get_asset(self, asset_id: str) -> Optional[VisualAsset]:
        return self._assets.get(asset_id)

    def list_assets(self, campaign_id: str = None) -> List[VisualAsset]:
        assets = list(self._assets.values())
        if campaign_id:
            assets = [a for a in assets if a.campaign_id == campaign_id]
        return assets

    def update_feedback(self, asset_id: str, feedback_tag: str, approval_status: AssetApprovalStatus = AssetApprovalStatus.REGENERATING) -> Optional[VisualAsset]:
        asset = self.get_asset(asset_id)
        if asset:
            asset.feedback_tag = feedback_tag
            asset.approval_status = approval_status
            asset.version += 1
            self.save_asset(asset)
        return asset

global_asset_store = AssetLibraryStore()
