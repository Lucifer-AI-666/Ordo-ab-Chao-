/**
 * TaurosPrivateAgent - Web Interface Integration
 * Privacy-first cybersecurity agent for DibTauroS/Ordo-ab-Chao framework
 *
 * Owner: Dib Anouar
 * License: LUP v1.0 (personal and non-commercial use only)
 */

'use strict';

class TaurosPrivateAgent {
    constructor(config = {}) {
        this.config = {
            baseUrl: config.baseUrl || 'http://127.0.0.1:8788',
            enableLogging: config.enableLogging !== undefined ? config.enableLogging : true,
            theme: config.theme || 'dark',
            language: config.language || 'it'
        };

        this.state = {
            mode: 'DEFEND',
            connected: false,
            operationHistory: [],
            currentOperation: null
        };

        this.init();
    }

    /**
     * Initialize the Tauros agent interface
     */
    init() {
        this._log('TaurosPrivateAgent initializing...', 'info');
        this._createInterface();
        this._checkConnection();
        this._log('TaurosPrivateAgent ready - DibTauroS/Ordo-ab-Chao', 'info');
    }

    /**
     * Create the main web interface
     */
    _createInterface() {
        const container = document.getElementById('tauros-auto-init');
        if (!container) return;

        container.innerHTML = `
<div id="tauros-agent" style="
    font-family: 'Courier New', monospace;
    background: #0a0a0a;
    color: #00ff41;
    min-height: 100vh;
    padding: 20px;
    box-sizing: border-box;
">
    <!-- Header -->
    <div style="
        border: 1px solid #00ff41;
        padding: 15px;
        margin-bottom: 20px;
        text-align: center;
    ">
        <pre style="color: #00ff41; font-size: 12px; margin: 0;">
 ████████╗ █████╗ ██╗   ██╗██████╗  ██████╗ ███████╗
    ██╔══╝██╔══██╗██║   ██║██╔══██╗██╔═══██╗██╔════╝
    ██║   ███████║██║   ██║██████╔╝██║   ██║███████╗
    ██║   ██╔══██║██║   ██║██╔══██╗██║   ██║╚════██║
    ██║   ██║  ██║╚██████╔╝██║  ██║╚██████╔╝███████║
    ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
        </pre>
        <div style="color: #888; font-size: 11px;">
            Private Agent • DibTauroS Framework • Ordo ab Chao
        </div>
    </div>

    <!-- Status Bar -->
    <div style="
        display: flex;
        gap: 15px;
        margin-bottom: 15px;
        flex-wrap: wrap;
    ">
        <div id="tauros-connection-status" style="
            padding: 6px 12px;
            border: 1px solid #333;
            font-size: 12px;
        ">⬤ Checking...</div>
        <div id="tauros-mode-indicator" style="
            padding: 6px 12px;
            border: 1px solid #00ff41;
            font-size: 12px;
            color: #00ff41;
        ">MODE: DEFEND</div>
        <div style="
            padding: 6px 12px;
            border: 1px solid #333;
            font-size: 12px;
            color: #888;
        ">Owner: Dib Anouar | LUP v1.0</div>
    </div>

    <!-- Main Grid -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">

        <!-- Operation Panel -->
        <div style="border: 1px solid #333; padding: 15px;">
            <h3 style="color: #00ff41; margin: 0 0 15px 0; font-size: 14px;">
                ⚡ OPERATION CONTROL
            </h3>

            <div style="margin-bottom: 10px;">
                <label style="display: block; color: #888; font-size: 11px; margin-bottom: 4px;">
                    PROMPT / COMMAND
                </label>
                <textarea id="tauros-prompt" style="
                    width: 100%;
                    background: #111;
                    border: 1px solid #333;
                    color: #00ff41;
                    padding: 8px;
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    resize: vertical;
                    min-height: 80px;
                    box-sizing: border-box;
                " placeholder="Enter operation (e.g., 'check processes', 'Wassim scan network')"></textarea>
            </div>

            <div style="margin-bottom: 10px;">
                <label style="display: block; color: #888; font-size: 11px; margin-bottom: 4px;">
                    TARGET
                </label>
                <input id="tauros-target" type="text" value="localhost" style="
                    width: 100%;
                    background: #111;
                    border: 1px solid #333;
                    color: #00ff41;
                    padding: 8px;
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    box-sizing: border-box;
                ">
            </div>

            <div style="margin-bottom: 15px; display: flex; align-items: center; gap: 8px;">
                <input id="tauros-dryrun" type="checkbox" checked style="cursor: pointer;">
                <label for="tauros-dryrun" style="color: #888; font-size: 11px; cursor: pointer;">
                    DRY-RUN (simulate only)
                </label>
            </div>

            <div style="display: flex; gap: 8px;">
                <button onclick="window.taurosAgent.executeOperation()" style="
                    flex: 1;
                    background: #001a00;
                    border: 1px solid #00ff41;
                    color: #00ff41;
                    padding: 8px;
                    cursor: pointer;
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                ">▶ EXECUTE</button>
                <button onclick="window.taurosAgent.clearOutput()" style="
                    background: #1a0000;
                    border: 1px solid #ff3333;
                    color: #ff3333;
                    padding: 8px;
                    cursor: pointer;
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                ">✕ CLEAR</button>
            </div>
        </div>

        <!-- Output Panel -->
        <div style="border: 1px solid #333; padding: 15px;">
            <h3 style="color: #00ff41; margin: 0 0 15px 0; font-size: 14px;">
                📋 OUTPUT
            </h3>
            <div id="tauros-output" style="
                background: #050505;
                border: 1px solid #222;
                padding: 10px;
                min-height: 200px;
                max-height: 400px;
                overflow-y: auto;
                font-size: 11px;
                color: #aaa;
                white-space: pre-wrap;
                word-break: break-word;
            ">Waiting for operation...</div>
        </div>

        <!-- Status Panel -->
        <div style="border: 1px solid #333; padding: 15px;">
            <h3 style="color: #00ff41; margin: 0 0 15px 0; font-size: 14px;">
                🛡️ AGENT STATUS
            </h3>
            <div id="tauros-status" style="font-size: 12px; color: #888;">
                Loading status...
            </div>
            <button onclick="window.taurosAgent.refreshStatus()" style="
                margin-top: 10px;
                background: #001a00;
                border: 1px solid #00ff41;
                color: #00ff41;
                padding: 6px 12px;
                cursor: pointer;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            ">↻ REFRESH</button>
        </div>

        <!-- Log Panel -->
        <div style="border: 1px solid #333; padding: 15px;">
            <h3 style="color: #00ff41; margin: 0 0 15px 0; font-size: 14px;">
                📜 OPERATION LOG
            </h3>
            <div id="tauros-log" style="
                background: #050505;
                border: 1px solid #222;
                padding: 10px;
                min-height: 150px;
                max-height: 250px;
                overflow-y: auto;
                font-size: 11px;
                color: #666;
            ">No operations yet.</div>
        </div>
    </div>

    <!-- Footer -->
    <div style="
        margin-top: 20px;
        border-top: 1px solid #222;
        padding-top: 10px;
        color: #444;
        font-size: 10px;
        text-align: center;
    ">
        TaurosPrivateAgent v1.0.0 | DibTauroS/Ordo-ab-Chao | Owner: Dib Anouar | LUP v1.0
    </div>
</div>
        `;
    }

