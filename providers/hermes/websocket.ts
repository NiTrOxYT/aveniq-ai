/**
 * AVENIQ AI — Hermes Integration Layer
 * Real-time Bi-directional JSON-RPC WebSocket Transport Implementation
 *
 * Implements official Hermes JSON-RPC Gateway Protocol (/api/ws):
 * - Handshake: Waits for 'gateway.ready' event
 * - RPC Methods: 'session.create', 'prompt.submit', 'prompt.cancel', 'session.close'
 * - Stream Events: 'message.delta', 'thinking.delta', 'tool.start', 'tool.complete', 'message.complete', 'error'
 */

import {
  HermesConfig,
  HermesExecutionOptions,
  HermesExecutionResult,
  HermesStreamChunk,
  HermesToolCall,
  HermesTransportError,
  HermesTransportType,
  IHermesTransport,
} from './types';

interface PendingRpcCall {
  resolve: (result: any) => void;
  reject: (error: any) => void;
  timerId: any;
}

interface PendingExecution {
  resolve: (result: HermesExecutionResult) => void;
  reject: (error: any) => void;
  onChunk?: (chunk: HermesStreamChunk) => void;
  options: HermesExecutionOptions;
  sessionId: string;
  startTime: number;
  outputBuffer: string;
  thoughtBuffer: string;
  toolCalls: HermesToolCall[];
  timerId: any;
}

export class HermesWebSocketTransport implements IHermesTransport {
  public readonly name: HermesTransportType = 'websocket';
  private config: HermesConfig;
  private socket: any = null;
  private isConnected: boolean = false;
  private isGatewayReady: boolean = false;
  private requestIdCounter: number = 1;
  private pendingCalls: Map<string | number, PendingRpcCall> = new Map();
  private activeExecutions: Map<string, PendingExecution> = new Map(); // sessionId -> PendingExecution
  private executionSessionMap: Map<string, string> = new Map(); // execId -> sessionId
  private pingIntervalTimer: any = null;

  constructor(config: HermesConfig) {
    this.config = config;
  }

  public async connect(): Promise<void> {
    if (this.isConnected && this.socket && this.isGatewayReady) return;

    return new Promise((resolve, reject) => {
      try {
        let WebSocketImpl = typeof window !== 'undefined' ? (window as any).WebSocket : (globalThis as any).WebSocket;
        if (!WebSocketImpl) {
          try {
            WebSocketImpl = require('ws');
          } catch {}
        }
        if (!WebSocketImpl) {
          throw new HermesTransportError('WebSocket implementation unavailable in current environment.', {
            code: 'WS_NO_IMPL',
            transport: 'websocket',
            retryable: false,
          });
        }

        const wsUrl = this.config.wsUrl || `${this.config.baseUrl.replace(/^http/, 'ws')}/api/ws`;
        this.socket = new WebSocketImpl(wsUrl);

        const connectTimeoutTimer = setTimeout(() => {
          if (!this.isGatewayReady) {
            this.disconnect();
            reject(new HermesTransportError(`WebSocket connection timed out waiting for gateway.ready at ${wsUrl}`, {
              code: 'WS_READY_TIMEOUT',
              transport: 'websocket',
              retryable: true,
            }));
          }
        }, 15000);

        this.socket.onopen = () => {
          this.isConnected = true;
          this.startHeartbeat();
        };

        this.socket.onmessage = (event: any) => {
          this.handleRawMessage(event.data, () => {
            clearTimeout(connectTimeoutTimer);
            this.isGatewayReady = true;
            resolve();
          });
        };

        this.socket.onerror = (err: any) => {
          if (!this.isGatewayReady) {
            clearTimeout(connectTimeoutTimer);
            reject(new HermesTransportError(`WebSocket connection error to ${wsUrl}`, {
              code: 'WS_CONNECT_ERROR',
              transport: 'websocket',
              retryable: true,
            }));
          }
        };

        this.socket.onclose = () => {
          clearTimeout(connectTimeoutTimer);
          this.stopHeartbeat();
          this.isConnected = false;
          this.isGatewayReady = false;
          this.socket = null;
          this.handleDisconnect();
        };
      } catch (err: any) {
        reject(new HermesTransportError(`Failed to initialize WebSocket transport: ${err.message}`, {
          code: 'WS_INIT_FAILED',
          transport: 'websocket',
          retryable: true,
        }));
      }
    });
  }

