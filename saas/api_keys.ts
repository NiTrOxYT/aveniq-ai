/**
 * AVENIQ AI — SaaS API Key Management Engine
 */

import { ApiKey } from './types';

export class ApiKeyManager {
  private keys: Map<string, ApiKey> = new Map(); // keyHash -> ApiKey

  public createKey(orgId: string, name: string, scopes: string[] = ['workflows:write', 'executions:write'], projectId?: string): { apiKey: ApiKey; rawKey: string } {
    const rawKey = `aq_live_${Date.now()}_${Math.random().toString(36).substring(2, 16)}`;
    const keyHash = ((globalThis as any).Buffer ? (globalThis as any).Buffer.from(rawKey).toString('base64') : btoa(rawKey));
    const keyPrefix = rawKey.substring(0, 15) + '...';

    const apiKey: ApiKey = {
      id: `key_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
      orgId,
      projectId,
      keyHash,
      keyPrefix,
      name,
      scopes,
      createdAt: new Date().toISOString(),
    };

    this.keys.set(keyHash, apiKey);
    return { apiKey, rawKey };
  }

  public validateKey(rawKey: string, requiredScope?: string): ApiKey {
    const keyHash = ((globalThis as any).Buffer ? (globalThis as any).Buffer.from(rawKey).toString('base64') : btoa(rawKey));
    const apiKey = this.keys.get(keyHash);

    if (!apiKey) {
      throw new Error('Invalid API Key.');
    }

    if (apiKey.expiresAt && new Date(apiKey.expiresAt) < new Date()) {
      throw new Error('API Key has expired.');
    }

    if (requiredScope && !apiKey.scopes.includes(requiredScope)) {
      throw new Error(`API Key lacks required scope '${requiredScope}'.`);
    }

    apiKey.lastUsedAt = new Date().toISOString();
    return apiKey;
  }

  public revokeKey(keyId: string): boolean {
    for (const [hash, key] of this.keys.entries()) {
      if (key.id === keyId) {
        this.keys.delete(hash);
        return true;
      }
    }
    return false;
  }
}
