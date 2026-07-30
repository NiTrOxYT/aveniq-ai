/**
 * AVENIQ AI — Real Google Gemini Provider Adapter
 * Direct, production-grade integration with Google Gemini API
 */

import fs from 'fs';
import path from 'path';

export interface GeminiAdapterConfig {
  apiKey?: string;
  primaryModel?: string;
  fallbackModels?: string[];
  timeoutMs?: number;
}

export class GeminiAdapter {
  public readonly name = 'gemini';
  private apiKey: string;
  private primaryModel: string;
  private fallbackModels: string[];
  private timeoutMs: number;

  constructor(customConfig?: Partial<GeminiAdapterConfig>) {
    let envKey = process.env.GEMINI_API_KEY;
    let envPrimary = process.env.GEMINI_PRIMARY_MODEL;
    let envFallback = process.env.GEMINI_FALLBACK_MODELS;

    if (!envKey) {
      try {
        const envPath = path.resolve(process.cwd(), '.env');
        if (fs.existsSync(envPath)) {
          const content = fs.readFileSync(envPath, 'utf8');
          for (const line of content.split('\n')) {
            const trimmed = line.trim();
            if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
              const [k, v] = trimmed.split('=', 2);
              if (k.trim() === 'GEMINI_API_KEY') envKey = v.trim();
              if (k.trim() === 'GEMINI_PRIMARY_MODEL') envPrimary = v.trim();
              if (k.trim() === 'GEMINI_FALLBACK_MODELS') envFallback = v.trim();
            }
          }
        }
      } catch {}
    }

    this.apiKey = customConfig?.apiKey || envKey || '';
    this.primaryModel = customConfig?.primaryModel || envPrimary || 'gemma-4-26b-a4b-it';
    const fallbackStr = envFallback || 'gemma-4-31b-it,gemini-2.5-pro,gemini-2.0-flash';
    this.fallbackModels = customConfig?.fallbackModels || fallbackStr.split(',').map((s) => s.trim()).filter(Boolean);
    this.timeoutMs = customConfig?.timeoutMs || 45000;
  }

  public getCandidateModels(): string[] {
    const candidates = [this.primaryModel];
    for (const fb of this.fallbackModels) {
      if (!candidates.includes(fb)) {
        candidates.push(fb);
      }
    }
    return candidates;
  }

  public async isHealthy(): Promise<boolean> {
    if (!this.apiKey) return false;
    try {
      const candidates = this.getCandidateModels();
      for (const model of candidates) {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${this.apiKey}`;
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ contents: [{ parts: [{ text: 'ready' }] }] }),
        });
        if (res.ok) return true;
      }
      return false;
    } catch {
      return false;
    }
  }

  public async execute(options: any): Promise<any> {
    return this.stream(options, () => {});
  }

  public async stream(options: any, onChunk: (chunk: any) => void): Promise<any> {
    const startTime = Date.now();
    const execId = options.executionId || `exec_${Date.now()}`;
    const prompt = options.prompt || '';
    const candidates = this.getCandidateModels();

    if (!this.apiKey) {
      return {
        executionId: execId,
        status: 'failed',
        output: '',
        durationMs: Date.now() - startTime,
        error: { code: 'NO_API_KEY', message: 'GEMINI_API_KEY is missing' },
      };
    }

    let lastError: any = null;

    for (const model of candidates) {
      try {
        const streamUrl = `https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?key=${this.apiKey}&alt=sse`;
        const response = await fetch(streamUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
        });

        if (!response.ok) {
          // Fallback to sync endpoint if stream sse endpoint fails
          const syncUrl = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${this.apiKey}`;
          const syncRes = await fetch(syncUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
          });

          if (!syncRes.ok) {
            const errText = await syncRes.text();
            lastError = new Error(`Gemini API model ${model} failed (${syncRes.status}): ${errText.substring(0, 150)}`);
            continue;
          }

          const syncData = await syncRes.json();
          const text = syncData?.candidates?.[0]?.content?.parts?.[0]?.text || '';
          onChunk({ type: 'token', content: text });

          return {
            executionId: execId,
            status: 'success',
            output: text,
            durationMs: Date.now() - startTime,
            tokenStats: {
              promptTokens: syncData?.usageMetadata?.promptTokenCount || Math.ceil(prompt.length / 4),
              completionTokens: syncData?.usageMetadata?.candidatesTokenCount || Math.ceil(text.length / 4),
              totalTokens: syncData?.usageMetadata?.totalTokenCount || (Math.ceil(prompt.length / 4) + Math.ceil(text.length / 4)),
            },
          };
        }

        if (!response.body) continue;

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let fullOutput = '';
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';

          for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed || !trimmed.startsWith('data: ')) continue;
            const raw = trimmed.substring(6);
            if (raw === '[DONE]') continue;

            try {
              const parsed = JSON.parse(raw);
              const chunkText = parsed?.candidates?.[0]?.content?.parts?.[0]?.text || '';
              if (chunkText) {
                fullOutput += chunkText;
                onChunk({ type: 'token', content: chunkText });
              }
            } catch {}
          }
        }

        if (!fullOutput && buffer) {
          try {
            const parsed = JSON.parse(buffer.replace(/^data:\s*/, ''));
            const chunkText = parsed?.candidates?.[0]?.content?.parts?.[0]?.text || '';
            if (chunkText) fullOutput += chunkText;
          } catch {}
        }

        return {
          executionId: execId,
          status: 'success',
          output: fullOutput,
          durationMs: Date.now() - startTime,
          tokenStats: {
            promptTokens: Math.ceil(prompt.length / 4),
            completionTokens: Math.ceil(fullOutput.length / 4),
            totalTokens: Math.ceil((prompt.length + fullOutput.length) / 4),
          },
        };
      } catch (err: any) {
        lastError = err;
      }
    }

    return {
      executionId: execId,
      status: 'failed',
      output: '',
      durationMs: Date.now() - startTime,
      error: { code: 'ALL_MODELS_FAILED', message: lastError?.message || 'All Gemini models failed' },
    };
  }

  public async cancel(executionId: string, reason?: string): Promise<boolean> {
    return true;
  }
}
