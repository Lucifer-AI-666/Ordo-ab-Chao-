# 🛡️ Copilot Private Agent - Universal Cybersecurity System

A comprehensive, privacy-first cybersecurity ecosystem built around the existing Copilot Private Agent. This system provides advanced scanning, reconnaissance, defense, penetration testing, threat intelligence, and automation capabilities with strict security controls and intelligent decision-making.

## 🚀 Features

### 🧠 Intelligent Core Engine
- **Smart Decision Making**: AI-powered command analysis and risk assessment
- **Auto-Detection**: Automatically detects target types and recommends appropriate actions
- **Wassim-Gated Security**: Advanced operations require authorization keyword
- **Adaptive Profiles**: DEFEND, TEST, STEALTH, AGGRESSIVE, and LEARNING modes

### 🔍 Universal Scanning (`cyber-scan.py`)
- **Auto-Detection**: Automatically identifies target type and selects appropriate scans
- **Escalation Logic**: Progressively escalates from passive to active scanning
- **Multi-Tool Integration**: Nmap, Masscan, Nuclei integration
- **Intelligent Reporting**: Generates detailed markdown and JSON reports

### 🕵️ Advanced Reconnaissance (`cyber-recon.py`)
- **OSINT Capabilities**: Passive information gathering
- **DNS Analysis**: Comprehensive DNS enumeration
- **Subdomain Discovery**: Multi-tool subdomain enumeration
- **Web Technology Detection**: Framework and technology identification
- **Social Media Intelligence**: Basic social profile detection

### 🛡️ Cyber Defense (`cyber-defend.py`)
- **Real-time Monitoring**: System health and security monitoring
- **Security Auditing**: Comprehensive system security assessment
- **Incident Detection**: Automated threat detection and alerting
- **Hardening Recommendations**: Network and system hardening guidance
- **Log Analysis**: Security event correlation and analysis

### ⚔️ Penetration Testing (`cyber-attack.py`)
- **Wassim-Gated Access**: Requires explicit authorization for all operations
- **Vulnerability Exploitation**: Controlled vulnerability testing (simulation mode)
- **Privilege Escalation**: Automated privilege escalation testing
- **Persistence Testing**: Backdoor and persistence mechanism testing
- **Lateral Movement**: Network lateral movement simulation

### 🎯 Threat Intelligence (`cyber-intel.py`)
- **IOC Analysis**: Indicators of Compromise analysis and reputation checking
- **Threat Feed Monitoring**: Multiple threat intelligence feed integration
- **Attribution Analysis**: Threat actor attribution and campaign tracking
- **Reputation Scoring**: Automated threat reputation assessment

### 🤖 Automation & Orchestration (`cyber-auto.py`)
- **Workflow Creation**: Visual workflow builder for security operations
- **Incident Response**: Automated incident response workflows
- **Scheduled Operations**: Automated recurring security tasks
- **Smart Escalation**: Intelligent escalation based on findings

### 🌐 Web Dashboard & API
- **REST API**: Complete API for all cybersecurity operations
- **Web Dashboard**: Real-time monitoring and control interface
- **Token-Based Security**: Secure API access with bearer tokens
- **Real-time Updates**: Live status monitoring and alerting

## 📁 Project Structure

```
priv-cyber-agents-private/
├── CopilotPrivateAgent.Modelfile    # Original Ollama model
├── install.sh                       # One-click installation script
├── commands/                        # Universal cyber commands
│   ├── cyber-scan.py               # Universal scanner
│   ├── cyber-recon.py              # Advanced reconnaissance
│   ├── cyber-defend.py             # Defense and monitoring
│   ├── cyber-attack.py             # Penetration testing
│   ├── cyber-intel.py              # Threat intelligence
│   └── cyber-auto.py               # Automation engine
├── config/                         # Intelligent configuration
│   ├── allowlist.example.json     # Target allowlist template
│   ├── privileges.json            # Granular permissions
│   ├── profiles.json              # Operational profiles
│   └── tools.json                 # External tool configs
├── engine/                         # Core intelligence
│   ├── brain.py                   # Decision making engine
│   ├── learning.py                # Machine learning (future)
│   ├── prediction.py              # Threat prediction (future)
│   └── automation.py              # Auto-response (future)
├── api/                           # REST API server
│   ├── server.py                  # FastAPI server
│   ├── webhooks.py                # Webhook handlers (future)
│   └── plugins.py                 # Plugin system (future)
├── web/                           # Web dashboard
│   ├── dashboard.html             # Main dashboard (integrated in API)
│   ├── monitor.html               # Real-time monitoring (future)
│   └── reports.html               # Report generation (future)
├── logs/                          # Advanced logging
│   ├── actions.log                # Action logs
│   ├── decisions.log              # AI decision logs
│   └── learning.log               # Learning evolution logs
└── tests/                         # Test suite
    └── basic_test.py              # Basic functionality tests
```

