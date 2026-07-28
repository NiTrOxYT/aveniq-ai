import pytest
import os
import json
import uuid
from datetime import datetime, timezone, timedelta
from automation.storage.schedule_store import ScheduleStore, global_schedule_store
from apps.dashboard.api import DashboardServerHandler

class MockHTTPHandler:
    def __init__(self, path):
        self.path = path
        self.status_code = None
        self.json_data = None
        
    def _send_json(self, status, payload):
        self.status_code = status
        self.json_data = payload

def test_compute_next_executions_triggers():
    store = ScheduleStore()
    base = datetime(2026, 7, 28, 10, 0, 0, tzinfo=timezone.utc)  # Tuesday 10:00

    # Hourly
    h_runs = store.compute_next_executions("hourly", time_str="10:00", count=2, base_time=base)
    assert len(h_runs) == 2
    assert "2026-07-28T11:00:00" in h_runs[0]

    # Daily
    d_runs = store.compute_next_executions("daily", time_str="08:00", count=2, base_time=base)
    assert len(d_runs) == 2
    assert "2026-07-29T08:00:00" in d_runs[0]

    # Weekdays only (Base is Tue Jul 28 -> Next weekday Wed Jul 29)
    w_runs = store.compute_next_executions("weekdays_only", time_str="08:00", count=2, base_time=base)
    assert "2026-07-29T08:00:00" in w_runs[0]

    # Weekly (Mon 9:00 cron -> Next Monday Aug 3)
    wk_runs = store.compute_next_executions("weekly", time_str="09:00", cron_str="0 9 * * 1", count=2, base_time=base)
    assert "2026-08-03T09:00:00" in wk_runs[0]

    # Monthly
    m_runs = store.compute_next_executions("monthly", time_str="08:00", count=2, base_time=base)
    assert len(m_runs) == 2
    assert datetime.fromisoformat(m_runs[0]) > base

def test_getter_purity(tmp_path):
    s_dir = tmp_path / "schedules"
    h_dir = tmp_path / "history"
    s_dir.mkdir()
    h_dir.mkdir()

    store = ScheduleStore(schedules_dir=str(s_dir), history_dir=str(h_dir))
    sch = store.create_schedule({
        "name": "Test Purity Schedule",
        "trigger": "daily",
        "time": "08:00",
        "prompt": "Test prompt"
    })

    filepath = s_dir / f"{sch['id']}.json"
    mtime_before = filepath.stat().st_mtime

    # Call get_schedule & list_schedules multiple times
    store.get_schedule(sch['id'])
    store.list_schedules()

    mtime_after = filepath.stat().st_mtime
    assert mtime_before == mtime_after, "Getter functions must be pure and not write to disk"

def test_startup_schedule_repair(tmp_path):
    s_dir = tmp_path / "schedules"
    h_dir = tmp_path / "history"
    s_dir.mkdir()
    h_dir.mkdir()

    store = ScheduleStore(schedules_dir=str(s_dir), history_dir=str(h_dir))
    sch_id = str(uuid.uuid4())
    past_iso = "2026-01-01T00:00:00+00:00"
    
    stale_data = {
        "id": sch_id,
        "name": "Stale Schedule",
        "trigger": "weekly",
        "time": "09:00",
        "cron": "0 9 * * 1",
        "enabled": True,
        "state": "active",
        "next_run": past_iso
    }
    with open(s_dir / f"{sch_id}.json", "w") as f:
        json.dump(stale_data, f)

    repaired = store.repair_stale_schedules()
    assert len(repaired) == 1
    assert repaired[0]["next_run"] > past_iso

def test_dashboard_api_contracts():
    handler = MockHTTPHandler("/dashboard/overview")
    DashboardServerHandler.do_GET(handler)
    assert handler.status_code == 200
    assert "active_campaigns" in handler.json_data
    assert "overall_score" in handler.json_data

    handler = MockHTTPHandler("/dashboard/activity")
    DashboardServerHandler.do_GET(handler)
    assert handler.status_code == 200
    assert "activity_timeline" in handler.json_data
    assert isinstance(handler.json_data["activity_timeline"], list)

    handler = MockHTTPHandler("/dashboard/reasoning")
    DashboardServerHandler.do_GET(handler)
    assert handler.status_code == 200
    assert "topic" in handler.json_data
    assert "opportunity_selection_reasoning" in handler.json_data
    assert "expected_business_impact" in handler.json_data

    handler = MockHTTPHandler("/api/automation/schedules")
    DashboardServerHandler.do_GET(handler)
    assert handler.status_code == 200
    assert "schedules" in handler.json_data
