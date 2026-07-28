"""
Versioned Workflow JSON Loader for AVENIQ AI v2 Native Workflow Engine.
Loads workflow schemas from automation/workflows/<workflow_id>/v<version>.json or automation/workflows/<workflow_id>.json.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from automation.engine.workflow import WorkflowDefinition

logger = logging.getLogger("WorkflowLoader")

class WorkflowLoader:
    def __init__(self, base_dir: str = "automation/workflows"):
        self.base_dir = base_dir

    def load_workflow(self, workflow_id: str, version: Optional[str] = None) -> WorkflowDefinition:
        clean_id = workflow_id.strip()
        filepaths_to_check = []

        if version:
            v_str = f"v{version}" if not str(version).startswith("v") else str(version)
            filepaths_to_check.append(os.path.join(self.base_dir, clean_id, f"{v_str}.json"))
            filepaths_to_check.append(os.path.join(self.base_dir, f"{clean_id}_{v_str}.json"))

        filepaths_to_check.append(os.path.join(self.base_dir, clean_id, "workflow.json"))
        filepaths_to_check.append(os.path.join(self.base_dir, clean_id, "v1.json"))
        filepaths_to_check.append(os.path.join(self.base_dir, f"{clean_id}.json"))

        for path in filepaths_to_check:
            if os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    logger.debug(f"[WorkflowLoader] Loaded workflow '{clean_id}' from '{path}'")
                    return WorkflowDefinition.from_dict(data)
                except Exception as e:
                    logger.error(f"[WorkflowLoader] Failed reading '{path}': {e}")
                    raise

        # If file not found, generate default 17-node DAG workflow definition dynamically
        return self.create_default_marketing_workflow(clean_id)

    def list_workflows(self) -> List[Dict[str, Any]]:
        workflows = []
        if not os.path.isdir(self.base_dir):
            return workflows

        try:
            for item in os.listdir(self.base_dir):
                item_path = os.path.join(self.base_dir, item)
                if os.path.isdir(item_path):
                    for vfile in os.listdir(item_path):
                        if vfile.endswith(".json"):
                            try:
                                with open(os.path.join(item_path, vfile), "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                workflows.append({
                                    "id": data.get("workflow_id") or data.get("id") or item,
                                    "name": data.get("name") or item,
                                    "version": data.get("version") or "1.0.0",
                                    "nodes_count": len(data.get("nodes") or data.get("graph") or []),
                                    "file": os.path.join(item, vfile)
                                })
                            except Exception:
                                pass
                elif item.endswith(".json"):
                    try:
                        with open(item_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        workflows.append({
                            "id": data.get("workflow_id") or data.get("id") or item[:-5],
                            "name": data.get("name") or item[:-5],
                            "version": data.get("version") or "1.0.0",
                            "nodes_count": len(data.get("nodes") or data.get("graph") or []),
                            "file": item
                        })
                    except Exception:
                        pass
        except Exception as e:
            logger.warning(f"[WorkflowLoader] List workflows error: {e}")

        return workflows

    def create_default_marketing_workflow(self, workflow_id: str) -> WorkflowDefinition:
        data = {
            "workflow_id": workflow_id,
            "name": "Daily Autonomous Marketing & Multi-Channel Content Engine",
            "version": "2.0.0",
            "trigger": {"cron": "0 9 * * *", "timezone": "Asia/Kolkata"},
            "outputs": ["telegram", "dashboard", "file"],
            "nodes": [
                {"id": "research", "type": "agent", "agent": "ResearchWorker", "depends_on": []},
                {"id": "competitors", "type": "agent", "agent": "StrategyWorker", "depends_on": ["research"]},
                {"id": "seo", "type": "agent", "agent": "CampaignWorker", "depends_on": ["research"]},
                {"id": "plan", "type": "agent", "agent": "CampaignWorker", "depends_on": ["competitors", "seo"]},
                {"id": "blog", "type": "agent", "agent": "CampaignWorker", "depends_on": ["plan"]},
                {"id": "linkedin", "type": "agent", "agent": "CampaignWorker", "depends_on": ["blog"]},
                {"id": "instagram", "type": "agent", "agent": "CreativeAdapter", "depends_on": ["blog"]},
                {"id": "facebook", "type": "agent", "agent": "CampaignWorker", "depends_on": ["blog"]},
                {"id": "x", "type": "agent", "agent": "CampaignWorker", "depends_on": ["blog"]},
                {"id": "hashtags", "type": "agent", "agent": "CampaignWorker", "depends_on": ["linkedin", "instagram", "facebook", "x"]},
                {"id": "cta", "type": "agent", "agent": "CampaignWorker", "depends_on": ["linkedin", "instagram", "facebook", "x"]},
                {"id": "creative", "type": "agent", "agent": "CreativeAdapter", "depends_on": ["hashtags", "cta"]},
                {"id": "carousel", "type": "agent", "agent": "CreativeAdapter", "depends_on": ["creative"]},
                {"id": "quality", "type": "agent", "agent": "ApprovalWorker", "depends_on": ["creative", "carousel"], "condition": "quality_score >= 90"},
                {"id": "supabase", "type": "agent", "agent": "DeliveryAdapter", "depends_on": ["quality"]},
                {"id": "telegram", "type": "agent", "agent": "PublishingWorker", "depends_on": ["supabase"]}
            ]
        }
        return WorkflowDefinition.from_dict(data)

global_workflow_loader = WorkflowLoader()