## 🔧 Installation

### One-Click Installation
```bash
curl -sSL https://raw.githubusercontent.com/Lucifer-AI-666/priv-cyber-agents-private/main/install.sh | bash
```

### Manual Installation
```bash
git clone https://github.com/Lucifer-AI-666/priv-cyber-agents-private.git
cd priv-cyber-agents-private
chmod +x install.sh
./install.sh
```

### What the installer does:
- ✅ Auto-detects OS (Linux/macOS)
- ✅ Installs system dependencies (nmap, masscan, nuclei, etc.)
- ✅ Sets up Python virtual environment
- ✅ Configures Ollama with security hardening
- ✅ Creates systemd services for automation
- ✅ Auto-detects local network and updates allowlist
- ✅ Generates secure API tokens
- ✅ Sets up firewall rules for security

## 🎯 Quick Start

### 1. Test System Status
```bash
# Check if everything is working
python3 tests/basic_test.py

# Test Ollama agent
ollama run copilot_private "scan my network"
```

### 2. Basic Operations
```bash
# Network scanning
cyber-scan 192.168.1.1
cyber-scan 192.168.1.0/24 --intensity aggressive

# Reconnaissance
cyber-recon google.com --type dns_lookup
cyber-recon example.com --intensity passive

# System defense
cyber-defend monitor
cyber-defend audit --output security_audit.md

# Threat intelligence
cyber-intel ioc_analysis 8.8.8.8
cyber-intel threat_feeds
```

### 3. Advanced Operations (Wassim-gated)
```bash
# Penetration testing (requires Wassim keyword)
cyber-attack 192.168.1.100 --wassim "Wassim authorized pentest" --type comprehensive

# Advanced scanning
ollama run copilot_private "Wassim perform aggressive scan on 192.168.1.0/24"
```

### 4. Web Dashboard
```bash
# Start API server
sudo systemctl start copilot-gateway

# Access dashboard
open http://127.0.0.1:8787/dashboard
```

## 🔐 Security Features

### Privacy-by-Default
- **Localhost Only**: All services bound to 127.0.0.1 by default
- **No Data Exfiltration**: No data sent to external services without explicit consent
- **Encrypted Logs**: All sensitive logs encrypted with user keys
- **Token-Based Access**: Secure API access with rotating tokens

### Access Control
- **Wassim-Gated Operations**: Invasive actions require authorization keyword
- **Granular Permissions**: Role-based access control (RBAC)
- **Target Allowlisting**: Only approved targets can be tested
- **Time-Based Restrictions**: Operations can be limited to business hours

### Audit & Compliance
- **Complete Audit Trail**: Every action logged with integrity protection
- **GDPR Compliance**: Privacy-compliant data processing
- **Evidence Chain**: Cryptographic evidence chain for legal purposes
- **Incident Response**: Automated incident detection and response

## 🎮 Usage Examples

### Comprehensive Network Assessment
```bash
# Automated workflow
cyber-auto create_workflow --workflow-file comprehensive_scan.json
cyber-auto execute_workflow wf_20240815_123456

# Manual step-by-step
cyber-scan 192.168.1.0/24 --type host_discovery
cyber-scan 192.168.1.100 --type port_scan --intensity aggressive
cyber-recon 192.168.1.100 --type service_enumeration
cyber-defend detect --target 192.168.1.100
```

### Threat Hunting Workflow
```bash
# IOC analysis
cyber-intel ioc_analysis 192.168.1.100
cyber-intel threat_feeds --format json

# Defensive monitoring
cyber-defend monitor --continuous
cyber-defend analyze_logs /var/log/auth.log
```

### Incident Response Automation
```bash
# Automated incident response
cyber-auto incident_response malware_detected --severity high

# Manual incident response
cyber-defend detect
cyber-scan localhost --type vulnerability_scan
cyber-intel threat_feeds --format json
```

## 🔄 Operational Profiles

### DEFEND (Default)
- **Purpose**: Defensive security posture
- **Actions**: Monitor, harden, analyze, report
- **Risk Level**: Low
- **Auto-Response**: Enabled