    /**
     * Check API connection
     */
    async _checkConnection() {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);
        try {
            const response = await fetch(`${this.config.baseUrl}/tauros/status`, {
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (response.ok) {
                this.state.connected = true;
                this._updateConnectionStatus(true);
                const data = await response.json();
                this._updateStatusPanel(data);
            } else {
                this._updateConnectionStatus(false);
            }
        } catch (e) {
            clearTimeout(timeoutId);
            this._updateConnectionStatus(false);
            this._log(`Connection failed: ${e.message}`, 'error');
        }
    }

    /**
     * Update connection status indicator
     */
    _updateConnectionStatus(connected) {
        const el = document.getElementById('tauros-connection-status');
        if (!el) return;
        if (connected) {
            el.textContent = '⬤ CONNECTED';
            el.style.color = '#00ff41';
            el.style.borderColor = '#00ff41';
        } else {
            el.textContent = '⬤ OFFLINE';
            el.style.color = '#ff3333';
            el.style.borderColor = '#ff3333';
        }
    }

    /**
     * Update agent status panel
     */
    _updateStatusPanel(data) {
        const el = document.getElementById('tauros-status');
        if (!el) return;

        el.innerHTML = `
<div style="line-height: 1.8;">
    <div><span style="color: #555;">Agent:</span> <span style="color: #00ff41;">${data.agent || 'N/A'}</span></div>
    <div><span style="color: #555;">Version:</span> <span style="color: #aaa;">${data.version || 'N/A'}</span></div>
    <div><span style="color: #555;">Owner:</span> <span style="color: #aaa;">${data.owner || 'N/A'}</span></div>
    <div><span style="color: #555;">Mode:</span> <span style="color: #00ff41;">${data.current_mode || 'N/A'}</span></div>
    <div><span style="color: #555;">MONICA:</span> <span style="color: ${data.monica_disabled ? '#ff3333' : '#00ff41'};">${data.monica_disabled ? 'DISABLED' : 'ACTIVE'}</span></div>
    <div><span style="color: #555;">Allowlist targets:</span> <span style="color: #aaa;">${data.allowlist_targets || 0}</span></div>
    <div><span style="color: #555;">Timestamp:</span> <span style="color: #666; font-size: 10px;">${data.timestamp || 'N/A'}</span></div>
</div>
        `;

        if (data.current_mode) {
            this.state.mode = data.current_mode;
            const modeEl = document.getElementById('tauros-mode-indicator');
            if (modeEl) modeEl.textContent = `MODE: ${data.current_mode}`;
        }
    }

    /**
     * Execute an operation via the API
     */
    async executeOperation() {
        const prompt = document.getElementById('tauros-prompt')?.value?.trim();
        const target = document.getElementById('tauros-target')?.value?.trim() || 'localhost';
        const dryRun = document.getElementById('tauros-dryrun')?.checked !== false;

        if (!prompt) {
            this._setOutput('⚠ Please enter a prompt before executing.', 'warn');
            return;
        }

        this._setOutput('⏳ Executing operation...', 'info');
        this._appendLog(`[${new Date().toISOString()}] Operation: ${prompt} | Target: ${target} | DryRun: ${dryRun}`);

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 30000);
            const response = await fetch(`${this.config.baseUrl}/tauros/execute`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt, target, dry_run: dryRun }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            const result = await response.json();
            this._displayResult(result);
            this.state.operationHistory.push({ prompt, target, dryRun, result, timestamp: new Date().toISOString() });
        } catch (e) {
            this._setOutput(`❌ Error: ${e.message}`, 'error');
            this._log(`Operation error: ${e.message}`, 'error');
        }
    }

    /**
     * Display operation result
     */
    _displayResult(result) {
        const statusColor = {
            'success': '#00ff41',
            'simulated': '#00aaff',
            'denied': '#ff8800',
            'blocked': '#ff3333',
            'error': '#ff3333',
            'timeout': '#ffaa00',
            'not_implemented': '#888888'
        }[result.status] || '#aaaaaa';

        const output = `STATUS: ${result.status.toUpperCase()}
${'-'.repeat(40)}
${JSON.stringify(result, null, 2)}`;

        const el = document.getElementById('tauros-output');
        if (el) {
            el.textContent = output;
            el.style.color = statusColor;
        }
    }

    /**
     * Refresh agent status from API
     */
    async refreshStatus() {
        await this._checkConnection();
    }

    /**
     * Clear output panel
     */
    clearOutput() {
        const el = document.getElementById('tauros-output');
        if (el) {
            el.textContent = 'Output cleared.';
            el.style.color = '#aaa';
        }
    }

    /**
     * Append a line to the operation log panel
     */
    _appendLog(message) {
        const el = document.getElementById('tauros-log');
        if (!el) return;
        const line = document.createElement('div');
        line.style.borderBottom = '1px solid #111';
        line.style.paddingBottom = '4px';
        line.style.marginBottom = '4px';
        line.textContent = message;
        if (el.firstChild && el.firstChild.textContent === 'No operations yet.') {
            el.innerHTML = '';
        }
        el.appendChild(line);
        el.scrollTop = el.scrollHeight;
    }

    /**
     * Set output panel content
     */
    _setOutput(message, level = 'info') {
        const el = document.getElementById('tauros-output');
        if (!el) return;
        const colors = { info: '#aaa', warn: '#ffaa00', error: '#ff3333', success: '#00ff41' };
        el.textContent = message;
        el.style.color = colors[level] || '#aaa';
    }

    /**
     * Internal logger
     */
    _log(message, level = 'info') {
        if (!this.config.enableLogging) return;
        const prefix = '[TaurosAgent]';
        switch (level) {
            case 'error': console.error(prefix, message); break;
            case 'warn':  console.warn(prefix, message);  break;
            default:      console.log(prefix, message);
        }
    }
}

// Auto-initialize if the init container is present and not already initialized
if (document.getElementById('tauros-auto-init') && !window.taurosAgent) {
    window.taurosAgent = new TaurosPrivateAgent({
        baseUrl: window.location.origin,
        enableLogging: true
    });
}
