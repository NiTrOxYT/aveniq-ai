/**
 * AVENIQ AI — Runtime Dashboard API Interface
 * Exposes workflow definitions, execution history, replay endpoints, and real-time state.
 */

import { WorkflowDefinition } from './definition';
import { ExecutionReplayStore } from './replay';
import { RuntimeScheduler, WorkflowRuntimeState } from './scheduler';
import { ExecutionPersistenceStore, NodeExecutionRecord } from '../providers/persistence';

export class DashboardApi {
  private scheduler: RuntimeScheduler;
  private store: ExecutionPersistenceStore;
  private replayStore: ExecutionReplayStore;
  private workflowDefinitions: Map<string, WorkflowDefinition> = new Map();

  constructor(scheduler: RuntimeScheduler) {
    this.scheduler = scheduler;
    this.store = ExecutionPersistenceStore.getInstance();
    this.replayStore = ExecutionReplayStore.getInstance();
  }

  public registerWorkflow(def: WorkflowDefinition): void {
    this.workflowDefinitions.set(def.id, def);
  }

  public listWorkflows(): WorkflowDefinition[] {
    return Array.from(this.workflowDefinitions.values());
  }

  public getWorkflow(workflowId: string): WorkflowDefinition | undefined {
    return this.workflowDefinitions.get(workflowId);
  }

  public getExecutionState(executionId: string): WorkflowRuntimeState | undefined {
    return this.scheduler.getExecutionState(executionId);
  }

  public getNodeRecords(workflowId: string, executionId: string): NodeExecutionRecord[] {
    return this.store.listRecordsForExecution(workflowId, executionId);
  }

  public async replayExecution(workflowId: string, executionId: string): Promise<WorkflowRuntimeState> {
    const def = this.getWorkflow(workflowId);
    if (!def) throw new Error(`Workflow '${workflowId}' not found`);

    return this.scheduler.executeWorkflow(def, {
      replayFromExecutionId: executionId,
    });
  }

  public async cancelExecution(executionId: string, reason?: string): Promise<boolean> {
    return this.scheduler.cancelWorkflow(executionId, reason);
  }
}
