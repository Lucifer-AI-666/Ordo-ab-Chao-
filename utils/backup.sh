#!/usr/bin/env bash
# Backup utility
# Owner: Dib Anouar

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: backup [options] <source> [destination]

Options:
    -c, --compress  Create compressed archive
    -t, --timestamp Use timestamp in backup name
    -h, --help      Show this help

Examples:
    backup /path/to/dir
    backup -c -t myproject /backups
    backup --compress important.txt
EOF
}

main() {
    local compress=false
    local use_timestamp=false
    local source=""
    local dest="./backups"
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -c|--compress)
                compress=true
                shift
                ;;
            -t|--timestamp)
                use_timestamp=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                if [[ -z "$source" ]]; then
                    source="$1"
                else
                    dest="$1"
                fi
                shift
                ;;
        esac
    done
    
    if [[ -z "$source" ]]; then
        echo "Error: Source required" >&2
        usage
        exit 1
    fi
    
    if [[ ! -e "$source" ]]; then
        echo "Error: Source not found: $source" >&2
        exit 1
    fi
    
    mkdir -p "$dest"
    
    local timestamp=""
    if [[ "$use_timestamp" == true ]]; then
        timestamp="_$(date +%Y%m%d_%H%M%S)"
    fi
    
    local basename=$(basename "$source")
    local backup_name="${basename}${timestamp}"
    
    echo -e "${BLUE}📦 Creating backup...${NC}"
    echo "  Source: $source"
    echo "  Destination: $dest"
    echo
    
    if [[ "$compress" == true ]]; then
        local archive="${dest}/${backup_name}.tar.gz"
        tar -czf "$archive" "$source"
        echo -e "${GREEN}✓ Created: $archive${NC}"
        echo "  Size: $(du -h "$archive" | cut -f1)"
    else
        local backup_path="${dest}/${backup_name}"
        cp -r "$source" "$backup_path"
        echo -e "${GREEN}✓ Created: $backup_path${NC}"
        echo "  Size: $(du -sh "$backup_path" | cut -f1)"
    fi
}

main "$@"
