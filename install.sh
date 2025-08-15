#!/bin/bash
# Copilot Private Agent - Universal Installation Script
# One-click setup for complete cybersecurity ecosystem

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
INSTALL_DIR="/opt/priv-cyber-agents"
LOG_FILE="/tmp/copilot-install.log"
CURRENT_USER="${SUDO_USER:-$USER}"
SYSTEM_ARCH=$(uname -m)
OS_TYPE=$(uname -s)

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}" | tee -a "$LOG_FILE"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "This script should not be run as root directly. Use sudo when needed."
        exit 1
    fi
}

# Detect operating system
detect_os() {
    if [[ "$OS_TYPE" == "Linux" ]]; then
        if command -v apt-get >/dev/null 2>&1; then
            OS_FAMILY="debian"
            PACKAGE_MANAGER="apt-get"
        elif command -v yum >/dev/null 2>&1; then
            OS_FAMILY="redhat"
            PACKAGE_MANAGER="yum"
        elif command -v dnf >/dev/null 2>&1; then
            OS_FAMILY="redhat"
            PACKAGE_MANAGER="dnf"
        elif command -v pacman >/dev/null 2>&1; then
            OS_FAMILY="arch"
            PACKAGE_MANAGER="pacman"
        else
            error "Unsupported Linux distribution"
            exit 1
        fi
    elif [[ "$OS_TYPE" == "Darwin" ]]; then
        OS_FAMILY="macos"
        if command -v brew >/dev/null 2>&1; then
            PACKAGE_MANAGER="brew"
        else
            error "Homebrew not found. Please install it first: https://brew.sh"
            exit 1
        fi
    else
        error "Unsupported operating system: $OS_TYPE"
        exit 1
    fi
    
    log "Detected OS: $OS_FAMILY with package manager: $PACKAGE_MANAGER"
}

# Install system dependencies
install_system_deps() {
    log "Installing system dependencies..."
    
    case "$OS_FAMILY" in
        debian)
            sudo $PACKAGE_MANAGER update
            sudo $PACKAGE_MANAGER install -y python3 python3-pip python3-venv curl wget git \
                nmap masscan nikto gobuster netcat-openbsd tcpdump net-tools \
                build-essential libssl-dev libffi-dev
            ;;
        redhat)
            sudo $PACKAGE_MANAGER update -y
            sudo $PACKAGE_MANAGER install -y python3 python3-pip curl wget git \
                nmap masscan nikto nmap-ncat tcpdump net-tools \
                gcc openssl-devel libffi-devel
            ;;
        arch)
            sudo $PACKAGE_MANAGER -Sy
            sudo $PACKAGE_MANAGER -S --noconfirm python python-pip curl wget git \
                nmap masscan nikto gobuster gnu-netcat tcpdump net-tools \
                base-devel openssl libffi
            ;;
        macos)
            $PACKAGE_MANAGER install python3 curl wget git nmap masscan nikto gobuster netcat
            ;;
    esac
    
    log "System dependencies installed successfully"
}

# Install Go and Go-based tools
install_go_tools() {
    log "Installing Go and Go-based security tools..."
    
    # Install Go if not present
    if ! command -v go >/dev/null 2>&1; then
        case "$OS_FAMILY" in
            debian|redhat)
                GO_VERSION="1.21.4"
                GO_ARCHIVE="go${GO_VERSION}.linux-amd64.tar.gz"
                cd /tmp
                wget "https://golang.org/dl/${GO_ARCHIVE}"
                sudo tar -C /usr/local -xzf "$GO_ARCHIVE"
                echo 'export PATH=$PATH:/usr/local/go/bin' | sudo tee -a /etc/profile
                export PATH=$PATH:/usr/local/go/bin
                ;;
            macos)
                $PACKAGE_MANAGER install go
                ;;
        esac
    fi
    
    # Install Go-based tools
    export GOPATH="$HOME/go"
    export PATH="$PATH:$GOPATH/bin"
    
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    go install -v github.com/OWASP/Amass/v4/cmd/amass@latest
    
    # Update nuclei templates
    "$GOPATH/bin/nuclei" -update-templates
    
    log "Go tools installed successfully"
}