  public async disconnect(): Promise<void> {
    this.stopHeartbeat();
    if (this.socket) {
      try {
        this.socket.close();
      } catch {}
      this.socket = null;
    }
    this.isConnected = false;
    this.isGatewayReady = false;
  }

  public async isHealthy(): Promise<boolean> {
    return this.isConnected && this.isGatewayReady && this.socket && this.socket.readyState === 1;
  }

  public async execute(options: HermesExecutionOptions): Promise<HermesExecutionResult> {
    return this.stream(options, () => {});
  }

  public async stream(
    options: HermesExecutionOptions,
    onChunk: (chunk: HermesStreamChunk) => void
  ): Promise<HermesExecutionResult> {
    if (!this.isConnected || !this.isGatewayReady) {
      await this.connect();
    }

    const execId = options.executionId || `exec_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    const timeoutMs = options.timeoutMs || this.config.timeoutMs;

    // 1. Create session or reuse provided session_id
    let sessionId = options.sessionId;
    if (!sessionId) {
      const sessionRes = await this.sendJsonRpcRequest<{ session_id: string }>('session.create', {});
      sessionId = sessionRes.session_id;
    }

    this.executionSessionMap.set(execId, sessionId);

    return new Promise((resolve, reject) => {
      const startTime = Date.now();

      const timerId = setTimeout(() => {
        this.activeExecutions.delete(sessionId!);
        this.executionSessionMap.delete(execId);
        resolve({
          executionId: execId,
          sessionId,
          status: 'timeout',
          output: pending?.outputBuffer || '',
          thought: pending?.thoughtBuffer || '',
          toolCalls: pending?.toolCalls || [],
          durationMs: Date.now() - startTime,
          error: {
            code: 'WS_TIMEOUT',
            message: `WebSocket execution timed out after ${timeoutMs}ms`,
            retryable: true,
          },
        });
      }, timeoutMs);

      const pending: PendingExecution = {
        resolve,
        reject,
        onChunk,
        options,
        sessionId: sessionId!,
        startTime,
        outputBuffer: '',
        thoughtBuffer: '',
        toolCalls: [],
        timerId,
      };

      this.activeExecutions.set(sessionId!, pending);

      if (options.abortSignal) {
        options.abortSignal.addEventListener('abort', () => {
          this.cancel(execId, 'Aborted by caller signal');
        });
      }

      // 2. Submit prompt via JSON-RPC 'prompt.submit'
      this.sendJsonRpcRequest('prompt.submit', {
        session_id: sessionId,
        text: options.prompt,
        model_override: options.modelOverride,
        provider_override: options.providerOverride,
        skills: options.skills || [],
        toolsets: options.toolsets || [],
        variables: options.variables || {},
      }).catch((err) => {
        clearTimeout(timerId);
        this.activeExecutions.delete(sessionId!);
        this.executionSessionMap.delete(execId);
        reject(new HermesTransportError(`Failed to submit prompt over JSON-RPC: ${err.message}`, {
          code: 'WS_SUBMIT_FAILED',
          transport: 'websocket',
          retryable: true,
        }));
      });
    });
  }

  public async cancel(executionId: string, reason?: string): Promise<boolean> {
    const sessionId = this.executionSessionMap.get(executionId);
    if (!sessionId) return false;

    const pending = this.activeExecutions.get(sessionId);
    if (!pending) return false;

    clearTimeout(pending.timerId);
    this.activeExecutions.delete(sessionId);
    this.executionSessionMap.delete(executionId);

    // Send prompt.cancel frame
    try {
      await this.sendJsonRpcRequest('prompt.cancel', {
        session_id: sessionId,
        reason: reason || 'Cancelled by AVENIQ Engine',
      });
    } catch {}

    pending.resolve({
      executionId,
      sessionId,
      status: 'cancelled',
      output: pending.outputBuffer,
      thought: pending.thoughtBuffer,
      toolCalls: pending.toolCalls,
      durationMs: Date.now() - pending.startTime,
    });

    return true;
  }

  /**
   * Helper to send JSON-RPC 2.0 requests and wait for matching response ID
   */
  public async sendJsonRpcRequest<T = any>(method: string, params: Record<string, any>, timeoutMs: number = 15000): Promise<T> {
    if (!this.isConnected || !this.socket) {
      throw new HermesTransportError('WebSocket is not connected', {
        code: 'WS_NOT_CONNECTED',
        transport: 'websocket',
        retryable: true,
      });
    }

    const reqId = `w${this.requestIdCounter++}`;
    const frame = {
      jsonrpc: '2.0',
      id: reqId,
      method,
      params,
    };

    return new Promise((resolve, reject) => {
      const timerId = setTimeout(() => {
        this.pendingCalls.delete(reqId);
        reject(new HermesTransportError(`JSON-RPC request '${method}' timed out (id: ${reqId})`, {
          code: 'RPC_TIMEOUT',
          transport: 'websocket',
          retryable: true,
        }));
      }, timeoutMs);

      this.pendingCalls.set(reqId, { resolve, reject, timerId });

      try {
        this.socket.send(JSON.stringify(frame));
      } catch (err: any) {
        clearTimeout(timerId);
        this.pendingCalls.delete(reqId);
        reject(new HermesTransportError(`Failed to write JSON-RPC frame: ${err.message}`, {
          code: 'RPC_WRITE_FAILED',
          transport: 'websocket',
          retryable: true,
        }));
      }
    });
  }

  private handleRawMessage(dataStr: string, onGatewayReady?: () => void): void {
    try {
      const msg = JSON.parse(dataStr);

      // 1. Check for JSON-RPC response to a pending call (`id` matches)
      if (msg.id !== undefined && msg.id !== null && this.pendingCalls.has(msg.id)) {
        const pendingCall = this.pendingCalls.get(msg.id)!;
        this.pendingCalls.delete(msg.id);
        clearTimeout(pendingCall.timerId);

        if (msg.error) {
          pendingCall.reject(new HermesTransportError(msg.error.message || 'JSON-RPC Error', {
            code: `RPC_ERROR_${msg.error.code || 'FAIL'}`,
            transport: 'websocket',
            retryable: true,
          }));
        } else {
          pendingCall.resolve(msg.result);
        }
        return;
      }

      // 2. Check for JSON-RPC Event Notifications (`method` === "event")
      if (msg.method === 'event' && msg.params) {
        const eventType = msg.params.type;
        const payload = msg.params.payload || {};
        const sessionId = msg.params.session_id || payload.session_id;

        if (eventType === 'gateway.ready') {
          if (onGatewayReady) onGatewayReady();
          return;
        }

        if (!sessionId) return;
        const pendingExec = this.activeExecutions.get(sessionId);
        if (!pendingExec) return;

        if (eventType === 'message.delta' || eventType === 'message.start') {
          const text = payload.text || payload.delta || '';
          pendingExec.outputBuffer += text;
          if (pendingExec.onChunk) {
            pendingExec.onChunk({
              type: 'token',
              content: text,
              executionId: pendingExec.options.executionId,
              timestamp: new Date().toISOString(),
              metadata: payload,
            });
          }
        } else if (eventType === 'thinking.delta' || eventType === 'reasoning.delta') {
          const text = payload.text || payload.delta || '';
          pendingExec.thoughtBuffer += text;
          if (pendingExec.onChunk) {
            pendingExec.onChunk({
              type: 'thought',
              content: text,
              executionId: pendingExec.options.executionId,
              timestamp: new Date().toISOString(),
              metadata: payload,
            });
          }
        } else if (eventType === 'tool.start' || eventType === 'tool.complete') {
          const toolCall: HermesToolCall = {
            id: payload.tool_id || `tool_${Math.random().toString(36).substring(2, 7)}`,
            name: payload.name || payload.tool || 'tool',
            arguments: payload.arguments || payload.args || {},
            status: eventType === 'tool.complete' ? 'completed' : 'running',
            result: payload.result,
            error: payload.error,
          };
          pendingExec.toolCalls.push(toolCall);
          if (pendingExec.onChunk) {
            pendingExec.onChunk({
              type: 'tool_call',
              content: JSON.stringify(toolCall),
              executionId: pendingExec.options.executionId,
              timestamp: new Date().toISOString(),
              metadata: payload,
            });
          }
        } else if (eventType === 'message.complete') {
          clearTimeout(pendingExec.timerId);
          this.activeExecutions.delete(sessionId);
          if (pendingExec.options.executionId) {
            this.executionSessionMap.delete(pendingExec.options.executionId);
          }

          if (pendingExec.onChunk) {
            pendingExec.onChunk({
              type: 'done',
              content: '[DONE]',
              executionId: pendingExec.options.executionId,
              timestamp: new Date().toISOString(),
            });
          }

          pendingExec.resolve({
            executionId: pendingExec.options.executionId || `exec_${Date.now()}`,
            sessionId,
            status: 'success',
            output: payload.text || pendingExec.outputBuffer,
            thought: payload.thought || pendingExec.thoughtBuffer,
            toolCalls: pendingExec.toolCalls,
            durationMs: Date.now() - pendingExec.startTime,
            tokenStats: payload.token_stats ? {
              inputTokens: payload.token_stats.input_tokens || 0,
              outputTokens: payload.token_stats.output_tokens || 0,
              totalTokens: payload.token_stats.total_tokens || 0,
            } : undefined,
            raw: payload,
          });
        } else if (eventType === 'error') {
          clearTimeout(pendingExec.timerId);
          this.activeExecutions.delete(sessionId);
          if (pendingExec.options.executionId) {
            this.executionSessionMap.delete(pendingExec.options.executionId);
          }

          pendingExec.resolve({
            executionId: pendingExec.options.executionId || `exec_${Date.now()}`,
            sessionId,
            status: 'failed',
            output: pendingExec.outputBuffer,
            thought: pendingExec.thoughtBuffer,
            toolCalls: pendingExec.toolCalls,
            durationMs: Date.now() - pendingExec.startTime,
            error: {
              code: payload.code || 'HERMES_WS_ERROR',
              message: payload.message || payload.error || 'Hermes Stream Error',
              retryable: true,
            },
          });
        }
      }
    } catch {}
  }

  private startHeartbeat(): void {
    this.stopHeartbeat();
    this.pingIntervalTimer = setInterval(() => {
      if (this.isConnected && this.socket && this.socket.readyState === 1) {
        try {
          this.socket.send(JSON.stringify({ jsonrpc: '2.0', method: 'ping', params: {} }));
        } catch {}
      }
    }, 25000);
  }

  private stopHeartbeat(): void {
    if (this.pingIntervalTimer) {
      clearInterval(this.pingIntervalTimer);
      this.pingIntervalTimer = null;
    }
  }

  private handleDisconnect(): void {
    for (const [id, call] of this.pendingCalls.entries()) {
      clearTimeout(call.timerId);
      call.reject(new HermesTransportError('WebSocket disconnected during RPC call', {
        code: 'WS_DISCONNECTED',
        transport: 'websocket',
        retryable: true,
      }));
    }
    this.pendingCalls.clear();

    for (const [sessionId, pending] of this.activeExecutions.entries()) {
      clearTimeout(pending.timerId);
      pending.resolve({
        executionId: pending.options.executionId || `exec_${Date.now()}`,
        sessionId,
        status: 'failed',
        output: pending.outputBuffer,
        thought: pending.thoughtBuffer,
        toolCalls: pending.toolCalls,
        durationMs: Date.now() - pending.startTime,
        error: {
          code: 'WS_DISCONNECTED',
          message: 'WebSocket connection lost during prompt execution',
          retryable: true,
        },
      });
    }
    this.activeExecutions.clear();
    this.executionSessionMap.clear();
  }
}
