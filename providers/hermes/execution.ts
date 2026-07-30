/**
 * AVENIQ AI — Hermes Integration Layer
 * Execution Service & Lifecycle Management
 */

import {
  HermesExecutionOptions,
  HermesExecutionResult,
  HermesStreamChunk,
  IHermesAdapter,
} from './types';

export interface ActiveExecutionState {
  executionId: string;
  sessionId?: string;
  options: HermesExecutionOptions;
  startTime: number;
  status: 'running' | 'cancelling' | 'completed' | 'failed';
  abortController: AbortController;
  timeoutTimer: any;
  chunks: HermesStreamChunk[];
}

export interface ExecutionServiceConfig {
  defaultTimeoutMs?: number;
  sessionTimeoutMs?: number;
  providerTimeoutMs?: number;
  streamingTimeoutMs?: number;
  maxConcurrentExecutions?: number;
  delegateRetriesToAveniq?: boolean;
}

export class ExecutionService {
  private adapter: IHermesAdapter;
  private config: ExecutionServiceConfig;
  private activeExecutions: Map<string, ActiveExecutionState> = new Map();

  constructor(adapter: IHermesAdapter, config: ExecutionServiceConfig = {}) {
    this.adapter = adapter;
    this.config = {
      defaultTimeoutMs: 60000,
      sessionTimeoutMs: 30000,
      providerTimeoutMs: 45000,
      streamingTimeoutMs: 15000,
      maxConcurrentExecutions: 20,
      delegateRetriesToAveniq: true,
      ...config,
    };
  }

  /**
   * Execute task synchronously or with callback streaming
   */
  public async run(
    options: HermesExecutionOptions,
    onChunk?: (chunk: HermesStreamChunk) => void
  ): Promise<HermesExecutionResult> {
    const execId = options.executionId || `exec_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    const timeoutMs = options.timeoutMs || this.config.defaultTimeoutMs;
    const streamingTimeoutMs = this.config.streamingTimeoutMs || 15000;

    const abortController = new AbortController();
    if (options.abortSignal) {
      options.abortSignal.addEventListener('abort', () => abortController.abort());
    }

    const timeoutTimer = setTimeout(() => {
      abortController.abort();
    }, timeoutMs);

    let streamingWatchdogTimer: any = null;

    const resetStreamingWatchdog = () => {
      if (streamingWatchdogTimer) clearTimeout(streamingWatchdogTimer);
      streamingWatchdogTimer = setTimeout(() => {
        console.warn(`[ExecutionService] Streaming watchdog timeout (${streamingTimeoutMs}ms) reached for execution ${execId}`);
        abortController.abort();
      }, streamingTimeoutMs);
    };

    const state: ActiveExecutionState = {
      executionId: execId,
      sessionId: options.sessionId,
      options: { ...options, executionId: execId },
      startTime: Date.now(),
      status: 'running',
      abortController,
      timeoutTimer,
      chunks: [],
    };

    this.activeExecutions.set(execId, state);

    const mergedOptions: HermesExecutionOptions = {
      ...options,
      executionId: execId,
      abortSignal: abortController.signal,
      timeoutMs,
    };

    const handleChunk = (chunk: HermesStreamChunk) => {
      resetStreamingWatchdog();
      state.chunks.push(chunk);
      if (onChunk) onChunk(chunk);
      if (options.onStreamChunk) options.onStreamChunk(chunk);
    };

    try {
      let result: HermesExecutionResult;
      if (onChunk || options.onStreamChunk) {
        result = await this.adapter.stream(mergedOptions, handleChunk);
      } else {
        result = await this.adapter.execute(mergedOptions);
      }

      state.status = result.status === 'success' ? 'completed' : 'failed';
      return result;
    } catch (err: any) {
      state.status = 'failed';
      // Delegate retry logic to AVENIQ Orchestration Engine
      if (this.config.delegateRetriesToAveniq) {
        throw err;
      }
      return {
        executionId: execId,
        sessionId: options.sessionId,
        status: 'failed',
        output: '',
        toolCalls: [],
        durationMs: Date.now() - state.startTime,
        error: {
          code: 'EXECUTION_SERVICE_ERROR',
          message: err.message || 'Execution failed in ExecutionService',
          details: err,
          retryable: true, // Signal to AVENIQ that this task can be retried by AVENIQ
        },
      };
    } finally {
      if (streamingWatchdogTimer) clearTimeout(streamingWatchdogTimer);
      clearTimeout(timeoutTimer);
      this.activeExecutions.delete(execId);
    }
  }

  /**
   * Cancel an active execution
   */
  public async cancel(executionId: string, reason?: string): Promise<boolean> {
    const state = this.activeExecutions.get(executionId);
    if (!state) return false;

    state.status = 'cancelling';
    state.abortController.abort();
    clearTimeout(state.timeoutTimer);

    const transportSuccess = await this.adapter.cancel(executionId, reason);
    this.activeExecutions.delete(executionId);
    return transportSuccess;
  }

  /**
   * Get active execution state
   */
  public getActiveExecution(executionId: string): ActiveExecutionState | undefined {
    return this.activeExecutions.get(executionId);
  }

  /**
   * List all active executions
   */
  public listActiveExecutions(): ActiveExecutionState[] {
    return Array.from(this.activeExecutions.values());
  }

  /**
   * Cleanup and cancel all running executions
   */
  public async dispose(): Promise<void> {
    const cancelPromises = Array.from(this.activeExecutions.keys()).map((id) =>
      this.cancel(id, 'ExecutionService disposing')
    );
    await Promise.all(cancelPromises);
    this.activeExecutions.clear();
  }
}
