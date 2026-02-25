#!/usr/bin/env bash
# Enhanced file listing utility
# Owner: Dib Anouar

set -euo pipefail

# Colors
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: list [options] [path]

Options:
    -a, --all       Show hidden files
    -l, --long      Long format with details
    -s, --size      Sort by size
    -t, --time      Sort by modification time
    -h, --help      Show this help

Examples:
    list                # List current directory
    list -a            # List all files including hidden
    list -l /path      # Long format listing
    list -s            # Sort by size
EOF
}

main() {
    local show_all=false
    local long_format=false
    local sort_by="name"
    local target_path="."
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -a|--all)
                show_all=true
                shift
                ;;
            -l|--long)
                long_format=true
                shift
                ;;
            -s|--size)
                sort_by="size"
                shift
                ;;
            -t|--time)
                sort_by="time"
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                target_path="$1"
                shift
                ;;
        esac
    done
    
    if [[ ! -e "$target_path" ]]; then
        echo -e "${RED}Error: Path '$target_path' does not exist${NC}" >&2
        exit 1
    fi
    
    echo -e "${BLUE}📁 Listing: $target_path${NC}"
    echo
    
    local ls_opts="-h"
    [[ "$show_all" == true ]] && ls_opts="$ls_opts -a"
    [[ "$long_format" == true ]] && ls_opts="$ls_opts -l"
    
    case "$sort_by" in
        size)
            ls_opts="$ls_opts -S"
            ;;
        time)
            ls_opts="$ls_opts -t"
            ;;
    esac
    
    # Use color output if available
    if ls --color=auto / >/dev/null 2>&1; then
        ls_opts="$ls_opts --color=auto"
    elif ls -G / >/dev/null 2>&1; then
        ls_opts="$ls_opts -G"
    fi
    
    ls $ls_opts "$target_path"
}

main "$@"
