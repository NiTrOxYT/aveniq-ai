/**
 * AVENIQ AI — Provider Registry
 * Manages provider adapters (Hermes, Gemini, Claude, DeepSeek, Groq)
 * and resolves provider instances for workflow node execution.
 */

import { HermesAdapter } from './hermes/adapter';
import { IHermesAdapter } from './hermes/types';

export interface IExecutionProvider {
  name: string;
  isHealthy(): Promise<boolean>;
  execute(options: any): Promise<any>;
  stream(options: any, onChunk: (chunk: any) => void): Promise<any>;
  cancel(executionId: string, reason?: string): Promise<boolean>;
}

export class ProviderRegistry {
  private static instance: ProviderRegistry;
  private providers: Map<string, IExecutionProvider> = new Map();
  private fallbackChain: string[] = ['gemini', 'groq', 'openrouter', 'ollama'];

  private constructor() {
    // Register Hermes adapter as default provider
    this.register('hermes', new HermesAdapter() as unknown as IExecutionProvider);
  }

  public static getInstance(): ProviderRegistry {
    if (!ProviderRegistry.instance) {
      ProviderRegistry.instance = new ProviderRegistry();
    }
    return ProviderRegistry.instance;
  }

  /**
   * Register a provider instance
   */
  public register(name: string, provider: IExecutionProvider): void {
    this.providers.set(name.toLowerCase(), provider);
  }

  /**
   * Resolve a registered provider by name
   */
  public resolve(name: string): IExecutionProvider {
    const key = name.toLowerCase();
    const provider = this.providers.get(key);
    if (!provider) {
      // Fallback to Hermes adapter if provider not explicitly registered
      const hermes = this.providers.get('hermes');
      if (hermes) return hermes;
      throw new Error(`Provider '${name}' is not registered in ProviderRegistry.`);
    }
    return provider;
  }

  /**
   * Check health of all registered providers
   */
  public async checkHealthAll(): Promise<Record<string, boolean>> {
    const healthMap: Record<string, boolean> = {};
    for (const [name, provider] of this.providers.entries()) {
      try {
        healthMap[name] = await provider.isHealthy();
      } catch {
        healthMap[name] = false;
      }
    }
    return healthMap;
  }

  /**
   * Get AVENIQ provider fallback order
   */
  public getFallbackChain(): string[] {
    return [...this.fallbackChain];
  }

  /**
   * Unregister provider
   */
  public unregister(name: string): void {
    this.providers.delete(name.toLowerCase());
  }
}
