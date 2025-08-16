#!/bin/bash
#
# deploy_tauros_lucy.sh - Deployment automatico CopilotPrivateAgent via SSH
# Creator: Lucifer-AI-666 (@Lucifer-AI-666)
# Ecosystem: Tauros/Lucy Intelligence Platform
# Deploy Time: 2025-08-16 09:40:35 UTC
#

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
readonly DEPLOY_USER="${DEPLOY_USER:-tauros}"
readonly DEPLOY_PORT="${DEPLOY_PORT:-22}"
readonly REMOTE_DIR="${REMOTE_DIR:-/opt/tauros-lucy}"
readonly OLLAMA_MODEL="copilot_private"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# Logging
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $*${NC}" >&2
}

warn() {
    echo -e "${YELLOW}[WARN] $*${NC}" >&2
}

error() {
    echo -e "${RED}[ERROR] $*${NC}" >&2
    exit 1
}

info() {
    echo -e "${BLUE}[INFO] $*${NC}" >&2
}

# Usage
usage() {
    cat << EOF
🚀 CopilotPrivateAgent Tauros/Lucy Deployment Tool

Usage: $0 [OPTIONS] TARGET

OPTIONS:
    -u, --user USER         Deploy user (default: $DEPLOY_USER)
    -p, --port PORT         SSH port (default: $DEPLOY_PORT)
    -d, --directory DIR     Remote directory (default: $REMOTE_DIR)
    -k, --key KEYFILE       SSH private key file
    --dry-run              Show what would be done without executing
    --hosts FILE           Deploy to multiple hosts from file
    --cluster              Deploy in cluster mode
    --primary HOST         Primary cluster node
    --secondaries HOSTS    Secondary cluster nodes (comma-separated)
    -h, --help             Show this help

EXAMPLES:
    # Single host deployment
    $0 user@tauros-server.local
    
    # Multi-host deployment
    $0 --hosts hosts.txt
    
    # Cluster deployment
    $0 --cluster --primary tauros-01.local --secondaries "tauros-02.local,tauros-03.local"

TARGET:
    user@hostname or IP address for single host deployment
EOF
}

# Deploy to single host
deploy_single_host() {
    local host="$1"
    
    log "🚀 Starting deployment to $host"
    log "📦 Installing Ollama and creating model..."
    
    ssh "$host" "
        # Install Ollama if needed
        if ! which ollama >/dev/null 2>&1; then
            curl -fsSL https://ollama.ai/install.sh | sh
        fi
        
        # Create directory structure
        sudo mkdir -p $REMOTE_DIR/{config,logs,scripts,backups}
        sudo mkdir -p /var/log/tauros-lucy
        
        # Start Ollama service
        sudo systemctl enable ollama --now
        
        # Wait for service to be ready
        timeout 60 sh -c 'until curl -s http://127.0.0.1:11434/api/health; do sleep 2; done'
    "
    
    # Upload Modelfile
    scp "$PROJECT_ROOT/CopilotPrivateAgent.Modelfile" "$host:$REMOTE_DIR/"
    
    # Create and test model
    ssh "$host" "
        cd $REMOTE_DIR
        ollama create $OLLAMA_MODEL -f CopilotPrivateAgent.Modelfile
        echo '✅ Testing model...'
        ollama run $OLLAMA_MODEL 'Status check Tauros/Lucy' | head -3
    "
    
    log "✅ Deployment to $host completed successfully!"
}

# Main execution
main() {
    log "🚀 CopilotPrivateAgent Tauros/Lucy Deployment Tool"
    
    if [[ $# -eq 0 ]]; then
        usage
        exit 1
    fi
    
    local target="$1"
    deploy_single_host "$target"
    
    log "🎉 Deployment completed successfully!"
    log "🔗 Quick test: ssh $target 'ollama run $OLLAMA_MODEL \"Status check Tauros/Lucy\"'"
}

# Execute main function with all arguments
main "$@"