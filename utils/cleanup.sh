#!/usr/bin/env bash
# Cleanup utility for temporary and build files
# Owner: Dib Anouar

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: cleanup [options]

Options:
    -n, --dry-run   Show what would be deleted without deleting
    -a, --all       Clean all (including node_modules, venv)
    -h, --help      Show this help

Removes:
    - Python cache (__pycache__, *.pyc, *.pyo)
    - Build artifacts (dist/, build/, *.egg-info)
    - Temporary files (*.tmp, *.temp, *~)
    - Log files (*.log)
    - OS files (.DS_Store, Thumbs.db)
    - With --all: node_modules, .venv, venv
EOF
}

main() {
    local dry_run=false
    local clean_all=false
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -n|--dry-run)
                dry_run=true
                shift
                ;;
            -a|--all)
                clean_all=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                echo -e "${RED}Error: Unknown option: $1${NC}" >&2
                usage
                exit 1
                ;;
        esac
    done
    
    echo -e "${BLUE}🧹 Ordo-ab-Chao Cleanup Utility${NC}"
    [[ "$dry_run" == true ]] && echo -e "${YELLOW}   (DRY RUN - no files will be deleted)${NC}"
    echo
    
    local count=0
    
    # Python cache files
    echo -e "${YELLOW}Cleaning Python cache...${NC}"
    while IFS= read -r -d '' file; do
        if [[ "$dry_run" == true ]]; then
            echo "  Would delete: $file"
        else
            rm -rf "$file"
        fi
        ((count++))
    done < <(find . -type d -name "__pycache__" -print0 2>/dev/null)
    
    while IFS= read -r -d '' file; do
        if [[ "$dry_run" == true ]]; then
            echo "  Would delete: $file"
        else
            rm -f "$file"
        fi
        ((count++))
    done < <(find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -print0 2>/dev/null)
    
    # Build artifacts
    echo -e "${YELLOW}Cleaning build artifacts...${NC}"
    for dir in dist build *.egg-info; do
        if [[ -d "$dir" ]]; then
            if [[ "$dry_run" == true ]]; then
                echo "  Would delete: $dir"
            else
                rm -rf "$dir"
            fi
            ((count++))
        fi
    done
    
    # Temporary files
    echo -e "${YELLOW}Cleaning temporary files...${NC}"
    while IFS= read -r -d '' file; do
        if [[ "$dry_run" == true ]]; then
            echo "  Would delete: $file"
        else
            rm -f "$file"
        fi
        ((count++))
    done < <(find . -type f \( -name "*.tmp" -o -name "*.temp" -o -name "*~" \) -print0 2>/dev/null)
    
    # Log files
    echo -e "${YELLOW}Cleaning log files...${NC}"
    while IFS= read -r -d '' file; do
        if [[ "$dry_run" == true ]]; then
            echo "  Would delete: $file"
        else
            rm -f "$file"
        fi
        ((count++))
    done < <(find . -type f -name "*.log" -print0 2>/dev/null)
    
    # OS files
    echo -e "${YELLOW}Cleaning OS files...${NC}"
    while IFS= read -r -d '' file; do
        if [[ "$dry_run" == true ]]; then
            echo "  Would delete: $file"
        else
            rm -f "$file"
        fi
        ((count++))
    done < <(find . -type f \( -name ".DS_Store" -o -name "Thumbs.db" \) -print0 2>/dev/null)
    
    # All mode
    if [[ "$clean_all" == true ]]; then
        echo -e "${YELLOW}Cleaning dependencies (--all mode)...${NC}"
        for dir in node_modules .venv venv; do
            if [[ -d "$dir" ]]; then
                if [[ "$dry_run" == true ]]; then
                    echo "  Would delete: $dir"
                else
                    rm -rf "$dir"
                fi
                ((count++))
            fi
        done
    fi
    
    echo
    if [[ "$dry_run" == true ]]; then
        echo -e "${BLUE}Would remove $count items${NC}"
    else
        echo -e "${GREEN}✓ Removed $count items${NC}"
    fi
}

main "$@"
