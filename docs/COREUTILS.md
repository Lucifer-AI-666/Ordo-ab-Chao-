# Coreutils Integration

The Ordo-ab-Chao project now includes a comprehensive suite of core utilities for enhanced file operations, system monitoring, and development workflows.

## Quick Start

```bash
# From project root
./coreutils <command> [options]

# Or use the full path
./utils/coreutils.sh <command> [options]
```

## Key Features

### Development Tools
- **gitinfo**: View repository status, commits, and contributors
- **cleanup**: Remove temporary files, build artifacts, and caches
- **backup**: Create timestamped backups with optional compression
- **count**: Analyze line, word, and character counts in files

### Security Tools
- **checksum**: Generate and verify SHA-256/MD5 checksums
- **search**: Find files by name or content with pattern matching
- **sysinfo**: Display comprehensive system information

### File Management
- **list**: Enhanced file listing with sorting options
- **diskusage**: Analyze disk space usage
- **backup**: Create compressed, timestamped backups

## Common Usage Examples

### Before Making Changes
```bash
# Check repository status
./coreutils gitinfo

# Create backup
./coreutils backup -c -t .

# Clean temporary files
./coreutils cleanup
```

### Security Audit
```bash
# Generate checksums for important files
./coreutils checksum create /path/to/important/files

# Search for sensitive data
./coreutils search -c "password"
./coreutils search -c "api_key"

# System information
./coreutils sysinfo
```

### Code Analysis
```bash
# Find all Python files
./coreutils search "*.py"

# Count lines of code
./coreutils count $(./coreutils search "*.py" | cut -d' ' -f2)

# Check disk usage
./coreutils diskusage
```

## Documentation

For detailed documentation on all available commands, see:
- `utils/README.md` - Complete utility reference
- `./coreutils --help` - Quick command overview
- `./coreutils <command> --help` - Command-specific help

## Integration with Workflow

The coreutils are designed to integrate seamlessly with the Ordo-ab-Chao development and security workflow:

1. **Pre-Commit**: Use `cleanup` to remove temporary files
2. **Security Checks**: Use `checksum` to verify file integrity
3. **Monitoring**: Use `sysinfo` and `diskusage` for system health
4. **Backup**: Use `backup` before major changes
5. **Analysis**: Use `search` and `count` for code analysis

All utilities follow the project's security-first approach and are licensed under LUP v1.0 for personal and non-commercial use.