# Install Ollama
install_ollama() {
    log "Installing Ollama..."
    
    if ! command -v ollama >/dev/null 2>&1; then
        curl -fsSL https://ollama.ai/install.sh | sh
        
        # Start Ollama service
        if command -v systemctl >/dev/null 2>&1; then
            sudo systemctl enable ollama
            sudo systemctl start ollama
        fi
        
        # Wait for Ollama to be ready
        sleep 5
        
        # Bind to localhost only for security
        sudo mkdir -p /etc/systemd/system/ollama.service.d/
        cat <<EOF | sudo tee /etc/systemd/system/ollama.service.d/override.conf
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
EOF
        
        if command -v systemctl >/dev/null 2>&1; then
            sudo systemctl daemon-reload
            sudo systemctl restart ollama
        fi
    fi
    
    log "Ollama installed and configured"
}

# Setup Python environment
setup_python_env() {
    log "Setting up Python environment..."
    
    # Create virtual environment
    python3 -m venv "$INSTALL_DIR/.venv"
    source "$INSTALL_DIR/.venv/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install Python dependencies
    cat <<EOF > "$INSTALL_DIR/requirements.txt"
requests>=2.31.0
click>=8.1.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
python-multipart>=0.0.6
jinja2>=3.1.0
aiofiles>=23.2.0
psutil>=5.9.0
python-dateutil>=2.8.0
cryptography>=41.0.0
pyyaml>=6.0.1
colorama>=0.4.6
rich>=13.7.0
httpx>=0.25.0
websockets>=12.0
schedule>=1.2.0
EOF
    
    pip install -r "$INSTALL_DIR/requirements.txt"
    
    log "Python environment configured"
}

# Create directory structure
create_directories() {
    log "Creating directory structure..."
    
    sudo mkdir -p "$INSTALL_DIR"
    sudo chown "$CURRENT_USER:$CURRENT_USER" "$INSTALL_DIR"
    
    mkdir -p "$INSTALL_DIR"/{commands,config,engine,api,web,logs,tests,tools}
    mkdir -p "$INSTALL_DIR/logs"/{actions,decisions,learning,scans}
    
    log "Directory structure created"
}

# Copy project files
copy_project_files() {
    log "Copying project files..."
    
    # Copy current directory contents to install directory
    cp -r . "$INSTALL_DIR/"
    
    # Set correct permissions
    chmod +x "$INSTALL_DIR/commands/"*.py
    chmod +x "$INSTALL_DIR/install.sh"
    
    # Create default config if not exists
    if [[ ! -f "$INSTALL_DIR/config/allowlist.json" ]]; then
        cp "$INSTALL_DIR/config/allowlist.example.json" "$INSTALL_DIR/config/allowlist.json"
    fi
    
    log "Project files copied"
}

# Configure Ollama models
configure_ollama_models() {
    log "Configuring Ollama models..."
    
    # Wait for Ollama to be ready
    for i in {1..30}; do
        if curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
            break
        fi
        sleep 2
    done
    
    # Pull base model if not exists
    if ! ollama list | grep -q "mistral:7b-instruct"; then
        ollama pull mistral:7b-instruct
    fi
    
    # Create copilot_private model
    cd "$INSTALL_DIR"
    if [[ -f "CopilotPrivateAgent.Modelfile" ]]; then
        ollama create copilot_private -f CopilotPrivateAgent.Modelfile
        log "Copilot Private Agent model created"
    fi
    
    log "Ollama models configured"
}

# Setup systemd services
setup_services() {
    log "Setting up systemd services..."
    
    # API Gateway service
    cat <<EOF | sudo tee /etc/systemd/system/copilot-gateway.service
[Unit]
Description=Copilot Private Agent API Gateway
After=network.target ollama.service
Wants=ollama.service

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$INSTALL_DIR
Environment=PATH=$INSTALL_DIR/.venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=$INSTALL_DIR
Environment=COPILOT_CONFIG_DIR=$INSTALL_DIR/config
Environment=COPILOT_LOG_DIR=$INSTALL_DIR/logs
ExecStart=$INSTALL_DIR/.venv/bin/python -m api.server
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    # Learning engine service
    cat <<EOF | sudo tee /etc/systemd/system/copilot-learning.service
[Unit]
Description=Copilot Private Agent Learning Engine
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$INSTALL_DIR
Environment=PATH=$INSTALL_DIR/.venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=$INSTALL_DIR
Environment=COPILOT_CONFIG_DIR=$INSTALL_DIR/config
Environment=COPILOT_LOG_DIR=$INSTALL_DIR/logs
ExecStart=$INSTALL_DIR/.venv/bin/python -m engine.learning
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable copilot-gateway copilot-learning
    
    log "Systemd services configured"
}

