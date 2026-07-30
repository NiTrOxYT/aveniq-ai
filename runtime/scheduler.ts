/**
 * AVENIQ AI — Workflow Runtime Scheduler & Parallel DAG Execution Engine
 */

import { CompiledWorkflowPlan, WorkflowCompiler } from './compiler';
import { ContextInterpolator } from './context';
import { WorkflowDefinition, WorkflowNodeDefinition } from './definition';
import { RuntimeEventBus } from './event_bus';
import { ExecutionCheckpoint, ExecutionReplayStore } from './replay';
import { AveniqEvent } from '../providers/events';
import { WorkflowNodeExecutor } from '../providers/node_executor';

export interface RuntimeExecutionOptions {
  executionId?: string;
  variables?: Record<string, any>;
  replayFromExecutionId?: string; // Skip already completed nodes from this execution checkpoint!
  concurrencyLimit?: number;
  onEvent?: (event: AveniqEvent) => void;
}

export interface WorkflowRuntimeState {
  workflowId: string;
  executionId: string;
  status: 'running' | 'completed' | 'failed' | 'cancelled';
  queuedNodes: string[];
  runningNodes: string[];
  completedNodes: string[];
  failedNodes: string[];
  startTime: number;
  endTime?: number;
  nodeOutputs: Record<string, string>;
}

export class RuntimeScheduler {
  private executor: WorkflowNodeExecutor;
  private eventBus: RuntimeEventBus;
  private replayStore: ExecutionReplayStore;
  private activeState: Map<string, WorkflowRuntimeState> = new Map();
  private abortControllers: Map<string, AbortController> = new Map();

  constructor() {
    this.executor = new WorkflowNodeExecutor();
    this.eventBus = RuntimeEventBus.getInstance();
    this.replayStore = ExecutionReplayStore.getInstance();
  }

