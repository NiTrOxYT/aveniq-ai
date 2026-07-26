/**
 * Global Searchable Command Palette (Cmd+K / Ctrl+K) for AVENIQ Dashboard.
 */

class CommandPalette {
    constructor() {
        this.overlay = null;
        this.input = null;
        this.commands = [
            { id: 'cmd_run', name: '🚀 Run Daily Autonomous Workflow Cycle', action: () => window.appController.runWorkflow() },
            { id: 'cmd_approve', name: '✅ Approve Pending Campaign Briefing', action: () => window.appController.approveCampaign() },
            { id: 'cmd_publish', name: '📢 Distribute Campaign to Target Channel', action: () => window.appController.publishNow() },
            { id: 'cmd_analytics', name: '📈 Open Performance Analytics Dashboard', action: () => window.appController.switchTab('analytics') },
            { id: 'cmd_brain', name: '🧠 Search Company Brain Knowledge', action: () => window.appController.switchTab('company-brain') },
            { id: 'cmd_workspace', name: '🏢 Provision New Isolated Workspace', action: () => window.appController.switchTab('workspaces') }
        ];
        this.init();
    }

    init() {
        window.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
                e.preventDefault();
                this.toggle();
            } else if (e.key === 'Escape' && this.isOpen()) {
                this.close();
            }
        });
    }

    isOpen() {
        return this.overlay && this.overlay.style.display === 'flex';
    }

    toggle() {
        if (this.isOpen()) this.close();
        else this.open();
    }

    open() {
        this.overlay = document.getElementById('cmd-palette-overlay');
        if (this.overlay) {
            this.overlay.style.display = 'flex';
            this.input = document.getElementById('cmd-input');
            if (this.input) {
                this.input.value = '';
                this.input.focus();
            }
            this.renderList(this.commands);
        }
    }

    close() {
        if (this.overlay) {
            this.overlay.style.display = 'none';
        }
    }

    renderList(items) {
        const list = document.getElementById('cmd-list');
        if (!list) return;

        list.innerHTML = items.map(cmd => `
            <li class="cmd-item" onclick="window.commandPalette.execute('${cmd.id}')">
                <span>${cmd.name}</span>
                <kbd style="background: var(--bg-card); padding: 2px 6px; border-radius: 4px; font-size: 0.75rem;">↵ Enter</kbd>
            </li>
        `).join('');
    }

    execute(cmdId) {
        const cmd = this.commands.find(c => c.id === cmdId);
        if (cmd) {
            this.close();
            cmd.action();
        }
    }
}

window.commandPalette = new CommandPalette();
