"""
Master Graph Execution Engine & Workflow Runner for AVENIQ AI v2.
Coordinates parallel DAG node execution, node state machine transitions, retries,
checkpoint persistence, typed artifacts, and execution event bus publishing.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Set
from datetime import datetime, timezone

from automation.engine.workflow import WorkflowDefinition, WorkflowNode, RetryPolicy
from automation.engine.node_state import NodeState
from automation.engine.context import WorkflowContext
from automation.engine.agent_registry import AgentRegistry
from automation.engine.executor import ThreadExecutor, BaseExecutor
from automation.engine.graph_resolver import GraphResolver
from automation.engine.checkpoint_store import global_checkpoint_store
from automation.engine.workflow_history import global_workflow_history_store
from automation.engine.events import (
    global_workflow_event_bus, WorkflowStarted, WorkflowCompleted, WorkflowFailed,
    NodeStarted, NodeCompleted, NodeFailed, NodeRetry, CheckpointSaved
)

logger = logging.getLogger("WorkflowRunner")

def _get_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class WorkflowRunner:
    def __init__(self, executor: Optional[BaseExecutor] = None):
        self.executor = executor or ThreadExecutor(max_workers=4)

    def execute(
        self,
        workflow_def: WorkflowDefinition,
        execution_id: Optional[str] = None,
        schedule_id: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        resume: bool = True
    ) -> Dict[str, Any]:
        start_ts = time.time()
        exec_id = execution_id or f"exec_wf_{int(start_ts)}_{abs(hash(workflow_def.workflow_id))%1000:03d}"
        context = WorkflowContext(exec_id, workflow_def.workflow_id, variables or workflow_def.variables)

        # Check cycle in graph
        if GraphResolver.detect_cycle(workflow_def.nodes):
            raise ValueError(f"Cycle detected in workflow graph for '{workflow_def.workflow_id}'")

        # Load existing checkpoints if resuming
        checkpoints = global_checkpoint_store.load_all_checkpoints(exec_id) if resume else {}
        completed_nodes: Set[str] = set()

        # Load historical execution records for continuous learning across runs
        try:
            past_records = global_workflow_history_store.list_history(limit=5)
            past_copy_samples = []
            past_image_prompts = []
            for rec in past_records:
                arts = rec.get("artifacts", {})
                if isinstance(arts, dict):
                    for k, v in arts.items():
                        if isinstance(v, dict):
                            c = v.get("copy") or v.get("caption")
                            if c and isinstance(c, str) and len(c) > 30 and c not in past_copy_samples:
                                past_copy_samples.append(c[:150])
                            gp = v.get("gemini_prompt")
                            if gp and isinstance(gp, str) and gp not in past_image_prompts:
                                past_image_prompts.append(gp)
            context.set("past_learnings", {
                "recent_copy_previews": past_copy_samples[:5],
                "recent_image_prompts": past_image_prompts[:3]
            })
        except Exception:
            pass

        for node in workflow_def.nodes:
            if resume and node.id in checkpoints:
                node.state = NodeState.SUCCESS
                completed_nodes.add(node.id)
                chk_data = checkpoints[node.id]
                context.set(node.id, chk_data.get("output", {}))
                logger.info(f"[WorkflowRunner] Resumed node '{node.id}' from checkpoint.")
            else:
                node.state = NodeState.WAITING

        global_workflow_event_bus.publish(WorkflowStarted(execution_id=exec_id, payload={"workflow_id": workflow_def.workflow_id, "workflow_name": workflow_def.name, "version": workflow_def.version}))

        total_nodes = len(workflow_def.nodes)
        failed_nodes: List[str] = []
        node_stats: Dict[str, Dict[str, Any]] = {}

        while len(completed_nodes) + len(failed_nodes) < total_nodes:
            ready_nodes = GraphResolver.get_ready_nodes(workflow_def.nodes, completed_nodes)
            if not ready_nodes:
                # No ready nodes left and incomplete -> check if stuck or failed
                break

            # Mark ready nodes
            for n in ready_nodes:
                n.state = NodeState.READY

            # Execute ready nodes in parallel using executor
            futures = {}
            for node in ready_nodes:
                # Check node condition
                if not GraphResolver.eval_condition(node.condition, context):
                    node.state = NodeState.SKIPPED
                    completed_nodes.add(node.id)
                    logger.info(f"[WorkflowRunner] Node '{node.id}' skipped due to condition evaluation.")
                    continue

                node.state = NodeState.RUNNING
                global_workflow_event_bus.publish(NodeStarted(execution_id=exec_id, event_type="NODE_STARTED", payload={"node_id": node.id, "agent": node.agent}))
                fut = self.executor.submit(self._run_node_with_retry, node, context, exec_id)
                futures[node.id] = (node, fut)

            # Wait for submitted futures to finish
            for nid, (node, fut) in futures.items():
                try:
                    res, err, retries_used = fut.result(timeout=node.timeout + 10.0)
                    duration_ms = res.get("duration_ms", 0) if isinstance(res, dict) else 0

                    if err is None:
                        node.state = NodeState.SUCCESS
                        completed_nodes.add(node.id)
                        out_data = res.get("output") if isinstance(res, dict) else res
                        context.set(node.id, out_data)

                        # Save checkpoint
                        chk_payload = {"node_id": node.id, "status": "SUCCESS", "output": out_data, "completed_at": _get_utc_now()}
                        global_checkpoint_store.save_node_checkpoint(exec_id, node.id, chk_payload)
                        global_workflow_event_bus.publish(CheckpointSaved(execution_id=exec_id, payload={"node_id": node.id}))
                        global_workflow_event_bus.publish(NodeCompleted(execution_id=exec_id, payload={"node_id": node.id, "duration_ms": duration_ms}))

                        node_stats[node.id] = {"status": "SUCCESS", "retries": retries_used, "duration_ms": duration_ms}
                    else:
                        node.state = NodeState.FAILED
                        failed_nodes.append(node.id)
                        context.add_error(node.id, err)
                        global_workflow_event_bus.publish(NodeFailed(execution_id=exec_id, payload={"node_id": node.id, "error": err}))
                        node_stats[node.id] = {"status": "FAILED", "retries": retries_used, "error": err}
                except Exception as ex:
                    node.state = NodeState.FAILED
                    failed_nodes.append(node.id)
                    err_msg = str(ex)
                    context.add_error(node.id, err_msg)
                    global_workflow_event_bus.publish(NodeFailed(execution_id=exec_id, payload={"node_id": node.id, "error": err_msg}))
                    node_stats[node.id] = {"status": "FAILED", "retries": 0, "error": err_msg}

        total_duration_sec = round(time.time() - start_ts, 3)
        overall_status = "SUCCESS" if not failed_nodes else "FAILED"
        context.status = overall_status

        # Publish Workflow Level Event
        if overall_status == "SUCCESS":
            global_workflow_event_bus.publish(WorkflowCompleted(execution_id=exec_id, payload={"duration_sec": total_duration_sec, "nodes_completed": len(completed_nodes)}))
        else:
            global_workflow_event_bus.publish(WorkflowFailed(execution_id=exec_id, payload={"failed_nodes": failed_nodes}))

        # Save Workflow History Record
        history_record = {
            "execution_id": exec_id,
            "workflow_id": workflow_def.workflow_id,
            "workflow_name": workflow_def.name,
            "version": workflow_def.version,
            "schedule_id": schedule_id,
            "started_at": context.started_at,
            "completed_at": _get_utc_now(),
            "duration_sec": total_duration_sec,
            "status": overall_status,
            "completed_nodes": list(completed_nodes),
            "failed_nodes": failed_nodes,
            "node_statistics": node_stats,
            "artifacts": {**context.data, **(context.artifacts if isinstance(context.artifacts, dict) else {})},
            "errors": context.data.get("errors", [])
        }
        global_workflow_history_store.save_history(exec_id, history_record)

        return {
            "execution_id": exec_id,
            "workflow_id": workflow_def.workflow_id,
            "version": workflow_def.version,
            "status": overall_status,
            "duration_sec": total_duration_sec,
            "completed_nodes": list(completed_nodes),
            "failed_nodes": failed_nodes,
            "context": context.to_dict(),
            "history": history_record
        }

    def _run_node_with_retry(self, node: WorkflowNode, context: WorkflowContext, exec_id: str) -> tuple:
        max_tries = max(node.retry_policy.max_retries, 1)
        delay = max(node.retry_policy.retry_delay, 0.1)
        last_error = None

        agent_target = AgentRegistry.get(node.agent) or AgentRegistry.get(node.id)

        for attempt in range(1, max_tries + 1):
            if attempt > 1:
                global_workflow_event_bus.publish(NodeRetry(execution_id=exec_id, payload={"node_id": node.id, "attempt": attempt}))
                time.sleep(delay)
                if node.retry_policy.exponential_backoff:
                    delay *= 2

            t0 = time.time()
            try:
                if agent_target is None:
                    out = {"status": "success", "step": node.id, "summary": f"Executed node '{node.id}' natively."}
                else:
                    target_obj = agent_target() if isinstance(agent_target, type) else agent_target
                    setattr(context, "current_node_id", node.id)
                    if hasattr(target_obj, "execute") and callable(getattr(target_obj, "execute")):
                        try:
                            res = target_obj.execute(context)
                        except TypeError:
                            res = target_obj.execute()
                        out = res if isinstance(res, dict) else {"result": str(res)}
                    elif hasattr(target_obj, "act") and callable(getattr(target_obj, "act")):
                        try:
                            res = target_obj.act(context, None)
                        except TypeError:
                            res = target_obj.act(context)
                        out = res if isinstance(res, dict) else {"result": str(res)}
                    elif callable(target_obj):
                        try:
                            res = target_obj(context)
                        except TypeError:
                            res = target_obj()
                        out = res if isinstance(res, dict) else {"result": str(res)}
                    else:
                        out = {"status": "success", "node": node.id}

                duration_ms = int((time.time() - t0) * 1000)
                return {"output": out, "duration_ms": duration_ms}, None, attempt - 1
            except Exception as e:
                last_error = str(e)
                logger.warning(f"[NodeRunner] Error executing '{node.id}' (Attempt {attempt}/{max_tries}): {e}")

        return None, last_error or "Unknown Node Error", max_tries - 1

global_workflow_runner = WorkflowRunner()
