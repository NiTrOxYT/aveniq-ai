/**
 * AVENIQ AI — Hermes Integration Layer
 * HTTP REST & SSE Transport Implementation
 */

import {
  HermesConfig,
  HermesExecutionOptions,
  HermesExecutionResult,
  HermesStreamChunk,
  HermesTransportError,
  HermesTransportType,
  IHermesTransport,
} from './types';

export class HermesHttpTransport implements IHermesTransport {
  public readonly name: HermesTransportType = 'http';
  private config: HermesConfig;
  private isConnected: boolean = false;

  constructor(config: HermesConfig) {
    this.config = config;
  }

  public async connect(): Promise<void> {
    const healthy = await this.isHealthy();
    if (!healthy) {
      throw new HermesTransportError('Failed to connect to Hermes HTTP API endpoint.', {
        code: 'HTTP_CONNECT_FAILED',
        transport: 'http',
        retryable: true,
      });
    }
    this.isConnected = true;
  }

  public async disconnect(): Promise<void> {
    this.isConnected = false;
  }

  public async isHealthy(): Promise<boolean> {
    try {
      const url = `${this.config.baseUrl}/api/health`;
      const response = await this.fetchWithTimeout(url, { method: 'GET' }, 5000);
      return response.ok;
    } catch {
      return false;
    }
  }

  public async execute(options: HermesExecutionOptions): Promise<HermesExecutionResult> {
    const startTime = Date.now();
    const execId = options.executionId || `exec_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    const timeoutMs = options.timeoutMs || this.config.timeoutMs;

    try {
      const payload = {
        prompt: options.prompt,
        session_id: options.sessionId,
        execution_id: execId,
        model_override: options.modelOverride,
        provider_override: options.providerOverride,
        skills: options.skills || [],
        toolsets: options.toolsets || [],
        variables: options.variables || {},
      };

      const url = `${this.config.baseUrl}/api/plugins/kanban/tasks`;
      const response = await this.fetchWithTimeout(
        url,
        {
          method: 'POST',
          headers: this.getHeaders(),
          body: JSON.stringify(payload),
          signal: options.abortSignal,
        },
        timeoutMs
      );

      if (!response.ok) {
        const errorText = await response.text().catch(() => 'Unknown Error');
        throw new HermesTransportError(`Hermes HTTP execution failed with status ${response.status}: ${errorText}`, {
          code: `HTTP_ERROR_${response.status}`,
          transport: 'http',
          status: response.status,
          retryable: response.status >= 500 || response.status === 429,
        });
      }

      const resData = await response.json();
      const durationMs = Date.now() - startTime;

      return {
        executionId: execId,
        sessionId: options.sessionId || resData.session_id,
        status: 'success',
        output: resData.output || resData.result || resData.body || '',
        thought: resData.thought || resData.reasoning || '',
        toolCalls: (resData.tool_calls || []).map((t: any) => ({
          id: t.id || `tool_${Math.random().toString(36).substring(2, 7)}`,
          name: t.name || t.tool,
          arguments: t.arguments || t.args || {},
          status: t.status || 'completed',
          result: t.result,
        })),
        durationMs,
        tokenStats: resData.token_stats ? {
          inputTokens: resData.token_stats.input_tokens || 0,
          outputTokens: resData.token_stats.output_tokens || 0,
          totalTokens: resData.token_stats.total_tokens || 0,
        } : undefined,
        raw: resData,
      };
    } catch (err: any) {
      const durationMs = Date.now() - startTime;
      if (err instanceof HermesTransportError) {
        throw err;
      }
      const isAbort = err.name === 'AbortError';
      const isTimeout = err.name === 'TimeoutError' || err.message?.includes('timeout');

      return {
        executionId: execId,
        sessionId: options.sessionId,
        status: isAbort ? 'cancelled' : isTimeout ? 'timeout' : 'failed',
        output: '',
        toolCalls: [],
        durationMs,
        error: {
          code: isAbort ? 'ABORTED' : isTimeout ? 'TIMEOUT' : 'HTTP_EXEC_FAILED',
          message: err.message || 'HTTP Execution Failed',
          details: err,
          retryable: !isAbort && (isTimeout || true), // Delegate retry logic to AVENIQ engine
        },
      };
    }
  }

  public async stream(
    options: HermesExecutionOptions,
    onChunk: (chunk: HermesStreamChunk) => void
  ): Promise<HermesExecutionResult> {
    const startTime = Date.now();
    const execId = options.executionId || `exec_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    const timeoutMs = options.timeoutMs || this.config.timeoutMs;

    try {
      const payload = {
        prompt: options.prompt,
        session_id: options.sessionId,
        execution_id: execId,
        model_override: options.modelOverride,
        provider_override: options.providerOverride,
        skills: options.skills || [],
        toolsets: options.toolsets || [],
        variables: options.variables || {},
        stream: true,
      };

      const url = `${this.config.baseUrl}/api/files/upload-stream`;
      const response = await this.fetchWithTimeout(
        url,
        {
          method: 'POST',
          headers: this.getHeaders(),
          body: JSON.stringify(payload),
          signal: options.abortSignal,
        },
        timeoutMs
      );

      if (!response.ok || !response.body) {
        // Fallback to sync execute if streaming endpoint is unavailable
        return this.execute(options);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let fullOutput = '';
      let fullThought = '';
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || trimmed.startsWith(':')) continue;

          if (trimmed.startsWith('data: ')) {
            const rawData = trimmed.substring(6);
            if (rawData === '[DONE]') continue;

            try {
              const parsed = JSON.parse(rawData);
              const chunkType = parsed.type || 'token';
              const content = parsed.content || parsed.text || parsed.delta || '';

              if (chunkType === 'thought') fullThought += content;
              if (chunkType === 'token') fullOutput += content;

              const chunk: HermesStreamChunk = {
                type: chunkType,
                content,
                executionId: execId,
                timestamp: new Date().toISOString(),
                metadata: parsed.metadata,
              };

              onChunk(chunk);
            } catch {
              // Direct string token chunk fallback
              fullOutput += rawData;
              onChunk({
                type: 'token',
                content: rawData,
                executionId: execId,
                timestamp: new Date().toISOString(),
              });
            }
          }
        }
      }

