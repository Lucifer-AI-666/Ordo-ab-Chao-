/**
 * CopilotPrivateAgent JavaScript Integration
 * 
 * Web interface client for DibTauroS/Ordo-ab-Chao cybersecurity framework
 * 
 * Owner: Dib Anouar
 * License: LUP v1.0 (personal and non-commercial use only)
 */

class CopilotPrivateAgent {
    /**
     * Initialize CopilotPrivateAgent web client
     * @param {Object} config - Configuration object
     * @param {string} config.baseUrl - Base URL for agent API (default: http://localhost:8787)
     * @param {string} config.token - Bearer token for authentication
     * @param {boolean} config.enableLogging - Enable console logging (default: true)
     */
    constructor(config = {}) {
        this.baseUrl = config.baseUrl || 'http://localhost:8787';
        this.token = config.token || null;
        this.enableLogging = config.enableLogging !== false;
        this.wsConnection = null;
        this.eventHandlers = {};
        
        // Security context
        this.currentMode = 'DEFEND';
        this.allowedTargets = [];
        
        this.log('CopilotPrivateAgent web client initialized', 'info');
        this.log('Framework: DibTauroS/Ordo-ab-Chao', 'info');
        
        // Initialize UI components
        this.initializeUI();
        
        // Load initial status
        this.loadStatus();
    }

    /**
     * Initialize UI components and event handlers
     */
    initializeUI() {
        // Create main container if it doesn't exist
        if (!document.getElementById('copilot-container')) {
            this.createMainContainer();
        }
        
        // Setup event handlers
        this.setupEventHandlers();
        
        // Load DibTauroS branding
        this.loadBranding();
    }

    /**
     * Create main UI container
     */
    createMainContainer() {
        const container = document.createElement('div');
        container.id = 'copilot-container';
        container.className = 'copilot-agent-container';
        
        container.innerHTML = `
            <div class="copilot-header">
                <div class="copilot-logo">
                    <span class="copilot-title">CopilotPrivateAgent</span>
                    <span class="copilot-subtitle">DibTauroS • Ordo ab Chao</span>
                </div>
                <div class="copilot-status">
                    <span id="copilot-mode" class="mode-indicator">DEFEND</span>
                    <span id="copilot-connection" class="connection-status">●</span>
                </div>
            </div>
            
            <div class="copilot-interface">
                <div class="copilot-input-section">
                    <div class="input-group">
                        <label for="copilot-target">Target:</label>
                        <input type="text" id="copilot-target" value="localhost" placeholder="Target system/IP">
                    </div>
                    
                    <div class="input-group">
                        <label for="copilot-prompt">Command/Prompt:</label>
                        <textarea id="copilot-prompt" placeholder="Enter your cybersecurity operation prompt..."></textarea>
                    </div>
                    
                    <div class="control-group">
                        <label class="checkbox-label">
                            <input type="checkbox" id="copilot-dryrun" checked>
                            Dry Run (Simulation)
                        </label>
                        
                        <label class="checkbox-label">
                            <input type="checkbox" id="copilot-wassim">
                            TEST Mode (Wassim)
                        </label>
                    </div>
                    
                    <div class="button-group">
                        <button id="copilot-execute" class="btn-primary">Execute Operation</button>
                        <button id="copilot-status" class="btn-secondary">Check Status</button>
                        <button id="copilot-clear" class="btn-secondary">Clear Log</button>
                    </div>
                </div>
                
                <div class="copilot-output-section">
                    <div class="output-header">
                        <span>Operation Log</span>
                        <span id="copilot-timestamp"></span>
                    </div>
                    <div id="copilot-output" class="output-content"></div>
                </div>
            </div>
            
            <div class="copilot-footer">
                <span>Owner: Dib Anouar • License: LUP v1.0</span>
                <span>Privacy-first cybersecurity framework</span>
            </div>
        `;
        
        // Add to body or specified parent
        document.body.appendChild(container);
        
        // Add CSS styles
        this.injectStyles();
    }

