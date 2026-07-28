/* ==========================================================================
   AVENIQ OS — ENTERPRISE AI OPERATING SYSTEM WIDGETS & RENDERERS (v14)
   Live Backend Integration Verification & Interactive Service Testers
   Strict Connection Status Hierarchy: Not Configured -> Configured -> Connected
   Auto-Dispatch Generated Imagen Assets to Telegram Channel
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
    connections: null,
    selectedApprovalIndex: 0,
    activeTab: 'strategy',
    runtime: null,
  };

  // ── Runtime poller ──────────────────────────────────────────────────────────
  let _runtimePoller = null;

  function startRuntimePolling(api) {
    if (_runtimePoller) return;
    _runtimePoller = setInterval(async () => {
      try {
        const rt = await api.getAutomationRuntime();
        if (!rt || rt.error) return;
        state.runtime = rt;
        renderActiveAutomationCard(rt);
        renderWorkflowPipeline(rt);
        renderRuntimeMetrics(rt);
        if (!rt.running) stopRuntimePolling();
      } catch (e) { console.warn('[AVENIQ Runtime Poller]', e); }
    }, 5000);
  }

  function stopRuntimePolling() {
    if (_runtimePoller) { clearInterval(_runtimePoller); _runtimePoller = null; }
  }

  // ── Stop confirmation modal ─────────────────────────────────────────────────
  function showStopModal(api) {
    let overlay = document.getElementById('stop-modal-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'stop-modal-overlay';
      overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:9999;display:flex;align-items:center;justify-content:center;';
      document.body.appendChild(overlay);
    }
    overlay.innerHTML = `
      <div style="background:var(--bg-secondary,#1a1a2e);border:1px solid var(--border-color,#2a2a4a);border-radius:12px;padding:2rem;max-width:420px;width:90%;">
        <div style="font-size:1rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">⏹ Stop Automation?</div>
        <div style="font-size:0.88rem;color:var(--text-secondary,#8888aa);margin-bottom:1.5rem;">Current stage will finish safely. Remaining stages will not execute. Execution saved as <b>Cancelled</b>. You can resume later.</div>
        <div style="display:flex;gap:0.75rem;justify-content:flex-end;">
          <button id="stop-modal-cancel" style="padding:0.45rem 1.1rem;border-radius:8px;border:1px solid var(--border-color,#2a2a4a);background:transparent;color:#fff;cursor:pointer;">Cancel</button>
          <button id="stop-modal-confirm" style="padding:0.45rem 1.1rem;border-radius:8px;border:none;background:#f43f5e;color:#fff;font-weight:700;cursor:pointer;">Stop Automation</button>
        </div>
      </div>
    `;
    overlay.style.display = 'flex';
    document.getElementById('stop-modal-cancel').onclick = () => { overlay.style.display = 'none'; };
    document.getElementById('stop-modal-confirm').onclick = async () => {
      overlay.style.display = 'none';
      try {
        await api.cancelAutomation();
        startRuntimePolling(api);
      } catch(e) { console.error('[AVENIQ Stop]', e); }
    };
  }

  // 1. EXECUTIVE MISSION BRIEFING HERO SURFACE
  function renderHeroMissionBriefing(overview) {
    const container = document.getElementById('hero-mission-container');
    if (!container) return;
    const safe = (overview && typeof overview === 'object' && !overview.error) ? overview : {};
    const leads = safe.leads != null ? safe.leads : '--';
    container.innerHTML = `
      <div class="monolithic-hero-surface">
        <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1.25rem;">
          <div class="pulse-dot"></div>
          <span style="font-size:0.75rem;font-weight:700;color:var(--accent-emerald);letter-spacing:0.05em;font-family:var(--font-mono);">AVENIQ AUTONOMOUS ENGINE</span>
        </div>
        <div class="hero-ai-title">AVENIQ</div>
        <div style="font-size:1.2rem;font-weight:600;color:var(--accent-indigo);margin-bottom:0.75rem;">Enterprise Growth Operating System</div>
        <div class="hero-ai-subtitle" style="margin-bottom:1.5rem;">Monitoring enterprise opportunities across Reddit, GitHub, Product Hunt and Google News.</div>
        <div id="runtime-metrics-bar" style="border-top:1px solid var(--border-color);padding-top:1.25rem;"></div>
      </div>`;
  }

  // 1b. RUNTIME METRICS BAR (live chips — no placeholders)
  function renderRuntimeMetrics(runtime) {
    const el = document.getElementById('runtime-metrics-bar');
    if (!el) return;
    const rt = runtime || {};
    const chip = (color, label) =>
      `<div style="display:flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.03);border:1px solid var(--border-color);padding:0.4rem 0.85rem;border-radius:var(--radius-full);font-size:0.8rem;font-weight:500;color:var(--text-primary);">
        <span style="color:${color};">\u25cf</span> ${label}</div>`;
    const fmtNext = (iso) => {
      if (!iso) return 'None scheduled';
      const d = new Date(iso);
      return isNaN(d) ? iso : d.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
    };
    el.innerHTML = `<div style="display:flex;flex-wrap:wrap;gap:0.75rem;">
      ${chip('var(--accent-emerald)', rt.running ? 'Running' : 'Idle')}
      ${chip('var(--accent-indigo)', `${rt.queue_size != null ? rt.queue_size : '--'} Queued`)}
      ${chip('var(--accent-cyan)', `${rt.completed_today != null ? rt.completed_today : '--'} Completed Today`)}
      ${rt.failed_today ? chip('var(--accent-rose)', `${rt.failed_today} Failed Today`) : ''}
      ${chip('var(--accent-amber)', `Next: ${fmtNext(rt.next_execution)}`)}
    </div>`;
  }

  // 2. LIVE PIPELINE FLOW (driven by runtime.pipeline)
  function renderWorkflowPipeline(runtime) {
    const container = document.getElementById('pipeline-nodes');
    if (!container) return;
    const rt = runtime || {};
    let nodes = (rt.pipeline && rt.pipeline.length > 0) ? rt.pipeline : [];
    if (nodes.length === 0) {
      nodes = [
        { name: 'Research Engine', icon: '🔍', status: 'waiting' },
        { name: 'Strategy Planning', icon: '🧠', status: 'waiting' },
        { name: 'Campaign Copywriting', icon: '✍️', status: 'waiting' },
        { name: 'Compliance Review', icon: '🛡️', status: 'waiting' },
        { name: 'Platform Publishing', icon: '🚀', status: 'waiting' },
        { name: 'Learning Synthesis', icon: '📈', status: 'waiting' }
      ];
    }
    const statusColor = { completed:'var(--accent-emerald)', running:'var(--accent-cyan)', failed:'var(--accent-rose)', cancelled:'var(--accent-amber)', skipped:'var(--text-muted)', waiting:'var(--text-muted)' };
    const statusClass = { completed:'completed', running:'running', failed:'failed', cancelled:'cancelled', skipped:'idle', waiting:'idle' };
    container.innerHTML = `<div class="living-flow-container">${nodes.map(node => {
      const st = node.status || 'waiting';
      const dur = node.duration_ms != null ? ` <span style="font-size:0.6rem;color:var(--text-muted);">${node.duration_ms}ms</span>` : '';
      return `<div class="flow-node-item ${statusClass[st] || 'idle'}">
        <div class="flow-node-circle">${node.icon || '⚙️'}</div>
        <div style="font-size:0.75rem;font-weight:600;color:var(--text-primary);margin-top:0.2rem;">${node.name}</div>
        <div style="font-size:0.65rem;color:${statusColor[st] || 'var(--text-muted)'}">${st.toUpperCase()}${dur}</div>
      </div>`;
    }).join('')}</div>`;
  }

  // 2b. ACTIVE AUTOMATION CARD
  function renderActiveAutomationCard(runtime) {
    const container = document.getElementById('active-automation-card');
    if (!container) return;
    const rt = runtime || {};
    const api = window.AVENIQ_API;

    if (rt.recovered && !rt.running) {
      container.innerHTML = `
        <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);border-radius:var(--radius-md);padding:1.25rem;margin-bottom:1.25rem;">
          <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;">
            <span style="color:var(--accent-amber);">⚠️</span>
            <span style="font-weight:700;color:var(--accent-amber);font-size:0.88rem;">Recovered Previous Session</span>
          </div>
          <div style="font-size:0.82rem;color:var(--text-secondary);">
            Last: <b>${rt.schedule_name || '--'}</b> &middot; Status: <b>${rt.recovered_status || 'interrupted'}</b> &middot; Stage: <b>${rt.current_stage || '--'}</b>
          </div>
          ${(rt.schedule_id && rt.current_stage_index != null) ?
            `<button onclick="window.AVENIQ._resumeJob('${rt.schedule_id}', ${rt.current_stage_index})" style="margin-top:0.75rem;padding:0.35rem 1rem;border-radius:8px;border:none;background:var(--accent-amber);color:#000;font-weight:700;cursor:pointer;">⟳ Resume from ${rt.current_stage || 'last stage'}</button>` : ''}
        </div>`;
      return;
    }
    if (!rt.running) {
      container.innerHTML = `
        <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.5rem;text-align:center;margin-bottom:1.25rem;">
          <div style="font-size:1.5rem;margin-bottom:0.5rem;">⏸</div>
          <div style="font-weight:700;color:var(--text-primary);font-size:0.95rem;">No Active Automation</div>
          <div style="font-size:0.82rem;color:var(--text-muted);margin-top:0.25rem;">Scheduler Ready — Waiting for next execution</div>
        </div>`;
      return;
    }
    const pct = typeof rt.progress === 'number' ? rt.progress.toFixed(1) : '0';
    const elapsed = rt.elapsed_seconds != null ? `${Math.floor(rt.elapsed_seconds/60)}m ${rt.elapsed_seconds%60}s` : '--';
    const remaining = rt.estimated_remaining_seconds != null ? `~${Math.floor(rt.estimated_remaining_seconds/60)}m ${rt.estimated_remaining_seconds%60}s left` : '';
    container.innerHTML = `
      <div style="background:rgba(99,102,241,0.06);border:1px solid rgba(99,102,241,0.25);border-radius:var(--radius-md);padding:1.25rem;margin-bottom:1.25rem;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.75rem;">
          <div style="display:flex;align-items:center;gap:0.5rem;"><div class="pulse-dot"></div><span style="font-size:0.75rem;font-weight:700;color:var(--accent-indigo);letter-spacing:0.05em;">AUTOMATION RUNNING</span></div>
          <button id="btn-stop-automation" style="padding:0.3rem 0.85rem;border-radius:8px;border:1px solid rgba(244,63,94,0.4);background:rgba(244,63,94,0.1);color:var(--accent-rose);font-size:0.78rem;font-weight:700;cursor:pointer;">⏹ Stop</button>
        </div>
        <div style="font-weight:700;color:#fff;font-size:1.05rem;margin-bottom:0.25rem;">${rt.schedule_name || '--'}</div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:0.5rem;font-size:0.78rem;color:var(--text-secondary);margin-bottom:0.85rem;">
          <span>Dept: <b style="color:#fff;">${rt.department || '--'}</b></span>
          <span>Stage: <b style="color:var(--accent-cyan);">${rt.current_stage || '--'}</b></span>
          <span>Elapsed: <b style="color:#fff;">${elapsed}</b></span>
          <span>Worker: <b style="color:#fff;">${rt.worker || '--'}</b></span>
          <span style="font-family:var(--font-mono);font-size:0.7rem;">ID: ${rt.execution_id || '--'}</span>
          ${remaining ? `<span style="color:var(--text-muted);">${remaining}</span>` : ''}
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between;font-size:0.78rem;color:var(--text-secondary);margin-bottom:0.3rem;">
          <span>${rt.completed_stages || 0} / ${rt.total_stages || 0} stages</span>
          <span style="font-family:var(--font-mono);color:var(--accent-cyan);">${pct}%</span>
        </div>
        <div style="width:100%;height:6px;background:rgba(255,255,255,0.06);border-radius:var(--radius-full);overflow:hidden;">
          <div style="width:${pct}%;height:100%;background:linear-gradient(90deg,var(--accent-indigo),var(--accent-cyan));border-radius:var(--radius-full);transition:width 0.5s ease;"></div>
        </div>
      </div>`;
    const stopBtn = document.getElementById('btn-stop-automation');
    if (stopBtn && api) stopBtn.onclick = () => showStopModal(api);
  }

  // 3. LIVE ACTIVITY FEED
  function renderLiveActivityFeed(events) {
    const container = document.getElementById('activity-timeline-list');
    if (!container) return;
    let items = (Array.isArray(events) && events.length > 0) ? events : [];
    if (items.length === 0 && state.activity && Array.isArray(state.activity.activity_timeline)) {
      items = state.activity.activity_timeline;
    }
    if (items.length === 0) {
      container.innerHTML = `<div class="feed-item"><div style="color:var(--text-muted);font-size:0.85rem;padding:0.5rem 0;">Scheduler Standby — Idle</div></div>`;
      return;
    }
    const eventLabel = (type) => {
      const map = { STAGE_STARTED:'▶ Stage started', STAGE_COMPLETED:'✓ Stage completed', STAGE_FAILED:'✗ Stage failed', STAGE_SKIPPED:'⊘ Stage skipped', AUTOMATION_STARTED:'🚀 Automation started', AUTOMATION_COMPLETED:'✅ Automation completed', AUTOMATION_CANCELLED:'⏹ Automation cancelled', AUTOMATION_FAILED:'❌ Automation failed', AUTOMATION_CANCEL_REQUESTED:'⚠️ Stop requested', SCHEDULER_RECOVERED:'♻ Session recovered', SUCCESS:'✅ Event Completed', INFO:'ℹ Activity Event' };
      return map[type] || type;
    };
    container.innerHTML = items.map(ev => {
      const name = ev.event || ev.name || (ev.payload ? (ev.payload.schedule_name || ev.payload.stage || ev.type) : ev.type);
      const ts = (ev.time || ev.timestamp) ? new Date(ev.time || ev.timestamp).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit',second:'2-digit'}) : '';
      return `<div class="feed-item"><div class="feed-icon">⚡</div><div style="flex:1;"><div style="display:flex;align-items:center;justify-content:space-between;"><div style="font-weight:600;color:#fff;font-size:0.88rem;">${eventLabel(ev.type || 'INFO')} — ${name}</div><div style="font-family:var(--font-mono);font-size:0.72rem;color:var(--text-muted);">${ts}</div></div></div></div>`;
    }).join('');
  }

  // legacy alias kept for init call compatibility
  function renderTimeline(activity) { renderLiveActivityFeed([]); }

  // 4. REASONING CARD (live — no fallback fakes)
  function renderReasoningCard(reasoning) {
    const container = document.getElementById('reasoning-summary-card');
    if (!container) return;
    const rep = (reasoning && typeof reasoning === 'object' && !reasoning.error && reasoning.topic) ? reasoning : null;
    if (!rep) {
      container.innerHTML = `<div style="padding:1rem;color:var(--text-muted);font-size:0.85rem;font-style:italic;">No reasoning session active.</div>`;
      return;
    }
    const impact = rep.expected_business_impact || {};
    const confidenceVal = impact.confidence_score ? (impact.confidence_score * 100).toFixed(0) : null;
    const ctrGain = impact.expected_ctr_gain || null;
    container.innerHTML = `
      <div style="display:flex;flex-direction:column;gap:0.75rem;">
        <div><div style="font-size:0.75rem;color:var(--accent-cyan);font-weight:700;">SELECTED OPPORTUNITY</div><div style="font-size:1.1rem;font-weight:700;color:#fff;">${rep.topic}</div></div>
        <div><div style="font-size:0.75rem;color:var(--text-muted);font-weight:600;">WHY THIS OPPORTUNITY</div><div style="font-size:0.85rem;color:var(--text-secondary);margin-top:0.25rem;">${rep.opportunity_selection_reasoning || ''}</div></div>
        ${(confidenceVal || ctrGain) ? `<div style="display:flex;gap:1rem;margin-top:0.5rem;">
          ${confidenceVal ? `<div style="background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.25);padding:0.5rem 0.85rem;border-radius:var(--radius-md);"><div style="font-size:0.7rem;color:var(--text-muted);">AI CONFIDENCE</div><div style="font-weight:700;color:var(--accent-indigo);">${confidenceVal}%</div></div>` : ''}
          ${ctrGain ? `<div style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);padding:0.5rem 0.85rem;border-radius:var(--radius-md);"><div style="font-size:0.7rem;color:var(--text-muted);">EXPECTED IMPACT</div><div style="font-weight:700;color:var(--accent-emerald);">${ctrGain}</div></div>` : ''}
        </div>` : ''}
      </div>`;
  }

  // 5. AUTOMATION DETAILS (LIVE BACKEND INTEGRATION STATUS)
  function renderAutomation(overview, connections) {
    const container = document.getElementById('automation-details-content');
    if (!container) return;

    const conn = connections || {};
    const tg = conn.telegram || { configured: false, connected: false, status: 'Not Configured', reason: 'TELEGRAM_BOT_TOKEN missing in .env' };
    const gm = conn.gemini || { configured: false, connected: false, status: 'Not Configured', model: 'gemini-2.5-pro', reason: 'GEMINI_API_KEY missing in .env' };
    const im = conn.imagen || { configured: false, connected: false, status: 'Not Configured', reason: 'API key missing or client uninitialized' };
    const pipe = conn.pipeline || { status: null, schedule: null, runner: 'Python Async Engine' };

    function getBadgeStyle(status) {
      if (status === 'Connected') return 'background: rgba(16,185,129,0.15); color: var(--accent-emerald); border: 1px solid rgba(16,185,129,0.3);';
      if (status === 'Configured') return 'background: rgba(245,158,11,0.15); color: var(--accent-amber); border: 1px solid rgba(245,158,11,0.3);';
      return 'background: rgba(244,63,94,0.15); color: var(--accent-rose); border: 1px solid rgba(244,63,94,0.3);';
    }

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.25rem;">
        <!-- Active Automation Card (populated by renderActiveAutomationCard) -->
        <div id="active-automation-card"></div>
        <!-- 3 Live Integration Service Cards with Real Test Action Buttons -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">
          <!-- 1. Telegram Dispatcher Card -->
          <div style="background: rgba(255,255,255,0.02); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color); display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">TELEGRAM BOT DISPATCH</span>
                <span id="badge-telegram" style="font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: var(--radius-full); ${getBadgeStyle(tg.status)}">
                  ${(tg.status || 'Not Configured').toUpperCase()}
                </span>
              </div>
              <div style="font-weight: 700; color: #fff; font-size: 0.95rem; margin-bottom: 0.25rem;">${tg.bot_name || 'Unconfigured'}</div>
              <div style="font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 0.75rem;">${tg.reason || 'Telegram API Integration'}</div>
            </div>
            <button class="btn btn-secondary" id="btn-test-telegram" style="width: 100%; justify-content: center;">
              ⚡ Test Telegram Connection
            </button>
            <div id="test-telegram-result" style="margin-top: 0.75rem; font-size: 0.78rem;"></div>
          </div>

          <!-- 2. Gemini LLM Engine Card -->
          <div style="background: rgba(255,255,255,0.02); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color); display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">GEMINI LLM ENGINE</span>
                <span id="badge-gemini" style="font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: var(--radius-full); ${getBadgeStyle(gm.status)}">
                  ${(gm.status || 'Not Configured').toUpperCase()}
                </span>
              </div>
              <div style="font-weight: 700; color: #fff; font-size: 0.95rem; margin-bottom: 0.25rem;">${gm.model || 'gemini-2.5-pro'}</div>
              <div style="font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 0.75rem;">${gm.reason || 'Google Gemini 2.5 Pro LLM API'}</div>
            </div>
            <button class="btn btn-secondary" id="btn-test-gemini" style="width: 100%; justify-content: center;">
              💡 Test Gemini LLM
            </button>
            <div id="test-gemini-result" style="margin-top: 0.75rem; font-size: 0.78rem;"></div>
          </div>

          <!-- 3. Google Imagen 3 Engine Card -->
          <div style="background: rgba(255,255,255,0.02); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color); display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">IMAGE SYNTHESIS ENGINE</span>
                <span id="badge-imagen" style="font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: var(--radius-full); ${getBadgeStyle(im.status)}">
                  ${(im.status || 'Not Configured').toUpperCase()}
                </span>
              </div>
              <div style="font-weight: 700; color: #fff; font-size: 0.95rem; margin-bottom: 0.25rem;" id="imagen-model-display">${im.configured_model || im.model || 'gemini-2.5-flash-image'}</div>
              <div style="font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.5rem;" id="imagen-telemetry-meta">
                Backend: ${im.backend || 'AI Studio'} • SDK: ${im.sdk_version || 'google-genai'}
              </div>
              <div style="font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 0.75rem;">${im.reason || 'Google Imagen 3 API'}</div>
            </div>
            <button class="btn btn-secondary" id="btn-test-imagen" style="width: 100%; justify-content: center;">
              🖼️ Generate Test Image
            </button>
            <div id="test-imagen-result" style="margin-top: 0.75rem; font-size: 0.78rem;"></div>
          </div>
        </div>

        <!-- Automation Schedules Management Section -->
        <div id="automation-schedules-container" style="margin-top: 1.5rem;"></div>
      </div>
    `;

    // Attach Live Connection Test Handlers
    const testTgBtn = document.getElementById('btn-test-telegram');
    const testGmBtn = document.getElementById('btn-test-gemini');
    const testImBtn = document.getElementById('btn-test-imagen');

    if (testTgBtn) {
      testTgBtn.addEventListener('click', async () => {
        const resBox = document.getElementById('test-telegram-result');
        const badge = document.getElementById('badge-telegram');
        if (resBox) resBox.innerHTML = '<span style="color: var(--accent-indigo);">Sending Telegram test message...</span>';
        try {
          const api = window.AVENIQ_API || (window.AVENIQ_APP ? await window.AVENIQ_APP.require('api') : null);
          const res = await api.testTelegram();
          if (res.success) {
            if (badge) {
              badge.textContent = 'CONNECTED';
              badge.style.cssText = 'font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: var(--radius-full); background: rgba(16,185,129,0.15); color: var(--accent-emerald); border: 1px solid rgba(16,185,129,0.3);';
            }
            if (resBox) resBox.innerHTML = `
              <div style="background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3); padding: 0.6rem; border-radius: var(--radius-sm); color: var(--accent-emerald);">
                <div style="font-weight: 700;">✅ Connected</div>
                <div>Message ID: ${res.message_id}</div>
                <div style="font-size: 0.72rem; color: var(--text-muted); margin-top: 0.2rem;">Sent to Channel: ${res.channel}</div>
              </div>
            `;
          } else {
            if (badge) {
              badge.textContent = (res.status || 'ERROR').toUpperCase();
              badge.style.cssText = 'font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: var(--radius-full); background: rgba(244,63,94,0.15); color: var(--accent-rose); border: 1px solid rgba(244,63,94,0.3);';
            }
            const errDetail = res.description || res.error || 'Telegram API Error';
            const codeStr = res.error_code ? ` (Error ${res.error_code})` : '';
            if (resBox) resBox.innerHTML = `
              <div style="background: rgba(244,63,94,0.15); border: 1px solid rgba(244,63,94,0.3); padding: 0.6rem; border-radius: var(--radius-sm); color: var(--accent-rose);">
                <div style="font-weight: 700;">❌ ${res.status || 'ERROR'}${codeStr}</div>
                <div>${errDetail}</div>
                ${res.chat_id ? `<div style="font-size: 0.72rem; color: var(--text-muted); margin-top: 0.2rem;">Target Chat ID: ${res.chat_id}</div>` : ''}
              </div>
            `;
          }
        } catch (err) {
          if (resBox) resBox.innerHTML = `<span style="color: var(--accent-rose);">❌ Connection error: ${err.message}</span>`;
        }
      });
    }

    if (testGmBtn) {
      testGmBtn.addEventListener('click', async () => {
        const resBox = document.getElementById('test-gemini-result');
        const badge = document.getElementById('badge-gemini');
        if (resBox) resBox.innerHTML = '<span style="color: var(--accent-indigo);">Executing Gemini LLM prompt...</span>';
        try {
          const api = window.AVENIQ_API || (window.AVENIQ_APP ? await window.AVENIQ_APP.require('api') : null);
          const res = await api.testGemini();
          if (res.success) {
            if (badge) {
              badge.textContent = 'CONNECTED';
              badge.style.cssText = 'font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: var(--radius-full); background: rgba(16,185,129,0.15); color: var(--accent-emerald); border: 1px solid rgba(16,185,129,0.3);';
            }
            if (resBox) resBox.innerHTML = `
              <div style="background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3); padding: 0.6rem; border-radius: var(--radius-sm); color: #fff;">
                <div style="font-weight: 700; color: var(--accent-emerald);">✅ Gemini Connected</div>
                <div style="display: flex; gap: 0.75rem; font-size: 0.72rem; color: var(--text-muted); margin: 0.2rem 0;">
                  <span>Model: <b>${res.model}</b></span>
                  <span>Latency: <b>${res.latency_ms} ms</b></span>
                  <span>Tokens: <b>${res.tokens}</b></span>
                </div>
                <div style="font-family: var(--font-mono); font-size: 0.72rem; background: rgba(0,0,0,0.3); padding: 0.4rem; border-radius: 4px; color: var(--accent-cyan); white-space: pre-wrap;">${res.output}</div>
              </div>
            `;
          } else {
            if (badge) {
              badge.textContent = (res.status || 'NOT CONFIGURED').toUpperCase();
            }
            if (resBox) resBox.innerHTML = `
              <div style="background: rgba(244,63,94,0.15); border: 1px solid rgba(244,63,94,0.3); padding: 0.6rem; border-radius: var(--radius-sm); color: var(--accent-rose);">
                <div style="font-weight: 700;">❌ ${res.status || 'Not Configured'}</div>
                <div>${res.error || 'Gemini API error'}</div>
              </div>
            `;
          }
        } catch (err) {
          if (resBox) resBox.innerHTML = `<span style="color: var(--accent-rose);">❌ API Exception: ${err.message}</span>`;
        }
      });
    }

    if (testImBtn) {
      testImBtn.addEventListener('click', async () => {
        const resBox = document.getElementById('test-imagen-result');
        const badge = document.getElementById('badge-imagen');
        if (resBox) resBox.innerHTML = '<span style="color: var(--accent-indigo);">Generating image via Google Imagen 3 & sending to Telegram...</span>';
        try {
          const api = window.AVENIQ_API || (window.AVENIQ_APP ? await window.AVENIQ_APP.require('api') : null);
          const res = await api.testImagen();
          if (res.success) {
            if (badge) {
              badge.textContent = 'CONNECTED';
              badge.style.cssText = 'font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: var(--radius-full); background: rgba(16,185,129,0.15); color: var(--accent-emerald); border: 1px solid rgba(16,185,129,0.3);';
            }
            const tgStatus = (res.telegram && res.telegram.sent)
              ? `<div style="font-size: 0.75rem; color: var(--accent-emerald); font-weight: 700; margin-top: 0.35rem;">📤 Sent to Telegram (Message ID: ${res.telegram.message_id})</div>`
              : `<div style="font-size: 0.75rem; color: var(--accent-amber); font-weight: 600; margin-top: 0.35rem;">⚠️ Telegram send failed: ${res.telegram ? res.telegram.reason : 'Not configured'}</div>`;

            if (resBox) resBox.innerHTML = `
              <div style="background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3); padding: 0.6rem; border-radius: var(--radius-sm); color: #fff;">
                <div style="font-weight: 700; color: var(--accent-emerald);">✅ Imagen Connected</div>
                <div style="font-size: 0.72rem; color: var(--text-muted); margin-top: 0.2rem;">
                  Configured Model: ${res.configured_model || res.model}<br>
                  Runtime Model: ${res.runtime_model || res.model}<br>
                  Backend: ${res.backend || 'AI Studio'} • SDK: ${res.sdk_version || 'google-genai'}<br>
                  Latency: ${res.generation_time_ms} ms
                </div>
                <div style="font-size: 0.72rem; color: var(--accent-cyan); font-family: var(--font-mono); margin-top: 0.2rem;">Saved: ${res.file_path}</div>
                ${tgStatus}
              </div>
            `;
          } else {
            if (badge) {
              badge.textContent = res.status || 'ERROR';
              badge.style.cssText = 'font-size: 0.7rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: var(--radius-full); background: rgba(244,63,94,0.15); color: var(--accent-rose); border: 1px solid rgba(244,63,94,0.3);';
            }
            if (resBox) resBox.innerHTML = `
              <div style="background: rgba(244,63,94,0.12); border: 1px solid rgba(244,63,94,0.3); padding: 0.6rem; border-radius: var(--radius-sm); color: #fff;">
                <div style="font-weight: 700; color: var(--accent-rose);">❌ ${res.error_code || 'IMAGEN_ERROR'}</div>
                <div style="font-size: 0.72rem; color: var(--text-secondary); margin-top: 0.2rem;">${res.reason || 'Image generation failed'}</div>
                <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 0.3rem;">
                  Configured: ${res.configured_model || 'N/A'} • Runtime: ${res.runtime_model || 'N/A'}<br>
                  Backend: ${res.backend || 'AI Studio'} • SDK: ${res.sdk_version || 'google-genai'}
                </div>
              </div>
            `;
          }
        } catch (err) {
          if (resBox) resBox.innerHTML = `<span style="color: var(--accent-rose);">❌ Imagen Error: ${err.message}</span>`;
        }
      });
    }

    // Render Automation Schedules Section
    renderAutomationSchedulesSection();
  }

  // ==============================================================================
  // AUTOMATION SCHEDULES MANAGEMENT ENGINE (UI, KPIs, CRUD, EXPAND, MODALS)
  // ==============================================================================
  let schState = {
    query: '',
    department: '',
    status: '',
    schedules: [],
    selectedIds: new Set(),
    summary: {},
    activeEditingSchedule: null
  };

  async function renderAutomationSchedulesSection() {
    const container = document.getElementById('automation-schedules-container');
    if (!container) return;

    // Toast Container Injection
    if (!document.getElementById('sch-toast-container')) {
      const toastBox = document.createElement('div');
      toastBox.id = 'sch-toast-container';
      toastBox.style.cssText = 'position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 9999; display: flex; flex-direction: column; gap: 0.5rem; max-width: 380px; pointer-events: none;';
      document.body.appendChild(toastBox);
    }

    // Modal Containers Injection
    if (!document.getElementById('modal-schedule-editor')) {
      injectScheduleModals();
    }

    try {
      const api = window.AVENIQ_API || (window.AVENIQ_APP ? await window.AVENIQ_APP.require('api') : null);
      if (!api) return;

      const [summaryRes, schedulesRes] = await Promise.all([
        api.getScheduleSummary(),
        api.getSchedules(schState.query, schState.department, schState.status)
      ]);

      schState.summary = summaryRes || {};
      schState.schedules = (schedulesRes && schedulesRes.schedules) ? schedulesRes.schedules : [];
    } catch (err) {
      console.warn('[Automation Schedules] Load error:', err);
    }

    const sum = schState.summary;

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.25rem;">
        <!-- KPI Summary Cards Banner -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 0.75rem;">
          <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 0.85rem 1rem;">
            <div style="font-size: 0.7rem; color: var(--text-muted); font-weight: 700;">TOTAL SCHEDULES</div>
            <div style="font-size: 1.35rem; font-weight: 800; color: #fff; margin-top: 0.2rem;">${sum.total_schedules || 0}</div>
          </div>
          <div style="background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.25); border-radius: var(--radius-md); padding: 0.85rem 1rem;">
            <div style="font-size: 0.7rem; color: var(--accent-emerald); font-weight: 700;">RUNNING / ACTIVE</div>
            <div style="font-size: 1.35rem; font-weight: 800; color: var(--accent-emerald); margin-top: 0.2rem;">${sum.running || 0}</div>
          </div>
          <div style="background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.25); border-radius: var(--radius-md); padding: 0.85rem 1rem;">
            <div style="font-size: 0.7rem; color: var(--accent-amber); font-weight: 700;">PAUSED</div>
            <div style="font-size: 1.35rem; font-weight: 800; color: var(--accent-amber); margin-top: 0.2rem;">${sum.paused || 0}</div>
          </div>
          <div style="background: rgba(244,63,94,0.08); border: 1px solid rgba(244,63,94,0.25); border-radius: var(--radius-md); padding: 0.85rem 1rem;">
            <div style="font-size: 0.7rem; color: var(--accent-rose); font-weight: 700;">DISABLED</div>
            <div style="font-size: 1.35rem; font-weight: 800; color: var(--accent-rose); margin-top: 0.2rem;">${sum.disabled || 0}</div>
          </div>
          <div style="background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.25); border-radius: var(--radius-md); padding: 0.85rem 1rem;">
            <div style="font-size: 0.7rem; color: #ef4444; font-weight: 700;">FAILED TODAY</div>
            <div style="font-size: 1.35rem; font-weight: 800; color: #ef4444; margin-top: 0.2rem;">${sum.failed_today || 0}</div>
          </div>
          <div style="background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.25); border-radius: var(--radius-md); padding: 0.85rem 1rem;">
            <div style="font-size: 0.7rem; color: var(--accent-indigo); font-weight: 700;">NEXT EXECUTION</div>
            <div style="font-size: 0.78rem; font-weight: 700; color: #fff; margin-top: 0.35rem; font-family: var(--font-mono); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              ${sum.next_execution ? formatShortTime(sum.next_execution) : 'None'}
            </div>
          </div>
        </div>

        <!-- Automation Schedules Main Card -->
        <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1.25rem;">
          <!-- Card Header & Toolbar -->
          <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 0.75rem; margin-bottom: 1rem; padding-bottom: 0.85rem; border-bottom: 1px solid rgba(255,255,255,0.06);">
            <div>
              <div style="font-size: 1.05rem; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 0.5rem;">
                <span>⏱️ Automation Schedules</span>
                <span style="font-size: 0.72rem; background: rgba(99,102,241,0.15); color: var(--accent-indigo); padding: 0.15rem 0.5rem; border-radius: var(--radius-full); font-weight: 700;">Control Center</span>
              </div>
              <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.15rem;">Manage scheduled autonomous workflows, triggers, and execution history.</div>
            </div>

            <!-- Toolbar Action Buttons & Filters -->
            <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem;">
              <input type="text" id="sch-search-input" placeholder="🔍 Search schedules..." value="${schState.query}" style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 0.4rem 0.75rem; border-radius: var(--radius-sm); font-size: 0.8rem; min-width: 180px;">
              
              <select id="sch-dept-filter" style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 0.4rem 0.5rem; border-radius: var(--radius-sm); font-size: 0.8rem;">
                <option value="" ${!schState.department ? 'selected' : ''}>All Depts</option>
                <option value="Creative" ${schState.department === 'Creative' ? 'selected' : ''}>Creative</option>
                <option value="Content" ${schState.department === 'Content' ? 'selected' : ''}>Content</option>
                <option value="Research" ${schState.department === 'Research' ? 'selected' : ''}>Research</option>
                <option value="Strategy" ${schState.department === 'Strategy' ? 'selected' : ''}>Strategy</option>
                <option value="Editorial" ${schState.department === 'Editorial' ? 'selected' : ''}>Editorial</option>
                <option value="Delivery" ${schState.department === 'Delivery' ? 'selected' : ''}>Delivery</option>
                <option value="Analytics" ${schState.department === 'Analytics' ? 'selected' : ''}>Analytics</option>
              </select>

              <select id="sch-status-filter" style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 0.4rem 0.5rem; border-radius: var(--radius-sm); font-size: 0.8rem;">
                <option value="" ${!schState.status ? 'selected' : ''}>All Status</option>
                <option value="active" ${schState.status === 'active' ? 'selected' : ''}>Active</option>
                <option value="paused" ${schState.status === 'paused' ? 'selected' : ''}>Paused</option>
                <option value="disabled" ${schState.status === 'disabled' ? 'selected' : ''}>Disabled</option>
              </select>

              <select id="sch-bulk-select" style="background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.3); color: var(--accent-indigo); padding: 0.4rem 0.5rem; border-radius: var(--radius-sm); font-size: 0.8rem; font-weight: 700;">
                <option value="">Bulk Actions...</option>
                <option value="enable">⚡ Enable Selected</option>
                <option value="disable">🔴 Disable Selected</option>
                <option value="pause">🟡 Pause Selected</option>
                <option value="run_now">▶ Run Selected</option>
                <option value="delete">🗑 Delete Selected</option>
              </select>

              <button class="btn btn-secondary" id="sch-btn-import" title="Import JSON" style="padding: 0.4rem 0.65rem; font-size: 0.8rem;">📥 Import</button>
              <button class="btn btn-secondary" id="sch-btn-export" title="Export JSON" style="padding: 0.4rem 0.65rem; font-size: 0.8rem;">📤 Export</button>
              <button class="btn btn-secondary" id="sch-btn-refresh" title="Refresh" style="padding: 0.4rem 0.65rem; font-size: 0.8rem;">🔄</button>
              
              <button class="btn btn-primary" id="sch-btn-add" style="padding: 0.4rem 0.85rem; font-size: 0.82rem; font-weight: 700; background: var(--accent-indigo);">
                ✅ Add Schedule
              </button>
            </div>
          </div>

          <!-- Schedule Table Container -->
          <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; color: #fff;">
              <thead>
                <tr style="background: rgba(255,255,255,0.03); color: var(--text-muted); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid var(--border-color);">
                  <th style="padding: 0.65rem; text-align: center; width: 32px;">
                    <input type="checkbox" id="sch-select-all" style="cursor: pointer;">
                  </th>
                  <th style="padding: 0.65rem; text-align: left;">Status</th>
                  <th style="padding: 0.65rem; text-align: left;">Name & Description</th>
                  <th style="padding: 0.65rem; text-align: left;">Department</th>
                  <th style="padding: 0.65rem; text-align: left;">Trigger & TZ</th>
                  <th style="padding: 0.65rem; text-align: left;">Next Run</th>
                  <th style="padding: 0.65rem; text-align: left;">Last Run</th>
                  <th style="padding: 0.65rem; text-align: right;">Actions</th>
                </tr>
              </thead>
              <tbody id="sch-table-body">
                ${renderScheduleRowsHtml(schState.schedules)}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;

    attachScheduleEventListeners();
  }

  function renderScheduleRowsHtml(schedules) {
    if (!schedules || schedules.length === 0) {
      return `
        <tr>
          <td colspan="8" style="padding: 2rem; text-align: center; color: var(--text-muted); font-size: 0.85rem;">
            No automation schedules found matching your criteria. Click <b>Add Schedule</b> to create one.
          </td>
        </tr>
      `;
    }

    return schedules.map(s => {
      const isSelected = schState.selectedIds.has(s.id);
      const isEnabled = s.enabled !== false && s.state !== 'disabled';
      const isPaused = s.state === 'paused';
      
      let badgeStyle = 'background: rgba(16,185,129,0.15); color: var(--accent-emerald); border: 1px solid rgba(16,185,129,0.3);';
      let statusText = '🟢 ACTIVE';

      if (isPaused) {
        badgeStyle = 'background: rgba(245,158,11,0.15); color: var(--accent-amber); border: 1px solid rgba(245,158,11,0.3);';
        statusText = '🟡 PAUSED';
      } else if (!isEnabled) {
        badgeStyle = 'background: rgba(244,63,94,0.15); color: var(--accent-rose); border: 1px solid rgba(244,63,94,0.3);';
        statusText = '🔴 DISABLED';
      }

      const priorityStyle = s.priority === 'CRITICAL' ? 'color: #ef4444;' : s.priority === 'HIGH' ? 'color: var(--accent-amber);' : 'color: var(--text-muted);';

      return `
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s ease;" class="sch-row-${s.id}">
          <td style="padding: 0.75rem 0.65rem; text-align: center;">
            <input type="checkbox" class="sch-check-item" data-id="${s.id}" ${isSelected ? 'checked' : ''} style="cursor: pointer;">
          </td>
          <td style="padding: 0.75rem 0.65rem;">
            <span style="font-size: 0.68rem; font-weight: 700; padding: 0.2rem 0.5rem; border-radius: var(--radius-full); ${badgeStyle}">
              ${statusText}
            </span>
          </td>
          <td style="padding: 0.75rem 0.65rem;">
            <div style="font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.4rem;">
              <span>${escapeHtml(s.name)}</span>
              <span style="font-size: 0.65rem; font-weight: 800; ${priorityStyle}">[${s.priority || 'MEDIUM'}]</span>
            </div>
            <div style="font-size: 0.74rem; color: var(--text-muted); max-width: 320px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              ${escapeHtml(s.description || 'No description')}
            </div>
          </td>
          <td style="padding: 0.75rem 0.65rem;">
            <span style="font-size: 0.75rem; background: rgba(255,255,255,0.04); padding: 0.2rem 0.5rem; border-radius: 4px; color: var(--accent-cyan);">
              ${escapeHtml(s.department || 'General')}
            </span>
          </td>
          <td style="padding: 0.75rem 0.65rem;">
            <div style="font-size: 0.78rem; font-weight: 600; color: #fff; text-transform: capitalize;">${s.trigger || 'daily'} (${s.time || '08:00'})</div>
            <div style="font-size: 0.7rem; color: var(--text-muted);">${s.timezone || 'Asia/Kolkata'}</div>
          </td>
          <td style="padding: 0.75rem 0.65rem; font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent-indigo);">
            ${s.next_run ? formatShortTime(s.next_run) : 'None'}
          </td>
          <td style="padding: 0.75rem 0.65rem; font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted);">
            ${s.last_run ? formatShortTime(s.last_run) : 'Never'}
          </td>
          <td style="padding: 0.75rem 0.65rem; text-align: right;">
            <div style="display: flex; align-items: center; justify-content: flex-end; gap: 0.35rem;">
              <button class="btn btn-secondary btn-sch-edit" data-id="${s.id}" title="Edit Schedule" style="padding: 0.25rem 0.5rem; font-size: 0.72rem;">✏ Edit</button>
              <button class="btn btn-secondary btn-sch-run" data-id="${s.id}" title="Run Immediately" style="padding: 0.25rem 0.5rem; font-size: 0.72rem; color: var(--accent-emerald);">▶ Run</button>
              <button class="btn btn-secondary btn-sch-toggle" data-id="${s.id}" title="${isPaused ? 'Resume Schedule' : 'Pause Schedule'}" style="padding: 0.25rem 0.5rem; font-size: 0.72rem; color: var(--accent-amber);">${isPaused ? '▶ Resume' : '⏸ Pause'}</button>
              <button class="btn btn-secondary btn-sch-duplicate" data-id="${s.id}" title="Duplicate" style="padding: 0.25rem 0.4rem; font-size: 0.72rem;">📋</button>
              <button class="btn btn-secondary btn-sch-delete" data-id="${s.id}" title="Delete" style="padding: 0.25rem 0.4rem; font-size: 0.72rem; color: var(--accent-rose);">🗑</button>
              <button class="btn btn-secondary btn-sch-expand" data-id="${s.id}" title="Expand Details" style="padding: 0.25rem 0.4rem; font-size: 0.72rem;">▼</button>
            </div>
          </td>
        </tr>
        <!-- Expandable Detail Row -->
        <tr id="sch-detail-${s.id}" style="display: none; background: rgba(0,0,0,0.25); border-bottom: 1px solid var(--border-color);">
          <td colspan="8" style="padding: 1rem 1.25rem;">
            <div style="display: flex; flex-direction: column; gap: 0.85rem;">
              <!-- Detail Header Info -->
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;">
                <div>
                  <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700;">PROMPT WORKFLOW TEMPLATE</div>
                  <div style="font-family: var(--font-mono); font-size: 0.76rem; background: rgba(0,0,0,0.4); padding: 0.5rem; border-radius: 4px; color: var(--accent-cyan); margin-top: 0.25rem; white-space: pre-wrap;">${escapeHtml(s.prompt || 'No prompt set')}</div>
                </div>
                <div>
                  <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700;">OUTPUT DESTINATIONS</div>
                  <div style="display: flex; gap: 0.4rem; margin-top: 0.35rem; flex-wrap: wrap;">
                    ${(s.outputs || ['dashboard']).map(o => `<span style="font-size: 0.7rem; background: rgba(99,102,241,0.15); color: var(--accent-indigo); padding: 0.15rem 0.45rem; border-radius: 4px; font-weight: 700; text-transform: uppercase;">${o}</span>`).join('')}
                  </div>
                  <div style="font-size: 0.72rem; color: var(--text-muted); margin-top: 0.6rem;">
                    Created: ${formatShortTime(s.created_at)} • Updated: ${formatShortTime(s.updated_at)}
                  </div>
                </div>
                <div>
                  <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 700;">PERFORMANCE TELEMETRY</div>
                  <div style="font-size: 0.75rem; color: #fff; margin-top: 0.25rem; line-height: 1.4;">
                    Executions: <b>${s.statistics ? s.statistics.execution_count : 0}</b> • Success Rate: <b>${getSuccessRate(s.statistics)}%</b><br>
                    Avg Duration: <b>${s.statistics ? s.statistics.average_duration_ms : 0} ms</b> • Failures: <b>${s.statistics ? s.statistics.failure_count : 0}</b>
                  </div>
                </div>
              </div>

              <!-- Last Result & History Log Container -->
              <div id="sch-history-container-${s.id}" style="margin-top: 0.5rem;">
                <button class="btn btn-secondary btn-load-history" data-id="${s.id}" style="font-size: 0.75rem; padding: 0.3rem 0.65rem;">
                  📜 View Execution History Log
                </button>
                <div class="sch-history-content" style="margin-top: 0.5rem;"></div>
              </div>
            </div>
          </td>
        </tr>
      `;
    }).join('');
  }

  function attachScheduleEventListeners() {
    const api = window.AVENIQ_API;

    // Search & Filters
    const searchInp = document.getElementById('sch-search-input');
    const deptFlt = document.getElementById('sch-dept-filter');
    const statusFlt = document.getElementById('sch-status-filter');

    if (searchInp) {
      searchInp.addEventListener('input', (e) => {
        schState.query = e.target.value;
        renderAutomationSchedulesSection();
      });
    }
    if (deptFlt) {
      deptFlt.addEventListener('change', (e) => {
        schState.department = e.target.value;
        renderAutomationSchedulesSection();
      });
    }
    if (statusFlt) {
      statusFlt.addEventListener('change', (e) => {
        schState.status = e.target.value;
        renderAutomationSchedulesSection();
      });
    }

    // Refresh button
    const btnRef = document.getElementById('sch-btn-refresh');
    if (btnRef) btnRef.addEventListener('click', () => renderAutomationSchedulesSection());

    // Add Schedule button
    const btnAdd = document.getElementById('sch-btn-add');
    if (btnAdd) btnAdd.addEventListener('click', () => openScheduleModal());

    // Import / Export buttons
    const btnImp = document.getElementById('sch-btn-import');
    const btnExp = document.getElementById('sch-btn-export');
    if (btnImp) btnImp.addEventListener('click', () => openImportExportModal('import'));
    if (btnExp) btnExp.addEventListener('click', () => openImportExportModal('export'));

    // Checkbox select all
    const chkAll = document.getElementById('sch-select-all');
    if (chkAll) {
      chkAll.addEventListener('change', (e) => {
        const checked = e.target.checked;
        document.querySelectorAll('.sch-check-item').forEach(c => {
          c.checked = checked;
          const sid = c.getAttribute('data-id');
          if (checked) schState.selectedIds.add(sid);
          else schState.selectedIds.delete(sid);
        });
      });
    }

    document.querySelectorAll('.sch-check-item').forEach(c => {
      c.addEventListener('change', (e) => {
        const sid = e.target.getAttribute('data-id');
        if (e.target.checked) schState.selectedIds.add(sid);
        else schState.selectedIds.delete(sid);
      });
    });

    // Bulk actions
    const bulkSel = document.getElementById('sch-bulk-select');
    if (bulkSel) {
      bulkSel.addEventListener('change', async (e) => {
        const act = e.target.value;
        if (!act) return;
        if (schState.selectedIds.size === 0) {
          showToast('Please select at least one schedule.', 'warning');
          e.target.value = '';
          return;
        }

        if (act === 'delete' && !confirm(`Delete ${schState.selectedIds.size} selected automation schedule(s)?`)) {
          e.target.value = '';
          return;
        }

        try {
          const res = await api.bulkSchedules(act, Array.from(schState.selectedIds));
          if (res.success) {
            showToast(`Bulk action '${act}' completed for ${res.affected_count} schedules.`, 'success');
            schState.selectedIds.clear();
            renderAutomationSchedulesSection();
          }
        } catch (err) {
          showToast(`Bulk action failed: ${err.message}`, 'error');
        }
        e.target.value = '';
      });
    }

    // Row Action Buttons: Edit, Run, Toggle, Duplicate, Delete, Expand
    document.querySelectorAll('.btn-sch-edit').forEach(b => {
      b.addEventListener('click', () => {
        const sid = b.getAttribute('data-id');
        const sch = schState.schedules.find(s => s.id === sid);
        if (sch) openScheduleModal(sch);
      });
    });

    document.querySelectorAll('.btn-sch-run').forEach(b => {
      b.addEventListener('click', async () => {
        const sid = b.getAttribute('data-id');
        showToast('Enqueueing schedule for background execution...', 'info');
        try {
          const res = await api.runSchedule(sid);
          if (res.success) {
            showToast('Schedule execution started in background.', 'success');
            renderAutomationSchedulesSection();
          }
        } catch (err) {
          showToast(`Execution failed: ${err.message}`, 'error');
        }
      });
    });

    document.querySelectorAll('.btn-sch-toggle').forEach(b => {
      b.addEventListener('click', async () => {
        const sid = b.getAttribute('data-id');
        const sch = schState.schedules.find(s => s.id === sid);
        const newState = (sch && sch.state === 'paused') ? 'active' : 'paused';
        try {
          const res = await api.toggleSchedule(sid, newState);
          if (res.success) {
            showToast(`Schedule state changed to '${newState}'.`, 'success');
            renderAutomationSchedulesSection();
          }
        } catch (err) {
          showToast(`Toggle failed: ${err.message}`, 'error');
        }
      });
    });

    document.querySelectorAll('.btn-sch-duplicate').forEach(b => {
      b.addEventListener('click', async () => {
        const sid = b.getAttribute('data-id');
        try {
          const res = await api.duplicateSchedule(sid);
          if (res.success) {
            showToast(`Schedule duplicated successfully.`, 'success');
            renderAutomationSchedulesSection();
          }
        } catch (err) {
          showToast(`Duplicate failed: ${err.message}`, 'error');
        }
      });
    });

    document.querySelectorAll('.btn-sch-delete').forEach(b => {
      b.addEventListener('click', async () => {
        const sid = b.getAttribute('data-id');
        if (confirm('Delete this automation schedule? This action cannot be undone.')) {
          try {
            const res = await api.deleteSchedule(sid);
            if (res.success) {
              showToast('Schedule deleted.', 'success');
              renderAutomationSchedulesSection();
            }
          } catch (err) {
            showToast(`Delete failed: ${err.message}`, 'error');
          }
        }
      });
    });

    document.querySelectorAll('.btn-sch-expand').forEach(b => {
      b.addEventListener('click', () => {
        const sid = b.getAttribute('data-id');
        const dRow = document.getElementById(`sch-detail-${sid}`);
        if (dRow) {
          const isOpen = dRow.style.display !== 'none';
          dRow.style.display = isOpen ? 'none' : 'table-row';
          b.textContent = isOpen ? '▼' : '▲';
        }
      });
    });

    // History Log Loader
    document.querySelectorAll('.btn-load-history').forEach(b => {
      b.addEventListener('click', async () => {
        const sid = b.getAttribute('data-id');
        const box = b.nextElementSibling;
        box.innerHTML = '<span style="font-size: 0.75rem; color: var(--accent-indigo);">Loading execution history logs...</span>';
        try {
          const res = await api.getScheduleHistory(sid);
          const history = (res && res.history) ? res.history : [];
          if (history.length === 0) {
            box.innerHTML = '<div style="font-size: 0.75rem; color: var(--text-muted); font-style: italic;">No historical execution records found. Run schedule to generate history.</div>';
            return;
          }

          box.innerHTML = `
            <table style="width: 100%; border-collapse: collapse; font-size: 0.74rem; background: rgba(0,0,0,0.3); border-radius: 4px;">
              <thead>
                <tr style="color: var(--text-muted); border-bottom: 1px solid var(--border-color); text-align: left;">
                  <th style="padding: 0.4rem;">Execution ID</th>
                  <th style="padding: 0.4rem;">Trigger</th>
                  <th style="padding: 0.4rem;">Status</th>
                  <th style="padding: 0.4rem;">Duration</th>
                  <th style="padding: 0.4rem;">Completed At</th>
                  <th style="padding: 0.4rem;">Checklist & Summary</th>
                </tr>
              </thead>
              <tbody>
                ${history.map(h => `
                  <tr style="border-bottom: 1px solid rgba(255,255,255,0.03);">
                    <td style="padding: 0.4rem; font-family: var(--font-mono); color: var(--accent-cyan);">${h.execution_id}</td>
                    <td style="padding: 0.4rem; text-transform: capitalize;">${h.trigger}</td>
                    <td style="padding: 0.4rem;">
                      <span style="color: ${h.status === 'success' ? 'var(--accent-emerald)' : 'var(--accent-rose)'}; font-weight: 700;">
                        ${(h.status || 'success').toUpperCase()}
                      </span>
                    </td>
                    <td style="padding: 0.4rem;">${h.duration_ms} ms</td>
                    <td style="padding: 0.4rem; font-family: var(--font-mono); color: var(--text-muted);">${formatShortTime(h.completed_at)}</td>
                    <td style="padding: 0.4rem;">
                      <div>${escapeHtml(h.output_summary)}</div>
                      <div style="font-size: 0.7rem; color: var(--accent-emerald); display: flex; gap: 0.4rem; margin-top: 0.15rem;">
                        ${(h.checklist || []).join(' • ')}
                      </div>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          `;
        } catch (err) {
          box.innerHTML = `<span style="font-size: 0.75rem; color: var(--accent-rose);">Failed to load history: ${err.message}</span>`;
        }
      });
    });
  }

  // ==============================================================================
  // MODAL DIALOGS (ADD/EDIT SCHEDULE & IMPORT/EXPORT)
  // ==============================================================================
  function injectScheduleModals() {
    const modalHtml = `
      <!-- Schedule Editor Modal -->
      <div id="modal-schedule-editor" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.75); backdrop-filter: blur(10px); z-index: 99999; align-items: center; justify-content: center; padding: 1rem;">
        <div style="background: #0f172a; border: 1px solid var(--border-color); border-radius: var(--radius-md); width: 100%; max-width: 650px; max-height: 90vh; display: flex; flex-direction: column; overflow: hidden; box-shadow: var(--shadow-modal);">
          <!-- Modal Header -->
          <div style="padding: 1rem 1.25rem; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.02);">
            <div style="font-size: 1.05rem; font-weight: 800; color: #fff;" id="sch-modal-title">Add Automation Schedule</div>
            <button id="sch-modal-close" style="background: none; border: none; color: var(--text-muted); font-size: 1.25rem; cursor: pointer;">✕</button>
          </div>

          <!-- Modal Body -->
          <div style="padding: 1.25rem; overflow-y: auto; display: flex; flex-direction: column; gap: 1rem;">
            <!-- Validation Banner -->
            <div id="sch-modal-error" style="display: none; background: rgba(244,63,94,0.15); border: 1px solid rgba(244,63,94,0.3); color: var(--accent-rose); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); font-size: 0.78rem;"></div>

            <!-- General Fields -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.85rem;">
              <div>
                <label style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">Automation Name *</label>
                <input type="text" id="sch-inp-name" placeholder="e.g. Daily Content Pipeline" style="width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 0.5rem; border-radius: var(--radius-sm); font-size: 0.82rem; margin-top: 0.2rem;">
              </div>
              <div>
                <label style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">Department</label>
                <select id="sch-inp-dept" style="width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 0.5rem; border-radius: var(--radius-sm); font-size: 0.82rem; margin-top: 0.2rem;">
                  <option value="Creative">Creative</option>
                  <option value="Content">Content</option>
                  <option value="Research">Research</option>
                  <option value="Strategy">Strategy</option>
                  <option value="Editorial">Editorial</option>
                  <option value="Delivery">Delivery</option>
                  <option value="Analytics">Analytics</option>
                </select>
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.85rem;">
              <div>
                <label style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">Priority</label>
                <select id="sch-inp-priority" style="width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 0.5rem; border-radius: var(--radius-sm); font-size: 0.82rem; margin-top: 0.2rem;">
                  <option value="LOW">LOW</option>
                  <option value="MEDIUM" selected>MEDIUM</option>
                  <option value="HIGH">HIGH</option>
                  <option value="CRITICAL">CRITICAL</option>
                </select>
              </div>
              <div>
                <label style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">Timezone</label>
                <input type="text" id="sch-inp-tz" value="Asia/Kolkata" style="width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 0.5rem; border-radius: var(--radius-sm); font-size: 0.82rem; margin-top: 0.2rem;">
              </div>
            </div>

            <div>
              <label style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">Description</label>
              <textarea id="sch-inp-desc" rows="2" placeholder="Brief summary of what this automation executes..." style="width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 0.5rem; border-radius: var(--radius-sm); font-size: 0.82rem; margin-top: 0.2rem; resize: vertical;"></textarea>
            </div>

            <!-- Trigger Settings & Live Preview -->
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 0.85rem; border-radius: var(--radius-sm);">
              <div style="font-size: 0.78rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem;">Trigger Schedule & Recurrence</div>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.85rem;">
                <div>
                  <label style="font-size: 0.72rem; color: var(--text-muted);">Trigger Type</label>
                  <select id="sch-inp-trigger" style="width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 0.45rem; border-radius: 4px; font-size: 0.8rem; margin-top: 0.2rem;">
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                    <option value="hourly">Hourly</option>
                    <option value="every_x_minutes">Every X Minutes</option>
                    <option value="every_x_hours">Every X Hours</option>
                    <option value="every_x_days">Every X Days</option>
                    <option value="weekdays_only">Weekdays Only</option>
                    <option value="one_time">One Time</option>
                    <option value="custom_cron">Custom Cron</option>
                  </select>
                </div>
                <div>
                  <label style="font-size: 0.72rem; color: var(--text-muted);">Execution Time (HH:MM)</label>
                  <input type="text" id="sch-inp-time" value="08:00" style="width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 0.45rem; border-radius: 4px; font-size: 0.8rem; margin-top: 0.2rem;">
                </div>
              </div>

              <!-- Upcoming Executions Live Preview Box -->
              <div style="margin-top: 0.75rem; background: rgba(0,0,0,0.4); padding: 0.6rem; border-radius: 4px;">
                <div style="font-size: 0.7rem; color: var(--accent-indigo); font-weight: 700; margin-bottom: 0.3rem;">📅 Upcoming Executions Preview:</div>
                <div id="sch-preview-list" style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-secondary); line-height: 1.4;">
                  Computing upcoming executions...
                </div>
              </div>
            </div>

            <!-- Prompt Editor & Variable Pills -->
            <div>
              <label style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;">Prompt Workflow Template *</label>
              <textarea id="sch-inp-prompt" rows="3" placeholder="Enter instructions for AI execution..." style="width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: #fff; padding: 0.5rem; border-radius: var(--radius-sm); font-size: 0.82rem; margin-top: 0.2rem; resize: vertical;"></textarea>
              <div style="display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.35rem; align-items: center;">
                <span style="font-size: 0.7rem; color: var(--text-muted);">Variables:</span>
                ${['{{today}}', '{{date}}', '{{time}}', '{{company}}', '{{department}}', '{{campaign}}', '{{month}}', '{{year}}'].map(v => `<button type="button" class="btn-var-pill" data-var="${v}" style="background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.3); color: var(--accent-indigo); padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.7rem; cursor: pointer;">${v}</button>`).join('')}
              </div>
            </div>

            <!-- Outputs Checkboxes & Enable Switch -->
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.02); padding: 0.75rem; border-radius: var(--radius-sm); border: 1px solid var(--border-color);">
              <div>
                <label style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700; display: block; margin-bottom: 0.2rem;">Output Channels</label>
                <div style="display: flex; gap: 0.85rem; font-size: 0.78rem; color: #fff;">
                  <label><input type="checkbox" class="sch-chk-out" value="telegram" checked> Telegram</label>
                  <label><input type="checkbox" class="sch-chk-out" value="dashboard" checked> Dashboard</label>
                  <label><input type="checkbox" class="sch-chk-out" value="email"> Email</label>
                  <label><input type="checkbox" class="sch-chk-out" value="file"> File</label>
                </div>
              </div>

              <div>
                <label style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700; display: block; margin-bottom: 0.2rem;">Enabled</label>
                <input type="checkbox" id="sch-inp-enabled" checked style="transform: scale(1.2); cursor: pointer;">
              </div>
            </div>
          </div>

          <!-- Modal Footer -->
          <div style="padding: 0.85rem 1.25rem; border-top: 1px solid var(--border-color); display: flex; align-items: center; justify-content: flex-end; gap: 0.65rem; background: rgba(255,255,255,0.02);">
            <button class="btn btn-secondary" id="sch-modal-cancel" style="font-size: 0.8rem;">Cancel</button>
            <button class="btn btn-primary" id="sch-modal-save" style="font-size: 0.8rem; background: var(--accent-indigo);">Save Schedule</button>
          </div>
        </div>
      </div>

      <!-- Import / Export Modal -->
      <div id="modal-schedule-import-export" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.75); backdrop-filter: blur(10px); z-index: 99999; align-items: center; justify-content: center; padding: 1rem;">
        <div style="background: #0f172a; border: 1px solid var(--border-color); border-radius: var(--radius-md); width: 100%; max-width: 580px; max-height: 85vh; display: flex; flex-direction: column; overflow: hidden; box-shadow: var(--shadow-modal);">
          <div style="padding: 1rem 1.25rem; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
            <div style="font-size: 1.05rem; font-weight: 800; color: #fff;" id="sch-ie-title">Import / Export Schedules</div>
            <button id="sch-ie-close" style="background: none; border: none; color: var(--text-muted); font-size: 1.25rem; cursor: pointer;">✕</button>
          </div>

          <div style="padding: 1.25rem; overflow-y: auto;">
            <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 0.5rem;" id="sch-ie-subtitle">Paste JSON schedules array to import or copy exported JSON:</div>
            <textarea id="sch-ie-json" rows="12" style="width: 100%; background: rgba(0,0,0,0.4); border: 1px solid var(--border-color); color: var(--accent-cyan); font-family: var(--font-mono); font-size: 0.75rem; padding: 0.65rem; border-radius: var(--radius-sm); resize: vertical;"></textarea>
          </div>

          <div style="padding: 0.85rem 1.25rem; border-top: 1px solid var(--border-color); display: flex; align-items: center; justify-content: flex-end; gap: 0.65rem;">
            <button class="btn btn-secondary" id="sch-ie-cancel" style="font-size: 0.8rem;">Cancel</button>
            <button class="btn btn-primary" id="sch-ie-submit" style="font-size: 0.8rem; background: var(--accent-indigo);">Import JSON</button>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHtml);
    attachModalHandlers();
  }

  function attachModalHandlers() {
    const editor = document.getElementById('modal-schedule-editor');
    const ieModal = document.getElementById('modal-schedule-import-export');

    document.getElementById('sch-modal-close').addEventListener('click', () => editor.style.display = 'none');
    document.getElementById('sch-modal-cancel').addEventListener('click', () => editor.style.display = 'none');

    document.getElementById('sch-ie-close').addEventListener('click', () => ieModal.style.display = 'none');
    document.getElementById('sch-ie-cancel').addEventListener('click', () => ieModal.style.display = 'none');

    // Variable Pills Click -> Insert into prompt
    document.querySelectorAll('.btn-var-pill').forEach(btn => {
      btn.addEventListener('click', () => {
        const v = btn.getAttribute('data-var');
        const txt = document.getElementById('sch-inp-prompt');
        if (txt) {
          txt.value += (txt.value ? ' ' : '') + v;
        }
      });
    });

    // Recalculate preview on trigger / time change
    const trigSel = document.getElementById('sch-inp-trigger');
    const timeInp = document.getElementById('sch-inp-time');
    const tzInp = document.getElementById('sch-inp-tz');

    const updatePreview = async () => {
      const api = window.AVENIQ_API;
      if (!api) return;
      try {
        const res = await api.previewSchedule({
          trigger: trigSel.value,
          time: timeInp.value,
          timezone: tzInp.value
        });
        const prevs = (res && res.upcoming_executions) ? res.upcoming_executions : [];
        const box = document.getElementById('sch-preview-list');
        if (box) {
          box.innerHTML = prevs.map((p, i) => `<div>${i+1}. ${formatShortTime(p)}</div>`).join('');
        }
      } catch (err) {
        console.warn('Preview calculation error:', err);
      }
    };

    if (trigSel) trigSel.addEventListener('change', updatePreview);
    if (timeInp) timeInp.addEventListener('input', updatePreview);
    if (tzInp) tzInp.addEventListener('input', updatePreview);

    // Save Schedule
    document.getElementById('sch-modal-save').addEventListener('click', async () => {
      const api = window.AVENIQ_API;
      const errBox = document.getElementById('sch-modal-error');
      errBox.style.display = 'none';

      const name = document.getElementById('sch-inp-name').value.trim();
      const prompt = document.getElementById('sch-inp-prompt').value.trim();

      if (!name) {
        errBox.textContent = 'Schedule Name cannot be empty.';
        errBox.style.display = 'block';
        return;
      }
      if (!prompt) {
        errBox.textContent = 'Prompt Workflow Template cannot be empty.';
        errBox.style.display = 'block';
        return;
      }

      const selectedOuts = Array.from(document.querySelectorAll('.sch-chk-out:checked')).map(c => c.value);

      const payload = {
        name: name,
        description: document.getElementById('sch-inp-desc').value.trim(),
        department: document.getElementById('sch-inp-dept').value,
        priority: document.getElementById('sch-inp-priority').value,
        trigger: document.getElementById('sch-inp-trigger').value,
        time: document.getElementById('sch-inp-time').value.trim(),
        timezone: document.getElementById('sch-inp-tz').value.trim(),
        prompt: prompt,
        outputs: selectedOuts,
        enabled: document.getElementById('sch-inp-enabled').checked,
        state: document.getElementById('sch-inp-enabled').checked ? 'active' : 'disabled'
      };

      try {
        let res;
        if (schState.activeEditingSchedule) {
          res = await api.updateSchedule(schState.activeEditingSchedule.id, payload);
          showToast('Schedule updated successfully.', 'success');
        } else {
          res = await api.createSchedule(payload);
          showToast('New schedule created successfully.', 'success');
        }

        if (res.success || res.id) {
          editor.style.display = 'none';
          renderAutomationSchedulesSection();
        } else {
          errBox.textContent = res.error || 'Failed to save schedule.';
          errBox.style.display = 'block';
        }
      } catch (err) {
        errBox.textContent = err.message;
        errBox.style.display = 'block';
      }
    });
  }

  function openScheduleModal(schedule = null) {
    schState.activeEditingSchedule = schedule;
    const editor = document.getElementById('modal-schedule-editor');
    const title = document.getElementById('sch-modal-title');
    const errBox = document.getElementById('sch-modal-error');
    errBox.style.display = 'none';

    if (schedule) {
      title.textContent = `Edit Schedule: ${schedule.name}`;
      document.getElementById('sch-inp-name').value = schedule.name || '';
      document.getElementById('sch-inp-dept').value = schedule.department || 'Creative';
      document.getElementById('sch-inp-priority').value = schedule.priority || 'MEDIUM';
      document.getElementById('sch-inp-tz').value = schedule.timezone || 'Asia/Kolkata';
      document.getElementById('sch-inp-desc').value = schedule.description || '';
      document.getElementById('sch-inp-trigger').value = schedule.trigger || 'daily';
      document.getElementById('sch-inp-time').value = schedule.time || '08:00';
      document.getElementById('sch-inp-prompt').value = schedule.prompt || '';
      document.getElementById('sch-inp-enabled').checked = schedule.enabled !== false && schedule.state !== 'disabled';

      const outs = schedule.outputs || ['dashboard'];
      document.querySelectorAll('.sch-chk-out').forEach(c => {
        c.checked = outs.includes(c.value);
      });
    } else {
      title.textContent = 'Add Automation Schedule';
      document.getElementById('sch-inp-name').value = '';
      document.getElementById('sch-inp-dept').value = 'Creative';
      document.getElementById('sch-inp-priority').value = 'MEDIUM';
      document.getElementById('sch-inp-tz').value = 'Asia/Kolkata';
      document.getElementById('sch-inp-desc').value = '';
      document.getElementById('sch-inp-trigger').value = 'daily';
      document.getElementById('sch-inp-time').value = '08:00';
      document.getElementById('sch-inp-prompt').value = '';
      document.getElementById('sch-inp-enabled').checked = true;

      document.querySelectorAll('.sch-chk-out').forEach(c => {
        c.checked = (c.value === 'telegram' || c.value === 'dashboard');
      });
    }

    editor.style.display = 'flex';
    document.getElementById('sch-inp-trigger').dispatchEvent(new Event('change'));
  }

  async function openImportExportModal(mode = 'import') {
    const modal = document.getElementById('modal-schedule-import-export');
    const title = document.getElementById('sch-ie-title');
    const subtitle = document.getElementById('sch-ie-subtitle');
    const jsonTxt = document.getElementById('sch-ie-json');
    const submitBtn = document.getElementById('sch-ie-submit');
    const api = window.AVENIQ_API;

    if (mode === 'export') {
      title.textContent = 'Export Automation Schedules JSON';
      subtitle.textContent = 'Copy JSON schedule definitions:';
      submitBtn.style.display = 'none';
      try {
        const res = await api.exportSchedules(Array.from(schState.selectedIds));
        jsonTxt.value = JSON.stringify(res, null, 2);
      } catch (err) {
        jsonTxt.value = JSON.stringify(schState.schedules, null, 2);
      }
    } else {
      title.textContent = 'Import Automation Schedules JSON';
      subtitle.textContent = 'Paste JSON schedules array to import:';
      submitBtn.style.display = 'inline-block';
      submitBtn.textContent = 'Import JSON';
      jsonTxt.value = '';

      submitBtn.onclick = async () => {
        try {
          const parsed = JSON.parse(jsonTxt.value);
          const res = await api.importSchedules(parsed);
          if (res.success) {
            showToast(`Imported ${res.imported_count} schedules cleanly.`, 'success');
            modal.style.display = 'none';
            renderAutomationSchedulesSection();
          }
        } catch (err) {
          alert(`Import Error: ${err.message}`);
        }
      };
    }

    modal.style.display = 'flex';
  }

  function showToast(msg, type = 'info') {
    const box = document.getElementById('sch-toast-container');
    if (!box) return;

    const toast = document.createElement('div');
    let bg = 'rgba(99,102,241,0.9)';
    if (type === 'success') bg = 'rgba(16,185,129,0.9)';
    if (type === 'error') bg = 'rgba(244,63,94,0.9)';
    if (type === 'warning') bg = 'rgba(245,158,11,0.9)';

    toast.style.cssText = `background: ${bg}; color: #fff; padding: 0.65rem 1rem; border-radius: var(--radius-sm); font-size: 0.8rem; font-weight: 600; box-shadow: 0 4px 12px rgba(0,0,0,0.3); pointer-events: auto; backdrop-filter: blur(4px); transition: opacity 0.3s ease;`;
    toast.textContent = msg;
    box.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  function formatShortTime(isoStr) {
    if (!isoStr) return 'N/A';
    try {
      const dt = new Date(isoStr);
      if (isNaN(dt.getTime())) return isoStr;
      return dt.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    } catch (e) {
      return isoStr;
    }
  }

  function getSuccessRate(stats) {
    if (!stats || !stats.execution_count) return 100;
    return Math.round((stats.success_count / stats.execution_count) * 100);
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // 6. CAMPAIGNS
  function renderCampaigns() {
    const container = document.getElementById('campaigns-cards-grid');
    if (!container) return;

    const schedules = schState.schedules || [];
    if (schedules.length === 0) {
      container.innerHTML = `
        <div style="padding: 1.5rem; color: var(--text-muted); font-size: 0.85rem; font-style: italic;">
          No active campaign schedules registered. Create a schedule in the Control Center to populate campaigns.
        </div>
      `;
      return;
    }

    container.innerHTML = schedules.map(s => `
      <div class="glass-panel campaign-card-carousel" style="padding: 1.25rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
          <span style="font-size: 0.7rem; font-family: var(--font-mono); color: var(--accent-cyan);">${s.outputs ? s.outputs.join(' + ').toUpperCase() : 'TELEGRAM'}</span>
          <span style="font-size: 0.68rem; background: rgba(16,185,129,0.15); color: var(--accent-emerald); padding: 0.15rem 0.4rem; border-radius: var(--radius-full); font-weight: 600;">${(s.state || 'ACTIVE').toUpperCase()}</span>
        </div>
        <div style="font-weight: 700; font-size: 1rem; color: #fff; margin-bottom: 0.5rem;">${escapeHtml(s.name)}</div>
        <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted);">
          <span>Dept: ${escapeHtml(s.department || 'Creative')}</span>
          <span style="color: var(--accent-indigo); font-weight: 700;">Trigger: ${s.trigger || 'daily'}</span>
        </div>
      </div>
    `).join('');
  }

  // 7. APPROVAL CENTER
  function renderApprovalCenter(approvals, reasoning) {
    const listContainer = document.getElementById('approval-items-list');
    const previewPane = document.getElementById('approval-preview-pane');
    if (!listContainer || !previewPane) return;

    const pending = (approvals && approvals.pending_approvals && Array.isArray(approvals.pending_approvals))
      ? approvals.pending_approvals
      : [];

    if (pending.length === 0) {
      listContainer.innerHTML = `<div style="padding: 1rem; color: var(--text-muted); font-size: 0.82rem; font-style: italic;">No pending approvals waiting for human review.</div>`;
      previewPane.innerHTML = `<div style="padding: 2rem; color: var(--text-muted); text-align: center; font-size: 0.85rem;">All sessions approved. System running automatically.</div>`;
      return;
    }

    listContainer.innerHTML = pending.map((item, idx) => `
      <div class="approval-card-item ${idx === state.selectedApprovalIndex ? 'selected' : ''}" onclick="window.AVENIQ.selectApproval(${idx})">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
          <span style="font-size: 0.7rem; font-family: var(--font-mono); color: var(--accent-indigo);">${item.session_id}</span>
          <span style="font-size: 0.68rem; background: rgba(245,158,11,0.15); color: var(--accent-amber); padding: 0.15rem 0.4rem; border-radius: var(--radius-full); font-weight: 600;">APPROVAL REQUIRED</span>
        </div>
        <div style="font-weight: 700; color: #fff; font-size: 0.9rem;">${item.topic || 'Enterprise AI Campaign'}</div>

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

  // 8. RESEARCH OPERATIONS CENTER (2-COLUMN RESPONSIVE DASHBOARD)
  async function renderMarketIntelligence() {
    const container = document.getElementById('market-signals-grid');
    if (!container) return;

    const api = window.AVENIQ_API;
    if (!api || typeof api.getResearchOverview !== 'function') {
      container.innerHTML = `<div style="padding:1.5rem;color:var(--text-muted);font-size:0.85rem;">API client not ready.</div>`;
      return;
    }

    container.innerHTML = `<div style="padding:1rem;color:var(--text-muted);font-size:0.85rem;"><div class="pulse-dot"></div> Loading Research Operations Center...</div>`;

    try {
      const overview = await api.getResearchOverview();
      const health = (overview && overview.health) ? overview.health : {};
      const sources = health.sources || {};
      const signals = (overview && overview.market_signals) ? overview.market_signals : [];
      const trends = (overview && overview.trending_topics) ? overview.trending_topics : [];
      const aiSummary = (overview && overview.ai_summary) ? overview.ai_summary : {};

      const providerBadge = (status, noKey) => {
        if (status === 'Connected' || status === 'Healthy') {
          return `<span style="background:rgba(16,185,129,0.15);color:var(--accent-emerald);padding:0.2rem 0.5rem;border-radius:var(--radius-full);font-size:0.68rem;font-weight:700;">🟢 CONNECTED</span>`;
        }
        if (noKey) {
          return `<span style="background:rgba(245,158,11,0.15);color:var(--accent-amber);padding:0.2rem 0.5rem;border-radius:var(--radius-full);font-size:0.68rem;font-weight:700;">🟡 NO KEY REQ</span>`;
        }
        return `<span style="background:rgba(244,63,94,0.15);color:var(--accent-rose);padding:0.2rem 0.5rem;border-radius:var(--radius-full);font-size:0.68rem;font-weight:700;">🔴 NOT CONFIG</span>`;
      };

      const sourceList = [
        { id: 'github', name: 'GitHub API', cat: 'Code & Dev' },
        { id: 'reddit', name: 'Reddit API', cat: 'Community' },
        { id: 'google_news', name: 'Google News RSS', cat: 'Search' },
        { id: 'hackernews', name: 'Hacker News API', cat: 'Community' },
        { id: 'pypi', name: 'PyPI Registry', cat: 'Code & Dev' },
        { id: 'npm', name: 'npm Registry', cat: 'Code & Dev' },
        { id: 'huggingface', name: 'Hugging Face', cat: 'AI & ML' },
        { id: 'google_trends', name: 'Google Trends RSS', cat: 'Business' },
        { id: 'producthunt', name: 'Product Hunt', cat: 'Startup' },
        { id: 'yc_news', name: 'Y Combinator RSS', cat: 'Startup' },
      ];

      container.innerHTML = `
        <style>
          .intel-responsive-grid { display: grid; grid-template-columns: minmax(320px, 38%) 1fr; gap: 1.25rem; width: 100%; }
          @media (max-width: 1024px) { .intel-responsive-grid { grid-template-columns: 1fr !important; } }
          .drawer-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(6px); z-index: 9999; display: none; justify-content: flex-end; }
          .drawer-panel { width: 450px; max-width: 90vw; height: 100%; background: var(--bg-secondary, #131525); border-left: 1px solid var(--border-color); padding: 1.5rem; overflow-y: auto; display: flex; flex-direction: column; gap: 1.25rem; }
        </style>

        <!-- Provider Details Drawer Element -->
        <div id="provider-drawer-overlay" class="drawer-overlay" onclick="if(event.target===this) this.style.display='none'">
          <div id="provider-drawer-content" class="drawer-panel" onclick="event.stopPropagation()"></div>
        </div>

        <div class="intel-responsive-grid">
          
          <!-- LEFT COLUMN (40% Desktop): Source Health, Controls & External Data Sources -->
          <div style="display:flex;flex-direction:column;gap:1.25rem;">
            
            <!-- Operations Summary Card -->
            <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;">
                <div>
                  <h3 style="font-size:1.05rem;font-weight:700;color:#fff;margin:0;">🔬 Research Operations</h3>
                  <div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.2rem;">Live data source health & verification</div>
                </div>
                <button onclick="window.AVENIQ.refreshAllResearchSources()" style="padding:0.4rem 0.85rem;background:var(--accent-indigo);color:#fff;border:none;border-radius:8px;font-size:0.75rem;font-weight:700;cursor:pointer;">
                  ⟳ Refresh All
                </button>
              </div>

              <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;">
                <div style="background:rgba(255,255,255,0.03);padding:0.65rem 0.85rem;border-radius:8px;border:1px solid var(--border-color);">
                  <div style="font-size:0.68rem;color:var(--text-muted);font-weight:600;">CONFIGURED</div>
                  <div style="font-size:1.2rem;font-weight:800;color:var(--accent-indigo);">${health.total_configured || sourceList.length}</div>
                </div>
                <div style="background:rgba(255,255,255,0.03);padding:0.65rem 0.85rem;border-radius:8px;border:1px solid var(--border-color);">
                  <div style="font-size:0.68rem;color:var(--text-muted);font-weight:600;">CONNECTED</div>
                  <div style="font-size:1.2rem;font-weight:800;color:var(--accent-emerald);">${health.total_connected || 0}</div>
                </div>
                <div style="background:rgba(255,255,255,0.03);padding:0.65rem 0.85rem;border-radius:8px;border:1px solid var(--border-color);">
                  <div style="font-size:0.68rem;color:var(--text-muted);font-weight:600;">FAILED / OFFLINE</div>
                  <div style="font-size:1.2rem;font-weight:800;color:var(--accent-rose);">${health.total_failed || 0}</div>
                </div>
                <div style="background:rgba(255,255,255,0.03);padding:0.65rem 0.85rem;border-radius:8px;border:1px solid var(--border-color);">
                  <div style="font-size:0.68rem;color:var(--text-muted);font-weight:600;">AVG LATENCY</div>
                  <div style="font-size:1.2rem;font-weight:800;color:var(--accent-cyan);">${health.avg_latency_ms || 0} ms</div>
                </div>
              </div>
            </div>

            <!-- Data Sources List Cards -->
            <div style="display:flex;flex-direction:column;gap:0.75rem;">
              <h4 style="font-size:0.9rem;font-weight:700;color:#fff;margin:0;">📡 External Providers</h4>
              ${sourceList.map(src => {
                const s = sources[src.id] || {};
                const st = s.status || 'Not Tested';
                const lat = s.latency_ms ? `${s.latency_ms}ms` : '--';
                return `
                  <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:0.85rem 1rem;display:flex;flex-direction:column;gap:0.5rem;">
                    <div style="display:flex;align-items:center;justify-content:space-between;">
                      <span style="font-weight:700;color:#fff;font-size:0.88rem;">${src.name}</span>
                      ${providerBadge(st, s.no_key_required)}
                    </div>
                    <div style="display:flex;align-items:center;justify-content:space-between;font-size:0.73rem;color:var(--text-muted);">
                      <span>Category: <b>${src.cat}</b></span>
                      <span>Latency: <b>${lat}</b></span>
                    </div>
                    <div style="display:flex;gap:0.4rem;margin-top:0.25rem;">
                      <button onclick="window.AVENIQ.testResearchSource('${src.id}')" style="flex:1;padding:0.3rem 0.5rem;background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.3);color:var(--accent-indigo);border-radius:6px;font-size:0.72rem;font-weight:600;cursor:pointer;">⚡ Test</button>
                      <button onclick="window.AVENIQ.refreshResearchSource('${src.id}')" style="flex:1;padding:0.3rem 0.5rem;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);color:var(--accent-emerald);border-radius:6px;font-size:0.72rem;font-weight:600;cursor:pointer;">⟳ Refresh</button>
                      <button onclick="window.AVENIQ.openProviderDrawer('${src.id}')" style="padding:0.3rem 0.6rem;background:rgba(255,255,255,0.05);border:1px solid var(--border-color);color:#fff;border-radius:6px;font-size:0.72rem;font-weight:600;cursor:pointer;">🔍 Details</button>
                    </div>
                  </div>`;
              }).join('')}
            </div>

          </div>

          <!-- RIGHT COLUMN (60% Desktop): Market Signals, Trending Topics & Research Feed -->
          <div style="display:flex;flex-direction:column;gap:1.25rem;">
            
            <!-- High Confidence Market Signals -->
            <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
              <h4 style="font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">📊 High Confidence Market Signals</h4>
              ${signals.length === 0 ? `<div style="color:var(--text-muted);font-size:0.82rem;font-style:italic;">No cross-source market signals detected yet. Click 'Refresh All' to analyze sources.</div>` : 
                signals.map(sig => `
                  <div style="background:rgba(255,255,255,0.03);border:1px solid var(--border-color);padding:0.85rem;border-radius:8px;margin-bottom:0.6rem;">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.3rem;">
                      <span style="font-weight:700;color:#fff;font-size:0.88rem;">${sig.topic}</span>
                      <span style="font-size:0.68rem;background:rgba(16,185,129,0.15);color:var(--accent-emerald);padding:0.15rem 0.45rem;border-radius:var(--radius-full);font-weight:700;">${sig.confidence} CONFIDENCE</span>
                    </div>
                    <div style="font-size:0.78rem;color:var(--text-secondary);margin-bottom:0.4rem;">${sig.summary}</div>
                    <div style="display:flex;align-items:center;justify-content:space-between;font-size:0.7rem;color:var(--text-muted);">
                      <span>Sources: ${(sig.sources||[]).join(', ')} · Momentum: ${sig.momentum}</span>
                    </div>
                  </div>
                `).join('')
              }
            </div>

            <!-- Trending Topics -->
            <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
              <h4 style="font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">🔥 Cross-Platform Trending Topics</h4>
              ${trends.length === 0 ? `<div style="color:var(--text-muted);font-size:0.82rem;font-style:italic;">No trends analyzed yet.</div>` :
                trends.slice(0, 5).map(tr => `
                  <div style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,0.03);padding:0.75rem 0.85rem;border-radius:8px;margin-bottom:0.5rem;border:1px solid var(--border-color);">
                    <div>
                      <div style="font-weight:700;color:#fff;font-size:0.85rem;"># ${tr.topic}</div>
                      <div style="font-size:0.72rem;color:var(--text-muted);">${tr.provider_count} Sources (${(tr.providers||[]).join(', ')})</div>
                    </div>
                    <div style="text-align:right;">
                      <div style="font-weight:800;color:var(--accent-cyan);font-size:0.9rem;">${tr.trend_score} pts</div>
                      <div style="font-size:0.68rem;color:var(--accent-emerald);font-weight:600;">▲ ${tr.momentum}</div>
                    </div>
                  </div>
                `).join('')
              }
            </div>

            <!-- Unified Research Feed & Search -->
            <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
              <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.75rem;margin-bottom:1rem;">
                <h4 style="font-size:0.95rem;font-weight:700;color:#fff;margin:0;">📰 Unified Research Feed</h4>
                <input id="research-search-input" type="text" placeholder="Search across all providers..." onkeyup="window.AVENIQ.filterResearchFeed()" style="padding:0.45rem 0.75rem;background:rgba(0,0,0,0.3);border:1px solid var(--border-color);color:#fff;border-radius:6px;font-size:0.8rem;width:240px;">
              </div>
              <div id="research-feed-list" style="display:flex;flex-direction:column;gap:0.6rem;">
                <div style="color:var(--text-muted);font-size:0.82rem;font-style:italic;">Loading research feed...</div>
              </div>
            </div>

          </div>

        </div>
      `;

      // Load initial feed
      window.AVENIQ.filterResearchFeed();

    } catch (err) {
      console.error('[AVENIQ Research Ops Center Error]', err);
      container.innerHTML = `<div style="padding:1.5rem;color:var(--accent-rose);font-size:0.85rem;">Failed to load Research Operations Center: ${err.message}</div>`;
    }
  }

  // 9. COMPANY BRAIN KNOWLEDGE ENGINE v3.1 (PRODUCTION ARCHITECTURE)
  let companyBrainPollerStarted = false;

  async function renderCompanyBrain() {
    const container = document.getElementById('company-brain-content');
    if (!container) return;

    const api = window.AVENIQ_API;
    if (!api || typeof api.getCompanyBrainOverview !== 'function') {
      container.innerHTML = `<div style="padding:1rem;color:var(--text-muted);font-size:0.85rem;">API client not ready.</div>`;
      return;
    }

    try {
      const overview = await api.getCompanyBrainOverview();
      const stats = overview.statistics || {};
      const health = overview.health || {};
      const items = overview.recent_items || [];
      const entities = overview.entities || [];
      const rels = overview.relationships || [];
      const reflections = overview.reflections || [];
      const activity = overview.activity_timeline || [];

      container.innerHTML = `
        <div style="display:flex;flex-direction:column;gap:1.5rem;width:100%;">
          
          <!-- Section 1: Live Operational Health Metrics -->
          <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;margin-bottom:1rem;">
              <div>
                <h3 style="font-size:1.1rem;font-weight:700;color:#fff;margin:0;">🧠 Company Brain Knowledge Layer v3.1</h3>
                <div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.2rem;">Modular event-driven knowledge engine for AVENIQ AI Runtime</div>
              </div>
              <div style="font-size:0.72rem;color:var(--text-muted);font-family:var(--font-mono);">
                Auto-sync: <b>30s</b> · Repository Size: <b>${stats.storage_size_kb || 0} KB</b>
              </div>
            </div>

            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:0.75rem;">
              <div style="background:rgba(255,255,255,0.03);padding:0.75rem;border-radius:8px;border:1px solid var(--border-color);">
                <div style="font-size:0.68rem;color:var(--text-muted);font-weight:600;">TOTAL ITEMS</div>
                <div style="font-size:1.25rem;font-weight:800;color:var(--accent-indigo);margin-top:0.2rem;">${health.total_knowledge_items || stats.total_knowledge_items || 0}</div>
              </div>
              <div style="background:rgba(255,255,255,0.03);padding:0.75rem;border-radius:8px;border:1px solid var(--border-color);">
                <div style="font-size:0.68rem;color:var(--text-muted);font-weight:600;">VERIFIED</div>
                <div style="font-size:1.25rem;font-weight:800;color:var(--accent-emerald);margin-top:0.2rem;">${health.verified_count || stats.verified_count || 0}</div>
              </div>
              <div style="background:rgba(255,255,255,0.03);padding:0.75rem;border-radius:8px;border:1px solid var(--border-color);">
                <div style="font-size:0.68rem;color:var(--text-muted);font-weight:600;">NEEDS REVIEW</div>
                <div style="font-size:1.25rem;font-weight:800;color:var(--accent-amber);margin-top:0.2rem;">${health.needs_review_count || 0}</div>
              </div>
              <div style="background:rgba(255,255,255,0.03);padding:0.75rem;border-radius:8px;border:1px solid var(--border-color);">
                <div style="font-size:0.68rem;color:var(--text-muted);font-weight:600;">ENTITIES / LINKS</div>
                <div style="font-size:1.25rem;font-weight:800;color:var(--accent-cyan);margin-top:0.2rem;">${stats.entities_count || 0} / ${stats.relationships_count || 0}</div>
              </div>
              <div style="background:rgba(255,255,255,0.03);padding:0.75rem;border-radius:8px;border:1px solid var(--border-color);">
                <div style="font-size:0.68rem;color:var(--text-muted);font-weight:600;">LINK DENSITY</div>
                <div style="font-size:1.25rem;font-weight:800;color:#fff;margin-top:0.2rem;">${health.avg_relationships_per_entity || 0.0}</div>
              </div>
              <div style="background:rgba(255,255,255,0.03);padding:0.75rem;border-radius:8px;border:1px solid var(--border-color);">
                <div style="font-size:0.68rem;color:var(--text-muted);font-weight:600;">MERGED DUPS</div>
                <div style="font-size:1.25rem;font-weight:800;color:var(--accent-indigo);margin-top:0.2rem;">${health.duplicate_merge_count || 0}</div>
              </div>
            </div>
          </div>

          <!-- Section 2: Global Unified Search -->
          <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.75rem;margin-bottom:1rem;">
              <h4 style="font-size:0.95rem;font-weight:700;color:#fff;margin:0;">🌐 Platform Unified Search</h4>
              <input id="brain-search-input" type="text" placeholder="Search across all modules (Telegram, Gemini, Campaign)..." onkeyup="window.AVENIQ.searchCompanyBrain()" style="padding:0.45rem 0.85rem;background:rgba(0,0,0,0.3);border:1px solid var(--border-color);color:#fff;border-radius:6px;font-size:0.82rem;width:340px;max-width:100%;">
            </div>
            <div id="brain-search-results" style="display:flex;flex-direction:column;gap:0.6rem;">
              <!-- Populated dynamically -->
            </div>
          </div>

          <!-- Section 3: Strategic Reflections Queue -->
          <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
            <h4 style="font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">💡 Strategic Reflections & Learning Insights</h4>
            ${reflections.length === 0 ? `<div style="color:var(--text-muted);font-size:0.82rem;font-style:italic;">No reflections generated yet. Significant market signals will populate here automatically.</div>` :
              reflections.map(ref => `
                <div style="background:rgba(255,255,255,0.03);border:1px solid var(--border-color);padding:0.85rem;border-radius:8px;margin-bottom:0.5rem;">
                  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.3rem;">
                    <div style="font-weight:700;color:var(--accent-amber);font-size:0.88rem;">${ref.title}</div>
                    <span style="font-size:0.68rem;color:var(--text-muted);font-family:var(--font-mono);">${new Date(ref.created_at).toLocaleTimeString()}</span>
                  </div>
                  <div style="font-size:0.8rem;color:#fff;margin-bottom:0.25rem;"><b>Observation:</b> ${ref.observation}</div>
                  <div style="font-size:0.78rem;color:var(--accent-cyan);"><b>Recommendation:</b> ${ref.recommendation}</div>
                </div>
              `).join('')
            }
          </div>

          <!-- Section 4: Interactive Graph & Relationships -->
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:1rem;">
            <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
              <h4 style="font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">🏷️ Discovered Entity Nodes</h4>
              ${entities.length === 0 ? `<div style="color:var(--text-muted);font-size:0.82rem;font-style:italic;">No entities discovered yet.</div>` :
                `<div style="display:flex;flex-wrap:wrap;gap:0.4rem;">
                  ${entities.map(e => `<span style="background:rgba(255,255,255,0.04);border:1px solid var(--border-color);color:#fff;padding:0.25rem 0.6rem;border-radius:6px;font-size:0.78rem;font-weight:600;">${e.name} <span style="color:var(--text-muted);font-size:0.68rem;">(${e.category})</span></span>`).join('')}
                </div>`
              }
            </div>

            <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
              <h4 style="font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">🔗 Graph Provenance Edges</h4>
              ${rels.length === 0 ? `<div style="color:var(--text-muted);font-size:0.82rem;font-style:italic;">No relationships discovered.</div>` :
                rels.map(r => `
                  <div style="background:rgba(255,255,255,0.03);border:1px solid var(--border-color);padding:0.6rem 0.8rem;border-radius:6px;margin-bottom:0.4rem;font-size:0.78rem;display:flex;align-items:center;justify-content:space-between;">
                    <div><b style="color:#fff;">${r.entity_a || r.source}</b> <span style="color:var(--accent-indigo);">--[${r.relationship || r.predicate}]--></span> <b style="color:var(--accent-cyan);">${r.entity_b || r.target}</b></div>
                    <span style="font-size:0.68rem;color:var(--text-muted);">${r.method || 'heuristic'} · ${( (r.confidence||1.0)*100 ).toFixed(0)}%</span>
                  </div>
                `).join('')
              }
            </div>
          </div>

          <!-- Section 5: Real Activity Timeline -->
          <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
            <h4 style="font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">📜 Knowledge Event Log</h4>
            ${activity.length === 0 ? `<div style="color:var(--text-muted);font-size:0.82rem;font-style:italic;">No activity recorded.</div>` :
              activity.map(act => `
                <div style="display:flex;align-items:center;justify-content:space-between;padding:0.5rem 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:0.8rem;">
                  <span style="color:#fff;font-weight:600;">⚡ ${act.event}</span>
                  <span style="font-family:var(--font-mono);font-size:0.72rem;color:var(--text-muted);">${new Date(act.timestamp).toLocaleTimeString()}</span>
                </div>
              `).join('')
            }
          </div>

        </div>
      `;

      // Perform initial search list populate
      window.AVENIQ.searchCompanyBrain();

      // Start 30-second live auto-refresh if not started
      if (!companyBrainPollerStarted) {
        companyBrainPollerStarted = true;
        setInterval(() => { renderCompanyBrain(); }, 30000);
      }

    } catch(err) {
      console.error('[AVENIQ Company Brain Error]', err);
      container.innerHTML = `<div style="padding:1rem;color:var(--accent-rose);font-size:0.85rem;">Failed to load Company Brain: ${err.message}</div>`;
    }
  }

  // 10. KNOWLEDGE RAG
  async function renderKnowledge() {
    const container = document.getElementById('knowledge-content');
    if (!container) return;

    const api = window.AVENIQ_API;
    let items = [];
    if (api && typeof api.searchCompanyBrain === 'function') {
      try {
        const res = await api.searchCompanyBrain('');
        items = res.items || [];
      } catch (e) {}
    }

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div style="background: rgba(255,255,255,0.03); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
          <div style="display:flex;align-items:center;justify-content:space-between;">
            <div style="font-weight: 700; color: #fff;">📚 Vector Knowledge Collections (${items.length} items)</div>
            <span style="font-size:0.72rem;color:var(--accent-cyan);">Persisted Knowledge Storage</span>
          </div>
          <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top:0.4rem;">Indexed technical documentation, domain entities, and company brain memories.</div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.75rem;">
          ${items.slice(0, 8).map(item => `
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 0.85rem; border-radius: var(--radius-sm);">
              <div style="font-weight: 600; font-size: 0.88rem; color: #fff;">${item.title || 'Knowledge Item'}</div>
              <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.3rem;">${item.summary || item.body || ''}</div>
              <div style="margin-top: 0.5rem; display: flex; gap: 0.3rem; font-size: 0.68rem; color: var(--accent-indigo);">
                <span style="background: rgba(99,102,241,0.15); padding: 0.1rem 0.4rem; border-radius: 4px;">${item.type || 'Knowledge'}</span>
                <span style="background: rgba(255,255,255,0.05); color: var(--text-muted); padding: 0.1rem 0.4rem; border-radius: 4px;">${item.category || 'General'}</span>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  // 11. CLOSED-LOOP LEARNING
  async function renderLearning() {
    const container = document.getElementById('learning-content');
    if (!container) return;

    const api = window.AVENIQ_API;
    let reflections = [];
    if (api && typeof api.getReflections === 'function') {
      try {
        const res = await api.getReflections();
        reflections = (res && res.reflections) ? res.reflections : (Array.isArray(res) ? res : []);
      } catch (e) {}
    }

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div style="background: rgba(255,255,255,0.03); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
          <div style="display:flex;align-items:center;justify-content:space-between;">
            <div style="font-weight: 700; color: #fff;">📈 Closed-Loop Performance Optimization (${reflections.length} insights)</div>
            <span style="font-size:0.72rem;color:var(--accent-emerald);">Evidence-Grounded Learning</span>
          </div>
          <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top:0.4rem;">Feedback loops process engagement metrics to fine-tune strategy planning and execution quality.</div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
          ${reflections.slice(0, 6).map(r => `
            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 1rem; border-radius: var(--radius-sm);">
              <div style="font-weight: 600; font-size: 0.9rem; color: var(--accent-cyan);">${r.title || 'Strategic Reflection'}</div>
              <div style="font-size: 0.82rem; color: var(--text-primary); margin-top: 0.38rem;">${r.observation || ''}</div>
              <div style="font-size: 0.78rem; color: var(--accent-emerald); margin-top: 0.38rem;">💡 Recommendation: ${r.recommendation || ''}</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  // 12. ANALYTICS
  function renderAnalytics(analytics) {
    const container = document.getElementById('analytics-content');
    if (!container) return;

    const safeAnalytics = (analytics && typeof analytics === 'object' && !analytics.error) ? analytics : {};
    const rate = safeAnalytics.engagement_rate || '--';
    const impressions = safeAnalytics.impressions != null ? safeAnalytics.impressions.toLocaleString() : '--';
    const conversions = safeAnalytics.conversions != null ? safeAnalytics.conversions : '--';
    const cost = safeAnalytics.total_cost !== undefined ? `$${safeAnalytics.total_cost.toFixed(4)}` : '--';

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
    searchCompanyBrain: async function () {
      const input = document.getElementById('brain-search-input');
      const list = document.getElementById('brain-search-results');
      if (!list) return;

      const q = input ? input.value.trim() : '';
      const api = window.AVENIQ_API;
      if (!api || typeof api.searchCompanyBrain !== 'function') return;

      try {
        const res = await api.searchCompanyBrain(q);
        const items = res.items || [];

        if (items.length === 0) {
          list.innerHTML = `<div style="color:var(--text-muted);font-size:0.82rem;font-style:italic;padding:0.5rem 0;">No knowledge items match '${q || 'index'}'.</div>`;
          return;
        }

        const typeColor = (t) => {
          const map = { Company:'var(--accent-indigo)', Technology:'var(--accent-cyan)', Service:'var(--accent-emerald)', Campaign:'var(--accent-amber)', Learning:'var(--accent-rose)' };
          return map[t] || 'var(--accent-indigo)';
        };

        list.innerHTML = items.map(item => `
          <div style="background:rgba(255,255,255,0.03);border:1px solid var(--border-color);padding:0.85rem;border-radius:8px;">
            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
              <div style="font-weight:700;color:#fff;font-size:0.9rem;">${item.title}</div>
              <div style="display:flex;gap:0.4rem;align-items:center;">
                <span style="background:${typeColor(item.type)};color:#fff;font-size:0.68rem;font-weight:700;padding:0.15rem 0.5rem;border-radius:4px;">${item.type}</span>
                <span style="background:rgba(255,255,255,0.05);color:var(--text-muted);font-size:0.68rem;padding:0.15rem 0.4rem;border-radius:4px;">${item.source}</span>
              </div>
            </div>
            <div style="font-size:0.8rem;color:var(--text-secondary);margin-top:0.4rem;line-height:1.5;">${item.summary || item.body || ''}</div>
            <div style="display:flex;align-items:center;justify-content:space-between;margin-top:0.6rem;font-size:0.72rem;color:var(--text-muted);">
              <div>Category: <b style="color:#fff;">${item.category}</b> · Refs: <b style="color:var(--accent-cyan);">${item.ref_count || 1}</b></div>
              <div style="display:flex;gap:0.3rem;">
                ${(item.tags || []).slice(0, 4).map(t => `<span style="color:var(--accent-indigo);">#${t}</span>`).join(' ')}
              </div>
            </div>
          </div>
        `).join('');
      } catch(e) {
        list.innerHTML = `<div style="color:var(--accent-rose);font-size:0.8rem;">Search failed: ${e.message}</div>`;
      }
    },
    _resumeJob: async function (scheduleId, fromStageIndex) {
      const api = window.AVENIQ_API;
      if (!api) return;
      try {
        await api.resumeAutomation(scheduleId, fromStageIndex);
        startRuntimePolling(api);
      } catch(e) { console.error('[AVENIQ Resume]', e); }
    },
    testResearchSource: async function (provider) {
      const api = window.AVENIQ_API;
      if (!api || typeof api.testResearchSource !== 'function') return;
      try {
        const res = await api.testResearchSource(provider);
        alert(`⚡ Test Connection Result for ${provider.toUpperCase()}:\n\nStatus: ${res.status}\nLatency: ${res.latency_ms}ms\nRate Limit: ${res.rate_limit || 'N/A'}\nSample Items: ${res.sample_data ? res.sample_data.length : 0}\nError: ${res.error || 'None'}`);
        renderMarketIntelligence();
      } catch(e) { alert(`Test failed: ${e.message}`); }
    },
    openProviderDrawer: async function (provider) {
      const overlay = document.getElementById('provider-drawer-overlay');
      const content = document.getElementById('provider-drawer-content');
      if (!overlay || !content) return;

      overlay.style.display = 'flex';
      content.innerHTML = `<div style="color:var(--text-muted);padding:1rem;"><div class="pulse-dot"></div> Loading ${provider.toUpperCase()} telemetry...</div>`;

      const api = window.AVENIQ_API;
      let data = {};
      if (api && typeof api.getResearchProvider === 'function') {
        try {
          data = await api.getResearchProvider(provider);
        } catch(e) {
          try { data = await api.testResearchSource(provider); } catch(err) { data = { provider, status: 'Failed', error: err.message }; }
        }
      }

      const st = data.status || 'NOT CONFIG';
      const isConnected = st === 'Connected' || st === 'Healthy' || st === 'CONNECTED';
      const badgeColor = isConnected ? 'var(--accent-emerald)' : (data.no_key_required ? 'var(--accent-amber)' : 'var(--accent-rose)');

      const diag = data.diagnostics || {};
      const cfg = data.config || diag.config || {};

      content.innerHTML = `
        <div style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border-color);padding-bottom:1rem;">
          <div>
            <div style="font-size:1.1rem;font-weight:700;color:#fff;">${provider.toUpperCase()} Telemetry</div>
            <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.2rem;">Detailed provider status, OAuth grant & rate limits</div>
          </div>
          <button onclick="document.getElementById('provider-drawer-overlay').style.display='none'" style="background:transparent;border:none;color:#fff;font-size:1.2rem;cursor:pointer;padding:0.2rem 0.5rem;">✕</button>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;">
          <div style="background:rgba(255,255,255,0.03);padding:0.75rem;border-radius:8px;border:1px solid var(--border-color);">
            <div style="font-size:0.7rem;color:var(--text-muted);font-weight:600;">STATUS</div>
            <div style="font-size:0.95rem;font-weight:700;color:${badgeColor};margin-top:0.2rem;">${st.toUpperCase()}</div>
          </div>
          <div style="background:rgba(255,255,255,0.03);padding:0.75rem;border-radius:8px;border:1px solid var(--border-color);">
            <div style="font-size:0.7rem;color:var(--text-muted);font-weight:600;">LATENCY</div>
            <div style="font-size:0.95rem;font-weight:700;color:var(--accent-cyan);margin-top:0.2rem;">${data.latency_ms || 0} ms</div>
          </div>
          <div style="background:rgba(255,255,255,0.03);padding:0.75rem;border-radius:8px;border:1px solid var(--border-color);">
            <div style="font-size:0.7rem;color:var(--text-muted);font-weight:600;">GRANT TYPE</div>
            <div style="font-size:0.85rem;font-weight:700;color:var(--accent-indigo);margin-top:0.2rem;">${data.grant_type || diag.grant_type || 'N/A'}</div>
          </div>
          <div style="background:rgba(255,255,255,0.03);padding:0.75rem;border-radius:8px;border:1px solid var(--border-color);">
            <div style="font-size:0.7rem;color:var(--text-muted);font-weight:600;">RATE LIMIT</div>
            <div style="font-size:0.78rem;font-weight:600;color:#fff;margin-top:0.2rem;">${data.rate_limit || 'N/A'}</div>
          </div>
        </div>

        <!-- Configuration Verification Checklist -->
        <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);padding:0.85rem;border-radius:8px;">
          <div style="font-size:0.75rem;font-weight:700;color:var(--accent-indigo);margin-bottom:0.4rem;">ENVIRONMENT CONFIGURATION</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem;font-size:0.75rem;">
            <span>Client ID: <b style="color:${cfg.client_id ? 'var(--accent-emerald)' : 'var(--accent-rose)'}">${cfg.client_id ? '✓ Present' : '✗ Missing'}</b></span>
            <span>Client Secret: <b style="color:${cfg.client_secret ? 'var(--accent-emerald)' : 'var(--accent-rose)'}">${cfg.client_secret ? '✓ Present' : '✗ Missing'}</b></span>
            <span>User Agent: <b style="color:${cfg.user_agent ? 'var(--accent-emerald)' : 'var(--accent-rose)'}">${cfg.user_agent ? '✓ Present' : '✗ Missing'}</b></span>
            <span>Username: <b style="color:${cfg.username ? 'var(--accent-emerald)' : 'var(--text-muted)'}">${cfg.username ? '✓ Present' : 'Optional'}</b></span>
          </div>
        </div>

        ${data.error ? `
          <div style="background:rgba(244,63,94,0.1);border:1px solid rgba(244,63,94,0.3);padding:0.85rem;border-radius:8px;">
            <div style="font-size:0.75rem;font-weight:700;color:var(--accent-rose);">FAILURE DIAGNOSTICS</div>
            <div style="font-size:0.78rem;color:var(--text-secondary);margin-top:0.25rem;">${data.error}</div>
            ${diag.possible_cause ? `<div style="font-size:0.72rem;color:var(--accent-amber);margin-top:0.35rem;">Possible Cause: ${diag.possible_cause}</div>` : ''}
          </div>
        ` : ''}

        <div>
          <div style="font-size:0.78rem;font-weight:700;color:var(--accent-indigo);margin-bottom:0.4rem;">SAMPLE RESPONSE PAYLOAD (${data.sample_data ? data.sample_data.length : 0} items)</div>
          <pre style="background:rgba(0,0,0,0.5);border:1px solid var(--border-color);padding:0.85rem;border-radius:8px;font-size:0.72rem;color:var(--accent-cyan);max-height:220px;overflow-y:auto;font-family:var(--font-mono);">${JSON.stringify(data.sample_data || [], null, 2)}</pre>
        </div>

        <div style="display:flex;gap:0.5rem;margin-top:auto;padding-top:1rem;border-top:1px solid var(--border-color);">
          <button onclick="window.AVENIQ.refreshResearchSource('${provider}'); document.getElementById('provider-drawer-overlay').style.display='none';" style="flex:1;padding:0.5rem;background:var(--accent-indigo);color:#fff;border:none;border-radius:8px;font-weight:700;font-size:0.8rem;cursor:pointer;">⟳ Force Refresh Cache</button>
          <button onclick="document.getElementById('provider-drawer-overlay').style.display='none'" style="padding:0.5rem 1rem;background:transparent;border:1px solid var(--border-color);color:#fff;border-radius:8px;font-size:0.8rem;cursor:pointer;">Close</button>
        </div>
      `;
    },
    refreshResearchSource: async function (provider) {
      const api = window.AVENIQ_API;
      if (!api || typeof api.refreshResearchSource !== 'function') return;
      try {
        await api.refreshResearchSource(provider);
        renderMarketIntelligence();
      } catch(e) { console.error(e); }
    },
    refreshAllResearchSources: async function () {
      const api = window.AVENIQ_API;
      if (!api || typeof api.refreshAllResearchSources !== 'function') return;
      try {
        await api.refreshAllResearchSources();
        renderMarketIntelligence();
      } catch(e) { console.error(e); }
    },
    filterResearchFeed: async function () {
      const input = document.getElementById('research-search-input');
      const container = document.getElementById('research-feed-list');
      if (!container) return;
      const api = window.AVENIQ_API;
      if (!api || typeof api.searchResearchFeed !== 'function') return;

      const q = input ? input.value : '';
      try {
        const res = await api.searchResearchFeed(q);
        const items = (res && res.items) ? res.items : [];
        if (items.length === 0) {
          container.innerHTML = `<div style="padding:1rem;color:var(--text-muted);font-size:0.82rem;font-style:italic;">No research items match query '${q}'. Click 'Refresh All' to fetch live data.</div>`;
          return;
        }
        container.innerHTML = items.map(item => `
          <div style="background:rgba(255,255,255,0.03);border:1px solid var(--border-color);padding:0.75rem 1rem;border-radius:8px;display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;">
            <div style="flex:1;">
              <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem;">
                <span style="font-size:0.65rem;background:rgba(99,102,241,0.15);color:var(--accent-indigo);padding:0.15rem 0.4rem;border-radius:4px;font-weight:700;">${(item.provider||'').toUpperCase()}</span>
                <span style="font-size:0.65rem;color:var(--text-muted);">${(item.category||'').toUpperCase()}</span>
                ${item.author ? `<span style="font-size:0.7rem;color:var(--text-muted);">by ${item.author}</span>` : ''}
              </div>
              <a href="${item.url || '#'}" target="_blank" style="font-weight:700;color:#fff;font-size:0.88rem;text-decoration:none;">${item.title}</a>
              <div style="font-size:0.78rem;color:var(--text-secondary);margin-top:0.25rem;">${(item.summary||'').slice(0, 160)}${(item.summary||'').length > 160 ? '...' : ''}</div>
            </div>
            ${item.score ? `<div style="font-size:0.75rem;font-family:var(--font-mono);color:var(--accent-emerald);font-weight:700;">★ ${item.score}</div>` : ''}
          </div>
        `).join('');
      } catch(e) { console.error('[Research Feed Filter Error]', e); }
    },
    init: async function () {
      let overview = {}, activity = null, approvals = null, analytics = null, reasoning = null, connections = null;

      // Deterministic API dependency resolution with fallback
      let api = window.AVENIQ_API || window.apiClient;
      if (!api && window.AVENIQ_APP && typeof window.AVENIQ_APP.require === 'function') {
        try {
          api = await window.AVENIQ_APP.require('api');
        } catch (err) {}
      }
      api = api || window.AVENIQ_API;

      if (!api || typeof api.getOverview !== 'function') {
        console.warn("[AVENIQ BOOTSTRAP] API client is not initialized yet.");
        return;
      }

      // Fetch all dashboard data including runtime state and events in parallel
      try {
        const results = await Promise.allSettled([
          api.getOverview(),
          api.getActivity(),
          api.getApprovals(),
          api.getAnalytics(),
          api.getReasoning(),
          api.getConnections ? api.getConnections() : Promise.resolve(null),
          api.getAutomationRuntime ? api.getAutomationRuntime() : Promise.resolve(null),
          api.getAutomationEvents ? api.getAutomationEvents(50) : Promise.resolve(null),
        ]);

        overview     = (results[0].status === 'fulfilled' && results[0].value && !results[0].value.error) ? results[0].value : {};
        activity     = (results[1].status === 'fulfilled' && results[1].value && !results[1].value.error) ? results[1].value : null;
        approvals    = (results[2].status === 'fulfilled' && results[2].value && !results[2].value.error) ? results[2].value : null;
        analytics    = (results[3].status === 'fulfilled' && results[3].value && !results[3].value.error) ? results[3].value : null;
        reasoning    = (results[4].status === 'fulfilled' && results[4].value && !results[4].value.error) ? results[4].value : null;
        connections  = (results[5].status === 'fulfilled' && results[5].value && !results[5].value.error) ? results[5].value : null;
        const runtime  = (results[6].status === 'fulfilled' && results[6].value && !results[6].value.error) ? results[6].value : null;
        const eventsResp = (results[7].status === 'fulfilled' && results[7].value) ? results[7].value : null;
        state.runtime = runtime;
        state.events  = eventsResp ? (eventsResp.events || []) : [];
      } catch (err) {
        console.error("[AVENIQ RUNTIME ERROR] Error fetching API data:", err.stack || err);
      }

      state.overview    = overview;
      state.activity    = activity;
      state.approvals   = approvals;
      state.analytics   = analytics;
      state.reasoning   = reasoning;
      state.connections = connections;

      // Render workspace components
      try { renderHeroMissionBriefing(overview); } catch (e) { console.error('[AVENIQ RENDER ERROR] Hero render failed:', e.stack || e); }
      try { renderRuntimeMetrics(state.runtime); } catch (e) { console.error('[AVENIQ RENDER ERROR] RuntimeMetrics render failed:', e.stack || e); }
      try { renderActiveAutomationCard(state.runtime); } catch (e) { console.error('[AVENIQ RENDER ERROR] ActiveAutomation render failed:', e.stack || e); }
      try { renderWorkflowPipeline(state.runtime); } catch (e) { console.error('[AVENIQ RENDER ERROR] Pipeline render failed:', e.stack || e); }
      try { renderLiveActivityFeed(state.events || []); } catch (e) { console.error('[AVENIQ RENDER ERROR] ActivityFeed render failed:', e.stack || e); }
      try { renderReasoningCard(reasoning); } catch (e) { console.error('[AVENIQ RENDER ERROR] Reasoning render failed:', e.stack || e); }
      try { renderAutomation(overview, connections); } catch (e) { console.error('[AVENIQ RENDER ERROR] Automation render failed:', e.stack || e); }
      // After renderAutomation inserts #active-automation-card, populate it
      try { renderActiveAutomationCard(state.runtime); } catch (e) { /* already rendered above */ }
      try { await renderAutomationControlCenter(); } catch (e) { console.error('[AVENIQ RENDER ERROR] AutomationControlCenter render failed:', e.stack || e); }
      try { renderCampaigns(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Campaigns render failed:', e.stack || e); }
      try { renderApprovalCenter(approvals, reasoning); } catch (e) { console.error('[AVENIQ RENDER ERROR] Approval render failed:', e.stack || e); }
      try { renderMarketIntelligence(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Market Intel render failed:', e.stack || e); }
      try { renderCompanyBrain(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Company Brain render failed:', e.stack || e); }
      try { renderKnowledge(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Knowledge render failed:', e.stack || e); }
      try { renderLearning(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Learning render failed:', e.stack || e); }
      try { renderAnalytics(analytics); } catch (e) { console.error('[AVENIQ RENDER ERROR] Analytics render failed:', e.stack || e); }
      try { renderSettings(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Settings render failed:', e.stack || e); }
      try { renderWorkforce(); } catch (e) { console.error('[AVENIQ RENDER ERROR] Workforce render failed:', e.stack || e); }

      // Start live runtime poller if automation is running or scheduler recovered
      if (state.runtime && (state.runtime.running || state.runtime.recovered)) {
        startRuntimePolling(api);
      }
    }
  };

  // 13. AI WORKFORCE v2.1 (GOAL-ORIENTED DYNAMIC MULTI-AGENT RUNTIME)
  async function renderWorkforce() {
    const container = document.getElementById('workforce-content');
    if (!container) return;

    const api = window.AVENIQ_API;
    if (!api || typeof api.getWorkforce !== 'function') return;

    try {
      const workforceRes = await api.getWorkforce();
      const goalsRes = await api.getGoals();

      const workers = workforceRes.workers || [];
      const goals = goalsRes.goals || [];

      container.innerHTML = `
        <div style="display:flex;flex-direction:column;gap:1.5rem;width:100%;">
          
          <!-- Header -->
          <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
            <div>
              <h3 style="font-size:1.1rem;font-weight:700;color:#fff;margin:0;">🤖 Autonomous AI Workforce v2.1</h3>
              <div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.2rem;">Goal-oriented capability-matched multi-agent runtime</div>
            </div>
            <button onclick="window.AVENIQ.dispatchNewGoal()" style="background:var(--accent-indigo);color:#fff;border:none;padding:0.5rem 1rem;border-radius:6px;font-size:0.8rem;font-weight:700;cursor:pointer;">+ Dispatch Autonomous Goal</button>
          </div>

          <!-- Active Goals & Task Graphs -->
          <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
            <h4 style="font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.85rem;">🎯 Active Autonomous Goals & DAG Task Graphs</h4>
            ${goals.length === 0 ? `<div style="color:var(--text-muted);font-size:0.82rem;font-style:italic;">No goals dispatched yet.</div>` :
              goals.map(g => `
                <div style="background:rgba(255,255,255,0.03);border:1px solid var(--border-color);border-radius:8px;padding:1rem;margin-bottom:0.75rem;">
                  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.5rem;">
                    <div>
                      <b style="color:#fff;font-size:0.9rem;">${g.objective}</b>
                      <span style="font-size:0.72rem;color:var(--text-muted);margin-left:0.5rem;">(${g.type} · ${g.priority.toUpperCase()} Priority)</span>
                    </div>
                    <span style="background:rgba(255,255,255,0.05);border:1px solid var(--border-color);color:var(--accent-cyan);padding:0.2rem 0.5rem;border-radius:4px;font-size:0.72rem;font-weight:700;">${g.status.toUpperCase()}</span>
                  </div>

                  <!-- Task Graph DAG Steps -->
                  <div style="display:flex;flex-wrap:wrap;gap:0.4rem;margin-top:0.6rem;">
                    ${(g.tasks || []).map(t => `
                      <span style="background:rgba(0,0,0,0.3);border:1px solid ${t.status==='completed'?'var(--accent-emerald)':t.status==='in_progress'?'var(--accent-amber)':'var(--border-color)'};padding:0.35rem 0.6rem;border-radius:6px;font-size:0.75rem;">
                        <b style="color:#fff;">${t.required_capability}</b>
                        <span style="color:var(--text-muted);font-size:0.68rem;">(${t.assigned_worker || 'unassigned'} · ${t.status})</span>
                      </span>
                    `).join('')}
                  </div>
                </div>
              `).join('')
            }
          </div>

          <!-- Active AI Workers Matrix -->
          <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:1.25rem;">
            <h4 style="font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.85rem;">⚡ AI Workers Capability Matrix</h4>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0.75rem;">
              ${workers.map(w => `
                <div style="background:rgba(255,255,255,0.03);border:1px solid var(--border-color);border-radius:8px;padding:0.85rem;">
                  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.4rem;">
                    <b style="color:#fff;font-size:0.88rem;">${w.name}</b>
                    <span style="color:${w.state==='idle'?'var(--accent-emerald)':'var(--accent-amber)'};font-size:0.72rem;font-weight:700;">● ${w.state.toUpperCase()}</span>
                  </div>
                  <div style="font-size:0.72rem;color:var(--text-muted);margin-bottom:0.4rem;">
                    Capabilities: ${(w.capabilities || []).map(c => `<code>${c}</code>`).join(', ')}
                  </div>
                  <div style="display:flex;gap:0.75rem;font-size:0.72rem;color:#fff;font-family:var(--font-mono);">
                    <span>Tasks: <b>${w.tasks_completed || 0}</b></span>
                    <span>Success Rate: <b>${( (w.success_rate||1.0)*100 ).toFixed(0)}%</b></span>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

        </div>
      `;
    } catch(err) {
      console.error('[AVENIQ Workforce Error]', err);
    }
  }

  // Dispatch goal handler
  window.AVENIQ.dispatchNewGoal = async function() {
    const api = window.AVENIQ_API;
    if (!api) return;
    const obj = prompt("Enter Autonomous Goal Objective:", "Launch multi-channel AI campaign for AVENIQ AI Runtime");
    if (!obj) return;
    try {
      await api.createGoal(obj);
      renderWorkforce();
    } catch(e) {
      alert("Failed to dispatch goal: " + e.message);
    }
  };

  // Auto-bootstrap dashboard initialization on DOM ready
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        window.AVENIQ.init().catch(err => console.error('[AVENIQ Bootstrap Error]', err));
      });
    } else {
      window.AVENIQ.init().catch(err => console.error('[AVENIQ Bootstrap Error]', err));
    }
  }
})();
