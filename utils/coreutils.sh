#!/usr/bin/env bash
# Ordo-ab-Chao Coreutils Collection
# Owner: Dib Anouar
# License: LUP v1.0 (personal and non-commercial use only)
#
# Main entry point for core utilities

set -euo pipefail

# Resolve symlinks to find actual script location
SCRIPT_PATH="${BASH_SOURCE[0]}"
while [ -L "$SCRIPT_PATH" ]; do
    SCRIPT_DIR="$(cd -P "$(dirname "$SCRIPT_PATH")" && pwd)"
    SCRIPT_PATH="$(readlink "$SCRIPT_PATH")"
    [[ $SCRIPT_PATH != /* ]] && SCRIPT_PATH="$SCRIPT_DIR/$SCRIPT_PATH"
done
UTILS_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
PROJECT_ROOT="$(dirname "$UTILS_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print usage information
usage() {
    cat << EOF
${GREEN}Ordo-ab-Chao Coreutils${NC}
Enhanced Unix utilities for development and security operations

${YELLOW}Usage:${NC}
    $(basename "$0") <command> [options]

${YELLOW}Available Commands:${NC}
    ${BLUE}File Operations:${NC}
        list        Enhanced file listing with details
        search      Smart file search with pattern matching
        backup      Create timestamped backups
        diskusage   Analyze disk usage
    
    ${BLUE}Text Processing:${NC}
        count       Count lines, words, characters in files
    
    ${BLUE}System Information:${NC}
        sysinfo     Display system information
    
    ${BLUE}Security & Development:${NC}
        checksum    Calculate and verify file checksums
        gitinfo     Display git repository information
        cleanup     Clean temporary and build files
    
${YELLOW}Examples:${NC}
    $(basename "$0") list -a          # List all files with details
    $(basename "$0") search "*.py"    # Find all Python files
    $(basename "$0") checksum verify  # Verify file integrity
    $(basename "$0") cleanup          # Clean temporary files

${YELLOW}Help:${NC}
    $(basename "$0") <command> --help # Show help for specific command

EOF
}

# Execute a utility command
execute_command() {
    local cmd="$1"
    shift
    
    local cmd_file="${UTILS_DIR}/${cmd}.sh"
    
    if [[ -f "$cmd_file" && -x "$cmd_file" ]]; then
        "$cmd_file" "$@"
    else
        echo -e "${RED}Error: Command '$cmd' not found${NC}" >&2
        echo "Run '$(basename "$0")' to see available commands" >&2
        exit 1
    fi
}

# Main execution
main() {
    if [[ $# -eq 0 ]]; then
        usage
        exit 0
    fi
    
    local command="$1"
    shift
    
    case "$command" in
        -h|--help|help)
            usage
            exit 0
            ;;
        list|search|backup|sysinfo|diskusage|checksum|gitinfo|cleanup|count)
            execute_command "$command" "$@"
            ;;
        *)
            echo -e "${RED}Error: Unknown command '$command'${NC}" >&2
            usage
            exit 1
            ;;
    esac
}

main "$@"
