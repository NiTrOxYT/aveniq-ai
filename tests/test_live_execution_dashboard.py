"""
Unit test suite for Live Workflow Execution Monitoring Dashboard endpoints in apps/dashboard/api.py.
Validates GET /api/workflows/<execution_id>, GET /api/automation/runtime/stream, and GET /api/automation/runtime/graph.
"""

import json
import urllib.request
import threading
from http.server import HTTPServer
from apps.dashboard.api import DashboardServerHandler
from automation.storage.schedule_store import global_schedule_store
from automation.execution.scheduler import global_automation_scheduler
from automation.engine.checkpoint_store import global_checkpoint_store

def test_workflow_execution_monitoring_api():
    server = HTTPServer(('127.0.0.1', 8101), DashboardServerHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    try:
        # Create a test schedule & run execution
        sch = global_schedule_store.create_schedule({
            "name": "Live Execution Test Schedule",
            "department": "Creative",
            "workflow_id": "marketing_daily",
            "trigger": "daily"
        })

        run_res = global_automation_scheduler.execute_job_now(sch["id"], trigger_type="manual")
        exec_id = run_res["execution_id"]

        # 1. Test GET /api/workflows/<execution_id>
        url_exec = f"http://127.0.0.1:8101/api/workflows/{exec_id}"
        req_exec = urllib.request.urlopen(url_exec)
        res_exec = json.loads(req_exec.read().decode('utf-8'))

        assert res_exec["execution_id"] == exec_id
        assert res_exec["workflow_id"] == "marketing_daily"
        assert len(res_exec["completed_nodes"]) >= 16
        assert "research" in res_exec["completed_nodes"]
        assert "telegram" in res_exec["completed_nodes"]
        assert len(res_exec["nodes"]) == 17

        # 2. Test GET /api/automation/runtime/graph
        url_graph = "http://127.0.0.1:8101/api/automation/runtime/graph"
        req_graph = urllib.request.urlopen(url_graph)
        res_graph = json.loads(req_graph.read().decode('utf-8'))

        assert res_graph["workflow_id"] == "marketing_daily"
        assert len(res_graph["nodes"]) == 17
        assert res_graph["critical_path"] == ["research", "blog", "quality", "telegram"]

        # 3. Test GET /api/automation/runtime/stream (SSE stream)
        url_stream = "http://127.0.0.1:8101/api/automation/runtime/stream"
        req_stream = urllib.request.urlopen(url_stream)
        stream_chunk = req_stream.readline().decode('utf-8')
        req_stream.close()
        assert "data:" in stream_chunk

        # 4. Test GET /api/automation/history
        url_hist = "http://127.0.0.1:8101/api/automation/history"
        req_hist = urllib.request.urlopen(url_hist)
        res_hist = json.loads(req_hist.read().decode('utf-8'))
        assert "history" in res_hist
        assert res_hist["total"] >= 1

        # 5. Test GET /api/workflows/<execution_id>/details (Execution Observability Center)
        url_det = f"http://127.0.0.1:8101/api/workflows/{exec_id}/details"
        req_det = urllib.request.urlopen(url_det)
        res_det = json.loads(req_det.read().decode('utf-8'))

        assert res_det["summary"]["execution_id"] == exec_id
        assert len(res_det["execution_story"]) >= 5
        assert res_det["telegram_report"]["bot_name"] == "@AveniqAIBot"
        assert res_det["performance_analytics"]["completed_nodes"] >= 16

        # 6. Test GET /api/workflows/<execution_id>/export (JSON Audit Package)
        url_exp = f"http://127.0.0.1:8101/api/workflows/{exec_id}/export"
        req_exp = urllib.request.urlopen(url_exp)
        res_exp = json.loads(req_exp.read().decode('utf-8'))
        assert res_exp["summary"]["execution_id"] == exec_id

        global_schedule_store.delete_schedule(sch["id"])
    finally:
        server.shutdown()
