/**
 * AVENIQ AI — Execution Persistence & Audit Store
 * Persists workflow execution records, node statuses, token metrics, and error logs.
 */

import { AveniqEvent } from './events';

export interface NodeExecutionRecord {
  executionId: string;
  workflowId: string;
  nodeId: string;
  provider: string;
  model: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  startTime: number;
  endTime?: number;
  durationMs?: number;
  prompt: string;
  output?: string;
  thought?: string;
  tokenStats?: {
    inputTokens: number;
    outputTokens: number;
    totalTokens: number;
  };
  error?: {
    code: string;
    message: string;
    retryable: boolean;
  };
  events: AveniqEvent[];
}

export class ExecutionPersistenceStore {
  private static instance: ExecutionPersistenceStore;
  private records: Map<string, NodeExecutionRecord> = new Map();

  private constructor() {}

  public static getInstance(): ExecutionPersistenceStore {
    if (!ExecutionPersistenceStore.instance) {
      ExecutionPersistenceStore.instance = new ExecutionPersistenceStore();
    }
    return ExecutionPersistenceStore.instance;
  }

  public createRecord(init: {
    executionId: string;
    workflowId: string;
    nodeId: string;
    provider: string;
    model: string;
    prompt: string;
  }): NodeExecutionRecord {
    const record: NodeExecutionRecord = {
      ...init,
      status: 'pending',
      startTime: Date.now(),
      events: [],
    };
    const key = `${init.workflowId}:${init.executionId}:${init.nodeId}`;
    this.records.set(key, record);
    return record;
  }

  public getRecord(workflowId: string, executionId: string, nodeId: string): NodeExecutionRecord | undefined {
    const key = `${workflowId}:${executionId}:${nodeId}`;
    return this.records.get(key);
  }

  public updateRecord(
    workflowId: string,
    executionId: string,
    nodeId: string,
    updates: Partial<NodeExecutionRecord>
  ): NodeExecutionRecord | undefined {
    const key = `${workflowId}:${executionId}:${nodeId}`;
    const existing = this.records.get(key);
    if (!existing) return undefined;

    const updated = { ...existing, ...updates };
    if (updates.status === 'completed' || updates.status === 'failed' || updates.status === 'cancelled') {
      updated.endTime = Date.now();
      updated.durationMs = updated.endTime - updated.startTime;
    }
    this.records.set(key, updated);
    return updated;
  }

  public appendEvent(workflowId: string, executionId: string, nodeId: string, event: AveniqEvent): void {
    const record = this.getRecord(workflowId, executionId, nodeId);
    if (record) {
      record.events.push(event);
    }
  }

  public listRecordsForExecution(workflowId: string, executionId: string): NodeExecutionRecord[] {
    const result: NodeExecutionRecord[] = [];
    for (const record of this.records.values()) {
      if (record.workflowId === workflowId && record.executionId === executionId) {
        result.push(record);
      }
    }
    return result;
  }

  public clear(): void {
    this.records.clear();
  }
}
