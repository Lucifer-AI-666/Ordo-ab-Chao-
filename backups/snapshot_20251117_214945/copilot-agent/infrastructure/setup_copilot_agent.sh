#!/bin/bash
# CopilotPrivateAgent Setup Script
# DibTauroS/Ordo-ab-Chao cybersecurity framework
# Owner: Dib Anouar
# License: LUP v1.0 (personal and non-commercial use only)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emoji fallbacks for systems without Unicode support
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$LANG" == *"UTF-8"* ]]; then
    ROCKET="🚀"
    CHECK="✅"
    CROSS="❌"
    WARNING="⚠️"
    INFO="ℹ️"
    LOCK="🔒"
    GEAR="⚙️"
    BOOK="📖"
else
    ROCKET="[>]"
    CHECK="[+]"
    CROSS="[-]"
    WARNING="[!]"
    INFO="[i]"
    LOCK="[S]"
    GEAR="[C]"
    BOOK="[D]"
fi

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COPILOT_DIR="$PROJECT_ROOT"

print_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    CopilotPrivateAgent                       ║"
    echo "║                  DibTauroS • Ordo ab Chao                   ║"
    echo "║                                                              ║"
    echo "║  Owner: Dib Anouar                                           ║"
    echo "║  License: LUP v1.0 (personal and non-commercial use only)   ║"
    echo "║  Privacy-first cybersecurity framework                      ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        "info")
            echo -e "${BLUE}${INFO} ${timestamp} - $message${NC}"
            ;;
        "success")
            echo -e "${GREEN}${CHECK} ${timestamp} - $message${NC}"
            ;;
        "warning")
            echo -e "${YELLOW}${WARNING} ${timestamp} - $message${NC}"
            ;;
        "error")
            echo -e "${RED}${CROSS} ${timestamp} - $message${NC}"
            ;;
        "security")
            echo -e "${PURPLE}${LOCK} ${timestamp} - $message${NC}"
            ;;
    esac
}

check_requirements() {
    log "info" "Checking system requirements..."
    
    local missing_deps=()
    
    # Check for required commands
    local required_commands=("python3" "docker" "docker-compose" "curl" "git")
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log "error" "Missing required dependencies: ${missing_deps[*]}"
        log "info" "Please install the missing dependencies and run this script again"
        exit 1
    fi
    
    # Check Python version
    local python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    local required_version="3.8"
    
    if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
        log "error" "Python 3.8+ required, found Python $python_version"
        exit 1
    fi
    
    log "success" "All requirements satisfied"
}

setup_directories() {
    log "info" "Setting up directory structure..."
    
    # Create required directories
    local dirs=(
        "$COPILOT_DIR/config"
        "$COPILOT_DIR/logs"
        "$COPILOT_DIR/branding"
        "$COPILOT_DIR/docs"
    )
    
    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log "success" "Created directory: $dir"
        fi
    done
}

