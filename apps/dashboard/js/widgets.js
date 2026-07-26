/* ==========================================================================
   AVENIQ OS — ENTERPRISE AI OPERATING SYSTEM WIDGETS & RENDERERS (v6)
   Sequential Executive Mission Briefing AI Workspace Engine
   ========================================================================== */

(function () {
  'use strict';

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

  // 1. EXECUTIVE MISSION BRIEFING HERO SURFACE
  function renderHeroMissionBriefing(overview) {
    const container = document.getElementById('hero-mission-container');
    if (!container) return;

    const leads = overview.leads || 80;
    const score = overview.overall_score || '98.5/100';

    container.innerHTML = `
      <div class="monolithic-hero-surface">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem;">
          <div style="display: flex; align-items: center; gap: 0.6rem;">
            <div class="pulse-dot"></div>
            <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent-emerald); tracking: 0.05em; font-family: var(--font-mono);">AVENIQ AUTONOMOUS ENGINE</span>
          </div>
          <div style="display: flex; align-items: center; gap: 0.6rem;">
            <span class="pulse-status" style="background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.25);">NO ACTION REQUIRED</span>
          </div>
        </div>

        <div class="hero-ai-title">AVENIQ</div>
        <div style="font-size: 1.2rem; font-weight: 600; color: var(--accent-indigo); margin-bottom: 0.75rem;">Enterprise Growth Operating System</div>
        
        <div class="hero-ai-subtitle" style="margin-bottom: 1.75rem;">
          Currently researching enterprise opportunities across Reddit buying intent, GitHub star velocity, Product Hunt releases, and Google News RSS...
        </div>

        <!-- Animated AI Reasoning Progress -->
        <div style="max-width: 650px; margin-bottom: 2rem;">
          <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.82rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 0.4rem;">
            <span>AI Reasoning Progress</span>
            <span style="font-family: var(--font-mono); color: var(--accent-cyan);">74%</span>
          </div>
          <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.06); border-radius: var(--radius-full); overflow: hidden; position: relative;">
            <div style="width: 74%; height: 100%; background: linear-gradient(90deg, var(--accent-indigo), var(--accent-cyan)); border-radius: var(--radius-full); box-shadow: 0 0 15px var(--accent-indigo);"></div>
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-top: 0.4rem;">
            <span>Next reasoning checkpoint</span>
            <span style="font-family: var(--font-mono);">1 min 42 sec</span>
          </div>
        </div>

        <!-- Lightweight Supporting Status Chips (No Large KPI Cards) -->
        <div style="display: flex; flex-wrap: wrap; gap: 0.75rem; border-top: 1px solid var(--border-color); padding-top: 1.25rem;">
          <div style="display: flex; align-items: center; gap: 0.4rem; background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); padding: 0.4rem 0.85rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500; color: var(--text-primary);">
            <span style="color: var(--accent-emerald);">●</span> 14 Campaigns Active
          </div>
          <div style="display: flex; align-items: center; gap: 0.4rem; background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); padding: 0.4rem 0.85rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500; color: var(--text-primary);">
            <span style="color: var(--accent-indigo);">●</span> Confidence 98.6%
          </div>
          <div style="display: flex; align-items: center; gap: 0.4rem; background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); padding: 0.4rem 0.85rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500; color: var(--text-primary);">
            <span style="color: var(--accent-cyan);">●</span> ${leads} Market Signals Scanned
          </div>
          <div style="display: flex; align-items: center; gap: 0.4rem; background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); padding: 0.4rem 0.85rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500; color: var(--text-primary);">
            <span style="color: var(--accent-purple);">●</span> Brand QA ${score} Passed
          </div>
        </div>
      </div>
    `;
  }

  // 2. LIVING SVG PIPELINE FLOW
  function renderWorkflowPipeline() {
    const container = document.getElementById('pipeline-nodes');
    if (!container) return;

    const nodes = [
      { name: 'Research', icon: '🔍', status: 'completed' },
      { name: 'Market Intel', icon: '📡', status: 'completed' },
      { name: 'Company Brain', icon: '🧠', status: 'completed' },
      { name: 'Reasoning', icon: '💡', status: 'completed' },
      { name: 'Strategy', icon: '📊', status: 'completed' },
      { name: 'Content', icon: '✍️', status: 'completed' },
      { name: 'Images', icon: '🖼️', status: 'completed' },
      { name: 'Approval', icon: '⚡', status: 'running' },
      { name: 'Delivery', icon: '🚀', status: 'idle' },
      { name: 'Learning', icon: '📈', status: 'idle' }
    ];

    container.innerHTML = `
      <div class="living-flow-container">
        ${nodes.map(node => `
          <div class="flow-node-item ${node.status}">
            <div class="flow-node-circle">${node.icon}</div>
            <div style="font-size: 0.75rem; font-weight: 600; color: var(--text-primary); margin-top: 0.2rem;">${node.name}</div>
            <div style="font-size: 0.65rem; color: var(--text-muted);">${node.status.toUpperCase()}</div>
          </div>
        `).join('')}
      </div>
    `;
  }

  // 3. BREATHING ACTIVITY FEED
  function renderTimeline(activity) {
    const container = document.getElementById('activity-timeline-list');
    if (!container) return;

    const items = (activity && activity.activity_timeline) ? activity.activity_timeline : [
      { time: '08:00:02 AM', event: 'Market intelligence collection completed', type: 'INFO' },
      { time: '08:01:15 AM', event: 'Company Brain RAG documents retrieved', type: 'INFO' },
      { time: '08:01:30 AM', event: 'Daily strategy & copy synthesized by Gemini', type: 'INFO' },
      { time: '08:02:45 AM', event: 'Google Imagen visual marketing assets generated', type: 'INFO' },
      { time: '08:03:00 AM', event: 'Campaign briefing ready for human operator decision', type: 'AUDIT' }
    ];

    container.innerHTML = items.map(item => {
      const timeStr = item.time.includes('T') ? item.time.split('T')[1].slice(0, 8) : item.time;
      return `
        <div class="feed-item">
          <div class="feed-icon">⚡</div>
          <div style="flex: 1;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <div style="font-weight: 600; color: #fff; font-size: 0.88rem;">${item.event}</div>
              <div style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-muted);">${timeStr}</div>
            </div>
            <div style="font-size: 0.78rem; color: var(--text-secondary); margin-top: 0.15rem;">Automated pipeline execution phase • Status: Success</div>
          </div>
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
          <div style="font-size: 0.75rem; color: var(--accent-cyan); font-weight: 700;">SELECTED OPPORTUNITY</div>
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

  function renderCampaigns() {
    const container = document.getElementById('campaigns-cards-grid');
    if (!container) return;

    const campaigns = [
      { id: 'cmp_01', name: 'Enterprise AI Operations', platform: 'LinkedIn + X', score: '98.5', status: 'Actively Learning', roi: '+310%' },
      { id: 'cmp_02', name: 'Model Context Protocol Surge', platform: 'GitHub + RSS', score: '96.2', status: 'Actively Learning', roi: '+240%' },
      { id: 'cmp_03', name: 'Autonomous Agent Security', platform: 'TechCrunch', score: '95.0', status: 'Drafting', roi: '+180%' }
    ];

    container.innerHTML = campaigns.map(c => `
      <div class="glass-panel campaign-card-carousel" style="padding: 1.25rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
          <span style="font-size: 0.7rem; font-family: var(--font-mono); color: var(--accent-cyan);">${c.platform}</span>
          <span style="font-size: 0.68rem; background: rgba(16,185,129,0.15); color: var(--accent-emerald); padding: 0.15rem 0.4rem; border-radius: var(--radius-full); font-weight: 600;">${c.status}</span>
        </div>
        <div style="font-weight: 700; font-size: 1rem; color: #fff; margin-bottom: 0.5rem;">${c.name}</div>
        <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted);">
          <span>Quality: ${c.score}/100</span>
          <span style="color: var(--accent-indigo); font-weight: 700;">Est. ROI ${c.roi}</span>
        </div>
      </div>
    `).join('');
  }

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

    const selected = pending[state.selectedApprovalIndex] || pending[0];

    previewPane.innerHTML = `
      <div class="preview-tabs">
        <button class="tab-btn ${state.activeTab === 'strategy' ? 'active' : ''}" onclick="window.AVENIQ.setTab('strategy')">Strategy & Copy</button>
        <button class="tab-btn ${state.activeTab === 'images' ? 'active' : ''}" onclick="window.AVENIQ.setTab('images')">Visual Assets</button>
        <button class="tab-btn ${state.activeTab === 'reasoning' ? 'active' : ''}" onclick="window.AVENIQ.setTab('reasoning')">AI Reasoning</button>
      </div>

      <div style="flex: 1; overflow-y: auto;">
        <div style="font-weight: 700; color: #fff; font-size: 1.1rem; margin-bottom: 0.75rem;">${selected.topic || 'Enterprise AI Marketing Campaign'}</div>
        <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
          <div style="font-size: 0.75rem; font-weight: 700; color: var(--accent-indigo); margin-bottom: 0.5rem;">LINKEDIN POST COPY</div>
          <p style="color: var(--text-secondary); line-height: 1.6;">🚀 Autonomous AI agents are reshaping how marketing operations run. Here is a breakdown of how AVENIQ coordinates multi-agent research, copywriting, and visual asset synthesis automatically...</p>
        </div>
      </div>

      <div class="approval-action-bar">
        <div style="display: flex; gap: 0.5rem;">
          <button class="btn btn-success" onclick="window.AVENIQ.handleDecision('${selected.session_id}', 'Approve')">✅ Approve</button>
          <button class="btn btn-danger" onclick="window.AVENIQ.handleDecision('${selected.session_id}', 'Reject')">❌ Reject</button>
        </div>
      </div>
    `;
  }

  function renderMarketIntelligence() {
    const container = document.getElementById('market-signals-grid');
    if (!container) return;

    const trends = [
      { category: 'REDDIT BUYING INTENT', title: 'High demand for AI Agent workflow controls', growth: '+340%', source: 'r/artificial' },
      { category: 'GITHUB TRENDING', title: 'Model Context Protocol (MCP) tool launch surge', growth: '+215%', source: 'GitHub API' }
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

        renderHeroMissionBriefing(overview);
        renderWorkflowPipeline();
        renderTimeline(activity);
        renderReasoningCard(reasoning);
        renderCampaigns();
        renderApprovalCenter(approvals, reasoning);
        renderMarketIntelligence();
      } catch (err) {
        console.warn("AVENIQ API fallback active:", err);
        renderHeroMissionBriefing({});
        renderWorkflowPipeline();
        renderTimeline(null);
        renderReasoningCard(null);
        renderCampaigns();
        renderApprovalCenter(null, null);
        renderMarketIntelligence();
      }
    }
  };

  document.addEventListener('DOMContentLoaded', function () {
    window.AVENIQ.init();
  });

})();
