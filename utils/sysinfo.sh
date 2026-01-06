#!/usr/bin/env bash
# System information utility
# Owner: Dib Anouar

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

main() {
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${GREEN}    Ordo-ab-Chao System Information${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo
    
    echo -e "${YELLOW}Operating System:${NC}"
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        echo "  Name: $NAME"
        echo "  Version: $VERSION"
    elif [[ "$(uname)" == "Darwin" ]]; then
        echo "  Name: macOS"
        echo "  Version: $(sw_vers -productVersion)"
    else
        echo "  $(uname -s) $(uname -r)"
    fi
    echo
    
    echo -e "${YELLOW}Kernel:${NC}"
    echo "  $(uname -sr)"
    echo
    
    echo -e "${YELLOW}Hostname:${NC}"
    echo "  $(hostname)"
    echo
    
    echo -e "${YELLOW}Uptime:${NC}"
    uptime
    echo
    
    echo -e "${YELLOW}CPU:${NC}"
    if command -v lscpu &>/dev/null; then
        lscpu | grep -E "Model name|CPU\(s\):|Thread" | head -3
    elif [[ "$(uname)" == "Darwin" ]]; then
        sysctl -n machdep.cpu.brand_string
        echo "  Cores: $(sysctl -n hw.ncpu)"
    fi
    echo
    
    echo -e "${YELLOW}Memory:${NC}"
    if command -v free &>/dev/null; then
        free -h
    elif [[ "$(uname)" == "Darwin" ]]; then
        echo "  Total: $(($(sysctl -n hw.memsize) / 1024 / 1024 / 1024)) GB"
    fi
    echo
    
    echo -e "${YELLOW}Disk Usage:${NC}"
    df -h | head -n 1
    df -h / | tail -n 1
    echo
    
    echo -e "${YELLOW}Python Version:${NC}"
    if command -v python3 &>/dev/null; then
        python3 --version
    else
        echo "  Python not found"
    fi
    echo
    
    echo -e "${YELLOW}Git Version:${NC}"
    if command -v git &>/dev/null; then
        git --version
    else
        echo "  Git not found"
    fi
    echo
}

main "$@"
