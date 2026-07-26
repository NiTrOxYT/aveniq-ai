/**
 * Unified Relative-Origin REST API Client for AVENIQ Customer Portal.
 * Uses window.location.origin for relative routing over custom domains, HTTPS reverse proxies,
 * Cloudflare Tunnels, Tailscale, VPNs, and local environments.
 */

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
            console.warn(`Fetch error for ${endpoint}:`, err);
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
            console.warn(`Post error for ${endpoint}:`, err);
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
}

window.AVENIQ_API = new AVENIQApiClient();
window.apiClient = window.AVENIQ_API;
