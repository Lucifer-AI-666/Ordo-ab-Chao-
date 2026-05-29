# TaurosPrivateAgent Installation Guide

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Python**: 3.8 or higher
- **Docker**: 20.10 or higher (optional)
- **Memory**: Minimum 4GB RAM (8GB recommended for Ollama)
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

### Method 1: Automated Setup (Recommended)

```bash
cd 01-tauros
bash infrastructure/setup_tauros.sh
```

### Method 2: Python Virtual Environment

1. **Navigate to the tauros directory**:
   ```bash
   cd 01-tauros
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r infrastructure/requirements.txt
   ```

4. **Test the installation**:
   ```bash
   python3 core/tauros_agent.py --status
   ```

### Method 3: Docker Deployment

1. **Build the container** (from `01-tauros` directory):
   ```bash
   docker build -f infrastructure/Dockerfile.tauros -t tauros-agent .
   ```

2. **Run the container**:
   ```bash
   docker run --rm -p 127.0.0.1:8788:8788 tauros-agent
   ```

### Method 4: Docker Compose (Full Stack)

```bash
cd 01-tauros
docker compose -f infrastructure/docker-compose.yml up -d
# With Ollama:
docker compose -f infrastructure/docker-compose.yml --profile with-ollama up -d
```

## Configuration

### Environment Variables
Copy the template and edit `config/.env.tauros` to customize your installation:

```bash
cp config/.env.tauros.example config/.env.tauros
```

Then configure values such as:

```dotenv
MONICA_DISABLE=0      # Emergency kill switch (0=enabled, 1=disabled)
TAUROS_MODE=DEFEND    # Default operational mode
TAUROS_HOST=127.0.0.1
TAUROS_PORT=8788
LOG_LEVEL=INFO
```

### Target Allowlist
Edit `config/allowlist.json`:

```json
{
  "allowed_targets": [
    "localhost",
    "127.0.0.1",
    "192.168.1.0/24"
  ]
}
```

### Ollama Model Setup
```bash
ollama create tauros_private -f TaurosPrivateAgent.Modelfile
ollama run tauros_private
```

## Usage Examples

```bash
# Check agent status
python3 core/tauros_agent.py --status

# Run defensive operation (dry-run)
python3 core/tauros_agent.py --prompt "check system processes" --target localhost

# Execute real operation
python3 core/tauros_agent.py --prompt "uptime" --target localhost --real

# TEST mode operation (requires Wassim keyword)
python3 core/tauros_agent.py --prompt "Wassim scan network" --target localhost

# Start web interface
python3 core/web_server.py
# then open http://127.0.0.1:8788
```

## Verification

```bash
python3 verify_tauros.py
```

## Security Features

- **DEFEND Mode**: Always available, safe read-only operations
- **TEST Mode**: Requires "Wassim" keyword + allowlist validation
- **Allowlist Validation**: Only approved targets can be accessed
- **Audit Logging**: SHA-256 integrity chain in `logs/tauros_audit_chain.json`
- **MONICA Kill-Switch**: Set `MONICA_DISABLE=1` to halt all operations
- **Localhost Binding**: Services only accessible locally

## Troubleshooting

### Missing Dependencies
```bash
pip install --upgrade pip
pip install -r infrastructure/requirements.txt --force-reinstall
```

### Permission Errors
```bash
chmod 755 ../logs/
chmod 600 config/.env.tauros
```

### Port Already in Use
```bash
lsof -i :8788
export TAUROS_PORT=8789
```

---

**Framework**: DibTauroS/Ordo-ab-Chao
**Owner**: Dib Anouar
**License**: LUP v1.0 (Personal & Non-Commercial Use Only)
