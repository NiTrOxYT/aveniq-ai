"""
Growth Storage Manager for AVENIQ Brand Growth Intelligence.
Persists growth packages, portfolios, forecasts, and version histories to disk storage.
"""

import os, json
from typing import Dict, Any, Optional
from growth.models.schema import GrowthPackage
from brain.utils.logger import get_logger

logger = get_logger("aveniq.growth.storage")

class GrowthStorageManager:
    def __init__(self, base_dir: str = "growth/storage"):
        self.base_dir = base_dir
        self.growth_dir = os.path.join(base_dir, "growth")
        self.portfolios_dir = os.path.join(base_dir, "portfolios")
        self.history_dir = os.path.join(base_dir, "history")
        self.versions_dir = os.path.join(base_dir, "versions")

        for d in [self.growth_dir, self.portfolios_dir, self.history_dir, self.versions_dir]:
            os.makedirs(d, exist_ok=True)

    def save_package(self, pkg: GrowthPackage) -> str:
        filepath = os.path.join(self.growth_dir, f"{pkg.id}.json")
        data = {
            "id": pkg.id,
            "date": pkg.date,
            "executive_summary": pkg.executive_summary,
            "goals_count": len(pkg.goals),
            "portfolio_count": len(pkg.portfolio),
            "projected_leads": pkg.kpi_forecast.expected_leads,
            "overall_growth_score": pkg.metrics.overall_growth_score,
            "version": pkg.version,
            "quality_gate": {
                "passed": pkg.quality_gate.passed,
                "score": pkg.quality_gate.score,
                "checklist": pkg.quality_gate.checklist
            }
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save portfolio items separately
        port_file = os.path.join(self.portfolios_dir, f"portfolio_{pkg.id}.json")
        port_data = [
            {
                "id": p.portfolio_id,
                "name": p.campaign_name,
                "type": p.campaign_type,
                "funnel_stage": p.funnel_stage,
                "kpi": p.target_kpi,
                "weight_pct": p.allocated_weight_pct
            } for p in pkg.portfolio
        ]
        with open(port_file, "w", encoding="utf-8") as f:
            json.dump(port_data, f, indent=2)

        # Save to version control storage
        version_filepath = os.path.join(self.versions_dir, f"v_{pkg.version}_{pkg.id}.json")
        with open(version_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Save to historical memory
        hist_path = os.path.join(self.history_dir, f"history_{pkg.date}_{pkg.id}.json")
        with open(hist_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved growth package to {filepath}")
        return filepath

    def get_latest_package(self) -> Optional[Dict[str, Any]]:
        files = sorted([f for f in os.listdir(self.growth_dir) if f.endswith(".json")])
        if not files:
            return None
        with open(os.path.join(self.growth_dir, files[-1]), "r", encoding="utf-8") as f:
            return json.load(f)
