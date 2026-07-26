/**
 * Unified REST API Client for AVENIQ Customer Portal.
 * Connects web portal to Workflow OS (8092), Automation (8093), Analytics (8094), Workspace (8095), Publishing (8096), and Dashboard API (8097).
 */

class AVENIQApiClient {
    constructor() {
        this.basePorts = {
            workflow: 8092,
            automation: 8093,
            analytics: 8094,
            workspace: 8095,
            publishing: 8096,
            dashboard: 8097
        };
    }

    async get(service, endpoint) {
        const port = this.basePorts[service] || 8097;
        try {
            const res = await fetch(`http://localhost:${port}${endpoint}`);
            return await res.json();
        } catch (err) {
            console.warn(`Fetch error for ${service}:${endpoint}:`, err);
            return { error: err.message };
        }
    }

    async post(service, endpoint, payload = {}) {
        const port = this.basePorts[service] || 8097;
        try {
            const res = await fetch(`http://localhost:${port}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            return await res.json();
        } catch (err) {
            console.warn(`Post error for ${service}:${endpoint}:`, err);
            return { error: err.message };
        }
    }

    async getOverview() { return this.get('dashboard', '/dashboard/overview'); }
    async runDailyCycle() { return this.post('automation', '/automation/run'); }
    async approveCampaign(sessionId) { return this.post('automation', '/automation/approve', { session_id: sessionId }); }
    async publishCampaign(channel) { return this.post('publishing', '/publish', { channel }); }
    async getAnalyticsReport() { return this.get('analytics', '/analytics/reports'); }
    async getWorkspaces() { return this.get('workspace', '/workspace'); }
}

window.apiClient = new AVENIQApiClient();
