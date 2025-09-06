/**
 * Neo Cleopatra Viva - Main Interface Controller
 * 
 * Egyptian-themed cybersecurity interface for DibTauroS/Ordo-ab-Chao
 * 
 * Owner: Dib Anouar
 * License: LUP v1.0 (personal and non-commercial use only)
 */

class NeoCleopatraInterface {
    constructor() {
        this.copilotAgent = null;
        this.initializeInterface();
        this.setupEventHandlers();
        this.showWelcomeMessage();
    }

    /**
     * Initialize the Neo Cleopatra interface
     */
    initializeInterface() {
        // Create CopilotPrivateAgent instance
        this.copilotAgent = new CopilotPrivateAgent({
            baseUrl: window.location.origin,
            enableLogging: true
        });

        // Initialize UI state
        this.updateTimestamp();
        
        // Set initial status
        document.getElementById('connection-status').textContent = '⚡';
        document.getElementById('mode-indicator').textContent = 'DEFEND';
        
        console.log('🏛️ Neo Cleopatra Viva interface initialized');
    }

    /**
     * Setup event handlers for UI elements
     */
    setupEventHandlers() {
        // Execute operation button
        const executeBtn = document.getElementById('execute-btn');
        if (executeBtn) {
            executeBtn.addEventListener('click', () => this.executeOperation());
        }

        // Status check button
        const statusBtn = document.getElementById('status-btn');
        if (statusBtn) {
            statusBtn.addEventListener('click', () => this.checkStatus());
        }

        // Clear log button
        const clearBtn = document.getElementById('clear-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearLog());
        }

        // Test mode checkbox
        const testModeCheckbox = document.getElementById('test-mode');
        if (testModeCheckbox) {
            testModeCheckbox.addEventListener('change', (e) => {
                this.toggleTestMode(e.target.checked);
            });
        }

        // Enter key support in textarea
        const operationInput = document.getElementById('operation-input');
        if (operationInput) {
            operationInput.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter') {
                    this.executeOperation();
                }
            });
        }

        // Update timestamp every second
        setInterval(() => this.updateTimestamp(), 1000);
    }

    /**
     * Execute cybersecurity operation
     */
    async executeOperation() {
        const target = document.getElementById('target-input')?.value || 'localhost';
        const operation = document.getElementById('operation-input')?.value;
        const dryRun = document.getElementById('dry-run-mode')?.checked !== false;
        const testMode = document.getElementById('test-mode')?.checked;

        if (!operation || operation.trim() === '') {
            this.copilotAgent.logOutput('❌ Please enter an operation command', 'error');
            return;
        }

        // Add Egyptian flair to the command
        let finalOperation = operation;
        if (testMode && !operation.toLowerCase().includes('wassim')) {
            finalOperation = `Wassim ${operation}`;
        }

        // Add button loading state
        const executeBtn = document.getElementById('execute-btn');
        const originalText = executeBtn.innerHTML;
        executeBtn.innerHTML = '<span>🔄 Executing...</span>';
        executeBtn.disabled = true;

        try {
            await this.copilotAgent.executeOperation(finalOperation, target, dryRun);
        } finally {
            // Restore button state
            executeBtn.innerHTML = originalText;
            executeBtn.disabled = false;
        }
    }

    /**
     * Check system status
     */
    async checkStatus() {
        const statusBtn = document.getElementById('status-btn');
        const originalText = statusBtn.innerHTML;
        statusBtn.innerHTML = '<span>📡 Checking...</span>';
        statusBtn.disabled = true;

        try {
            await this.copilotAgent.loadStatus();
        } finally {
            statusBtn.innerHTML = originalText;
            statusBtn.disabled = false;
        }
    }

    /**
     * Clear operation log
     */
    clearLog() {
        this.copilotAgent.clearLog();
    }

    /**
     * Toggle between DEFEND and TEST modes
     */
    toggleTestMode(enabled) {
        const mode = enabled ? 'TEST' : 'DEFEND';
        this.copilotAgent.setMode(mode);
        
        // Update UI
        document.getElementById('mode-indicator').textContent = mode;
        
        // Add visual feedback
        const modeIndicator = document.getElementById('mode-indicator');
        if (enabled) {
            modeIndicator.style.background = 'linear-gradient(45deg, #FF6B35, #F7931E)';
            modeIndicator.style.color = 'white';
        } else {
            modeIndicator.style.background = '';
            modeIndicator.style.color = '';
        }
    }

    /**
     * Show welcome message
     */
    showWelcomeMessage() {
        setTimeout(() => {
            this.copilotAgent.logOutput('👑 Welcome to Neo Cleopatra Viva cybersecurity operations', 'success');
            this.copilotAgent.logOutput('🏛️ Framework: DibTauroS/Ordo-ab-Chao by Dib Anouar', 'info');
            this.copilotAgent.logOutput('🛡️ Privacy-first operations • License: LUP v1.0', 'info');
            this.copilotAgent.logOutput('⚡ Ready for cybersecurity operations', 'success');
            
            // Add some Egyptian mystique
            if (Math.random() > 0.5) {
                setTimeout(() => {
                    this.copilotAgent.logOutput('𓂀 "Knowledge is the treasure of the wise pharaoh" 𓂀', 'info');
                }, 1500);
            }
        }, 500);
    }

    /**
     * Update timestamp display
     */
    updateTimestamp() {
        const timestamp = new Date().toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        
        const timestampDisplay = document.getElementById('timestamp-display');
        if (timestampDisplay) {
            timestampDisplay.textContent = timestamp;
        }
    }

    /**
     * Add special Egyptian-themed operations
     */
    addEgyptianCommands() {
        const commands = [
            'pharaoh scan network',
            'sphinx analyze security',
            'pyramid fortify defenses',
            'anubis guard secrets',
            'isis protect data'
        ];

        // Add command suggestions (could be expanded)
        const operationInput = document.getElementById('operation-input');
        if (operationInput) {
            operationInput.addEventListener('focus', () => {
                if (operationInput.value === '') {
                    const randomCommand = commands[Math.floor(Math.random() * commands.length)];
                    operationInput.placeholder = `Try: "${randomCommand}" or enter your own command...`;
                }
            });
        }
    }

    /**
     * Handle special key combinations
     */
    handleKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl + Shift + C: Clear log
            if (e.ctrlKey && e.shiftKey && e.key === 'C') {
                e.preventDefault();
                this.clearLog();
            }
            
            // Ctrl + Shift + S: Check status
            if (e.ctrlKey && e.shiftKey && e.key === 'S') {
                e.preventDefault();
                this.checkStatus();
            }
            
            // Ctrl + Enter: Execute (when not in textarea)
            if (e.ctrlKey && e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
                this.executeOperation();
            }
        });
    }

    /**
     * Add particle effects for Egyptian atmosphere
     */
    addParticleEffects() {
        // Simple golden particles for ambiance
        const createParticle = () => {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: fixed;
                width: 3px;
                height: 3px;
                background: radial-gradient(circle, #FFD700, transparent);
                border-radius: 50%;
                pointer-events: none;
                z-index: -1;
                opacity: 0.6;
                animation: float 6s linear infinite;
            `;
            
            particle.style.left = Math.random() * window.innerWidth + 'px';
            particle.style.top = window.innerHeight + 'px';
            
            document.body.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, 6000);
        };

        // Create particles occasionally
        setInterval(() => {
            if (Math.random() > 0.8) {
                createParticle();
            }
        }, 2000);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.neoCleopatraInterface = new NeoCleopatraInterface();
    
    // Add the CSS for particle animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            to {
                transform: translateY(-${window.innerHeight + 50}px) rotate(360deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    console.log('🏛️ Neo Cleopatra Viva fully loaded and operational');
});

// Export for global access
window.NeoCleopatraInterface = NeoCleopatraInterface;