# Configure firewall
configure_firewall() {
    log "Configuring firewall..."
    
    # Allow only localhost connections to Ollama
    if command -v ufw >/dev/null 2>&1; then
        sudo ufw --force enable
        sudo ufw deny 11434
        sudo ufw allow from 127.0.0.1 to any port 11434
        sudo ufw allow from ::1 to any port 11434
    elif command -v firewall-cmd >/dev/null 2>&1; then
        sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="127.0.0.1" port protocol="tcp" port="11434" accept'
        sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv6" source address="::1" port protocol="tcp" port="11434" accept'
        sudo firewall-cmd --reload
    fi
    
    log "Firewall configured for security"
}

# Auto-detect network configuration
auto_detect_network() {
    log "Auto-detecting network configuration..."
    
    # Get default interface and network
    DEFAULT_INTERFACE=$(ip route | grep default | awk '{print $5}' | head -n1)
    if [[ -n "$DEFAULT_INTERFACE" ]]; then
        LOCAL_IP=$(ip addr show "$DEFAULT_INTERFACE" | grep 'inet ' | awk '{print $2}' | cut -d/ -f1 | head -n1)
        LOCAL_NETWORK=$(ip route | grep "$DEFAULT_INTERFACE" | grep -E '192\.168\.|10\.|172\.' | awk '{print $1}' | head -n1)
        
        if [[ -n "$LOCAL_NETWORK" ]]; then
            # Update allowlist with detected network
            python3 - <<EOF
import json
import os

config_file = "$INSTALL_DIR/config/allowlist.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        allowlist = json.load(f)
    
    # Add detected network
    if 'allowed_targets' not in allowlist:
        allowlist['allowed_targets'] = {}
    
    allowlist['allowed_targets']['auto_detected_local'] = {
        'cidrs': ['$LOCAL_NETWORK'],
        'auto_detected': True,
        'interface': '$DEFAULT_INTERFACE',
        'detected_ip': '$LOCAL_IP',
        'ports': ['22', '80', '443', '8080'],
        'scan_level': 'moderate'
    }
    
    with open(config_file, 'w') as f:
        json.dump(allowlist, f, indent=2)
    
    print(f"Added auto-detected network: $LOCAL_NETWORK")
EOF
        fi
    fi
    
    log "Network auto-detection completed"
}

# Create command aliases
create_aliases() {
    log "Creating command aliases..."
    
    # Create convenient symlinks
    sudo ln -sf "$INSTALL_DIR/commands/cyber-scan.py" /usr/local/bin/cyber-scan
    sudo ln -sf "$INSTALL_DIR/commands/cyber-recon.py" /usr/local/bin/cyber-recon
    sudo ln -sf "$INSTALL_DIR/commands/cyber-defend.py" /usr/local/bin/cyber-defend
    sudo ln -sf "$INSTALL_DIR/commands/cyber-attack.py" /usr/local/bin/cyber-attack
    sudo ln -sf "$INSTALL_DIR/commands/cyber-intel.py" /usr/local/bin/cyber-intel
    sudo ln -sf "$INSTALL_DIR/commands/cyber-auto.py" /usr/local/bin/cyber-auto
    
    # Add to PATH in profile
    if ! grep -q "$INSTALL_DIR" /home/"$CURRENT_USER"/.bashrc; then
        echo "export PATH=\"\$PATH:$INSTALL_DIR/commands\"" >> /home/"$CURRENT_USER"/.bashrc
        echo "export COPILOT_HOME=\"$INSTALL_DIR\"" >> /home/"$CURRENT_USER"/.bashrc
    fi
    
    log "Command aliases created"
}

