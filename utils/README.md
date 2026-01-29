# Ordo-ab-Chao Core Utilities

A collection of enhanced Unix utilities for development, security operations, and system administration.

**Owner:** Dib Anouar  
**License:** LUP v1.0 (personal and non-commercial use only)

## Installation

Make the main script executable and optionally add to your PATH:

```bash
chmod +x utils/coreutils.sh

# Optional: Create alias for easier access
echo 'alias oac-utils="'$(pwd)'/utils/coreutils.sh"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

```bash
./utils/coreutils.sh <command> [options]
```

Or with alias:
```bash
oac-utils <command> [options]
```

## Available Commands

### File Operations

#### `list` - Enhanced file listing
```bash
./utils/coreutils.sh list              # List current directory
./utils/coreutils.sh list -a           # Show hidden files
./utils/coreutils.sh list -l /path     # Long format
./utils/coreutils.sh list -s           # Sort by size
```

#### `search` - Smart file search
```bash
./utils/coreutils.sh search "*.py"          # Find all Python files
./utils/coreutils.sh search -c "TODO"       # Find files containing "TODO"
./utils/coreutils.sh search -t d "test"     # Find directories
./utils/coreutils.sh search -i "readme"     # Case-insensitive
```

#### `backup` - Create backups
```bash
./utils/coreutils.sh backup myproject              # Simple backup
./utils/coreutils.sh backup -c -t myproject        # Compressed with timestamp
./utils/coreutils.sh backup file.txt /backups      # Custom destination
```

### Text Processing

#### `count` - Count lines, words, characters
```bash
./utils/coreutils.sh count file.txt          # All counts
./utils/coreutils.sh count -l *.py           # Line count for Python files
./utils/coreutils.sh count -w document.md    # Word count
```

### System Information

#### `sysinfo` - Display system information
```bash
./utils/coreutils.sh sysinfo
```

Displays:
- Operating system details
- Kernel information
- CPU and memory specs
- Disk usage
- Software versions (Python, Git, etc.)

#### `diskusage` - Analyze disk usage
```bash
./utils/coreutils.sh diskusage                  # Current directory
./utils/coreutils.sh diskusage /var/log         # Specific path
./utils/coreutils.sh diskusage -s -l 10         # Top 10 largest
```

### Security & Development

#### `checksum` - File integrity verification
```bash
./utils/coreutils.sh checksum generate file.txt       # Generate checksums
./utils/coreutils.sh checksum create /path/to/dir     # Create checksum file
./utils/coreutils.sh checksum check checksums.sha256  # Verify integrity
```

#### `gitinfo` - Git repository information
```bash
./utils/coreutils.sh gitinfo
```

Displays:
- Repository details
- Branch information
- Commit statistics
- Working tree status
- Recent commits
- Contributors

#### `cleanup` - Clean temporary files
```bash
./utils/coreutils.sh cleanup               # Clean temp files
./utils/coreutils.sh cleanup -n            # Dry run (show what would be deleted)
./utils/coreutils.sh cleanup -a            # Clean all including dependencies
```

Removes:
- Python cache (`__pycache__`, `*.pyc`)
- Build artifacts (`dist/`, `build/`, `*.egg-info`)
- Temporary files (`*.tmp`, `*~`)
- Log files (`*.log`)
- OS files (`.DS_Store`, `Thumbs.db`)
- With `--all`: `node_modules`, `.venv`, `venv`

## Individual Command Help

Get help for any specific command:

```bash
./utils/coreutils.sh list --help
./utils/coreutils.sh search --help
./utils/coreutils.sh checksum --help
```

## Examples

### Development Workflow

```bash
# Check git status
./utils/coreutils.sh gitinfo

# Search for TODOs
./utils/coreutils.sh search -c "TODO"

# Clean up before commit
./utils/coreutils.sh cleanup -n  # Preview
./utils/coreutils.sh cleanup     # Execute

# Create backup before major changes
./utils/coreutils.sh backup -c -t .
```

### Security Audit

```bash
# Get system information
./utils/coreutils.sh sysinfo

# Create checksums for verification
./utils/coreutils.sh checksum create /important/files

# Search for sensitive patterns
./utils/coreutils.sh search -c "password"
./utils/coreutils.sh search -c "api_key"
```

### File Management

```bash
# Find large files
./utils/coreutils.sh diskusage -s -l 20

# Find all Python scripts
./utils/coreutils.sh search "*.py"

# Count lines of code
./utils/coreutils.sh count $(find . -name "*.py")

# List files sorted by size
./utils/coreutils.sh list -s
```

## Features

- **Color-coded output** for better readability
- **Cross-platform** support (Linux, macOS)
- **Minimal dependencies** - uses standard Unix tools
- **Safe operations** - dry-run options where applicable
- **Consistent interface** - similar options across commands
- **Comprehensive help** - built-in documentation

## Requirements

Standard Unix utilities:
- `bash` 4.0+
- `find`
- `grep`
- `ls`
- `du`
- `wc`
- `tar` (for compressed backups)
- `sha256sum` or `shasum` (for checksums)
- `git` (for gitinfo command)

## Integration with Ordo-ab-Chao

These utilities are designed to work seamlessly with the Ordo-ab-Chao cybersecurity framework:

- Clean build artifacts before deployment
- Verify file integrity for security
- Monitor system resources
- Manage backups of critical configurations
- Analyze repository structure

## License

LUP v1.0 - Personal and non-commercial use only  
© Dib Anouar

## Support

For issues or feature requests, refer to the main Ordo-ab-Chao repository documentation.
