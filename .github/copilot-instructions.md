# Copilot Instructions for Ordo-ab-Chao

## Project Overview
This is a mixed-language cybersecurity project combining an Android app with Python automation agents and web components. The project emphasizes security, privacy, and personal use.

## Licensing and Ownership
- All code is owned by Dib Anouar
- Licensed under LUP v1.0 (personal and non-commercial use only)
- Always include license headers in new Python files:
  ```python
  """
  <File description>
  
  Owner: Dib Anouar
  License: LUP v1.0 (personal and non-commercial use only)
  """
  ```

## Language-Specific Conventions

### Python
- Use Python 3.x syntax
- Include shebang line: `#!/usr/bin/env python3`
- Use type hints where appropriate: `from typing import Dict, List, Optional, Union`
- Use dataclasses for structured data: `from dataclasses import dataclass`
- Use Enum for constants: `from enum import Enum`
- Prefer Path objects over string paths: `from pathlib import Path`
- Use descriptive docstrings for all functions and classes
- Handle emoji printing with fallback for systems without emoji support
- Use logging module for structured logging
- Always create logs directory if needed: `logs_dir.mkdir(exist_ok=True)`

### Java (Android)
- Package: `com.lucifer.ordoabchao`
- Use Android AppCompat: `androidx.appcompat.app.AppCompatActivity`
- Disable JavaScript in WebView for security: `settings.setJavaScriptEnabled(false)`
- Use Italian comments where appropriate for UI descriptions
- Follow standard Android conventions for layouts and resources

### Shell Scripts
- Use bash for shell scripts
- Make scripts executable
- Include descriptive comments
- Handle both Linux and Windows paths where applicable

### JavaScript
- Disable or minimize JavaScript in WebView contexts for security
- Keep JavaScript minimal in embedded web components

## Security Practices

### Critical Security Requirements
- Always disable JavaScript in WebView unless absolutely necessary
- Use allowlist.json for target validation (never hardcode targets)
- Implement dual operation modes:
  - DEFEND mode: defensive operations only (default)
  - TEST mode: advanced operations (requires "Wassim" keyword + allowlist)
- Log all security operations with SHA-256 audit trail
- Store logs in dedicated `logs/` directory
- Never commit secrets or sensitive data
- Validate all external inputs
- Use secure defaults (e.g., JavaScript disabled)

### Allowlist Pattern
- Use `allowlist.json` for permitted targets
- Provide `allowlist.example.json` as template
- Never commit actual allowlist with real targets to public repos

## Project Structure
- `01-tauros/`: Tauros agent files
- `02-lucy/`: Lucy agent files
- `app/`: Android application module
- `copilot-agent/`: Core Python agent implementation
- `scripts/`: Build and utility scripts
- `web/`: Web components
- `legal/`: Legal documentation
- `logs/`: Generated logs (not committed)
- `gateway/`: Gateway components
- `docs/`: Documentation

## Build and Test

### Android Build
- Requires JDK 11+
- Requires Android SDK (API level 34 recommended)
- Set up `local.properties` with SDK path
- Build command: `./gradlew assembleDebug` (Linux/Mac) or `gradlew.bat assembleDebug` (Windows)
- Output: `app/build/outputs/apk/debug/app-debug.apk`

### Python Setup
- Ensure Python 3.x is installed
- Run initialization: `python3 inizia.py`
- Use `verifica.py` for verification

## File Organization
- Use emoji in print statements with fallback support
- Organize files by component (agents, scripts, legal, etc.)
- Keep minimal dependencies
- Document prerequisites in README files

## Code Style
- Use descriptive variable and function names
- Include inline comments for complex logic, especially in Italian where culturally appropriate
- Keep functions focused and single-purpose
- Prefer explicit error handling over silent failures
- Use consistent indentation (4 spaces for Python, standard for Java)

## Dependencies
- Minimize external dependencies
- Use standard libraries when possible
- For Gradle: use Google and Maven Central repositories
- For Python: use standard library features when available

## Documentation
- Update README files when adding new features
- Document security implications of changes
- Include usage examples in docstrings
- Maintain Italian/English bilingual comments where appropriate
