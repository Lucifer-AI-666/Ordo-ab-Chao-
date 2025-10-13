# Commit Verification Guide

## Overview

The `controlla_commit` tool provides comprehensive verification of git commits and repository health for the Ordo-ab-Chao framework.

## Usage

### Python Script (Recommended)

```bash
python3 controlla_commit.py
```

### Shell Script

```bash
./controlla_commit.sh
```

## Features

### 1. Git Status Check
- Verifies git repository is valid
- Shows current branch
- Lists uncommitted changes

### 2. Commit Integrity Check
- Displays last 5 commits
- Runs `git fsck` to verify object database
- Ensures no corruption in git history

### 3. Recent Activity
- Shows last 10 commits with details
- Includes commit hash, author, timestamp, and message
- Helps track recent development activity

### 4. Repository Structure Verification
- Runs `verifica.py` to check directory structure
- Verifies essential files are present
- Checks for Modelfiles in agent directories

### 5. CopilotAgent Verification
- Runs comprehensive CopilotAgent tests
- Checks configuration files
- Verifies branding files
- Tests core functionality
- Validates security controls
- Checks audit logging

## Exit Codes

- `0`: All checks passed successfully
- `1`: One or more checks failed

## Example Output

```
🔍 CONTROLLA COMMIT - Git & Repository Verification
Framework: DibTauroS/Ordo-ab-Chao
Owner: Dib Anouar
License: LUP v1.0

============================================================
  📊 Git Status Check
============================================================
✅ Git repository detected
📌 Current branch: main
✅ Working tree clean - no uncommitted changes

...

============================================================
  ✨ Final Status
============================================================

Checks passed: 5/5
   ✅ PASS - Git Status
   ✅ PASS - Commit Integrity
   ✅ PASS - Recent Activity
   ✅ PASS - Repository Structure
   ✅ PASS - CopilotAgent

============================================================
🎉 All checks passed! Repository is healthy.
```

## Integration

This tool can be integrated into:
- Pre-commit hooks
- CI/CD pipelines
- Regular health checks
- Development workflows

## Requirements

- Python 3.8+
- Git
- Access to repository files

## Related Scripts

- `verifica.py` - Repository structure verification
- `copilot-agent/verify_copilot.py` - CopilotAgent verification
- `inizia.py` / `inizia.sh` - Repository initialization

## License

LUP v1.0 (Personal and Non-Commercial Use Only)
Owner: Dib Anouar
