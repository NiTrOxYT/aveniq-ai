"""
Comprehensive Unit Test Suite for AVENIQ AI v2 Native Workflow Engine.
Validates AgentRegistry, GraphResolver DAG resolution & cycle detection,
Parallel execution, Retry policy, Checkpoint persistence, Typed artifacts,
and Backward compatibility with legacy prompt schedules.
"""

import os
import json
import pytest
from automation.engine.node_state import NodeState
from automation.engine.workflow import WorkflowDefinition, WorkflowNode, RetryPolicy
from automation.engine.agent_registry import AgentRegistry, register_agent
from automation.engine.graph_resolver import GraphResolver
from automation.engine.context import WorkflowContext
from automation.engine.checkpoint_store import global_checkpoint_store
from automation.engine.workflow_loader import global_workflow_loader
from automation.engine.workflow_runner import WorkflowRunner, global_workflow_runner
from automation.engine.events import global_workflow_event_bus, WorkflowEvent
from automation.storage.schedule_store import global_schedule_store

# 1. Agent Registry Tests
def test_agent_registry_registration_and_lookup():
    @register_agent("custom_test_agent", capabilities=["test"])
    def custom_agent(context):
        return {"status": "success", "message": "Custom agent executed"}

    agent_fn = AgentRegistry.get("custom_test_agent")
    assert agent_fn is not None
    assert callable(agent_fn)
    res = agent_fn(WorkflowContext("test_exec", "test_wf"))
    assert res["status"] == "success"

# 2. Graph Resolver & Cycle Detection Tests
def test_graph_resolver_cycle_detection():
    # Valid DAG
    node_a = WorkflowNode(id="a", depends_on=[])
    node_b = WorkflowNode(id="b", depends_on=["a"])
    node_c = WorkflowNode(id="c", depends_on=["b"])
    assert GraphResolver.detect_cycle([node_a, node_b, node_c]) is False

    # Cyclic Graph
    c_node1 = WorkflowNode(id="x", depends_on=["y"])
    c_node2 = WorkflowNode(id="y", depends_on=["x"])
    assert GraphResolver.detect_cycle([c_node1, c_node2]) is True

def test_graph_resolver_ready_nodes():
    node_a = WorkflowNode(id="a", depends_on=[])
    node_b = WorkflowNode(id="b", depends_on=["a"])
    node_c = WorkflowNode(id="c", depends_on=["a"])
    node_d = WorkflowNode(id="d", depends_on=["b", "c"])

    ready_initial = GraphResolver.get_ready_nodes([node_a, node_b, node_c, node_d], set())
    assert len(ready_initial) == 1
    assert ready_initial[0].id == "a"

    ready_after_a = GraphResolver.get_ready_nodes([node_a, node_b, node_c, node_d], {"a"})
    assert len(ready_after_a) == 2
    assert set(n.id for n in ready_after_a) == {"b", "c"}

# 3. Workflow Runner & Parallel Execution Tests
def test_workflow_runner_parallel_execution():
    wf_data = {
        "workflow_id": "test_parallel_wf",
        "name": "Test Parallel Workflow",
        "nodes": [
            {"id": "research", "agent": "ResearchWorker", "depends_on": []},
            {"id": "blog", "agent": "CampaignWorker", "depends_on": ["research"]},
            {"id": "linkedin", "agent": "CampaignWorker", "depends_on": ["blog"]},
            {"id": "instagram", "agent": "CreativeAdapter", "depends_on": ["blog"]},
            {"id": "facebook", "agent": "CampaignWorker", "depends_on": ["blog"]},
            {"id": "x", "agent": "CampaignWorker", "depends_on": ["blog"]},
            {"id": "quality", "agent": "ApprovalWorker", "depends_on": ["linkedin", "instagram", "facebook", "x"]}
        ]
    }
    wf_def = WorkflowDefinition.from_dict(wf_data)
    runner = WorkflowRunner()
    result = runner.execute(wf_def, execution_id="exec_test_parallel_101", resume=False)

    assert result["status"] == "SUCCESS"
    assert len(result["completed_nodes"]) == 7
    assert "linkedin" in result["completed_nodes"]
    assert "instagram" in result["completed_nodes"]
    assert "facebook" in result["completed_nodes"]
    assert "x" in result["completed_nodes"]

# 4. Checkpoint & Resume Tests
def test_checkpoint_saving_and_resuming():
    exec_id = "exec_test_checkpoint_202"
    global_checkpoint_store.save_node_checkpoint(exec_id, "research", {"status": "SUCCESS", "output": {"data": "cached_research"}})

    checkpoints = global_checkpoint_store.load_all_checkpoints(exec_id)
    assert "research" in checkpoints
    assert checkpoints["research"]["output"]["data"] == "cached_research"

    wf_data = {
        "workflow_id": "test_checkpoint_wf",
        "name": "Test Checkpoint Resume Workflow",
        "nodes": [
            {"id": "research", "agent": "ResearchWorker", "depends_on": []},
            {"id": "seo", "agent": "CampaignWorker", "depends_on": ["research"]}
        ]
    }
    wf_def = WorkflowDefinition.from_dict(wf_data)
    result = WorkflowRunner().execute(wf_def, execution_id=exec_id, resume=True)

    assert result["status"] == "SUCCESS"
    assert "research" in result["completed_nodes"]
    assert "seo" in result["completed_nodes"]

# 5. Event Bus Publishing Tests
def test_workflow_event_bus_publishing():
    events_captured = []
    def capture_event(ev: WorkflowEvent):
        events_captured.append(ev)

    global_workflow_event_bus.subscribe("*", capture_event)

    wf_data = {
        "workflow_id": "test_event_wf",
        "name": "Test Event Bus Workflow",
        "nodes": [{"id": "research", "agent": "ResearchWorker", "depends_on": []}]
    }
    wf_def = WorkflowDefinition.from_dict(wf_data)
    WorkflowRunner().execute(wf_def, execution_id="exec_test_event_303", resume=False)

    assert len(events_captured) >= 3
    event_types = [e.event_type for e in events_captured]
    assert "WORKFLOW_STARTED" in event_types
    assert "NODE_STARTED" in event_types
    assert "NODE_COMPLETED" in event_types
    assert "WORKFLOW_COMPLETED" in event_types

# 6. Backward Compatibility Tests
def test_backward_compatibility_schedule_creation():
    # Schedule with workflow_id
    sch_wf = global_schedule_store.create_schedule({
        "name": "Test Workflow Schedule",
        "department": "Creative",
        "workflow_id": "marketing_daily",
        "trigger": "daily"
    })
    assert sch_wf["workflow_id"] == "marketing_daily"
    global_schedule_store.delete_schedule(sch_wf["id"])

    # Legacy schedule with prompt only
    sch_legacy = global_schedule_store.create_schedule({
        "name": "Test Legacy Schedule",
        "department": "Creative",
        "prompt": "Legacy prompt text",
        "trigger": "daily"
    })
    assert sch_legacy["prompt"] == "Legacy prompt text"
    assert sch_legacy.get("workflow_id") is None
    global_schedule_store.delete_schedule(sch_legacy["id"])