  /**
   * Execute a workflow definition
   */
  public async executeWorkflow(
    definition: WorkflowDefinition,
    options: RuntimeExecutionOptions = {}
  ): Promise<WorkflowRuntimeState> {
    const plan = WorkflowCompiler.compile(definition);
    const executionId = options.executionId || `exec_rt_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    const abortController = new AbortController();
    this.abortControllers.set(executionId, abortController);

    // 1. Check for Replay Checkpoint
    let existingCheckpoint: ExecutionCheckpoint | undefined;
    if (options.replayFromExecutionId) {
      existingCheckpoint = this.replayStore.getCheckpoint(definition.id, options.replayFromExecutionId);
    }

    const state: WorkflowRuntimeState = {
      workflowId: definition.id,
      executionId,
      status: 'running',
      queuedNodes: [...plan.topologicalOrder],
      runningNodes: [],
      completedNodes: existingCheckpoint ? Object.keys(existingCheckpoint.completedNodeOutputs) : [],
      failedNodes: [],
      startTime: Date.now(),
      nodeOutputs: existingCheckpoint ? { ...existingCheckpoint.completedNodeOutputs } : {},
    };

    this.activeState.set(executionId, state);

    this.eventBus.emit({
      type: 'WorkflowStarted',
      workflowId: definition.id,
      executionId,
      timestamp: new Date().toISOString(),
      payload: { plan },
    });

    const nodeOutputsMap = new Map<string, string>(Object.entries(state.nodeOutputs));
    const globalVars = { ...definition.variables, ...options.variables };

    try {
      // 2. Execute parallel stages in topological order
      for (const batch of plan.executionBatches) {
        if (abortController.signal.aborted) {
          state.status = 'cancelled';
          break;
        }

        // Filter out nodes already completed via replay checkpoint
        const nodesToRun = batch.filter((n) => !state.completedNodes.includes(n.id));
        if (nodesToRun.length === 0) continue;

        state.runningNodes = nodesToRun.map((n) => n.id);
        state.queuedNodes = state.queuedNodes.filter((id) => !state.runningNodes.includes(id));

        nodesToRun.forEach((n) => {
          this.eventBus.emit({
            type: 'NodeQueued',
            workflowId: definition.id,
            executionId,
            nodeId: n.id,
            timestamp: new Date().toISOString(),
          });
        });

        // Run nodes in current batch concurrently
        const batchResults = await Promise.all(
          nodesToRun.map(async (nodeDef) => {
            if (abortController.signal.aborted) return null;

            this.eventBus.emit({
              type: 'NodeStarted',
              workflowId: definition.id,
              executionId,
              nodeId: nodeDef.id,
              timestamp: new Date().toISOString(),
            });

            // Interpolate prompt with outputs from upstream nodes
            const interpolatedPrompt = ContextInterpolator.interpolate(
              nodeDef.prompt,
              nodeOutputsMap,
              globalVars
            );

            const record = await this.executor.executeNode(
              {
                id: nodeDef.id,
                name: nodeDef.name || nodeDef.id,
                provider: nodeDef.provider || 'hermes',
                model: nodeDef.model || 'hermes-agent',
                prompt: interpolatedPrompt,
                retries: nodeDef.retries ?? 2,
                timeoutMs: nodeDef.timeoutMs || 45000,
              },
              {
                workflowId: definition.id,
                executionId,
                variables: globalVars,
                onEvent: (ev) => {
                  if (options.onEvent) options.onEvent(ev);
                  if (ev.type === 'Token' || ev.type === 'Thinking') {
                    this.eventBus.emit({
                      type: 'NodeStreaming',
                      workflowId: definition.id,
                      executionId,
                      nodeId: nodeDef.id,
                      timestamp: new Date().toISOString(),
                      payload: ev,
                    });
                  }
                },
              }
            );

            return { nodeDef, record };
          })
        );

        // Process batch outcomes
        for (const res of batchResults) {
          if (!res) continue;
          const { nodeDef, record } = res;
          state.runningNodes = state.runningNodes.filter((id) => id !== nodeDef.id);

          if (record.status === 'completed') {
            state.completedNodes.push(nodeDef.id);
            nodeOutputsMap.set(nodeDef.id, record.output || '');
            state.nodeOutputs[nodeDef.id] = record.output || '';

            this.eventBus.emit({
              type: 'NodeCompleted',
              workflowId: definition.id,
              executionId,
              nodeId: nodeDef.id,
              timestamp: new Date().toISOString(),
              payload: { output: record.output },
            });
          } else {
            state.failedNodes.push(nodeDef.id);
            this.eventBus.emit({
              type: 'NodeFailed',
              workflowId: definition.id,
              executionId,
              nodeId: nodeDef.id,
              timestamp: new Date().toISOString(),
              payload: { error: record.error },
            });
            throw new Error(`Node '${nodeDef.id}' failed execution: ${record.error?.message || 'Unknown error'}`);
          }
        }
      }

      state.status = state.status === 'cancelled' ? 'cancelled' : 'completed';
      state.endTime = Date.now();

      // Save Checkpoint for Replay Engine
      this.replayStore.saveCheckpoint({
        workflowId: definition.id,
        executionId,
        completedNodeOutputs: state.nodeOutputs,
        nodeStatuses: Object.fromEntries(state.completedNodes.map((id) => [id, 'completed'])),
        timestamp: new Date().toISOString(),
      });

      this.eventBus.emit({
        type: state.status === 'completed' ? 'WorkflowCompleted' : 'WorkflowCancelled',
        workflowId: definition.id,
        executionId,
        timestamp: new Date().toISOString(),
        payload: { state },
      });

      return state;
    } catch (err: any) {
      state.status = 'failed';
      state.endTime = Date.now();

      this.eventBus.emit({
        type: 'WorkflowFailed',
        workflowId: definition.id,
        executionId,
        timestamp: new Date().toISOString(),
        payload: { error: err.message, failedNodes: state.failedNodes },
      });

      return state;
    } finally {
      this.abortControllers.delete(executionId);
    }
  }

  /**
   * Cancel an active running workflow
   */
  public async cancelWorkflow(executionId: string, reason?: string): Promise<boolean> {
    const controller = this.abortControllers.get(executionId);
    const state = this.activeState.get(executionId);

    if (controller) {
      controller.abort();
    }

    if (state) {
      state.status = 'cancelled';
      state.endTime = Date.now();

      this.eventBus.emit({
        type: 'WorkflowCancelled',
        workflowId: state.workflowId,
        executionId,
        timestamp: new Date().toISOString(),
        payload: { reason },
      });
      return true;
    }

    return false;
  }

  /**
   * Get active state of an execution
   */
  public getExecutionState(executionId: string): WorkflowRuntimeState | undefined {
    return this.activeState.get(executionId);
  }
}
