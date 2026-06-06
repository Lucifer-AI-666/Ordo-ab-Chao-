#!/usr/bin/env bash
# setup_tauros.sh - Automated setup for TaurosPrivateAgent
# DibTauroS/Ordo-ab-Chao framework
#
# Owner: Dib Anouar
# License: LUP v1.0 (personal and non-commercial use only)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TAUROS_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$TAUROS_DIR/.venv"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

print_banner() {
    cat << 'BANNER'
╔══════════════════════════════════════════════════════════════╗
║      TaurosPrivateAgent - DibTauroS/Ordo-ab-Chao Setup      ║
║          Owner: Dib Anouar  |  License: LUP v1.0            ║
╚══════════════════════════════════════════════════════════════╝
BANNER
}

check_python() {
    info "Checking Python version..."
    if ! command -v python3 &>/dev/null; then
        error "Python 3 is required but not installed."
        exit 1
    fi
    PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    info "Python $PY_VERSION found."
    if python3 -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)"; then
        info "Python version OK (>= 3.8)"
    else
        error "Python 3.8 or higher is required (found $PY_VERSION)."
        exit 1
    fi
}

create_venv() {
    info "Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    info "Virtual environment created."
}

install_dependencies() {
    info "Installing Python dependencies..."
    "$VENV_DIR/bin/pip" install --upgrade pip --quiet
    "$VENV_DIR/bin/pip" install -r "$SCRIPT_DIR/requirements.txt" --quiet
    info "Dependencies installed."
}

setup_config() {
    info "Setting up configuration..."

    # Copy example allowlist if none exists
    if [ ! -f "$TAUROS_DIR/config/allowlist.json" ]; then
        if [ -f "$TAUROS_DIR/../allowlist.example.json" ]; then
            cp "$TAUROS_DIR/../allowlist.example.json" "$TAUROS_DIR/config/allowlist.json"
            warn "Copied example allowlist to config/allowlist.json - please customize it."
        fi
    else
        info "allowlist.json already exists."
    fi

    # Create logs directory
    mkdir -p "$TAUROS_DIR/../logs"
    info "Logs directory ready."
}

verify_installation() {
    info "Verifying installation..."
    if "$VENV_DIR/bin/python3" "$TAUROS_DIR/core/tauros_agent.py" --status > /dev/null 2>&1; then
        info "Agent status check: PASSED"
    else
        warn "Agent status check: FAILED (dependencies may need manual install)"
    fi
}

print_usage() {
    cat << 'USAGE'

╔══════════════════════════════════════════════════════════════╗
║                    SETUP COMPLETE                            ║
╠══════════════════════════════════════════════════════════════╣
║  Activate venv:                                              ║
║    source .venv/bin/activate                                 ║
║                                                              ║
║  Check status:                                               ║
║    python3 core/tauros_agent.py --status                     ║
║                                                              ║
║  Run operation (dry-run):                                    ║
║    python3 core/tauros_agent.py --prompt "check processes"   ║
║                                                              ║
║  Create Ollama model:                                        ║
║    ollama create tauros_private -f TaurosPrivateAgent.Modelfile
║                                                              ║
║  Start web interface:                                        ║
║    python3 core/web_server.py                                ║
╚══════════════════════════════════════════════════════════════╝
USAGE
}

main() {
    print_banner
    check_python
    create_venv
    install_dependencies
    setup_config
    verify_installation
    print_usage
}

main "$@"
