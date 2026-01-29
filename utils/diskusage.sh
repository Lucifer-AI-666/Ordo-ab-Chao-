#!/usr/bin/env bash
# Disk usage analyzer
# Owner: Dib Anouar

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: diskusage [options] [path]

Options:
    -s, --sort      Sort by size (largest first)
    -l, --limit N   Show top N entries (default: 20)
    -h, --help      Show this help

Examples:
    diskusage              # Analyze current directory
    diskusage /var/log     # Analyze specific directory
    diskusage -s -l 10     # Show top 10 largest
EOF
}

main() {
    local sort_by_size=false
    local limit=20
    local target_path="."
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -s|--sort)
                sort_by_size=true
                shift
                ;;
            -l|--limit)
                limit="$2"
                shift 2
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
    
    echo -e "${BLUE}💾 Disk Usage Analysis: $target_path${NC}"
    echo
    
    echo -e "${YELLOW}Total size:${NC}"
    du -sh "$target_path" 2>/dev/null
    echo
    
    echo -e "${YELLOW}Top $limit entries:${NC}"
    if [[ "$sort_by_size" == true ]]; then
        du -h "$target_path"/* 2>/dev/null | sort -hr | head -n "$limit"
    else
        du -h "$target_path"/* 2>/dev/null | head -n "$limit"
    fi
}

main "$@"
