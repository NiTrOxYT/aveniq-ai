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

        async request(endpoint, method = 'GET', payload = null) {
            try {
                const options = { method, headers: { 'Content-Type': 'application/json' } };
                if (payload && method !== 'GET') {
                    options.body = JSON.stringify(payload);
                }
                const res = await fetch(`${this.origin}${endpoint}`, options);
                return await res.json();
            } catch (err) {
                console.warn(`[AVENIQ API] ${method} error for ${endpoint}:`, err);
                return { error: err.message };
            }
        }

        async put(endpoint, payload = {}) { return this.request(endpoint, 'PUT', payload); }
        async delete(endpoint) { return this.request(endpoint, 'DELETE'); }
        async patch(endpoint, payload = {}) { return this.request(endpoint, 'PATCH', payload); }

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

        // Automation Schedule Management APIs
        async getSchedules(query = '', department = '', state = '') {
            const params = new URLSearchParams();
            if (query) params.append('q', query);
            if (department) params.append('department', department);
            if (state) params.append('state', state);
            const qStr = params.toString() ? `?${params.toString()}` : '';
            return this.get(`/api/automation/schedules${qStr}`);
        }
        async getScheduleSummary() { return this.get('/api/automation/schedules/summary'); }
        async createSchedule(data) { return this.post('/api/automation/schedules', data); }
        async updateSchedule(id, data) { return this.put(`/api/automation/schedules/${id}`, data); }
        async deleteSchedule(id) { return this.delete(`/api/automation/schedules/${id}`); }
        async toggleSchedule(id, state = null, enabled = null) { return this.patch(`/api/automation/schedules/${id}/toggle`, { state, enabled }); }
        async runSchedule(id) { return this.post(`/api/automation/schedules/${id}/run`); }
        async duplicateSchedule(id) { return this.post(`/api/automation/schedules/${id}/duplicate`); }
        async getScheduleHistory(id) { return this.get(`/api/automation/schedules/${id}/history`); }
        async bulkSchedules(action, schedule_ids) { return this.post('/api/automation/schedules/bulk', { action, schedule_ids }); }
        async exportSchedules(schedule_ids = null) {
            const endpoint = schedule_ids ? `/api/automation/schedules/export?id=${schedule_ids.join(',')}` : '/api/automation/schedules/export';
            return this.get(endpoint);
        }
        async importSchedules(schedules) { return this.post('/api/automation/schedules/import', { schedules }); }
        async previewSchedule(data) { return this.post('/api/automation/preview', data); }

        // Runtime state — single source of truth for all dashboard widgets
        async getAutomationRuntime() { return this.get('/api/automation/runtime'); }
        async getAutomationEvents(limit = 50) { return this.get(`/api/automation/events?limit=${limit}`); }
        async cancelAutomation() { return this.post('/api/automation/cancel', {}); }
        async resumeAutomation(scheduleId, fromStageIndex) {
            return this.post('/api/automation/resume', { schedule_id: scheduleId, from_stage_index: fromStageIndex });
        }
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
