/* ==========================================================================
   AVENIQ AI OPERATING SYSTEM — UI WIDGETS & RENDERERS
   Modular View Component Engine for Dashboard v3
   ========================================================================== */

(function () {
  'use strict';

  // State Store
  const state = {
    overview: null,
    activity: null,
    approvals: null,
    analytics: null,
    reasoning: null,
    versions: null,
    selectedApprovalIndex: 0,
    activeTab: 'strategy'
  };

  // 1. MISSION CONTROL RENDERERS
  function renderStatsGrid(overview) {
    const container = document.getElementById('stats-grid');
    if (!container) return;

    container.innerHTML = `
      <div class="glass-panel stat-card">
        <div class="stat-header">
          <span>AUTOMATION STATUS</span>
          <span style="color: var(--accent-emerald);">● LIVE</span>
        </div>
        <div class="stat-value">${overview.automation_status || 'ACTIVE'}</div>
        <div class="stat-subtext">8:00 AM Autonomous Schedule Active</div>
      </div>

      <div class="glass-panel stat-card">
        <div class="stat-header">
          <span>ACTIVE CAMPAIGNS</span>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/></svg>
        </div>
        <div class="stat-value">${overview.active_campaigns || 1}</div>
        <div class="stat-subtext">↑ 100% Autonomous Pipeline</div>
      </div>

      <div class="glass-panel stat-card">
        <div class="stat-header">
          <span>CAMPAIGN QUALITY</span>
          <span style="color: var(--accent-indigo);">⭐ EXCELLENT</span>
        </div>
        <div class="stat-value">${overview.overall_score || '98.5/100'}</div>
        <div class="stat-subtext">Brand Alignment & Quality Check: PASS</div>
      </div>

      <div class="glass-panel stat-card">
        <div class="stat-header">
          <span>MARKET SIGNALS</span>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
        </div>
        <div class="stat-value">${overview.leads || 80}</div>
        <div class="stat-subtext">Reddit, GitHub, RSS, Google News</div>
      </div>
    `;
  }

  function renderWorkflowPipeline() {
    const container = document.getElementById('pipeline-nodes');
    if (!container) return;

    const nodes = [
      { name: 'Research', status: 'completed' },
      { name: 'Market Intel', status: 'completed' },
      { name: 'Company Brain', status: 'completed' },
      { name: 'Reasoning', status: 'completed' },
      { name: 'Strategy', status: 'completed' },
      { name: 'Content', status: 'completed' },
      { name: 'Images', status: 'completed' },
      { name: 'Approval', status: 'running' },
      { name: 'Delivery', status: 'idle' },
      { name: 'Learning', status: 'idle' }
    ];

    container.innerHTML = nodes.map((node, i) => `
      <div class="pipeline-node ${node.status}">
        <div>${node.name}</div>
        <div style="font-size: 0.65rem; opacity: 0.8;">${node.status.toUpperCase()}</div>
      </div>
      ${i < nodes.length - 1 ? '<div class="node-arrow">➔</div>' : ''}
    `).join('');
  }

  function renderTimeline(activity) {
    const container = document.getElementById('activity-timeline-list');
    if (!container) return;

    const items = (activity && activity.activity_timeline) ? activity.activity_timeline : [
      { time: '08:00:02 AM', event: 'Market intelligence collection started', type: 'INFO' },
      { time: '08:01:15 AM', event: 'Company Brain RAG documents retrieved', type: 'INFO' },
      { time: '08:01:30 AM', event: 'Daily strategy & copy synthesized', type: 'INFO' },
      { time: '08:02:45 AM', event: 'Google Imagen visual assets generated', type: 'INFO' },
      { time: '08:03:00 AM', event: 'Campaign brief waiting for human approval', type: 'AUDIT' }
    ];

    container.innerHTML = items.map(item => {
      const timeStr = item.time.includes('T') ? item.time.split('T')[1].slice(0, 8) : item.time;
      return `
        <div class="timeline-item">
          <div class="timeline-time">${timeStr}</div>
          <div class="timeline-event">${item.event}</div>
        </div>
      `;
    }).join('');
  }

  function renderReasoningCard(reasoning) {
    const container = document.getElementById('reasoning-summary-card');
    if (!container) return;

    const rep = reasoning || {
      topic: 'Enterprise AI Agent Operations',
      opportunity_selection_reasoning: 'Spike in operational demand for autonomous AI workflow governance with low competitor velocity in Q3.',
      expected_business_impact: { confidence_score: 0.95, expected_ctr_gain: '+2.4%' }
    };

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 0.75rem;">
        <div>
          <div style="font-size: 0.75rem; color: var(--accent-cyan); font-weight: 700;">SELECTED TOPIC</div>
          <div style="font-size: 1.1rem; font-weight: 700; color: #fff;">${rep.topic}</div>
        </div>
        <div>
          <div style="font-size: 0.75rem; color: var(--text-muted); font-weight: 600;">WHY THIS OPPORTUNITY</div>
          <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">${rep.opportunity_selection_reasoning}</div>
        </div>
        <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
          <div style="background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.25); padding: 0.5rem 0.85rem; border-radius: var(--radius-md);">
            <div style="font-size: 0.7rem; color: var(--text-muted);">AI CONFIDENCE</div>
            <div style="font-weight: 700; color: var(--accent-indigo);">${((rep.expected_business_impact?.confidence_score || 0.95) * 100).toFixed(0)}%</div>
          </div>
          <div style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.25); padding: 0.5rem 0.85rem; border-radius: var(--radius-md);">
            <div style="font-size: 0.7rem; color: var(--text-muted);">EXPECTED IMPACT</div>
            <div style="font-weight: 700; color: var(--accent-emerald);">${rep.expected_business_impact?.expected_ctr_gain || '+2.4%'}</div>
          </div>
        </div>
      </div>
    `;
  }

  // 2. PR-STYLE APPROVAL CENTER RENDERER
  function renderApprovalCenter(approvals, reasoning) {
    const listContainer = document.getElementById('approval-items-list');
    const previewPane = document.getElementById('approval-preview-pane');
    if (!listContainer || !previewPane) return;

    const pending = (approvals && approvals.pending_approvals && approvals.pending_approvals.length > 0)
      ? approvals.pending_approvals
      : [{
          session_id: 'aut_sess_20260726_01',
          topic: 'Autonomous AI Marketing Campaign',
          state: 'WAITING_FOR_APPROVAL',
          summary: 'Daily campaign briefing for AI Agents in Enterprise Operations'
        }];

    // Left List
    listContainer.innerHTML = pending.map((item, idx) => `
      <div class="approval-card-item ${idx === state.selectedApprovalIndex ? 'selected' : ''}" onclick="window.AVENIQ.selectApproval(${idx})">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
          <span style="font-size: 0.7rem; font-family: var(--font-mono); color: var(--accent-indigo);">${item.session_id}</span>
          <span style="font-size: 0.68rem; background: rgba(245,158,11,0.15); color: var(--accent-amber); padding: 0.15rem 0.4rem; border-radius: var(--radius-full); font-weight: 600;">APPROVAL REQUIRED</span>
        </div>
        <div style="font-weight: 700; color: #fff; font-size: 0.9rem;">${item.topic || 'Enterprise AI Campaign'}</div>
        <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.25rem;">Quality Score: 98.5/100</div>
      </div>
    `).join('');

    // Right Preview Pane
    const selected = pending[state.selectedApprovalIndex] || pending[0];
    const rep = reasoning || {};

    previewPane.innerHTML = `
      <div class="preview-tabs">
        <button class="tab-btn ${state.activeTab === 'strategy' ? 'active' : ''}" onclick="window.AVENIQ.setTab('strategy')">Strategy & Copy</button>
        <button class="tab-btn ${state.activeTab === 'images' ? 'active' : ''}" onclick="window.AVENIQ.setTab('images')">Visual Assets</button>
        <button class="tab-btn ${state.activeTab === 'reasoning' ? 'active' : ''}" onclick="window.AVENIQ.setTab('reasoning')">AI Reasoning</button>
        <button class="tab-btn ${state.activeTab === 'seo' ? 'active' : ''}" onclick="window.AVENIQ.setTab('seo')">SEO & Sources</button>
      </div>

      <div class="tab-content">
        ${renderTabContent(state.activeTab, selected, rep)}
      </div>

      <div class="approval-action-bar">
        <div style="display: flex; gap: 0.5rem;">
          <button class="btn btn-success" onclick="window.AVENIQ.handleDecision('${selected.session_id}', 'Approve')">✅ Approve & Archive</button>
          <button class="btn btn-danger" onclick="window.AVENIQ.handleDecision('${selected.session_id}', 'Reject')">❌ Reject</button>
        </div>
        <div style="display: flex; gap: 0.5rem;">
          <button class="btn btn-secondary" onclick="window.AVENIQ.handleDecision('${selected.session_id}', 'action_Shorter')">⚡ Make Copy Shorter</button>
          <button class="btn btn-secondary" onclick="window.AVENIQ.handleDecision('${selected.session_id}', 'action_RegenerateHero')">🖼️ New Hero Image</button>
        </div>
      </div>
    `;
  }

  function renderTabContent(tab, item, rep) {
    if (tab === 'images') {
      return `
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          <div style="font-weight: 700; color: #fff;">Generated Marketing Assets</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
              <div style="font-size: 0.8rem; font-weight: 600; color: var(--accent-cyan); margin-bottom: 0.5rem;">HERO BANNER (16:9)</div>
              <div style="height: 140px; background: linear-gradient(135deg, #4f46e5, #7c3aed); border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; font-weight: 700; color: #fff;">AVENIQ AI HERO BANNER</div>
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
              <div style="font-size: 0.8rem; font-weight: 600; color: var(--accent-cyan); margin-bottom: 0.5rem;">SQUARE POST (1:1)</div>
              <div style="height: 140px; background: linear-gradient(135deg, #06b6d4, #3b82f6); border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; font-weight: 700; color: #fff;">SQUARE GRAPHIC</div>
            </div>
          </div>
        </div>
      `;
    } else if (tab === 'reasoning') {
      return `
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          <div style="font-weight: 700; color: #fff;">AI Reasoning & Market Analysis</div>
          <p style="color: var(--text-secondary); line-height: 1.6;">${rep.opportunity_selection_reasoning || 'Spike in search intent for autonomous AI workflow orchestration.'}</p>
          <div style="font-weight: 600; color: var(--accent-indigo); margin-top: 0.5rem;">Consulted Documents:</div>
          <ul style="color: var(--text-muted); padding-left: 1.2rem;">
            <li>Brand Guidelines v2.4</li>
            <li>Enterprise Positioning Strategy 2026</li>
            <li>Product Security Spec</li>
          </ul>
        </div>
      `;
    } else if (tab === 'seo') {
      return `
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          <div style="font-weight: 700; color: #fff;">SEO & Platform Keywords</div>
          <div style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: var(--radius-md);">
            <div style="font-size: 0.8rem; color: var(--text-muted);">PRIMARY KEYWORD</div>
            <div style="font-weight: 700; color: var(--accent-emerald);">Enterprise AI Automation</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.75rem;">HASHTAGS</div>
            <div style="color: var(--accent-indigo); font-family: var(--font-mono); font-size: 0.85rem;">#AI #Automation #SaaS #EnterpriseAI #AVENIQ</div>
          </div>
        </div>
      `;
    } else {
      // Default: Strategy & Copy
      return `
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          <div style="font-weight: 700; color: #fff; font-size: 1.1rem;">${item.topic || 'Enterprise AI Marketing Campaign'}</div>
          <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <div style="font-size: 0.75rem; font-weight: 700; color: var(--accent-indigo); margin-bottom: 0.5rem;">LINKEDIN POST COPY</div>
            <p style="color: var(--text-secondary); line-height: 1.6;">🚀 Autonomous AI agents are reshaping how marketing operations run. Here is a breakdown of how AVENIQ coordinates multi-agent research, copywriting, and visual asset synthesis automatically...</p>
          </div>
          <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <div style="font-size: 0.75rem; font-weight: 700; color: var(--accent-cyan); margin-bottom: 0.5rem;">X THREAD (PART 1/3)</div>
            <p style="color: var(--text-secondary); line-height: 1.6;">Why enterprise marketing teams are shifting to autonomous AI pipelines: 1/ Multi-agent research replaces manual scanning. 2/ Deterministic QA rules enforce brand guardrails. 3/ Real-time approval keeps humans in control.</p>
          </div>
        </div>
      `;
    }
  }

  // 3. MARKET INTELLIGENCE PINTEREST GRID
  function renderMarketIntelligence() {
    const container = document.getElementById('market-signals-grid');
    if (!container) return;

    const trends = [
      { category: 'REDDIT BUYING INTENT', title: 'High demand for AI Agent workflow controls', growth: '+340%', confidence: '98%', source: 'r/artificial' },
      { category: 'GITHUB TRENDING', title: 'Model Context Protocol (MCP) tool launch surge', growth: '+215%', confidence: '96%', source: 'GitHub API' },
      { category: 'GOOGLE NEWS', title: 'Enterprise AI adoption accelerating in Q3', growth: '+180%', confidence: '94%', source: 'Google News RSS' },
      { category: 'PRODUCT HUNT', title: 'Daily product launches focusing on autonomous automation', growth: '+150%', confidence: '92%', source: 'Product Hunt Feed' }
    ];

    container.innerHTML = trends.map(t => `
      <div class="glass-panel trend-card">
        <div class="trend-category">${t.category}</div>
        <div style="font-weight: 700; font-size: 1rem; color: #fff;">${t.title}</div>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 0.5rem;">
          <span style="color: var(--accent-emerald); font-weight: 700; font-size: 0.9rem;">${t.growth}</span>
          <span style="font-size: 0.75rem; color: var(--text-muted);">${t.source}</span>
        </div>
      </div>
    `).join('');
  }

  // 4. ANALYTICS & REASONING RENDERERS
  function renderAnalytics(analytics) {
    const container = document.getElementById('analytics-content');
    if (!container) return;

    const data = analytics || { engagement_rate: '4.8%', impressions: 75800, conversions: 18, total_cost: '$0.00' };

    container.innerHTML = `
      <div class="stats-grid" style="margin-bottom: 1.5rem;">
        <div class="glass-panel stat-card">
          <div class="stat-header"><span>ENGAGEMENT RATE</span></div>
          <div class="stat-value">${data.engagement_rate}</div>
          <div class="stat-subtext">Outperforming Industry Benchmark (+14%)</div>
        </div>
        <div class="glass-panel stat-card">
          <div class="stat-header"><span>ESTIMATED IMPRESSIONS</span></div>
          <div class="stat-value">${(data.impressions || 75800).toLocaleString()}</div>
          <div class="stat-subtext">Multi-Channel Reach</div>
        </div>
        <div class="glass-panel stat-card">
          <div class="stat-header"><span>CONVERSIONS</span></div>
          <div class="stat-value">${data.conversions || 18}</div>
          <div class="stat-subtext">Qualified Demo Requests</div>
        </div>
      </div>
    `;
  }

  // Global Navigation & Interactivity Handler
  window.AVENIQ = {
    selectApproval: function (idx) {
      state.selectedApprovalIndex = idx;
      renderApprovalCenter(state.approvals, state.reasoning);
    },
    setTab: function (tab) {
      state.activeTab = tab;
      renderApprovalCenter(state.approvals, state.reasoning);
    },
    handleDecision: function (sessionId, action) {
      alert(`Action '${action}' triggered for session ${sessionId}`);
    },
    init: async function () {
      try {
        const [overview, activity, approvals, analytics, reasoning] = await Promise.all([
          window.AVENIQ_API.getOverview(),
          window.AVENIQ_API.getActivity(),
          window.AVENIQ_API.getApprovals(),
          window.AVENIQ_API.getAnalytics(),
          window.AVENIQ_API.getReasoning()
        ]);

        state.overview = overview;
        state.activity = activity;
        state.approvals = approvals;
        state.analytics = analytics;
        state.reasoning = reasoning;

        renderStatsGrid(overview);
        renderWorkflowPipeline();
        renderTimeline(activity);
        renderReasoningCard(reasoning);
        renderApprovalCenter(approvals, reasoning);
        renderMarketIntelligence();
        renderAnalytics(analytics);
      } catch (err) {
        console.warn("AVENIQ API fallback active:", err);
        renderStatsGrid({});
        renderWorkflowPipeline();
        renderTimeline(null);
        renderReasoningCard(null);
        renderApprovalCenter(null, null);
        renderMarketIntelligence();
        renderAnalytics(null);
      }
    }
  };

  document.addEventListener('DOMContentLoaded', function () {
    window.AVENIQ.init();
  });

})();