setup_configuration() {
    log "info" "Setting up configuration files..."
    
    # Create .env.copilot if it doesn't exist
    local env_file="$COPILOT_DIR/config/.env.copilot"
    if [ ! -f "$env_file" ]; then
        cat > "$env_file" << 'EOF'
# CopilotPrivateAgent Environment Configuration
# DibTauroS/Ordo-ab-Chao framework

# Security Settings
MONICA_DISABLE=0
COPILOT_MODE=DEFEND

# Network Configuration
COPILOT_HOST=127.0.0.1
COPILOT_PORT=8787

# Logging Configuration
LOG_LEVEL=INFO
LOG_RETENTION_DAYS=30

# Ollama Configuration
OLLAMA_HOST=127.0.0.1
OLLAMA_PORT=11434
OLLAMA_MODEL=mistral:7b-instruct

# Security Keys (auto-generated)
COPILOT_SECRET_KEY=$(openssl rand -hex 32)
COPILOT_API_TOKEN=$(openssl rand -hex 24)

# Owner Information
COPILOT_OWNER="Dib Anouar"
COPILOT_LICENSE="LUP v1.0"
COPILOT_FRAMEWORK="DibTauroS/Ordo-ab-Chao"
EOF
        log "success" "Created environment configuration: $env_file"
    fi
    
    # Create allowlist.json if it doesn't exist
    local allowlist_file="$COPILOT_DIR/config/allowlist.json"
    if [ ! -f "$allowlist_file" ]; then
        cat > "$allowlist_file" << 'EOF'
{
  "allowed_targets": [
    "localhost",
    "127.0.0.1",
    "::1",
    "192.168.1.0/24",
    "10.0.0.0/8",
    "172.16.0.0/12"
  ],
  "blocked_targets": [
    "0.0.0.0/0",
    "::/0"
  ],
  "last_updated": "2024-01-01T00:00:00Z",
  "_comment": "Modify this file to customize allowed targets for security operations"
}
EOF
        log "success" "Created allowlist configuration: $allowlist_file"
    fi
    
    # Create modes.json if it doesn't exist
    local modes_file="$COPILOT_DIR/config/modes.json"
    if [ ! -f "$modes_file" ]; then
        cat > "$modes_file" << 'EOF'
{
  "DEFEND": {
    "description": "Defensive operations only - monitoring and analysis",
    "allowed_actions": [
      "scan",
      "monitor", 
      "analyze",
      "report",
      "log_review"
    ],
    "requires_authorization": false,
    "max_intensity": "low",
    "allowed_tools": [
      "ps",
      "netstat",
      "ss",
      "df",
      "uptime",
      "who"
    ]
  },
  "TEST": {
    "description": "Advanced testing operations - requires Wassim keyword",
    "allowed_actions": [
      "scan",
      "monitor",
      "analyze", 
      "report",
      "install",
      "firewall",
      "suid_check",
      "network_scan",
      "vulnerability_scan"
    ],
    "requires_authorization": true,
    "authorization_keyword": "Wassim",
    "max_intensity": "high",
    "allowed_tools": [
      "nmap",
      "ncat",
      "curl",
      "wget",
      "dig",
      "ping",
      "traceroute"
    ],
    "restrictions": {
      "target_must_be_in_allowlist": true,
      "requires_explicit_confirmation": true,
      "audit_log_required": true
    }
  }
}
EOF
        log "success" "Created modes configuration: $modes_file"
    fi
}

