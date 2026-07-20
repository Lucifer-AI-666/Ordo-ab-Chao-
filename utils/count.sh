#!/usr/bin/env bash
# Line/word count utility
# Owner: Dib Anouar

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: count [options] <file> [...]

Options:
    -l, --lines     Count lines
    -w, --words     Count words
    -c, --chars     Count characters
    -a, --all       Show all counts (default)
    -h, --help      Show this help

Examples:
    count file.txt         # All counts
    count -l *.py          # Line count for Python files
    count -w document.md   # Word count
EOF
}

main() {
    local show_lines=false
    local show_words=false
    local show_chars=false
    local files=()
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -l|--lines)
                show_lines=true
                shift
                ;;
            -w|--words)
                show_words=true
                shift
                ;;
            -c|--chars)
                show_chars=true
                shift
                ;;
            -a|--all)
                show_lines=true
                show_words=true
                show_chars=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                files+=("$1")
                shift
                ;;
        esac
    done
    
    # If no specific option, show all
    if [[ "$show_lines" == false && "$show_words" == false && "$show_chars" == false ]]; then
        show_lines=true
        show_words=true
        show_chars=true
    fi
    
    if [[ ${#files[@]} -eq 0 ]]; then
        echo "Error: No files specified" >&2
        usage
        exit 1
    fi
    
    echo -e "${BLUE}📊 File Statistics${NC}"
    echo
    
    for file in "${files[@]}"; do
        if [[ ! -f "$file" ]]; then
            echo -e "${YELLOW}Skipping: $file (not found)${NC}"
            continue
        fi
        
        echo -e "${GREEN}$file:${NC}"
        
        if [[ "$show_lines" == true ]]; then
            local lines=$(wc -l < "$file")
            echo "  Lines: $lines"
        fi
        
        if [[ "$show_words" == true ]]; then
            local words=$(wc -w < "$file")
            echo "  Words: $words"
        fi
        
        if [[ "$show_chars" == true ]]; then
            local chars=$(wc -c < "$file")
            echo "  Characters: $chars"
        fi
        
        echo
    done
}

main "$@"
