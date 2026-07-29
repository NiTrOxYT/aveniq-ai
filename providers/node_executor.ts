/**
 * AVENIQ AI — Workflow Node Executor
 * Generic, provider-agnostic executor for DAG workflow nodes.
 */

import { AveniqEvent, HermesEventTranslator } from './events';
import { ExecutionPersistenceStore, NodeExecutionRecord } from './persistence';
import { ProviderRegistry } from './registry';

export interface WorkflowNode {
  id: string;
  name: string;
  provider?: string;
  model?: string;
  prompt: string;
  inputVariables?: Record<string, any>;
  timeoutMs?: number;
  retries?: number;
}

export interface WorkflowExecutionContext {
  workflowId: string;
  executionId: string;
  variables?: Record<string, any>;
  onEvent?: (event: AveniqEvent) => void;
}

export class WorkflowNodeExecutor {
  private registry: ProviderRegistry;
  private store: ExecutionPersistenceStore;

  constructor() {
    this.registry = ProviderRegistry.getInstance();
    this.store = ExecutionPersistenceStore.getInstance();
  }

  /**
   * Execute a single workflow DAG node
   */
  public async executeNode(
    node: WorkflowNode,
    context: WorkflowExecutionContext
  ): Promise<NodeExecutionRecord> {
    const providerName = node.provider || 'hermes';
    const model = node.model || 'hermes-agent';
    const timeoutMs = node.timeoutMs || 45000;
    const maxRetries = node.retries ?? 2;

    // 1. Initialize Persistence Record
    const record = this.store.createRecord({
      executionId: context.executionId,
      workflowId: context.workflowId,
      nodeId: node.id,
      provider: providerName,
      model,
      prompt: node.prompt,
    });

    this.store.updateRecord(context.workflowId, context.executionId, node.id, {
      status: 'running',
    });

    // 2. Resolve Provider & Fallback Providers
    const providersToTry = [providerName, ...this.registry.getFallbackChain().filter((p) => p !== providerName)];
    let lastError: any = null;
    let attempts = 0;

    for (const currentProviderName of providersToTry) {
      if (attempts > maxRetries) break;
      attempts++;

      try {
        const provider = this.registry.resolve(currentProviderName);

        const handleChunk = (chunk: any) => {
          let aveniqEvent: AveniqEvent | null = null;
          if (chunk.metadata && chunk.type) {
            aveniqEvent = HermesEventTranslator.translate(chunk.type, chunk.metadata, {
              executionId: context.executionId,
              workflowId: context.workflowId,
              nodeId: node.id,
              model,
            });
          } else if (chunk.type === 'token') {
            aveniqEvent = {
              type: 'Token',
              executionId: context.executionId,
              workflowId: context.workflowId,
              nodeId: node.id,
              provider: currentProviderName,
              model,
              timestamp: new Date().toISOString(),
              content: chunk.content,
            };
          } else if (chunk.type === 'thought') {
            aveniqEvent = {
              type: 'Thinking',
              executionId: context.executionId,
              workflowId: context.workflowId,
              nodeId: node.id,
              provider: currentProviderName,
              model,
              timestamp: new Date().toISOString(),
              content: chunk.content,
            };
          }

          if (aveniqEvent) {
            this.store.appendEvent(context.workflowId, context.executionId, node.id, aveniqEvent);
            if (context.onEvent) context.onEvent(aveniqEvent);
          }
        };

        const res = await provider.stream(
          {
            executionId: `${context.executionId}_${node.id}`,
            prompt: node.prompt,
            modelOverride: model,
            timeoutMs,
            variables: { ...context.variables, ...node.inputVariables },
          },
          handleChunk
        );

        if (res.status === 'success') {
          const finalRecord = this.store.updateRecord(context.workflowId, context.executionId, node.id, {
            status: 'completed',
            output: res.output,
            thought: res.thought,
            tokenStats: res.tokenStats,
          })!;

          const completedEvent: AveniqEvent = {
            type: 'Completed',
            executionId: context.executionId,
            workflowId: context.workflowId,
            nodeId: node.id,
            provider: currentProviderName,
            model,
            timestamp: new Date().toISOString(),
            content: res.output,
          };
          this.store.appendEvent(context.workflowId, context.executionId, node.id, completedEvent);
          if (context.onEvent) context.onEvent(completedEvent);

          return finalRecord;
        }

        if (res.status === 'cancelled') {
          const cancelledRecord = this.store.updateRecord(context.workflowId, context.executionId, node.id, {
            status: 'cancelled',
            output: res.output,
          })!;
          return cancelledRecord;
        }

        lastError = res.error || new Error(`Provider ${currentProviderName} execution failed`);
      } catch (err: any) {
        lastError = err;
      }
    }

    // 3. Persist Failure if all provider attempts exhausted
    const failedRecord = this.store.updateRecord(context.workflowId, context.executionId, node.id, {
      status: 'failed',
      error: {
        code: lastError?.code || 'NODE_EXECUTION_FAILED',
        message: lastError?.message || 'Node execution failed across all providers',
        retryable: false,
      },
    })!;

    const failedEvent: AveniqEvent = {
      type: 'Failed',
      executionId: context.executionId,
      workflowId: context.workflowId,
      nodeId: node.id,
      provider: providerName,
      model,
      timestamp: new Date().toISOString(),
      error: {
        code: lastError?.code || 'NODE_EXECUTION_FAILED',
        message: lastError?.message || 'Execution failed',
        retryable: false,
      },
    };
    this.store.appendEvent(context.workflowId, context.executionId, node.id, failedEvent);
    if (context.onEvent) context.onEvent(failedEvent);

    return failedRecord;
  }

  /**
   * Cancel execution of a DAG node
   */
  public async cancelNode(
    nodeId: string,
    context: WorkflowExecutionContext,
    reason?: string
  ): Promise<boolean> {
    const record = this.store.getRecord(context.workflowId, context.executionId, nodeId);
    if (!record) return false;

    const provider = this.registry.resolve(record.provider);
    const success = await provider.cancel(`${context.executionId}_${nodeId}`, reason);

    this.store.updateRecord(context.workflowId, context.executionId, nodeId, {
      status: 'cancelled',
    });

    const cancelledEvent: AveniqEvent = {
      type: 'Cancelled',
      executionId: context.executionId,
      workflowId: context.workflowId,
      nodeId,
      provider: record.provider,
      model: record.model,
      timestamp: new Date().toISOString(),
      content: reason || 'Cancelled by Workflow Engine',
    };
    this.store.appendEvent(context.workflowId, context.executionId, nodeId, cancelledEvent);
    if (context.onEvent) context.onEvent(cancelledEvent);

    return success;
  }
}