    /**
     * Inject CSS styles for the interface
     */
    injectStyles() {
        const styleId = 'copilot-agent-styles';
        if (document.getElementById(styleId)) return;
        
        const style = document.createElement('style');
        style.id = styleId;
        style.textContent = `
            .copilot-agent-container {
                font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
                color: #00ff41;
                border: 2px solid #00ff41;
                border-radius: 8px;
                margin: 20px;
                padding: 0;
                box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
                max-width: 1200px;
            }
            
            .copilot-header {
                background: rgba(0, 255, 65, 0.1);
                padding: 15px 20px;
                border-bottom: 1px solid #00ff41;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .copilot-title {
                font-size: 1.5em;
                font-weight: bold;
                color: #00ff41;
                text-shadow: 0 0 5px rgba(0, 255, 65, 0.5);
            }
            
            .copilot-subtitle {
                font-size: 0.9em;
                color: #888;
                margin-left: 10px;
            }
            
            .mode-indicator {
                background: #00ff41;
                color: #000;
                padding: 3px 8px;
                border-radius: 4px;
                font-size: 0.8em;
                font-weight: bold;
            }
            
            .connection-status {
                color: #00ff41;
                font-size: 1.2em;
                margin-left: 10px;
            }
            
            .copilot-interface {
                padding: 20px;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            
            .input-group {
                margin-bottom: 15px;
            }
            
            .input-group label {
                display: block;
                margin-bottom: 5px;
                color: #00ff41;
                font-size: 0.9em;
            }
            
            .input-group input, .input-group textarea {
                width: 100%;
                background: rgba(0, 0, 0, 0.5);
                border: 1px solid #00ff41;
                color: #00ff41;
                padding: 8px;
                border-radius: 4px;
                font-family: inherit;
            }
            
            .input-group textarea {
                height: 80px;
                resize: vertical;
            }
            
            .control-group {
                margin: 20px 0;
            }
            
            .checkbox-label {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
                color: #ccc;
                font-size: 0.9em;
            }
            
            .checkbox-label input {
                margin-right: 8px;
                width: auto;
            }
            
            .button-group {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            
            .btn-primary, .btn-secondary {
                padding: 10px 20px;
                border: 1px solid #00ff41;
                border-radius: 4px;
                cursor: pointer;
                font-family: inherit;
                font-size: 0.9em;
                transition: all 0.3s ease;
            }
            
            .btn-primary {
                background: #00ff41;
                color: #000;
            }
            
            .btn-primary:hover {
                background: rgba(0, 255, 65, 0.8);
                box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
            }
            
            .btn-secondary {
                background: transparent;
                color: #00ff41;
            }
            
            .btn-secondary:hover {
                background: rgba(0, 255, 65, 0.1);
            }
            
            .output-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
                color: #00ff41;
                font-size: 0.9em;
            }
            
            .output-content {
                background: rgba(0, 0, 0, 0.7);
                border: 1px solid #333;
                border-radius: 4px;
                padding: 15px;
                height: 400px;
                overflow-y: auto;
                font-size: 0.85em;
                line-height: 1.4;
            }
            
            .copilot-footer {
                background: rgba(0, 255, 65, 0.05);
                padding: 10px 20px;
                border-top: 1px solid #333;
                display: flex;
                justify-content: space-between;
                font-size: 0.8em;
                color: #888;
            }
            
            .log-entry {
                margin-bottom: 10px;
                padding: 8px;
                border-left: 3px solid #00ff41;
                background: rgba(0, 255, 65, 0.05);
            }
            
            .log-entry.error {
                border-left-color: #ff4444;
                background: rgba(255, 68, 68, 0.05);
            }
            
            .log-entry.warning {
                border-left-color: #ffaa00;
                background: rgba(255, 170, 0, 0.05);
            }
            
            .log-timestamp {
                color: #666;
                font-size: 0.8em;
            }
            
            @media (max-width: 768px) {
                .copilot-interface {
                    grid-template-columns: 1fr;
                }
                
                .copilot-header {
                    flex-direction: column;
                    text-align: center;
                }
                
                .button-group {
                    justify-content: center;
                }
            }
        `;
        
        document.head.appendChild(style);
    }

