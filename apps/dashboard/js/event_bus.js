/**
 * Live SSE Event Bus for AVENIQ Web Dashboard.
 * Broadcasts real-time workflow, publishing, approval, and analytics updates across frontend modules.
 */

(function () {
    'use strict';

    class LiveEventBus {
        constructor() {
            this.listeners = {};
            this.sseSource = null;
        }

        on(eventType, callback) {
            if (!this.listeners[eventType]) {
                this.listeners[eventType] = [];
            }
            this.listeners[eventType].push(callback);
        }

        emit(eventType, data) {
            if (this.listeners[eventType]) {
                this.listeners[eventType].forEach(cb => cb(data));
            }
        }

        connectSSE(sseUrl = '/dashboard/sse') {
            try {
                this.sseSource = new EventSource(sseUrl);
                this.sseSource.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    this.emit(data.event_type || 'update', data);
                };
                this.sseSource.onerror = () => {
                    console.log('SSE Reconnecting...');
                };
            } catch (e) {
                console.warn('SSE EventSource not supported in current environment; falling back to local bus.');
            }
        }
    }

    const liveEventBus = new LiveEventBus();

    if (window.AVENIQ_APP && typeof window.AVENIQ_APP.register === 'function') {
        window.AVENIQ_APP.register('eventBus', liveEventBus);
    }

    window.liveEventBus = liveEventBus;
})();