      const durationMs = Date.now() - startTime;
      return {
        executionId: execId,
        sessionId: options.sessionId,
        status: 'success',
        output: fullOutput,
        thought: fullThought,
        toolCalls: [],
        durationMs,
      };
    } catch (err: any) {
      const durationMs = Date.now() - startTime;
      return {
        executionId: execId,
        sessionId: options.sessionId,
        status: err.name === 'AbortError' ? 'cancelled' : 'failed',
        output: '',
        toolCalls: [],
        durationMs,
        error: {
          code: err.name === 'AbortError' ? 'ABORTED' : 'STREAM_FAILED',
          message: err.message || 'Stream Execution Error',
          retryable: true,
        },
      };
    }
  }

  public async cancel(executionId: string, reason?: string): Promise<boolean> {
    try {
      const url = `${this.config.baseUrl}/api/plugins/kanban/runs/${executionId}/terminate`;
      const response = await this.fetchWithTimeout(
        url,
        {
          method: 'POST',
          headers: this.getHeaders(),
          body: JSON.stringify({ reason: reason || 'Cancelled by AVENIQ Orchestration Engine' }),
        },
        5000
      );
      return response.ok;
    } catch {
      return false;
    }
  }

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...this.config.headers,
    };
    if (this.config.authToken) {
      headers['Authorization'] = `Bearer ${this.config.authToken}`;
    }
    return headers;
  }

  private async fetchWithTimeout(url: string, init: RequestInit, timeoutMs: number): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    if (init.signal) {
      init.signal.addEventListener('abort', () => controller.abort());
    }

    try {
      const response = await fetch(url, { ...init, signal: controller.signal });
      return response;
    } catch (err: any) {
      if (err.name === 'AbortError') {
        throw new HermesTransportError(`HTTP Request timeout/aborted after ${timeoutMs}ms`, {
          code: 'HTTP_TIMEOUT',
          transport: 'http',
          retryable: true,
        });
      }
      throw err;
    } finally {
      clearTimeout(timeoutId);
    }
  }
}
