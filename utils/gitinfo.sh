#!/usr/bin/env bash
# Git repository information utility
# Owner: Dib Anouar

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

main() {
    if [[ ! -d .git ]]; then
        echo -e "${RED}Error: Not a git repository${NC}" >&2
        exit 1
    fi
    
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${GREEN}    Git Repository Information${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo
    
    echo -e "${YELLOW}Repository:${NC}"
    if git remote get-url origin &>/dev/null; then
        echo "  Remote: $(git remote get-url origin)"
    else
        echo "  Remote: None"
    fi
    echo
    
    echo -e "${YELLOW}Branch:${NC}"
    local branch=$(git branch --show-current)
    echo "  Current: $branch"
    local branch_count=$(git branch | wc -l)
    echo "  Total Branches: $branch_count"
    echo
    
    echo -e "${YELLOW}Commits:${NC}"
    local commit_count=$(git rev-list --count HEAD 2>/dev/null || echo "0")
    echo "  Total: $commit_count"
    echo "  Latest: $(git log -1 --pretty=format:'%h - %s (%ar)' 2>/dev/null || echo 'None')"
    echo
    
    echo -e "${YELLOW}Status:${NC}"
    local modified=$(git status --porcelain | grep "^ M" | wc -l)
    local added=$(git status --porcelain | grep "^A" | wc -l)
    local deleted=$(git status --porcelain | grep "^ D" | wc -l)
    local untracked=$(git status --porcelain | grep "^??" | wc -l)
    
    echo "  Modified: $modified"
    echo "  Added: $added"
    echo "  Deleted: $deleted"
    echo "  Untracked: $untracked"
    echo
    
    if [[ $((modified + added + deleted + untracked)) -gt 0 ]]; then
        echo -e "${YELLOW}Recent Changes:${NC}"
        git status --short
        echo
    fi
    
    echo -e "${YELLOW}Contributors:${NC}"
    git shortlog -sn --all | head -5
    echo
    
    echo -e "${YELLOW}Recent Commits:${NC}"
    git log --oneline --graph --decorate -10
    echo
}

main "$@"
