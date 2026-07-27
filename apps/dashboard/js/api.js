/**
 * Unified Relative-Origin REST API Client for AVENIQ Customer Portal.
 * Integrates with window.AVENIQ_APP Dependency Registry for deterministic initialization.
 * Includes live integration checks & real test dispatchers for Telegram, Gemini, and Google Imagen 3 API.
 */

(function () {
    'use strict';

    class AVENIQApiClient {
        constructor() {
            this.origin = (typeof window !== 'undefined' && window.location && window.location.origin) ? window.location.origin : '';
        }

        async get(endpoint) {
            try {
                const res = await fetch(`${this.origin}${endpoint}`);
                if (!res.ok) {
                    return { error: `HTTP ${res.status}` };
                }
                return await res.json();
            } catch (err) {
                console.warn(`[AVENIQ API] Fetch error for ${endpoint}:`, err);
                return { error: err.message };
            }
        }

        async post(endpoint, payload = {}) {
            try {
                const res = await fetch(`${this.origin}${endpoint}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                return await res.json();
            } catch (err) {
                console.warn(`[AVENIQ API] Post error for ${endpoint}:`, err);
                return { error: err.message };
            }
        }

        async getOverview() { return this.get('/dashboard/overview'); }
        async getActivity() { return this.get('/dashboard/activity'); }
        async getApprovals() { return this.get('/dashboard/approvals'); }
        async getAnalytics() { return this.get('/dashboard/analytics'); }
        async getReasoning() { return this.get('/dashboard/reasoning'); }
        async getVersions() { return this.get('/dashboard/versions'); }
        async getHealth() { return this.get('/dashboard/health'); }
        async getConnections() { return this.get('/dashboard/connections'); }

        async testTelegram() { return this.post('/dashboard/test/telegram'); }
        async testGemini() { return this.post('/dashboard/test/gemini'); }
        async testImagen() { return this.post('/dashboard/test/imagen'); }
    }

    const apiClient = new AVENIQApiClient();

    // Register with AVENIQ_APP registry
    if (window.AVENIQ_APP && typeof window.AVENIQ_APP.register === 'function') {
        window.AVENIQ_APP.register('api', apiClient);
    }

    // Global backwards-compatibility exports
    window.AVENIQ_API = apiClient;
    window.apiClient = apiClient;
})();
