/**
 * AVENIQ AI — Hermes Integration Layer
 * Primary Adapter Interface & Multi-Transport Facade
 */

import { HermesHttpTransport } from './http';
import { HermesMcpTransport } from './mcp';
import {
  HermesConfig,
  HermesExecutionOptions,
  HermesExecutionResult,
  HermesModelProvider,
  HermesStreamChunk,
  HermesTransportType,
  IHermesAdapter,
  IHermesTransport,
} from './types';
import { HermesWebSocketTransport } from './websocket';

export class HermesAdapter implements IHermesAdapter {
  private config: HermesConfig;
  private transports: Map<HermesTransportType, IHermesTransport> = new Map();

  constructor(customConfig?: Partial<HermesConfig>) {
    const env = ((globalThis as any).process?.env) || {};
    this.config = {
      baseUrl: env.HERMES_BASE_URL || 'http://127.0.0.1:9119',
      wsUrl: env.HERMES_WS_URL || 'ws://127.0.0.1:9119/api/ws',
      mcpEndpoint: env.HERMES_MCP_ENDPOINT || '/api/mcp',
      defaultTransport: 'websocket',
      timeoutMs: 30000,
      headers: {},
      capabilities: ['browser', 'terminal', 'filesystem', 'vision', 'skills', 'mcp'],
      ...customConfig,
    };

    this.transports.set('http', new HermesHttpTransport(this.config));
    this.transports.set('websocket', new HermesWebSocketTransport(this.config));
    this.transports.set('mcp', new HermesMcpTransport(this.config));
  }

  /**
   * Get transport instance by type
   */
  public getTransport(type?: HermesTransportType): IHermesTransport {
    const transportType = type || this.config.defaultTransport;
    const transport = this.transports.get(transportType);
    if (!transport) {
      throw new Error(`Transport '${transportType}' is not configured in HermesAdapter.`);
    }
    return transport;
  }

  /**
   * Execute task with provider routing and transport abstraction
   */
  public async execute(options: HermesExecutionOptions): Promise<HermesExecutionResult> {
    const enrichedOptions = this.applyProviderRouting(options);
    const transportType = options.transport || this.config.defaultTransport;
    const transport = this.getTransport(transportType);

    try {
      return await transport.execute(enrichedOptions);
    } catch (primaryErr: any) {
      // Fallback chain: Default transport -> HTTP -> secondary provider fallback
      if (transportType !== 'http') {
        try {
          const httpFallback = this.getTransport('http');
          return await httpFallback.execute(enrichedOptions);
        } catch {}
      }
      throw primaryErr;
    }
  }

  /**
   * Stream execution with provider routing
   */
  public async stream(
    options: HermesExecutionOptions,
    onChunk: (chunk: HermesStreamChunk) => void
  ): Promise<HermesExecutionResult> {
    const enrichedOptions = this.applyProviderRouting(options);
    const transportType = options.transport || this.config.defaultTransport;
    const transport = this.getTransport(transportType);

    try {
      return await transport.stream(enrichedOptions, onChunk);
    } catch (primaryErr: any) {
      // Fallback to HTTP stream if WebSocket stream fails
      if (transportType === 'websocket') {
        try {
          const httpFallback = this.getTransport('http');
          return await httpFallback.stream(enrichedOptions, onChunk);
        } catch {}
      }
      throw primaryErr;
    }
  }

  /**
   * Cancel execution across all active transports
   */
  public async cancel(executionId: string, reason?: string): Promise<boolean> {
    const results = await Promise.all(
      Array.from(this.transports.values()).map((t) => t.cancel(executionId, reason))
    );
    return results.some((success) => success);
  }

  /**
   * Health check status of all transports
   */
  public async checkHealth(): Promise<Record<HermesTransportType, boolean>> {
    const healthMap: Record<HermesTransportType, boolean> = {
      http: false,
      websocket: false,
      mcp: false,
    };

    for (const [type, transport] of this.transports.entries()) {
      try {
        healthMap[type] = await transport.isHealthy();
      } catch {
        healthMap[type] = false;
      }
    }

    return healthMap;
  }

  /**
   * Cleanup transport connections
   */
  public async dispose(): Promise<void> {
    for (const transport of this.transports.values()) {
      try {
        await transport.disconnect();
      } catch {}
    }
    this.transports.clear();
  }

  /**
   * Apply AVENIQ Model & Provider Routing Architecture:
   * - Research -> Gemini
   * - Coding -> DeepSeek
   * - Creative -> Claude
   * - Fast -> Groq / Llama
   * Fallback chain: Gemini -> Groq -> OpenRouter -> Ollama
   */
  private applyProviderRouting(options: HermesExecutionOptions): HermesExecutionOptions {
    if (options.providerOverride) {
      return options;
    }

    const promptLower = options.prompt.toLowerCase();
    let provider: HermesModelProvider = 'gemini';
    let model: string | undefined = options.modelOverride;

    if (promptLower.includes('code') || promptLower.includes('function') || promptLower.includes('refactor') || promptLower.includes('debug')) {
      provider = 'deepseek';
      model = model || 'deepseek-reasoner';
    } else if (promptLower.includes('creative') || promptLower.includes('copy') || promptLower.includes('article') || promptLower.includes('story')) {
      provider = 'claude';
      model = model || 'claude-3-5-sonnet';
    } else if (promptLower.includes('fast') || promptLower.includes('quick') || promptLower.includes('summary')) {
      provider = 'groq';
      model = model || 'llama3-70b-8192';
    } else {
      provider = 'gemini';
      model = model || 'gemini-2.5-pro';
    }

    return {
      ...options,
      providerOverride: provider,
      modelOverride: model,
    };
  }
}
