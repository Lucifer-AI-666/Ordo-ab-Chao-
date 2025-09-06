/**
 * CopilotPrivateAgent JavaScript Integration - Neo Cleopatra Viva Edition
 * 
 * Enhanced web interface client for DibTauroS/Ordo-ab-Chao cybersecurity framework
 * Egyptian-themed version for Neo Cleopatra Viva deployment
 * 
 * Owner: Dib Anouar
 * License: LUP v1.0 (personal and non-commercial use only)
 */

class CopilotPrivateAgent {
    /**
     * Initialize CopilotPrivateAgent web client
     * @param {Object} config - Configuration object
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
        
        this.log('🏛️ Neo Cleopatra Viva initialized', 'info');
        this.log('Framework: DibTauroS/Ordo-ab-Chao', 'info');
        
        // For Vercel deployment, we'll simulate API calls
        this.isVercelMode = window.location.hostname.includes('vercel.app') || 
                           window.location.hostname.includes('vercel.com') ||
                           window.location.protocol === 'file:' ||
                           (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1');
        
        if (this.isVercelMode) {
            this.log('📡 Running in Vercel deployment mode (simulation)', 'info');
        }
    }

    /**
     * Execute cybersecurity operation
     */
    async executeOperation(prompt, target = 'localhost', dryRun = true) {
        const timestamp = new Date().toLocaleTimeString();
        
        this.logOutput(`⚔️ Executing operation: ${prompt}`, 'info');
        this.logOutput(`🎯 Target: ${target} | 🛡️ Dry Run: ${dryRun}`, 'info');
        
        try {
            if (this.isVercelMode) {
                // Simulation mode for Vercel deployment
                await this.simulateOperation(prompt, target, dryRun);
            } else {
                // Real API call for local deployment
                const result = await this.callAPI('/copilot/execute', {
                    prompt: prompt,
                    target: target,
                    dry_run: dryRun
                });
                
                this.logOutput('📊 Operation Result:', 'success');
                this.logOutput(JSON.stringify(result, null, 2), 'result');
            }
            
        } catch (error) {
            this.logOutput(`❌ Error: ${error.message}`, 'error');
        }
    }

    /**
     * Simulate operation for Vercel deployment
     */
    async simulateOperation(prompt, target, dryRun) {
        // Add loading animation
        const loading = document.createElement('div');
        loading.className = 'log-entry';
        loading.innerHTML = '<div class="log-message">🔄 Analyzing security parameters...</div>';
        document.getElementById('operation-log').appendChild(loading);
        
        await this.delay(1000);
        
        // Simulate security analysis
        const results = {
            status: dryRun ? 'simulated' : 'executed',
            mode: this.currentMode,
            target: target,
            security_context: {
                framework: 'DibTauroS/Ordo-ab-Chao',
                privacy_mode: 'LOCAL_ONLY',
                audit_trail: 'SHA-256_ENABLED',
                target_validation: target === 'localhost' ? 'ALLOWED' : 'REQUIRES_ALLOWLIST'
            },
            timestamp: new Date().toISOString(),
            egyptian_blessing: '𓂀 May the wisdom of Thoth guide your cybersecurity endeavors 𓂀'
        };
        
        // Remove loading
        loading.remove();
        
        // Show results
        this.logOutput('✨ Neo Cleopatra Analysis Complete:', 'success');
        this.logOutput(JSON.stringify(results, null, 2), 'result');
        
        // Add Egyptian flair
        if (prompt.toLowerCase().includes('scan') || prompt.toLowerCase().includes('analyze')) {
            this.logOutput('🔍 The Eye of Horus reveals: Security scan initiated with royal protection', 'info');
        }
        
        if (this.currentMode === 'TEST') {
            this.logOutput('⚡ Advanced mode activated - The pharaoh\'s power flows through your commands', 'warning');
        }
    }

    /**
     * Load agent status
     */
    async loadStatus() {
        this.logOutput('📡 Checking system status...', 'info');
        
        try {
            if (this.isVercelMode) {
                // Simulate status for Vercel
                const status = {
                    status: 'operational',
                    mode: this.currentMode,
                    framework: 'DibTauroS/Ordo-ab-Chao',
                    deployment: 'Neo Cleopatra Viva on Vercel',
                    security_level: 'MAXIMUM',
                    privacy_protection: 'ENABLED',
                    owner: 'Dib Anouar',
                    license: 'LUP v1.0',
                    egyptian_status: '𓋹 The golden falcon soars - All systems operational 𓋹'
                };
                
                this.logOutput('👑 Royal Status Report:', 'success');
                this.logOutput(JSON.stringify(status, null, 2), 'result');
                
                // Update UI
                document.getElementById('connection-status').textContent = '⚡';
                document.getElementById('mode-indicator').textContent = this.currentMode;
                
            } else {
                const status = await this.callAPI('/copilot/status', null, 'GET');
                this.logOutput('📊 Agent Status:', 'success');
                this.logOutput(JSON.stringify(status, null, 2), 'result');
            }
            
        } catch (error) {
            this.logOutput(`❌ Status check failed: ${error.message}`, 'error');
        }
    }

    /**
     * Call API endpoint (for non-Vercel deployments)
     */
    async callAPI(endpoint, data = null, method = 'POST') {
        if (this.isVercelMode) {
            throw new Error('API calls not available in Vercel mode - using simulation');
        }
        
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
     * Log output to the interface
     */
    logOutput(message, type = 'info') {
        const output = document.getElementById('operation-log');
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
        const timestampDisplay = document.getElementById('timestamp-display');
        if (timestampDisplay) {
            timestampDisplay.textContent = timestamp;
        }
    }

    /**
     * Clear the output log
     */
    clearLog() {
        const output = document.getElementById('operation-log');
        if (output) {
            output.innerHTML = `
                <div class="welcome-message">
                    <p>🌟 Welcome to Neo Cleopatra Viva</p>
                    <p>Advanced cybersecurity operations interface</p>
                    <p>Framework: DibTauroS/Ordo-ab-Chao</p>
                    <hr>
                </div>
            `;
        }
        this.logOutput('🧹 Log cleared by royal decree', 'info');
    }

    /**
     * Console logging
     */
    log(message, level = 'info') {
        if (!this.enableLogging) return;
        
        const prefix = '[Neo Cleopatra Viva]';
        
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
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Utility delay function
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Update mode (DEFEND/TEST)
     */
    setMode(mode) {
        this.currentMode = mode;
        const modeIndicator = document.getElementById('mode-indicator');
        if (modeIndicator) {
            modeIndicator.textContent = mode;
        }
        
        this.logOutput(`⚡ Mode changed to: ${mode}`, 'warning');
        
        if (mode === 'TEST') {
            this.logOutput('👑 Pharaoh mode activated - Advanced operations enabled', 'warning');
        } else {
            this.logOutput('🛡️ Defensive mode - Standard operations enabled', 'info');
        }
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

// Make class globally available
window.CopilotPrivateAgent = CopilotPrivateAgent;