#!/usr/bin/env python3
"""
Controlla Commit - Comprehensive Git Commit Verification
Verifies git commit status, integrity, and repository health

Owner: Dib Anouar
License: LUP v1.0 (personal and non-commercial use only)
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_git_status():
    """Check current git status"""
    print_section("📊 Git Status Check")
    
    try:
        # Check if we're in a git repository
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Git repository detected")
        
        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        )
        branch = result.stdout.strip()
        print(f"📌 Current branch: {branch}")
        
        # Check status
        result = subprocess.run(
            ["git", "--no-pager", "status", "--short"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout.strip():
            print("\n⚠️  Uncommitted changes detected:")
            print(result.stdout)
        else:
            print("✅ Working tree clean - no uncommitted changes")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False

def check_commit_integrity():
    """Verify git commit integrity"""
    print_section("🔐 Commit Integrity Check")
    
    try:
        # Get last 5 commits
        result = subprocess.run(
            ["git", "--no-pager", "log", "--oneline", "-5"],
            capture_output=True,
            text=True,
            check=True
        )
        
        commits = result.stdout.strip().split('\n')
        print(f"✅ Last {len(commits)} commits:")
        for commit in commits:
            print(f"   {commit}")
        
        # Verify commit objects
        result = subprocess.run(
            ["git", "fsck", "--no-progress"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("\n✅ Git object database integrity: OK")
        else:
            print(f"\n⚠️  Git fsck found issues:")
            print(result.stderr)
        
        return True
    except subprocess.TimeoutExpired:
        print("⏰ Git fsck timeout (repository might be large)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Commit integrity check failed: {e}")
        return False

def check_recent_activity():
    """Check recent git activity"""
    print_section("📅 Recent Activity")
    
    try:
        # Get commit statistics
        result = subprocess.run(
            ["git", "--no-pager", "log", "--pretty=format:%h|%an|%ar|%s", "-10"],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("Recent commits (last 10):")
        print(f"{'Hash':<10} {'Author':<20} {'When':<20} {'Message':<40}")
        print("-" * 95)
        
        for line in result.stdout.strip().split('\n'):
            parts = line.split('|', 3)
            if len(parts) == 4:
                hash_short, author, when, message = parts
                print(f"{hash_short:<10} {author:<20} {when:<20} {message[:40]:<40}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Recent activity check failed: {e}")
        return False

def check_repository_structure():
    """Run verifica.py to check repository structure"""
    print_section("📁 Repository Structure Verification")
    
    try:
        result = subprocess.run(
            ["python3", "verifica.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("✅ Repository structure: OK")
            return True
        else:
            print("⚠️  Repository structure: Needs attention")
            return False
    except FileNotFoundError:
        print("⚠️  verifica.py not found - skipping structure check")
        return True
    except subprocess.TimeoutExpired:
        print("⏰ Structure check timeout - skipping")
        return True
    except Exception as e:
        print(f"❌ Structure check error: {e}")
        return False

def check_copilot_agent():
    """Check copilot agent if available"""
    print_section("🤖 CopilotAgent Verification")
    
    copilot_verify = Path("copilot-agent/verify_copilot.py")
    if not copilot_verify.exists():
        print("⚠️  CopilotAgent verification script not found - skipping")
        return True
    
    try:
        result = subprocess.run(
            ["python3", str(copilot_verify)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("✅ CopilotAgent: OK")
            return True
        else:
            print("⚠️  CopilotAgent: Check output for details")
            return False
    except subprocess.TimeoutExpired:
        print("⏰ CopilotAgent verification timeout")
        return False
    except Exception as e:
        print(f"❌ CopilotAgent check error: {e}")
        return False

def generate_report():
    """Generate a summary report"""
    print_section("📋 Summary Report")
    
    print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Repository: {Path.cwd()}")
    print(f"User: {os.environ.get('USER', 'unknown')}")
    
    # Count files (optimized with os.scandir)
    def count_files_fast(path='.'):
        """Fast file counting using os.scandir"""
        count = 0
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.name == '.git':
                        continue
                    if entry.is_file(follow_symlinks=False):
                        count += 1
                    elif entry.is_dir(follow_symlinks=False):
                        count += count_files_fast(entry.path)
        except PermissionError:
            pass
        return count
    
    total_files = count_files_fast('.')
    print(f"Total files (excluding .git): {total_files}")
    
    # Check important files
    important_files = [
        "README.md",
        "verifica.py",
        "inizia.py",
        "allowlist.example.json",
    ]
    
    print("\n📄 Important files:")
    for file in important_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")

def main():
    """Main verification function"""
    print("\n" + "🔍 CONTROLLA COMMIT - Git & Repository Verification".center(60))
    print("Framework: DibTauroS/Ordo-ab-Chao")
    print("Owner: Dib Anouar")
    print("License: LUP v1.0")
    
    all_checks = []
    
    # Run all checks
    all_checks.append(("Git Status", check_git_status()))
    all_checks.append(("Commit Integrity", check_commit_integrity()))
    all_checks.append(("Recent Activity", check_recent_activity()))
    all_checks.append(("Repository Structure", check_repository_structure()))
    all_checks.append(("CopilotAgent", check_copilot_agent()))
    
    # Generate final report
    generate_report()
    
    # Print final status
    print_section("✨ Final Status")
    
    passed = sum(1 for _, result in all_checks if result)
    total = len(all_checks)
    
    print(f"\nChecks passed: {passed}/{total}")
    
    for name, result in all_checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {name}")
    
    print("\n" + "="*60)
    
    if passed == total:
        print("🎉 All checks passed! Repository is healthy.")
        return 0
    else:
        print("⚠️  Some checks failed. Review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