### TEST (Wassim-gated)
- **Purpose**: Controlled testing environment
- **Actions**: Scan, enumerate, test, exploit
- **Risk Level**: Medium to High
- **Requirement**: Wassim keyword + allowlist

### STEALTH
- **Purpose**: Undetectable operations
- **Actions**: Passive scanning, OSINT
- **Risk Level**: Low
- **Features**: Random delays, evasion techniques

### AGGRESSIVE
- **Purpose**: Fast, intensive operations
- **Actions**: High-speed scanning, full enumeration
- **Risk Level**: High
- **Features**: Parallel execution, comprehensive coverage

### LEARNING
- **Purpose**: Safe training environment
- **Actions**: Simulation, training, analysis
- **Risk Level**: Minimal
- **Features**: Dry-run mode, sandbox execution

## 🛠️ API Reference

### Authentication
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:8787/status
```

### Scanning Operations
```bash
# Network scan
curl -X POST http://127.0.0.1:8787/scan \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target": "192.168.1.1", "scan_type": "auto", "intensity": "moderate"}'
```

### Reconnaissance
```bash
# Domain reconnaissance
curl -X POST http://127.0.0.1:8787/recon \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "recon_type": "auto"}'
```

### Defense Operations
```bash
# System monitoring
curl -X POST http://127.0.0.1:8787/defend \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "monitor"}'
```

## 📊 Monitoring & Logging

### Log Types
- **Actions Log**: All user actions and system operations
- **Decisions Log**: AI decision-making process and rationale
- **Learning Log**: System learning and adaptation
- **Security Log**: Security events and incidents
- **API Log**: All API requests and responses

### Monitoring Capabilities
- **Real-time System Health**: CPU, memory, network monitoring
- **Security Event Detection**: Anomaly detection and alerting
- **Threat Intelligence Updates**: Automated threat feed monitoring
- **Performance Metrics**: System performance and optimization

## 🔮 Advanced Features

### Machine Learning (Future)
- **Behavior Analysis**: Learn normal vs abnormal network behavior
- **Threat Prediction**: Predict attacks based on indicators
- **Auto-Tuning**: Automatically optimize scan parameters
- **False Positive Reduction**: Learn to reduce false positives

### Integration Capabilities
- **SIEM Integration**: Splunk, ELK Stack, QRadar compatibility
- **Ticketing Systems**: Jira, ServiceNow integration
- **Communication**: Slack, Discord, Teams notifications
- **Cloud Platforms**: AWS, Azure, GCP security integration

### Workflow Automation
- **Visual Workflow Builder**: Drag-and-drop workflow creation
- **Conditional Logic**: If-then-else workflow logic
- **Parallel Execution**: Concurrent operation execution
- **Error Handling**: Automatic error recovery and retry

## 🆘 Troubleshooting

### Common Issues

**Ollama not responding:**
```bash
systemctl status ollama
curl http://127.0.0.1:11434/api/tags
```

**Permission denied errors:**
```bash
# Check allowlist configuration
nano /opt/priv-cyber-agents/config/allowlist.json

# Verify Wassim keyword for advanced operations
cyber-attack target --wassim "Wassim authorized test"
```

**API connection issues:**
```bash
# Check API server status
systemctl status copilot-gateway

# Verify token
cat /opt/priv-cyber-agents/.env
```

**Missing tools:**
```bash
# Reinstall dependencies
./install.sh

# Manual tool installation
sudo apt-get install nmap masscan nuclei
```

## 📄 License & Legal

This project is licensed under the LUP v1.0 (Limited Use Personal) license for personal and non-commercial use. Enterprise licenses are available for commercial use.

### Security Disclaimer
This tool is designed for authorized security testing only. Users are responsible for ensuring they have proper authorization before testing any systems. The authors are not responsible for any misuse of this software.

### Privacy Statement
This system is designed with privacy-by-default principles. No data is transmitted to external services without explicit user consent. All operations are logged locally with optional encryption.

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and security policy before submitting pull requests.

### Development Setup
```bash
git clone https://github.com/Lucifer-AI-666/priv-cyber-agents-private.git
cd priv-cyber-agents-private
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 tests/basic_test.py
```

## 📞 Support

For support, questions, or enterprise licensing:
- Create an issue on GitHub
- Contact: [security@example.com]
- Documentation: [Wiki Link]

---

**Made with ❤️ for the cybersecurity community**

*"Empowering defenders, enabling attackers (ethically), advancing security for all."*