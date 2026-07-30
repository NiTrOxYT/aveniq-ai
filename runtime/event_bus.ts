/**
 * AVENIQ AI — Unified Runtime Event Bus
 */

export type RuntimeEventType =
  | 'WorkflowStarted'
  | 'NodeQueued'
  | 'NodeStarted'
  | 'NodeStreaming'
  | 'NodeCompleted'
  | 'NodeFailed'
  | 'WorkflowCompleted'
  | 'WorkflowFailed'
  | 'WorkflowCancelled';

export interface RuntimeEvent {
  type: RuntimeEventType;
  workflowId: string;
  executionId: string;
  nodeId?: string;
  timestamp: string;
  payload?: any;
}

export class RuntimeEventBus {
  private static instance: RuntimeEventBus;
  private listeners: Set<(event: RuntimeEvent) => void> = new Set();

  private constructor() {}

  public static getInstance(): RuntimeEventBus {
    if (!RuntimeEventBus.instance) {
      RuntimeEventBus.instance = new RuntimeEventBus();
    }
    return RuntimeEventBus.instance;
  }

  public subscribe(listener: (event: RuntimeEvent) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  public emit(event: RuntimeEvent): void {
    for (const listener of this.listeners) {
      try {
        listener(event);
      } catch {}
    }
  }
}
