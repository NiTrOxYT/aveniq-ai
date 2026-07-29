/**
 * AVENIQ AI — Execution Replay & Checkpoint Engine
 * Enables replaying entire workflows, single nodes, or failed branches
 * without rerunning completed upstream nodes.
 */

export interface ExecutionCheckpoint {
  workflowId: string;
  executionId: string;
  completedNodeOutputs: Record<string, string>; // nodeId -> output
  nodeStatuses: Record<string, 'completed' | 'failed' | 'cancelled'>;
  timestamp: string;
}

export class ExecutionReplayStore {
  private static instance: ExecutionReplayStore;
  private checkpoints: Map<string, ExecutionCheckpoint> = new Map();

  private constructor() {}

  public static getInstance(): ExecutionReplayStore {
    if (!ExecutionReplayStore.instance) {
      ExecutionReplayStore.instance = new ExecutionReplayStore();
    }
    return ExecutionReplayStore.instance;
  }

  public saveCheckpoint(checkpoint: ExecutionCheckpoint): void {
    const key = `${checkpoint.workflowId}:${checkpoint.executionId}`;
    this.checkpoints.set(key, checkpoint);
  }

  public getCheckpoint(workflowId: string, executionId: string): ExecutionCheckpoint | undefined {
    const key = `${workflowId}:${executionId}`;
    return this.checkpoints.get(key);
  }

  public clear(): void {
    this.checkpoints.clear();
  }
}