    /**
     * Setup event handlers for UI components
     */
    setupEventHandlers() {
        // Execute operation button
        document.getElementById('copilot-execute')?.addEventListener('click', () => {
            this.executeOperation();
        });
        
        // Status check button
        document.getElementById('copilot-status')?.addEventListener('click', () => {
            this.loadStatus();
        });
        
        // Clear log button
        document.getElementById('copilot-clear')?.addEventListener('click', () => {
            this.clearLog();
        });
        
        // Enter key in prompt textarea
        document.getElementById('copilot-prompt')?.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.executeOperation();
            }
        });
        
        // Wassim checkbox for TEST mode
        document.getElementById('copilot-wassim')?.addEventListener('change', (e) => {
            this.currentMode = e.target.checked ? 'TEST' : 'DEFEND';
            document.getElementById('copilot-mode').textContent = this.currentMode;
        });
    }

    /**
     * Load DibTauroS branding elements
     */
    loadBranding() {
        // This would load external branding files
        // For now, we use the embedded styling
        this.log('DibTauroS branding loaded', 'info');
    }

    /**
     * Execute cybersecurity operation
     */
    async executeOperation() {
        const target = document.getElementById('copilot-target')?.value || 'localhost';
        const prompt = document.getElementById('copilot-prompt')?.value;
        const dryRun = document.getElementById('copilot-dryrun')?.checked !== false;
        const wassim = document.getElementById('copilot-wassim')?.checked;
        
        if (!prompt.trim()) {
            this.logOutput('Error: Please enter a command/prompt', 'error');
            return;
        }
        
        // Add Wassim keyword if TEST mode is enabled
        const finalPrompt = wassim ? `Wassim ${prompt}` : prompt;
        
        this.logOutput(`Executing operation: ${finalPrompt}`, 'info');
        this.logOutput(`Target: ${target}, Dry Run: ${dryRun}`, 'info');
        
        try {
            const result = await this.callAPI('/copilot/execute', {
                prompt: finalPrompt,
                target: target,
                dry_run: dryRun
            });
            
            this.logOutput('Operation Result:', 'success');
            this.logOutput(JSON.stringify(result, null, 2), 'result');
            
        } catch (error) {
            this.logOutput(`Error: ${error.message}`, 'error');
        }
    }

    /**
     * Load agent status
     */
    async loadStatus() {
        this.logOutput('Loading agent status...', 'info');
        
        try {
            const status = await this.callAPI('/copilot/status');
            
            this.logOutput('Agent Status:', 'success');
            this.logOutput(JSON.stringify(status, null, 2), 'result');
            
            // Update UI elements
            if (status.current_mode) {
                document.getElementById('copilot-mode').textContent = status.current_mode;
            }
            
            // Update connection status
            this.updateConnectionStatus(true);
            
        } catch (error) {
            this.logOutput(`Status check failed: ${error.message}`, 'error');
            this.updateConnectionStatus(false);
        }
    }

    /**
     * Call API endpoint
     * @param {string} endpoint - API endpoint path
     * @param {Object} data - Request data
     * @param {string} method - HTTP method (default: POST)
     */
    async callAPI(endpoint, data = null, method = 'POST') {
        const url = `${this.baseUrl}${endpoint}`;
        
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (this.token) {
            options.headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        if (data && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(data);
        }
        
        this.log(`API call: ${method} ${url}`, 'debug');
        
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`API call failed: ${response.status} ${response.statusText}`);
        }
        
        return await response.json();
    }

    /**
     * Update connection status indicator
     * @param {boolean} connected - Connection status
     */
    updateConnectionStatus(connected) {
        const indicator = document.getElementById('copilot-connection');
        if (indicator) {
            indicator.style.color = connected ? '#00ff41' : '#ff4444';
            indicator.title = connected ? 'Connected' : 'Disconnected';
        }
    }

    /**
     * Log output to the interface
     * @param {string} message - Log message
     * @param {string} type - Log type (info, error, warning, success, result)
     */
    logOutput(message, type = 'info') {
        const output = document.getElementById('copilot-output');
        if (!output) return;
        
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        
        const timestamp = new Date().toLocaleTimeString();
        entry.innerHTML = `
            <div class="log-timestamp">[${timestamp}]</div>
            <div class="log-message">${this.escapeHtml(message)}</div>
        `;
        
        output.appendChild(entry);
        output.scrollTop = output.scrollHeight;
        
        // Update timestamp in header
        document.getElementById('copilot-timestamp').textContent = timestamp;
    }

    /**
     * Clear the output log
     */
    clearLog() {
        const output = document.getElementById('copilot-output');
        if (output) {
            output.innerHTML = '';
        }
        this.logOutput('Log cleared', 'info');
    }

    /**
     * Console logging
     * @param {string} message - Log message
     * @param {string} level - Log level
     */
    log(message, level = 'info') {
        if (!this.enableLogging) return;
        
        const prefix = '[CopilotPrivateAgent]';
        
        switch (level) {
            case 'error':
                console.error(prefix, message);
                break;
            case 'warn':
            case 'warning':
                console.warn(prefix, message);
                break;
            case 'debug':
                console.debug(prefix, message);
                break;
            default:
                console.log(prefix, message);
        }
    }

    /**
     * Escape HTML for safe display
     * @param {string} text - Text to escape
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Initialize WebSocket connection for real-time updates
     * @param {string} wsUrl - WebSocket URL
     */
    initWebSocket(wsUrl) {
        if (this.wsConnection) {
            this.wsConnection.close();
        }
        
        this.wsConnection = new WebSocket(wsUrl);
        
        this.wsConnection.onopen = () => {
            this.log('WebSocket connection established', 'info');
            this.updateConnectionStatus(true);
        };
        
        this.wsConnection.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            } catch (error) {
                this.log('Invalid WebSocket message received', 'error');
            }
        };
        
        this.wsConnection.onclose = () => {
            this.log('WebSocket connection closed', 'warning');
            this.updateConnectionStatus(false);
        };
        
        this.wsConnection.onerror = (error) => {
            this.log('WebSocket error', 'error');
            this.updateConnectionStatus(false);
        };
    }

    /**
     * Handle WebSocket messages
     * @param {Object} data - Message data
     */
    handleWebSocketMessage(data) {
        if (data.type === 'operation_update') {
            this.logOutput(`Operation Update: ${data.message}`, 'info');
        } else if (data.type === 'status_change') {
            this.logOutput(`Status Change: ${data.message}`, 'warning');
            if (data.mode) {
                this.currentMode = data.mode;
                document.getElementById('copilot-mode').textContent = data.mode;
            }
        }
    }

    /**
     * Register event handler
     * @param {string} event - Event name
     * @param {function} handler - Event handler function
     */
    on(event, handler) {
        if (!this.eventHandlers[event]) {
            this.eventHandlers[event] = [];
        }
        this.eventHandlers[event].push(handler);
    }

    /**
     * Emit event
     * @param {string} event - Event name
     * @param {*} data - Event data
     */
    emit(event, data) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event].forEach(handler => handler(data));
        }
    }

    /**
     * Destroy the agent instance
     */
    destroy() {
        if (this.wsConnection) {
            this.wsConnection.close();
        }
        
        const container = document.getElementById('copilot-container');
        if (container) {
            container.remove();
        }
        
        const styles = document.getElementById('copilot-agent-styles');
        if (styles) {
            styles.remove();
        }
        
        this.log('CopilotPrivateAgent instance destroyed', 'info');
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CopilotPrivateAgent;
}

// Global instantiation helper
window.createCopilotAgent = function(config) {
    return new CopilotPrivateAgent(config);
};

// Auto-initialize if container exists
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('copilot-auto-init')) {
        window.copilotAgent = new CopilotPrivateAgent();
    }
});