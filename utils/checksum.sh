#!/usr/bin/env bash
# File checksum utility
# Owner: Dib Anouar

set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: checksum <command> [file]

Commands:
    generate <file>     Generate checksums for a file
    verify <file>       Verify file against checksums
    create <dir>        Create checksum file for directory
    check <checksums>   Verify all files in checksum file

Examples:
    checksum generate myfile.txt
    checksum create /path/to/dir
    checksum check checksums.sha256
EOF
}

generate_checksum() {
    local file="$1"
    
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}Error: File not found: $file${NC}" >&2
        exit 1
    fi
    
    echo -e "${BLUE}Generating checksums for: $file${NC}"
    echo
    
    if command -v sha256sum &>/dev/null; then
        echo -e "${GREEN}SHA-256:${NC} $(sha256sum "$file" | cut -d' ' -f1)"
    elif command -v shasum &>/dev/null; then
        echo -e "${GREEN}SHA-256:${NC} $(shasum -a 256 "$file" | cut -d' ' -f1)"
    fi
    
    if command -v md5sum &>/dev/null; then
        echo -e "${GREEN}MD5:${NC} $(md5sum "$file" | cut -d' ' -f1)"
    elif command -v md5 &>/dev/null; then
        echo -e "${GREEN}MD5:${NC} $(md5 -q "$file")"
    fi
}

create_checksums() {
    local dir="${1:-.}"
    local output="checksums.sha256"
    
    echo -e "${BLUE}Creating checksum file for: $dir${NC}"
    
    if command -v sha256sum &>/dev/null; then
        find "$dir" -type f ! -name "checksums.*" -exec sha256sum {} \; > "$output"
    elif command -v shasum &>/dev/null; then
        find "$dir" -type f ! -name "checksums.*" -exec shasum -a 256 {} \; > "$output"
    fi
    
    echo -e "${GREEN}✓ Created: $output${NC}"
    echo "  Files: $(wc -l < "$output")"
}

check_checksums() {
    local checksum_file="$1"
    
    if [[ ! -f "$checksum_file" ]]; then
        echo -e "${RED}Error: Checksum file not found: $checksum_file${NC}" >&2
        exit 1
    fi
    
    echo -e "${BLUE}Verifying checksums from: $checksum_file${NC}"
    echo
    
    local failed=0
    local total=0
    
    while IFS= read -r line; do
        ((total++))
        local checksum=$(echo "$line" | awk '{print $1}')
        local file=$(echo "$line" | cut -d' ' -f3-)
        
        if [[ ! -f "$file" ]]; then
            echo -e "${RED}✗${NC} $file (missing)"
            ((failed++))
            continue
        fi
        
        local current_checksum
        if command -v sha256sum &>/dev/null; then
            current_checksum=$(sha256sum "$file" | cut -d' ' -f1)
        elif command -v shasum &>/dev/null; then
            current_checksum=$(shasum -a 256 "$file" | cut -d' ' -f1)
        fi
        
        if [[ "$checksum" == "$current_checksum" ]]; then
            echo -e "${GREEN}✓${NC} $file"
        else
            echo -e "${RED}✗${NC} $file (checksum mismatch)"
            ((failed++))
        fi
    done < "$checksum_file"
    
    echo
    echo -e "Total: $total, ${GREEN}Passed: $((total - failed))${NC}, ${RED}Failed: $failed${NC}"
    
    return $failed
}

main() {
    if [[ $# -eq 0 ]]; then
        usage
        exit 1
    fi
    
    local command="$1"
    shift
    
    case "$command" in
        generate)
            generate_checksum "$@"
            ;;
        create)
            create_checksums "$@"
            ;;
        check|verify)
            check_checksums "$@"
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown command: $command${NC}" >&2
            usage
            exit 1
            ;;
    esac
}

main "$@"
