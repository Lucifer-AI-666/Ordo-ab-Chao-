#!/usr/bin/env bash
# Controlla Commit - Quick Git Verification Script
# Wrapper for controlla_commit.py
# Usage: ./controlla_commit.sh

set -uo pipefail

echo "🔍 Controlla Commit - Git Verification"
echo ""

# Run the Python verification script
python3 controlla_commit.py
exit_code=$?

# Exit with the Python script's exit code
exit $exit_code
