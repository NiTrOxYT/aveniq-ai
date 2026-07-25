"""
Creative Storage Manager for AVENIQ Creative Department.
Persists media packages, AI prompts, storyboards, and version histories to disk storage.
"""

import os, json
from typing import Dict, Any, Optional
from creative.models.schema import MediaPackage
from brain.utils.logger import get_logger

logger = get_logger("aveniq.creative.storage")

class CreativeStorageManager:
    def __init__(self, base_dir: str = "creative/storage"):
        self.base_dir = base_dir
        self.packages_dir = os.path.join(base_dir, "packages")
        self.prompts_dir = os.path.join(base_dir, "prompts")
        self.storyboards_dir = os.path.join(base_dir, "storyboards")
        self.thumbnails_dir = os.path.join(base_dir, "thumbnails")
        self.assets_dir = os.path.join(base_dir, "assets")
        self.history_dir = os.path.join(base_dir, "history")
        self.versions_dir = os.path.join(base_dir, "versions")

        for d in [self.packages_dir, self.prompts_dir, self.storyboards_dir, self.thumbnails_dir, self.assets_dir, self.history_dir, self.versions_dir]:
            os.makedirs(d, exist_ok=True)

    def save_package(self, pkg: MediaPackage) -> str:
        filepath = os.path.join(self.packages_dir, f"{pkg.id}.json")
        data = {
            "id": pkg.id,
            "topic": pkg.topic,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "visual_theme": pkg.visual_theme,
            "overall_score": pkg.scores.overall_score,
            "version_info": {
                "version": pkg.version_info.version,
                "timestamp": pkg.version_info.timestamp,
                "director_id": pkg.version_info.director_id
            },
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": pkg.quality_gate.score,
                "checklist": pkg.quality_gate.checklist
            }
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save prompts separately for easy retrieval
        prompt_filepath = os.path.join(self.prompts_dir, f"prompts_{pkg.id}.json")
        prompt_data = {
            "midjourney": pkg.hero_brief.spec.prompts.midjourney_prompt,
            "dalle3": pkg.hero_brief.spec.prompts.dalle3_prompt,
            "flux": pkg.hero_brief.spec.prompts.flux_prompt,
            "sdxl_positive": pkg.hero_brief.spec.prompts.sdxl_positive_prompt,
            "sdxl_negative": pkg.hero_brief.spec.prompts.sdxl_negative_prompt,
            "sora": pkg.hero_brief.spec.prompts.sora_video_prompt,
            "runway": pkg.hero_brief.spec.prompts.runway_motion_prompt
        }
        with open(prompt_filepath, "w", encoding="utf-8") as f:
            json.dump(prompt_data, f, indent=2)

        # Save to version control storage
        version_filepath = os.path.join(self.versions_dir, f"v_{pkg.version_info.version}_{pkg.id}.json")
        with open(version_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save to historical memory
        hist_path = os.path.join(self.history_dir, f"history_{pkg.date}_{pkg.id}.json")
        with open(hist_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved media package to {filepath}")
        return filepath

    def get_latest_package(self) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.packages_dir) if f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.packages_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