setup_branding() {
    log "info" "Setting up DibTauroS branding..."
    
    # Create splash.txt
    local splash_file="$COPILOT_DIR/branding/splash.txt"
    cat > "$splash_file" << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██████╗ ██████╗ ██████╗ ██╗██╗      ██████╗ ████████╗                      ║
║ ██╔════╝██╔═══██╗██╔══██╗██║██║     ██╔═══██╗╚══██╔══╝                      ║
║ ██║     ██║   ██║██████╔╝██║██║     ██║   ██║   ██║                         ║
║ ██║     ██║   ██║██╔═══╝ ██║██║     ██║   ██║   ██║                         ║
║ ╚██████╗╚██████╔╝██║     ██║███████╗╚██████╔╝   ██║                         ║
║  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝    ╚═╝                         ║
║                                                                              ║
║                    Private Agent • DibTauroS Framework                      ║
║                              Ordo ab Chao                                   ║
║                                                                              ║
║  ╔══════════════════════════════════════════════════════════════════════╗   ║
║  ║  🔒 PRIVACY-FIRST CYBERSECURITY FRAMEWORK                           ║   ║
║  ║  🛡️  Owner: Dib Anouar                                              ║   ║
║  ║  📜 License: LUP v1.0 (Personal & Non-Commercial Use Only)         ║   ║
║  ║  🎯 Purpose: Ethical cybersecurity operations & OSINT              ║   ║
║  ║  ⚖️  Compliance: Local operations only, no external data sharing   ║   ║
║  ╚══════════════════════════════════════════════════════════════════════╝   ║
║                                                                              ║
║  Modes: DEFEND (default) | TEST (requires "Wassim" keyword)                 ║
║  Security: Allowlist-based targets, audit logging, privilege controls       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
    log "success" "Created splash banner: $splash_file"
    
    # Create html_banner.html
    local html_banner="$COPILOT_DIR/branding/html_banner.html"
    cat > "$html_banner" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CopilotPrivateAgent - DibTauroS Framework</title>
    <style>
        .copilot-banner {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
            color: #00ff41;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            padding: 20px;
            border: 2px solid #00ff41;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }
        
        .banner-title {
            font-size: 2.5em;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.8);
            margin-bottom: 10px;
        }
        
        .banner-subtitle {
            font-size: 1.2em;
            color: #888;
            margin-bottom: 20px;
        }
        
        .banner-info {
            background: rgba(0, 255, 65, 0.1);
            border: 1px solid #00ff41;
            border-radius: 4px;
            padding: 15px;
            margin: 15px 0;
            text-align: left;
        }
        
        .banner-info h3 {
            color: #00ff41;
            margin-top: 0;
        }
        
        .security-notice {
            background: rgba(255, 68, 68, 0.1);
            border: 1px solid #ff4444;
            color: #ff4444;
            padding: 10px;
            border-radius: 4px;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="copilot-banner">
        <div class="banner-title">COPILOT</div>
        <div class="banner-subtitle">Private Agent • DibTauroS Framework • Ordo ab Chao</div>
        
        <div class="banner-info">
            <h3>🔒 Privacy-First Cybersecurity Framework</h3>
            <p><strong>Owner:</strong> Dib Anouar</p>
            <p><strong>License:</strong> LUP v1.0 (Personal & Non-Commercial Use Only)</p>
            <p><strong>Purpose:</strong> Ethical cybersecurity operations & OSINT</p>
            <p><strong>Compliance:</strong> Local operations only, no external data sharing</p>
        </div>
        
        <div class="banner-info">
            <h3>⚙️ Operational Modes</h3>
            <p><strong>DEFEND:</strong> Standard defensive operations (always available)</p>
            <p><strong>TEST:</strong> Advanced testing operations (requires "Wassim" keyword)</p>
        </div>
        
        <div class="banner-info">
            <h3>🛡️ Security Controls</h3>
            <p>• Allowlist-based target validation</p>
            <p>• Comprehensive audit logging with SHA-256 integrity chain</p>
            <p>• Privilege-based operation controls</p>
            <p>• Dry-run mode for safe testing</p>
        </div>
        
        <div class="security-notice">
            <strong>⚠️ SECURITY NOTICE:</strong> This system is for authorized use only. 
            All operations are logged and monitored. Unauthorized access is prohibited.
        </div>
    </div>
</body>
</html>
EOF
    log "success" "Created HTML banner: $html_banner"
    
    # Create telegram_intro.txt
    local telegram_intro="$COPILOT_DIR/branding/telegram_intro.txt"
    cat > "$telegram_intro" << 'EOF'
🤖 **CopilotPrivateAgent Bot**
🛡️ *DibTauroS Cybersecurity Framework*

**Ordo ab Chao** - From Chaos, Order

━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔒 **Privacy-First Framework**
👤 Owner: Dib Anouar
📜 License: LUP v1.0 (Personal Use Only)
🎯 Purpose: Ethical Cybersecurity & OSINT

━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️ **Available Commands:**

🛡️ `/defend <target>` - Defensive operations
🧪 `/test <target> Wassim <command>` - Advanced testing
📊 `/status` - Agent status check
📋 `/allowlist` - View allowed targets
🔍 `/scan <target>` - Basic reconnaissance
📝 `/logs` - Recent operation logs

━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔐 **Security Features:**
• Allowlist-based target validation
• Audit logging with integrity chain
• Two-tier operational modes
• Local-only operations (no external data sharing)

⚠️ **Important:** All operations are logged and monitored. Use responsibly and ethically.

Type `/help` for detailed command information.
EOF
    log "success" "Created Telegram intro: $telegram_intro"
}

setup_documentation() {
    log "info" "Creating documentation..."
    
    # Create README_DIBTAUROS.md
    local readme_file="$COPILOT_DIR/branding/README_DIBTAUROS.md"
    cat > "$readme_file" << 'EOF'
# DibTauroS CopilotPrivateAgent Manifesto

## 🛡️ Vision: Ordo ab Chao

**"From Chaos, Order"** - The DibTauroS framework embodies the principle of bringing structure and security to the chaotic landscape of cybersecurity. Our CopilotPrivateAgent represents a new paradigm in privacy-first, ethical cybersecurity operations.

## 🎯 Mission Statement

To provide a comprehensive, privacy-respecting cybersecurity framework that empowers security professionals while maintaining the highest standards of ethical conduct and legal compliance.

## 🔐 Core Principles

### 1. Privacy by Design
- **Local Operations Only**: All data processing occurs locally
- **No External Dependencies**: No cloud services or external data sharing
- **User-Controlled**: Complete user control over all operations and data

### 2. Ethical Framework
- **Responsible Disclosure**: Built-in protections against misuse
- **Allowlist-Based Operations**: Explicit authorization required for all targets
- **Audit Trail**: Comprehensive logging with cryptographic integrity

### 3. Security-First Architecture
- **Multi-Tier Authorization**: DEFEND and TEST modes with different privilege levels
- **Fail-Safe Defaults**: Secure by default configuration
- **Principle of Least Privilege**: Minimal permissions for maximum security

## 🏗️ Framework Architecture

### Operational Modes

#### DEFEND Mode (Default)
- **Purpose**: Defensive cybersecurity operations
- **Authorization**: Always available
- **Capabilities**: Monitoring, analysis, reporting
- **Use Cases**: 
  - System health monitoring
  - Log analysis
  - Threat detection
  - Compliance reporting

#### TEST Mode (Gated)
- **Purpose**: Advanced testing and penetration testing
- **Authorization**: Requires "Wassim" keyword + allowlist approval
- **Capabilities**: Active scanning, vulnerability assessment
- **Use Cases**:
  - Penetration testing (authorized targets only)
  - Vulnerability scanning
  - Security assessment
  - Infrastructure testing

### Security Controls

#### Target Validation
- **Allowlist Enforcement**: Only approved targets can be scanned
- **IP Range Support**: CIDR notation for network ranges
- **Dynamic Updates**: Real-time allowlist modifications
- **Audit Logging**: All target access attempts logged

#### Operation Logging
- **SHA-256 Integrity Chain**: Cryptographic proof of log integrity
- **Immutable Records**: Append-only logging system
- **Comprehensive Coverage**: All operations logged with context
- **Retention Policies**: Configurable log retention periods

#### Privilege Management
- **Role-Based Access**: Different capabilities based on operational mode
- **Keyword Authentication**: Advanced operations require specific authorization
- **Session Management**: Secure session handling with timeouts
- **Emergency Shutdown**: MONICA_DISABLE kill-switch for immediate halt

## 🛠️ Technical Implementation

### Core Technologies
- **Python 3.8+**: Main application framework
- **FastAPI**: Web interface and API endpoints
- **Docker**: Containerized deployment
- **Ollama**: Local AI model integration
- **SQLite**: Local data storage

### Security Technologies
- **bcrypt**: Password hashing
- **python-jose**: JWT token management
- **cryptography**: Advanced cryptographic operations
- **scapy**: Network packet analysis

### Deployment Options
- **Docker Compose**: Full-stack deployment
- **Standalone Python**: Direct execution
- **Kubernetes**: Enterprise-scale deployment (optional)

## 📚 Usage Philosophy

### Ethical Guidelines

1. **Authorized Use Only**: Only scan and test systems you own or have explicit permission to test
2. **Responsible Disclosure**: Report vulnerabilities through appropriate channels
3. **Legal Compliance**: Ensure all operations comply with local laws and regulations
4. **Professional Conduct**: Use the framework only for legitimate cybersecurity purposes

### Best Practices

1. **Start with DEFEND Mode**: Begin all assessments in defensive mode
2. **Verify Allowlists**: Ensure target lists are current and authorized
3. **Review Logs Regularly**: Monitor operation logs for anomalies
4. **Keep Documentation**: Maintain records of all security assessments
5. **Update Regularly**: Keep the framework and its components updated

## 🔄 Continuous Improvement

### Development Roadmap
- Enhanced AI integration for threat analysis
- Extended protocol support for network operations
- Advanced reporting and visualization
- Integration with popular security tools
- Community-driven plugin architecture

### Feedback and Contributions
While this is a private framework for Dib Anouar's exclusive use, the principles and methodologies can inspire similar privacy-first approaches in the broader cybersecurity community.

## 📜 Legal and Compliance

### License Terms
- **LUP v1.0**: Limited Use Personal License
- **Personal Use Only**: Not for commercial distribution
- **No Warranty**: Provided as-is without guarantees
- **User Responsibility**: Users are responsible for legal compliance

### Privacy Commitment
- **No Telemetry**: No usage data collection
- **No External Connections**: No unauthorized network communications
- **Local Storage**: All data remains on user's systems
- **Open Audit**: Code available for security review

## 🎖️ Attribution

**Created by**: Dib Anouar  
**Framework**: DibTauroS  
**Project**: Ordo-ab-Chao  
**License**: LUP v1.0  
**Year**: 2024  

---

*"In the pursuit of cybersecurity excellence, we must never compromise on privacy, ethics, or user empowerment. The DibTauroS CopilotPrivateAgent represents these values in action."*

**- Dib Anouar, Creator of DibTauroS Framework**
EOF
    log "success" "Created DibTauroS manifesto: $readme_file"
    
    # Create INSTALLATION.md
    local install_doc="$COPILOT_DIR/docs/INSTALLATION.md"
    cat > "$install_doc" << 'EOF'
# CopilotPrivateAgent Installation Guide

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Python**: 3.8 or higher
- **Docker**: 20.10 or higher
- **Docker Compose**: 1.29 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: Minimum 2GB free space

### Required Software
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip docker.io docker-compose curl git

# macOS (using Homebrew)
brew install python3 docker docker-compose curl git

# Arch Linux
sudo pacman -S python docker docker-compose curl git
```

## Installation Methods

### Method 1: Automated Setup (Recommended)

1. **Clone the repository** (if not already available):
   ```bash
   git clone <repository-url>
   cd Ordo-ab-Chao-/copilot-agent
   ```

2. **Run the setup script**:
   ```bash
   chmod +x infrastructure/setup_copilot_agent.sh
   ./infrastructure/setup_copilot_agent.sh
   ```

3. **Follow the interactive prompts** to configure your installation.

### Method 2: Docker Compose Deployment

1. **Prepare the environment**:
   ```bash
   cd copilot-agent
   cp config/.env.copilot.example config/.env.copilot
   # Edit .env.copilot with your settings
   ```

2. **Start the services**:
   ```bash
   docker-compose -f infrastructure/docker-compose.yml up -d
   ```

3. **Verify the installation**:
   ```bash
   docker-compose -f infrastructure/docker-compose.yml ps
   ```

### Method 3: Python Virtual Environment

1. **Create a virtual environment**:
   ```bash
   python3 -m venv copilot-venv
   source copilot-venv/bin/activate  # On Windows: copilot-venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r infrastructure/requirements.txt
   ```

3. **Set up configuration**:
   ```bash
   mkdir -p config logs
   cp config/.env.copilot.example config/.env.copilot
   # Edit configuration files as needed
   ```

4. **Run the agent**:
   ```bash
   python3 core/copilot_agent.py --status
   ```

## Configuration

### Environment Variables
Edit `config/.env.copilot` to customize your installation:

```bash
# Security Settings
MONICA_DISABLE=0                    # Emergency kill switch (0=enabled, 1=disabled)
COPILOT_MODE=DEFEND                 # Default operational mode

# Network Configuration
COPILOT_HOST=127.0.0.1             # Bind to localhost only
COPILOT_PORT=8787                   # Web interface port

# Logging
LOG_LEVEL=INFO                      # Logging verbosity
LOG_RETENTION_DAYS=30               # Log retention period

# Ollama Integration
OLLAMA_HOST=127.0.0.1              # Ollama service host
OLLAMA_PORT=11434                   # Ollama service port
OLLAMA_MODEL=mistral:7b-instruct    # AI model to use
```

### Target Allowlist
Edit `config/allowlist.json` to define authorized targets:

```json
{
  "allowed_targets": [
    "localhost",
    "127.0.0.1",
    "192.168.1.0/24",
    "10.0.0.0/8"
  ],
  "blocked_targets": [
    "0.0.0.0/0"
  ]
}
```

### Operational Modes
Review and customize `config/modes.json` for operational settings:

```json
{
  "DEFEND": {
    "description": "Defensive operations only",
    "allowed_actions": ["scan", "monitor", "analyze", "report"],
    "requires_authorization": false
  },
  "TEST": {
    "description": "Advanced testing operations",
    "requires_authorization": true,
    "authorization_keyword": "Wassim"
  }
}
```

## Verification

### Basic Functionality Test
```bash
# Test the Python agent
python3 core/copilot_agent.py --status

# Test with a simple operation
python3 core/copilot_agent.py --prompt "system status check" --target localhost
```

### Docker Health Check
```bash
# Check container health
docker-compose -f infrastructure/docker-compose.yml ps

# View logs
docker-compose -f infrastructure/docker-compose.yml logs copilot-agent
```

### Web Interface Test
1. Open your browser to `http://127.0.0.1:8787`
2. Verify the interface loads correctly
3. Test a simple operation in DEFEND mode

## Ollama Setup (Optional)

### Install Ollama
```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Or use Docker (included in docker-compose.yml)
docker-compose -f infrastructure/docker-compose.yml up ollama -d
```

### Load the CopilotPrivateAgent Model
```bash
# Copy the Modelfile
cp core/CopilotPrivateAgent.Modelfile /tmp/

# Create the model
ollama create copilot-private -f /tmp/CopilotPrivateAgent.Modelfile

# Test the model
ollama run copilot-private "What are your operational modes?"
```

## Troubleshooting

### Common Issues

#### Permission Errors
```bash
# Fix Docker permissions (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Fix file permissions
sudo chown -R $USER:$USER logs/ config/
```

#### Port Conflicts
```bash
# Check what's using the port
sudo netstat -tulpn | grep :8787

# Change the port in .env.copilot
COPILOT_PORT=8788
```

#### Python Dependencies
```bash
# Update pip and reinstall dependencies
pip install --upgrade pip
pip install -r infrastructure/requirements.txt --force-reinstall
```

### Log Files
Check these locations for troubleshooting information:
- `logs/copilot_agent.log` - Main application log
- `logs/audit_chain.json` - Security audit trail
- Docker logs: `docker-compose logs copilot-agent`

### Performance Tuning

#### Resource Limits
Adjust Docker resource limits in `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 1G        # Increase if needed
      cpus: '1.0'       # Adjust based on your system
```

#### Log Rotation
Configure log rotation to prevent disk space issues:
```bash
# Add to crontab
0 0 * * * find /path/to/logs -name "*.log" -mtime +30 -delete
```

## Security Considerations

### Firewall Configuration
```bash
# Allow only local connections
sudo ufw allow from 127.0.0.1 to any port 8787
sudo ufw deny 8787
```

### File Permissions
```bash
# Secure configuration files
chmod 600 config/.env.copilot
chmod 644 config/allowlist.json
chmod 755 logs/
```

### Regular Updates
```bash
# Update the framework regularly
git pull origin main
docker-compose -f infrastructure/docker-compose.yml pull
docker-compose -f infrastructure/docker-compose.yml up -d
```

## Support

### Documentation
- Framework documentation: `docs/`
- API reference: `http://127.0.0.1:8787/docs` (when running)
- Branding guidelines: `branding/README_DIBTAUROS.md`

### Logging and Monitoring
- Enable debug logging: Set `LOG_LEVEL=DEBUG` in `.env.copilot`
- Monitor audit chain: Check `logs/audit_chain.json` regularly
- Health checks: Use `python3 core/copilot_agent.py --status`

---

**Note**: This framework is designed for personal use by Dib Anouar under the LUP v1.0 license. Ensure compliance with all applicable laws and regulations in your jurisdiction.
EOF
    log "success" "Created installation documentation: $install_doc"
}

setup_ollama_model() {
    log "info" "Setting up Ollama model..."
    
    # Check if Ollama is available
    if command -v ollama &> /dev/null; then
        log "info" "Ollama found, creating CopilotPrivateAgent model..."
        
        # Create the model
        ollama create copilot-private -f "$COPILOT_DIR/core/CopilotPrivateAgent.Modelfile" 2>/dev/null || {
            log "warning" "Could not create Ollama model (this is optional)"
        }
    else
        log "info" "Ollama not found, skipping model creation (optional component)"
    fi
}

setup_python_environment() {
    log "info" "Setting up Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "$COPILOT_DIR/venv" ]; then
        python3 -m venv "$COPILOT_DIR/venv"
        log "success" "Created Python virtual environment"
    fi
    
    # Activate virtual environment and install dependencies
    source "$COPILOT_DIR/venv/bin/activate"
    pip install --upgrade pip
    pip install -r "$COPILOT_DIR/infrastructure/requirements.txt"
    
    log "success" "Python dependencies installed"
}

run_tests() {
    log "info" "Running verification tests..."
    
    # Test Python agent
    if python3 "$COPILOT_DIR/core/copilot_agent.py" --status &>/dev/null; then
        log "success" "Python agent test passed"
    else
        log "warning" "Python agent test failed (check dependencies)"
    fi
    
    # Test configuration loading
    if [ -f "$COPILOT_DIR/config/allowlist.json" ] && [ -f "$COPILOT_DIR/config/modes.json" ]; then
        log "success" "Configuration files test passed"
    else
        log "error" "Configuration files test failed"
    fi
}

print_success_message() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    SETUP COMPLETED!                         ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    log "success" "CopilotPrivateAgent setup completed successfully!"
    echo
    log "info" "${BOOK} Next steps:"
    echo "  1. Review configuration files in config/"
    echo "  2. Customize allowlist.json for your environment"
    echo "  3. Start the agent with Docker Compose or Python"
    echo
    log "info" "${GEAR} Quick start commands:"
    echo "  # Docker deployment:"
    echo "  docker-compose -f infrastructure/docker-compose.yml up -d"
    echo
    echo "  # Python virtual environment:"
    echo "  source venv/bin/activate"
    echo "  python3 core/copilot_agent.py --status"
    echo
    echo "  # Web interface:"
    echo "  Open http://127.0.0.1:8787 in your browser"
    echo
    log "security" "${LOCK} Security reminders:"
    echo "  - All services bind to 127.0.0.1 (localhost only)"
    echo "  - TEST mode requires 'Wassim' keyword + target allowlist"
    echo "  - Check logs/ directory for audit trail"
    echo "  - Set MONICA_DISABLE=1 to emergency-stop all operations"
    echo
    log "info" "${BOOK} Documentation available in docs/ directory"
}

# Main execution
main() {
    print_banner
    
    log "info" "Starting CopilotPrivateAgent setup..."
    log "info" "Framework: DibTauroS/Ordo-ab-Chao"
    log "info" "Owner: Dib Anouar"
    log "security" "License: LUP v1.0 (personal and non-commercial use only)"
    
    check_requirements
    setup_directories
    setup_configuration
    setup_branding
    setup_documentation
    setup_python_environment
    setup_ollama_model
    run_tests
    
    print_success_message
}

# Run main function
main "$@"