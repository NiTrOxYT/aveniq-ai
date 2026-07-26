/* ==========================================================================
   AVENIQ AI OPERATING SYSTEM — RAYCAST / CURSOR COMMAND PALETTE
   Handles Cmd+K / Ctrl+K keyboard shortcut, modal overlay, and section jumps
   ========================================================================== */

(function () {
  'use strict';

  const commands = [
    { title: 'Go to Mission Control', view: 'mission-control', icon: '⚡' },
    { title: 'View Active Automation', view: 'automation', icon: '🔄' },
    { title: 'Inspect Active Campaigns', view: 'campaigns', icon: '🚀' },
    { title: 'Open Approval Center (PR Review)', view: 'approvals', icon: '✅' },
    { title: 'Explore Market Intelligence Signals', view: 'market-intelligence', icon: '📡' },
    { title: 'Query Company Brain Memory', view: 'company-brain', icon: '🧠' },
    { title: 'Search Knowledge RAG Collections', view: 'knowledge', icon: '📚' },
    { title: 'View Closed-Loop Learning Patterns', view: 'learning', icon: '📈' },
    { title: 'Inspect Analytics & Token Usage', view: 'analytics', icon: '📊' },
    { title: 'Open Workspace Settings', view: 'settings', icon: '⚙️' }
  ];

  let selectedIndex = 0;

  function initCommandPalette() {
    const overlay = document.getElementById('cmd-modal-overlay');
    const input = document.getElementById('cmd-search-input');
    const resultsContainer = document.getElementById('cmd-results-list');
    const openBtn = document.getElementById('open-cmd-palette');

    if (!overlay || !input || !resultsContainer) return;

    function openModal() {
      overlay.classList.add('active');
      input.value = '';
      selectedIndex = 0;
      renderResults('');
      input.focus();
    }

    function closeModal() {
      overlay.classList.remove('active');
    }

    function renderResults(query) {
      const filtered = commands.filter(c => c.title.toLowerCase().includes(query.toLowerCase()));
      if (filtered.length === 0) {
        resultsContainer.innerHTML = '<div style="padding: 1rem; color: var(--text-muted); font-size: 0.85rem;">No matching commands found</div>';
        return;
      }

      resultsContainer.innerHTML = filtered.map((c, i) => `
        <div class="cmd-item ${i === selectedIndex ? 'selected' : ''}" data-view="${c.view}">
          <span>${c.icon} ${c.title}</span>
          <span style="font-size: 0.7rem; color: var(--text-muted);">Jump</span>
        </div>
      `).join('');

      // Add click handlers
      const items = resultsContainer.querySelectorAll('.cmd-item');
      items.forEach((item, idx) => {
        item.addEventListener('click', () => {
          executeCommand(filtered[idx].view);
          closeModal();
        });
      });
    }

    function executeCommand(viewName) {
      const navItems = document.querySelectorAll('.nav-item');
      const views = document.querySelectorAll('.view-section');
      const headerTitle = document.getElementById('header-title');

      navItems.forEach(n => n.classList.remove('active'));
      views.forEach(v => v.classList.remove('active'));

      const targetNav = document.querySelector(`.nav-item[data-view="${viewName}"]`);
      const targetView = document.getElementById(`view-${viewName}`);

      if (targetNav) targetNav.classList.add('active');
      if (targetView) targetView.classList.add('active');
      if (headerTitle && targetNav) {
        headerTitle.textContent = targetNav.querySelector('span').textContent;
      }
    }

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (overlay.classList.contains('active')) {
          closeModal();
        } else {
          openModal();
        }
      } else if (e.key === 'Escape' && overlay.classList.contains('active')) {
        closeModal();
      }
    });

    if (openBtn) openBtn.addEventListener('click', openModal);
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal();
    });

    input.addEventListener('input', (e) => renderResults(e.target.value));

    // Nav Item Clicks
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(n => {
      n.addEventListener('click', () => {
        const v = n.getAttribute('data-view');
        executeCommand(v);
      });
    });
  }

  document.addEventListener('DOMContentLoaded', initCommandPalette);
})();
