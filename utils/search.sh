#!/usr/bin/env bash
# Smart file search utility
# Owner: Dib Anouar

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: search [options] <pattern> [path]

Options:
    -n, --name      Search by name (default)
    -c, --content   Search file contents
    -t, --type      File type (f=file, d=directory, l=link)
    -i, --ignore-case   Case insensitive search
    -h, --help      Show this help

Examples:
    search "*.py"           # Find all Python files
    search -c "TODO"        # Find files containing "TODO"
    search -t d "test"      # Find directories matching "test"
    search -i "readme"      # Case-insensitive name search
EOF
}

main() {
    local search_type="name"
    local pattern=""
    local search_path="."
    local file_type=""
    local ignore_case=""
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -n|--name)
                search_type="name"
                shift
                ;;
            -c|--content)
                search_type="content"
                shift
                ;;
            -t|--type)
                file_type="$2"
                shift 2
                ;;
            -i|--ignore-case)
                ignore_case="-iname"
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                if [[ -z "$pattern" ]]; then
                    pattern="$1"
                else
                    search_path="$1"
                fi
                shift
                ;;
        esac
    done
    
    if [[ -z "$pattern" ]]; then
        echo "Error: Pattern required" >&2
        usage
        exit 1
    fi
    
    echo -e "${BLUE}🔍 Searching for: $pattern${NC}"
    echo
    
    if [[ "$search_type" == "name" ]]; then
        local find_opts=""
        [[ -n "$file_type" ]] && find_opts="-type $file_type"
        
        if [[ -n "$ignore_case" ]]; then
            find_opts="$find_opts -iname"
        else
            find_opts="$find_opts -name"
        fi
        
        find "$search_path" $find_opts "$pattern" 2>/dev/null | while read -r file; do
            echo -e "${GREEN}✓${NC} $file"
        done
    else
        # Content search
        grep -r "$pattern" "$search_path" 2>/dev/null | while IFS=: read -r file line; do
            echo -e "${GREEN}✓${NC} ${BLUE}$file${NC}: $line"
        done
    fi
}

main "$@"
