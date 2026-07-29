/**
 * AVENIQ AI — Hermes Integration Layer
 * Model Context Protocol (MCP) Transport Implementation
 */

import {
  HermesConfig,
  HermesExecutionOptions,
  HermesExecutionResult,
  HermesStreamChunk,
  HermesToolDefinition,
  HermesTransportError,
  HermesTransportType,
  IHermesTransport,
} from './types';

export class HermesMcpTransport implements IHermesTransport {
  public readonly name: HermesTransportType = 'mcp';
  private config: HermesConfig;
  private isConnected: boolean = false;
  private discoveredTools: Map<string, HermesToolDefinition> = new Map();

  constructor(config: HermesConfig) {
    this.config = config;
  }

  public async connect(): Promise<void> {
    const healthy = await this.isHealthy();
    if (!healthy) {
      throw new HermesTransportError('MCP catalog/server endpoint unreachable.', {
        code: 'MCP_CONNECT_FAILED',
        transport: 'mcp',
        retryable: true,
      });
    }
    await this.refreshToolsCatalog();
    this.isConnected = true;
  }

  public async disconnect(): Promise<void> {
    this.isConnected = false;
    this.discoveredTools.clear();
  }

  public async isHealthy(): Promise<boolean> {
    try {
      const url = `${this.config.baseUrl}/api/mcp/catalog`;
      const response = await this.fetchWithTimeout(url, { method: 'GET' }, 5000);
      return response.ok;
    } catch {
      return false;
    }
  }

  public async refreshToolsCatalog(): Promise<HermesToolDefinition[]> {
    try {
      const url = `${this.config.baseUrl}/api/mcp/catalog`;
      const response = await this.fetchWithTimeout(url, { method: 'GET' }, 5000);
      if (!response.ok) return [];

      const catalogData = await response.json();
      const tools: HermesToolDefinition[] = [];

      const rawTools = catalogData.tools || catalogData.catalog || [];
      for (const t of rawTools) {
        const toolDef: HermesToolDefinition = {
          name: t.name || t.id,
          description: t.description || '',
          parameters: t.parameters || t.inputSchema || {},
          category: t.category || t.server_name || 'mcp',
          enabled: t.enabled !== false,
        };
        this.discoveredTools.set(toolDef.name, toolDef);
        tools.push(toolDef);
      }

      return tools;
    } catch {
      return Array.from(this.discoveredTools.values());
    }
  }

  public async execute(options: HermesExecutionOptions): Promise<HermesExecutionResult> {
    const startTime = Date.now();
    const execId = options.executionId || `mcp_exec_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    const timeoutMs = options.timeoutMs || this.config.timeoutMs;

    try {
      const payload = {
        execution_id: execId,
        session_id: options.sessionId,
        prompt: options.prompt,
        mcp_tools: options.toolsets || Array.from(this.discoveredTools.keys()),
        model_override: options.modelOverride,
        provider_override: options.providerOverride,
        variables: options.variables || {},
      };

      const url = `${this.config.baseUrl}/api/mcp/servers`;
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
        const errText = await response.text().catch(() => 'MCP Error');
        throw new HermesTransportError(`MCP Execution failed with status ${response.status}: ${errText}`, {
          code: `MCP_ERROR_${response.status}`,
          transport: 'mcp',
          status: response.status,
          retryable: response.status >= 500 || response.status === 429,
        });
      }

      const resData = await response.json();
      const durationMs = Date.now() - startTime;

      return {
        executionId: execId,
        sessionId: options.sessionId,
        status: 'success',
        output: resData.output || resData.content || '',
        thought: resData.thought || '',
        toolCalls: (resData.tool_calls || []).map((t: any) => ({
          id: t.id || `mcp_call_${Math.random().toString(36).substring(2, 7)}`,
          name: t.name,
          arguments: t.arguments || {},
          status: 'completed',
          result: t.result,
        })),
        durationMs,
        raw: resData,
      };
    } catch (err: any) {
      const durationMs = Date.now() - startTime;
      if (err instanceof HermesTransportError) {
        throw err;
      }
      return {
        executionId: execId,
        sessionId: options.sessionId,
        status: err.name === 'AbortError' ? 'cancelled' : 'failed',
        output: '',
        toolCalls: [],
        durationMs,
        error: {
          code: err.name === 'AbortError' ? 'ABORTED' : 'MCP_EXEC_FAILED',
          message: err.message || 'MCP Tool Execution Failed',
          retryable: true,
        },
      };
    }
  }

  public async stream(
    options: HermesExecutionOptions,
    onChunk: (chunk: HermesStreamChunk) => void
  ): Promise<HermesExecutionResult> {
    // MCP tool executions stream chunks via onChunk callback
    onChunk({
      type: 'status',
      content: 'Initializing MCP tool catalog execution...',
      executionId: options.executionId,
      timestamp: new Date().toISOString(),
    });

    const result = await this.execute(options);

    onChunk({
      type: 'token',
      content: result.output,
      executionId: result.executionId,
      timestamp: new Date().toISOString(),
    });

    onChunk({
      type: 'done',
      content: '[DONE]',
      executionId: result.executionId,
      timestamp: new Date().toISOString(),
    });

    return result;
  }

  public async cancel(executionId: string, reason?: string): Promise<boolean> {
    try {
      const url = `${this.config.baseUrl}/api/mcp/servers/cancel`;
      const response = await this.fetchWithTimeout(
        url,
        {
          method: 'POST',
          headers: this.getHeaders(),
          body: JSON.stringify({ execution_id: executionId, reason }),
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
        throw new HermesTransportError(`MCP Request timeout after ${timeoutMs}ms`, {
          code: 'MCP_TIMEOUT',
          transport: 'mcp',
          retryable: true,
        });
      }
      throw err;
    } finally {
      clearTimeout(timeoutId);
    }
  }
}