# Generate access tokens
generate_tokens() {
    log "Generating secure access tokens..."
    
    # Generate API token
    API_TOKEN=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    echo "COPILOT_API_TOKEN=$API_TOKEN" > "$INSTALL_DIR/.env"
    chmod 600 "$INSTALL_DIR/.env"
    
    # Generate learning encryption key
    LEARNING_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    echo "COPILOT_LEARNING_KEY=$LEARNING_KEY" >> "$INSTALL_DIR/.env"
    
    log "Access tokens generated and saved to $INSTALL_DIR/.env"
    info "API Token: $API_TOKEN"
    warn "Save this token securely - it won't be shown again!"
}

# Post-installation verification
verify_installation() {
    log "Verifying installation..."
    
    # Check Ollama
    if ! curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
        warn "Ollama not responding on localhost:11434"
    fi
    
    # Check Python environment
    if [[ ! -f "$INSTALL_DIR/.venv/bin/python" ]]; then
        warn "Python virtual environment not found"
    fi
    
    # Check commands
    for cmd in cyber-scan cyber-recon cyber-defend cyber-attack cyber-intel cyber-auto; do
        if [[ ! -f "$INSTALL_DIR/commands/$cmd.py" ]]; then
            warn "Command $cmd.py not found"
        fi
    done
    
    # Test basic functionality
    cd "$INSTALL_DIR"
    source .venv/bin/activate
    if python3 -c "from engine.brain import CopilotBrain; brain = CopilotBrain(); print('Brain test OK')" 2>/dev/null; then
        log "Core functionality test passed"
    else
        warn "Core functionality test failed"
    fi
    
    log "Installation verification completed"
}

# Usage instructions
show_usage() {
    cat <<EOF

${GREEN}🎉 Copilot Private Agent Installation Complete! 🎉${NC}

${BLUE}📍 Installation Directory:${NC} $INSTALL_DIR
${BLUE}📝 Log File:${NC} $LOG_FILE
${BLUE}🔐 Configuration:${NC} $INSTALL_DIR/.env

${YELLOW}🚀 Quick Start:${NC}
1. Test Ollama agent:
   ${GREEN}ollama run copilot_private "scan my network"${NC}

2. Use universal commands:
   ${GREEN}cyber-scan 192.168.1.1${NC}
   ${GREEN}cyber-recon google.com${NC}
   ${GREEN}cyber-defend --monitor${NC}

3. Advanced testing (requires Wassim keyword):
   ${GREEN}ollama run copilot_private "Wassim pentest 192.168.1.0/24"${NC}

4. Web dashboard:
   ${GREEN}sudo systemctl start copilot-gateway${NC}
   ${GREEN}curl http://127.0.0.1:8787/status${NC}

${YELLOW}🔧 Management Commands:${NC}
- Start services: ${GREEN}sudo systemctl start copilot-gateway copilot-learning${NC}
- View logs: ${GREEN}tail -f $INSTALL_DIR/logs/actions.log${NC}
- Update config: ${GREEN}nano $INSTALL_DIR/config/allowlist.json${NC}

${YELLOW}📚 Documentation:${NC}
- Main README: ${GREEN}$INSTALL_DIR/README.md${NC}
- Command help: ${GREEN}cyber-scan --help${NC}
- Web interface: ${GREEN}http://127.0.0.1:8787/dashboard${NC}

${RED}⚠️  Security Notes:${NC}
- All services bound to localhost only
- Invasive actions require "Wassim" keyword
- Review allowlist.json before testing
- API token saved in $INSTALL_DIR/.env

EOF
}

# Main installation function
main() {
    log "Starting Copilot Private Agent installation..."
    
    check_root
    detect_os
    
    create_directories
    copy_project_files
    
    install_system_deps
    install_go_tools
    install_ollama
    
    setup_python_env
    configure_ollama_models
    
    auto_detect_network
    configure_firewall
    
    setup_services
    create_aliases
    generate_tokens
    
    verify_installation
    show_usage
    
    log "Installation completed successfully!"
}

# Run main function
main "$@"