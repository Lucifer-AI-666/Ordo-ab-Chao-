# CopilotPrivateAgent Installation Guide

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Python**: 3.8 or higher
- **Docker**: 20.10 or higher (optional)
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: Minimum 2GB free space

### Required Software
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip curl git

# macOS (using Homebrew)
brew install python3 curl git

# Arch Linux
sudo pacman -S python curl git
```

## Installation Methods

### Method 1: Python Virtual Environment (Recommended)

1. **Navigate to the copilot-agent directory**:
   ```bash
   cd copilot-agent
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv copilot-venv
   source copilot-venv/bin/activate  # On Windows: copilot-venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r infrastructure/requirements.txt
   ```

4. **Test the installation**:
   ```bash
   python3 core/copilot_agent.py --status
   ```

### Method 2: Docker Deployment

1. **Build the container**:
   ```bash
   docker build -f infrastructure/Dockerfile.copilot -t copilot-agent .
   ```

2. **Run the container**:
   ```bash
   docker run --rm -p 127.0.0.1:8787:8787 copilot-agent
   ```

### Method 3: Direct Python Execution

1. **Install system dependencies**:
   ```bash
   pip install psutil requests cryptography fastapi uvicorn python-dotenv
   ```

2. **Run directly**:
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
```

### Target Allowlist
Edit `config/allowlist.json` to define authorized targets:

```json
{
  "allowed_targets": [
    "localhost",
    "127.0.0.1",
    "192.168.1.0/24"
  ]
}
```

### Operational Modes
Review `config/modes.json` for operational settings:

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

## Usage Examples

### Basic Commands

```bash
# Check agent status
python3 core/copilot_agent.py --status

# Run defensive operation (dry-run)
python3 core/copilot_agent.py --prompt "check system processes" --target localhost

# Execute real operation
python3 core/copilot_agent.py --prompt "ps" --target localhost --real

# TEST mode operation (requires Wassim keyword)
python3 core/copilot_agent.py --prompt "Wassim scan network" --target localhost
```

### Web Interface

1. **Start the web interface** (if implemented):
   ```bash
   python3 -m uvicorn core.web_server:app --host 127.0.0.1 --port 8787
   ```

2. **Open browser**: Navigate to `http://127.0.0.1:8787`

## Verification

### Test Basic Functionality
```bash
# Test status command
python3 core/copilot_agent.py --status

# Test dry-run operation
python3 core/copilot_agent.py --prompt "system check" --target localhost

# Test real operation (safe)
python3 core/copilot_agent.py --prompt "uptime" --target localhost --real
```

### Check Log Files
```bash
# View logs
ls -la logs/
cat logs/copilot_agent.log
cat logs/audit_chain.json
```

## Security Features

### Two-Tier Operational Modes
- **DEFEND Mode**: Always available, safe operations only
- **TEST Mode**: Requires "Wassim" keyword + allowlist validation

### Security Controls
- **Allowlist Validation**: Only approved targets can be accessed
- **Audit Logging**: All operations logged with SHA-256 integrity chain
- **Emergency Kill-Switch**: Set `MONICA_DISABLE=1` to halt all operations
- **Privilege Checks**: Operations validated against user privileges

### Privacy Protection
- **Local-Only Operations**: No external data transmission
- **No Telemetry**: No usage data collection
- **Localhost Binding**: Services only accessible locally

## Troubleshooting

### Common Issues

#### Missing Dependencies
```bash
pip install --upgrade pip
pip install -r infrastructure/requirements.txt --force-reinstall
```

#### Permission Errors
```bash
# Fix file permissions
chmod 755 logs/
chmod 600 config/.env.copilot
```

#### Port Already in Use
```bash
# Check what's using the port
netstat -tulpn | grep :8787

# Change port in configuration
export COPILOT_PORT=8788
```

### Log Analysis
- **Application Log**: `logs/copilot_agent.log`
- **Audit Chain**: `logs/audit_chain.json`
- **Operation History**: Check timestamps and status codes

## Support and Documentation

### Key Files
- **Core Agent**: `core/copilot_agent.py`
- **Web Integration**: `core/copilot_integration.js`
- **Configuration**: `config/` directory
- **Branding**: `branding/` directory

### Security Guidelines
1. **Always start with DEFEND mode**
2. **Verify allowlist before TEST operations**
3. **Monitor logs regularly**
4. **Use dry-run mode for testing**
5. **Keep configuration files secure**

---

**Framework**: DibTauroS/Ordo-ab-Chao  
**Owner**: Dib Anouar  
**License**: LUP v1.0 (Personal & Non-Commercial Use Only)

For questions or issues, refer to the manifesto in `branding/README_DIBTAUROS.md`.