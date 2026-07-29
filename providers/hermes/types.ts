/**
 * AVENIQ AI — Hermes Integration Layer
 * Core Type Definitions & Transport Interfaces
 */

export type HermesTransportType = 'http' | 'websocket' | 'mcp';

export interface HermesConfig {
  baseUrl: string;
  wsUrl: string;
  mcpEndpoint: string;
  defaultTransport: HermesTransportType;
  timeoutMs: number;
  authToken?: string;
  headers?: Record<string, string>;
  capabilities?: HermesCapability[];
}

export type HermesCapability = 
  | 'browser'
  | 'terminal'
  | 'filesystem'
  | 'vision'
  | 'skills'
  | 'mcp';

export type HermesModelProvider = 
  | 'gemini'
  | 'deepseek'
  | 'claude'
  | 'groq'
  | 'openrouter'
  | 'ollama';

export interface HermesExecutionOptions {
  prompt: string;
  sessionId?: string;
  executionId?: string;
  modelOverride?: string;
  providerOverride?: HermesModelProvider | string;
  skills?: string[];
  toolsets?: string[];
  variables?: Record<string, any>;
  timeoutMs?: number;
  abortSignal?: AbortSignal;
  transport?: HermesTransportType;
  onStreamChunk?: (chunk: HermesStreamChunk) => void;
}

export type HermesChunkType = 
  | 'token'
  | 'thought'
  | 'tool_call'
  | 'tool_result'
  | 'status'
  | 'error'
  | 'done';

export interface HermesStreamChunk {
  type: HermesChunkType;
  content: string;
  nodeId?: string;
  executionId?: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

export interface HermesToolCall {
  id: string;
  name: string;
  arguments: Record<string, any>;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
}

export interface HermesTokenStats {
  inputTokens: number;
  outputTokens: number;
  totalTokens: number;
}

export interface HermesExecutionResult {
  executionId: string;
  sessionId?: string;
  status: 'success' | 'failed' | 'cancelled' | 'timeout';
  output: string;
  thought?: string;
  toolCalls: HermesToolCall[];
  durationMs: number;
  tokenStats?: HermesTokenStats;
  error?: {
    code: string;
    message: string;
    details?: any;
    retryable: boolean;
  };
  raw?: any;
}

export interface HermesToolDefinition {
  name: string;
  description: string;
  parameters: Record<string, any>;
  category?: string;
  enabled: boolean;
}

export interface IHermesTransport {
  readonly name: HermesTransportType;
  connect(): Promise<void>;
  disconnect(): Promise<void>;
  execute(options: HermesExecutionOptions): Promise<HermesExecutionResult>;
  stream(
    options: HermesExecutionOptions,
    onChunk: (chunk: HermesStreamChunk) => void
  ): Promise<HermesExecutionResult>;
  cancel(executionId: string, reason?: string): Promise<boolean>;
  isHealthy(): Promise<boolean>;
}

export interface IHermesAdapter {
  getTransport(type?: HermesTransportType): IHermesTransport;
  execute(options: HermesExecutionOptions): Promise<HermesExecutionResult>;
  stream(
    options: HermesExecutionOptions,
    onChunk: (chunk: HermesStreamChunk) => void
  ): Promise<HermesExecutionResult>;
  cancel(executionId: string, reason?: string): Promise<boolean>;
  checkHealth(): Promise<Record<HermesTransportType, boolean>>;
  dispose(): Promise<void>;
}

export class HermesTransportError extends Error {
  public readonly code: string;
  public readonly transport: HermesTransportType;
  public readonly retryable: boolean;
  public readonly status?: number;

  constructor(message: string, options: { code: string; transport: HermesTransportType; retryable?: boolean; status?: number }) {
    super(message);
    this.name = 'HermesTransportError';
    this.code = options.code;
    this.transport = options.transport;
    this.retryable = options.retryable ?? true;
    this.status = options.status;
  }
}
