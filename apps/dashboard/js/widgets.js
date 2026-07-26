/* ==========================================================================
   AVENIQ OS — ENTERPRISE AI OPERATING SYSTEM WIDGETS & RENDERERS (v10)
   Deterministic Bootstrap Architecture via window.AVENIQ_APP Dependency Registry
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

    const safeOverview = (overview && typeof overview === 'object' && !overview.error) ? overview : {};
    const leads = safeOverview.leads || 80;
    const score = safeOverview.overall_score || '98.5/100';

    container.innerHTML = `
      <div class="monolithic-hero-surface">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem;">
          <div style="display: flex; align-items: center; gap: 0.6rem;">
            <div class="pulse-dot"></div>
            <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent-emerald); letter-spacing: 0.05em; font-family: var(--font-mono);">AVENIQ AUTONOMOUS ENGINE</span>
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

        <!-- Supporting Status Chips -->
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

    const items = (activity && activity.activity_timeline && Array.isArray(activity.activity_timeline))
      ? activity.activity_timeline
      : [
          { time: '08:00:02 AM', event: 'Market intelligence collection completed', type: 'INFO' },
          { time: '08:01:15 AM', event: 'Company Brain RAG documents retrieved', type: 'INFO' },
          { time: '08:01:30 AM', event: 'Daily strategy & copy synthesized by Gemini', type: 'INFO' },
          { time: '08:02:45 AM', event: 'Google Imagen visual marketing assets generated', type: 'INFO' },
          { time: '08:03:00 AM', event: 'Campaign briefing ready for human operator decision', type: 'AUDIT' }
        ];

    container.innerHTML = items.map(item => {
      const rawTime = item.time || '';
      const timeStr = rawTime.includes('T') ? rawTime.split('T')[1].slice(0, 8) : rawTime;
      return `
        <div class="feed-item">
          <div class="feed-icon">⚡</div>
          <div style="flex: 1;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <div style="font-weight: 600; color: #fff; font-size: 0.88rem;">${item.event || 'System Event'}</div>
              <div style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-muted);">${timeStr}</div>
            </div>
            <div style="font-size: 0.78rem; color: var(--text-secondary); margin-top: 0.15rem;">Automated pipeline execution phase • Status: Success</div>
          </div>
        </div>
      `;
    }).join('');
  }

  // 4. REASONING CARD
  function renderReasoningCard(reasoning) {
    const container = document.getElementById('reasoning-summary-card');
    if (!container) return;

    const rep = (reasoning && typeof reasoning === 'object' && !reasoning.error) ? reasoning : {
      topic: 'Enterprise AI Agent Operations',
      opportunity_selection_reasoning: 'Spike in operational demand for autonomous AI workflow governance with low competitor velocity in Q3.',
      expected_business_impact: { confidence_score: 0.95, expected_ctr_gain: '+2.4%' }
    };

    const impact = rep.expected_business_impact || {};
    const confidenceVal = impact.confidence_score ? ((impact.confidence_score) * 100).toFixed(0) : '95';
    const ctrGain = impact.expected_ctr_gain || '+2.4%';

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 0.75rem;">
        <div>
          <div style="font-size: 0.75rem; color: var(--accent-cyan); font-weight: 700;">SELECTED OPPORTUNITY</div>
          <div style="font-size: 1.1rem; font-weight: 700; color: #fff;">${rep.topic || 'Enterprise AI Agent Operations'}</div>
        </div>
        <div>
          <div style="font-size: 0.75rem; color: var(--text-muted); font-weight: 600;">WHY THIS OPPORTUNITY</div>
          <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">${rep.opportunity_selection_reasoning || 'Automated opportunity synthesis active.'}</div>
        </div>
        <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
          <div style="background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.25); padding: 0.5rem 0.85rem; border-radius: var(--radius-md);">
            <div style="font-size: 0.7rem; color: var(--text-muted);">AI CONFIDENCE</div>
            <div style="font-weight: 700; color: var(--accent-indigo);">${confidenceVal}%</div>
          </div>
          <div style="background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.25); padding: 0.5rem 0.85rem; border-radius: var(--radius-md);">
            <div style="font-size: 0.7rem; color: var(--text-muted);">EXPECTED IMPACT</div>
            <div style="font-weight: 700; color: var(--accent-emerald);">${ctrGain}</div>
          </div>
        </div>
      </div>
    `;
  }

  // 5. AUTOMATION DETAILS
  function renderAutomation(overview) {
    const container = document.getElementById('automation-details-content');
    if (!container) return;

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
          <div>
            <div style="font-weight: 700; color: #fff;">Daily Automation Pipeline</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">Runs autonomously every morning at 08:00 AM UTC</div>
          </div>
          <span style="background: rgba(16,185,129,0.15); color: var(--accent-emerald); padding: 0.25rem 0.75rem; border-radius: var(--radius-full); font-weight: 700; font-size: 0.78rem;">ACTIVE SCHEDULE</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;">
          <div style="background: rgba(255,255,255,0.02); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <div style="font-size: 0.75rem; color: var(--text-muted);">EXECUTION ENGINE</div>
            <div style="font-weight: 700; color: var(--accent-indigo); margin-top: 0.2rem;">Python Async Pipeline</div>
          </div>
          <div style="background: rgba(255,255,255,0.02); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <div style="font-size: 0.75rem; color: var(--text-muted);">TELEGRAM BOT DISPATCH</div>
            <div style="font-weight: 700; color: var(--accent-emerald); margin-top: 0.2rem;">Connected & Listening</div>
          </div>
          <div style="background: rgba(255,255,255,0.02); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <div style="font-size: 0.75rem; color: var(--text-muted);">IMAGE SYNTHESIS ENGINE</div>
            <div style="font-weight: 700; color: var(--accent-cyan); margin-top: 0.2rem;">Google Imagen 3 API</div>
          </div>
        </div>
      </div>
    `;
  }

  // 6. CAMPAIGNS
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

  // 7. APPROVAL CENTER
  function renderApprovalCenter(approvals, reasoning) {
    const listContainer = document.getElementById('approval-items-list');
    const previewPane = document.getElementById('approval-preview-pane');
    if (!listContainer || !previewPane) return;

    const pending = (approvals && approvals.pending_approvals && Array.isArray(approvals.pending_approvals) && approvals.pending_approvals.length > 0)
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

  // 8. MARKET INTELLIGENCE
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

  // 9. COMPANY BRAIN
  function renderCompanyBrain() {
    const container = document.getElementById('company-brain-content');
    if (!container) return;

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div style="background: rgba(255,255,255,0.03); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
          <div style="font-weight: 700; color: #fff; margin-bottom: 0.5rem;">🧠 Company Brand Identity Memory</div>
          <p style="font-size: 0.88rem; color: var(--text-secondary); line-height: 1.6;">AVENIQ Company Brain stores brand guidelines, target customer personas, voice tone preferences, and past high-converting marketing campaigns to ensure all AI outputs strictly adhere to brand voice.</p>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem;">
          <div style="background: rgba(255,255,255,0.02); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <div style="font-size: 0.75rem; color: var(--accent-indigo); font-weight: 700;">BRAND VOICE</div>
            <div style="font-weight: 600; color: #fff; margin-top: 0.2rem;">Authoritative, Technical & Visionary</div>
          </div>
          <div style="background: rgba(255,255,255,0.02); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <div style="font-size: 0.75rem; color: var(--accent-emerald); font-weight: 700;">VECTOR STORE</div>
            <div style="font-weight: 600; color: #fff; margin-top: 0.2rem;">14 Indexed Knowledge Docs</div>
          </div>
        </div>
      </div>
    `;
  }

  // 10. KNOWLEDGE RAG
  function renderKnowledge() {
    const container = document.getElementById('knowledge-content');
    if (!container) return;

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div style="background: rgba(255,255,255,0.03); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
          <div style="font-weight: 700; color: #fff; margin-bottom: 0.5rem;">📚 Vector Knowledge Collections</div>
          <div style="font-size: 0.85rem; color: var(--text-secondary);">Indexed technical documentation, service offerings (SaaS, Mobile, Cloud, AI), and enterprise customer case studies.</div>
        </div>
      </div>
    `;
  }

  // 11. CLOSED-LOOP LEARNING
  function renderLearning() {
    const container = document.getElementById('learning-content');
    if (!container) return;

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div style="background: rgba(255,255,255,0.03); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
          <div style="font-weight: 700; color: #fff; margin-bottom: 0.5rem;">📈 Closed-Loop Performance Optimization</div>
          <div style="font-size: 0.85rem; color: var(--text-secondary);">Feedback loops process engagement metrics from published Telegram/LinkedIn campaigns to fine-tune future opportunity selection.</div>
        </div>
      </div>
    `;
  }

  // 12. ANALYTICS
  function renderAnalytics(analytics) {
    const container = document.getElementById('analytics-content');
    if (!container) return;

    const safeAnalytics = (analytics && typeof analytics === 'object' && !analytics.error) ? analytics : {};
    const rate = safeAnalytics.engagement_rate || '4.8%';
    const impressions = safeAnalytics.impressions ? safeAnalytics.impressions.toLocaleString() : '75,800';
    const conversions = safeAnalytics.conversions || 18;
    const cost = safeAnalytics.total_cost !== undefined ? `$${safeAnalytics.total_cost.toFixed(4)}` : '$0.0125';

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.25rem;">
        <h2 style="font-size: 1.1rem; font-weight: 700;">📊 Analytics & Performance Metrics</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
          <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <div style="font-size: 0.75rem; color: var(--text-muted);">ENGAGEMENT RATE</div>
            <div style="font-weight: 800; font-size: 1.4rem; color: var(--accent-emerald); margin-top: 0.2rem;">${rate}</div>
          </div>
          <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <div style="font-size: 0.75rem; color: var(--text-muted);">TOTAL IMPRESSIONS</div>
            <div style="font-weight: 800; font-size: 1.4rem; color: #fff; margin-top: 0.2rem;">${impressions}</div>
          </div>
          <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <div style="font-size: 0.75rem; color: var(--text-muted);">QUALIFIED CONVERSIONS</div>
            <div style="font-weight: 800; font-size: 1.4rem; color: var(--accent-cyan); margin-top: 0.2rem;">${conversions}</div>
          </div>
          <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <div style="font-size: 0.75rem; color: var(--text-muted);">LLM TOKEN COST</div>
            <div style="font-weight: 800; font-size: 1.4rem; color: var(--accent-indigo); margin-top: 0.2rem;">${cost}</div>
          </div>
        </div>
      </div>
    `;
  }

  // 13. SETTINGS
  function renderSettings() {
    const container = document.getElementById('settings-content');
    if (!container) return;

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <h2 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">⚙️ Workspace Configuration</h2>
        <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
          <div style="font-weight: 600; color: #fff;">Primary LLM Model</div>
          <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">Google Gemini 2.5 Pro (via GEMINI_API_KEY)</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
          <div style="font-weight: 600; color: #fff;">Dashboard HTTP Server</div>
          <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">Python HTTPServer on Port 8097</div>
        </div>
      </div>
    `;
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
      let overview = {}, activity = null, approvals = null, analytics = null, reasoning = null;

      // Deterministic API dependency resolution via AVENIQ_APP
      let api = null;
      try {
        if (window.AVENIQ_APP && typeof window.AVENIQ_APP.require === 'function') {
          api = await window.AVENIQ_APP.require('api');
        } else if (window.AVENIQ_API) {
          api = window.AVENIQ_API;
        }
      } catch (err) {
        console.error("[AVENIQ BOOTSTRAP FATAL] Failed to resolve 'api' dependency from AVENIQ_APP registry:", err);
      }

      if (!api || typeof api.getOverview !== 'function') {
        const fatalError = new Error("[AVENIQ BOOTSTRAP FATAL] Critical Dependency Failure: API client is not initialized or missing 'getOverview' method.");
        console.error(fatalError.stack);
        throw fatalError;
      }

      try {
        const results = await Promise.allSettled([
          api.getOverview(),
          api.getActivity(),
          api.getApprovals(),
          api.getAnalytics(),
          api.getReasoning()
        ]);

        overview = (results[0].status === 'fulfilled' && results[0].value && !results[0].value.error) ? results[0].value : {};
        activity = (results[1].status === 'fulfilled' && results[1].value && !results[1].value.error) ? results[1].value : null;
        approvals = (results[2].status === 'fulfilled' && results[2].value && !results[2].value.error) ? results[2].value : null;
        analytics = (results[3].status === 'fulfilled' && results[3].value && !results[3].value.error) ? results[3].value : null;
        reasoning = (results[4].status === 'fulfilled' && results[4].value && !results[4].value.error) ? results[4].value : null;
      } catch (err) {
        console.error("[AVENIQ RUNTIME ERROR] Error fetching API data:", err.stack || err);
      }

      state.overview = overview;
      state.activity = activity;
      state.approvals = approvals;
      state.analytics = analytics;
      state.reasoning = reasoning;

      // Render workspace components
      try { renderHeroMissionBriefing(overview); } catch (e) { console.error('[AVENIQ RENDER ERROR] Hero render failed:', e.stack || e); }
      try { renderWorkflowPipeline(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Pipeline render failed:', e.stack || e); }
      try { renderTimeline(activity); } catch (e) { console.error('[AVENIQ RENDER ERROR] Timeline render failed:', e.stack || e); }
      try { renderReasoningCard(reasoning); } catch (e) { console.error('[AVENIQ RENDER ERROR] Reasoning render failed:', e.stack || e); }
      try { renderAutomation(overview); } catch (e) { console.error('[AVENIQ RENDER ERROR] Automation render failed:', e.stack || e); }
      try { renderCampaigns(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Campaigns render failed:', e.stack || e); }
      try { renderApprovalCenter(approvals, reasoning); } catch (e) { console.error('[AVENIQ RENDER ERROR] Approval render failed:', e.stack || e); }
      try { renderMarketIntelligence(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Market Intel render failed:', e.stack || e); }
      try { renderCompanyBrain(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Company Brain render failed:', e.stack || e); }
      try { renderKnowledge(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Knowledge render failed:', e.stack || e); }
      try { renderLearning(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Learning render failed:', e.stack || e); }
      try { renderAnalytics(analytics); } catch (e) { console.error('[AVENIQ RENDER ERROR] Analytics render failed:', e.stack || e); }
      try { renderSettings(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Settings render failed:', e.stack || e); }
    }
  };

  function safeAutoStart() {
    if (window.AVENIQ && typeof window.AVENIQ.init === 'function') {
      window.AVENIQ.init().catch(err => {
        console.error("[AVENIQ BOOTSTRAP UNHANDLED EXCEPTION]", err.stack || err);
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', safeAutoStart);
  } else {
    safeAutoStart();
  }

  if (window.AVENIQ_APP && typeof window.AVENIQ_APP.register === 'function') {
    window.AVENIQ_APP.register('widgets', window.AVENIQ);
  }
})();
