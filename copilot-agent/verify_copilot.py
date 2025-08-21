#!/usr/bin/env python3
"""
CopilotPrivateAgent Verification Script
Comprehensive testing of the DibTauroS/Ordo-ab-Chao framework

Owner: Dib Anouar
License: LUP v1.0 (personal and non-commercial use only)
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_banner():
    """Display the DibTauroS banner"""
    banner_file = Path(__file__).parent / "branding" / "splash.txt"
    if banner_file.exists():
        with open(banner_file, 'r') as f:
            print(f.read())
    else:
        print("CopilotPrivateAgent - DibTauroS Framework")
        print("Ordo ab Chao")

def test_core_functionality():
    """Test core agent functionality"""
    print("\n🧪 Testing Core Functionality...")
    
    tests = [
        {
            "name": "Agent Status Check",
            "command": ["python3", "core/copilot_agent.py", "--status"],
            "expect_success": True
        },
        {
            "name": "DEFEND Mode Operation (Dry Run)",
            "command": ["python3", "core/copilot_agent.py", "--prompt", "check processes", "--target", "localhost"],
            "expect_success": True
        },
        {
            "name": "TEST Mode Operation (Dry Run)",
            "command": ["python3", "core/copilot_agent.py", "--prompt", "Wassim scan network", "--target", "localhost"],
            "expect_success": True
        },
        {
            "name": "Real Operation Test",
            "command": ["python3", "core/copilot_agent.py", "--prompt", "uptime", "--target", "localhost", "--real"],
            "expect_success": True
        }
    ]
    
    for test in tests:
        try:
            result = subprocess.run(
                test["command"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if test["expect_success"] and result.returncode == 0:
                print(f"✅ {test['name']}: PASSED")
            elif not test["expect_success"] and result.returncode != 0:
                print(f"✅ {test['name']}: PASSED (Expected failure)")
            else:
                print(f"❌ {test['name']}: FAILED")
                print(f"   Return code: {result.returncode}")
                print(f"   Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"⏰ {test['name']}: TIMEOUT")
        except Exception as e:
            print(f"❌ {test['name']}: ERROR - {e}")

def test_security_controls():
    """Test security controls"""
    print("\n🔒 Testing Security Controls...")
    
    # Test MONICA disable
    print("Testing MONICA emergency disable...")
    env = os.environ.copy()
    env["MONICA_DISABLE"] = "1"
    
    try:
        result = subprocess.run(
            ["python3", "core/copilot_agent.py", "--prompt", "test", "--target", "localhost"],
            capture_output=True,
            text=True,
            env=env,
            timeout=10
        )
        
        if result.returncode == 0:
            output = json.loads(result.stdout.split('\n')[-2])  # Get last JSON line
            if output.get("status") == "blocked":
                print("✅ MONICA disable: PASSED")
            else:
                print("❌ MONICA disable: FAILED - Not blocked")
        else:
            print("❌ MONICA disable: FAILED - Command error")
    except Exception as e:
        print(f"❌ MONICA disable: ERROR - {e}")

def test_audit_logging():
    """Test audit logging functionality"""
    print("\n📝 Testing Audit Logging...")
    
    logs_dir = Path("../logs")
    agent_log = logs_dir / "copilot_agent.log"
    audit_chain = logs_dir / "audit_chain.json"
    
    if agent_log.exists():
        print("✅ Agent log file exists")
        with open(agent_log, 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                print(f"✅ Agent log has {len(lines)} entries")
            else:
                print("⚠️ Agent log is empty")
    else:
        print("❌ Agent log file missing")
    
    if audit_chain.exists():
        print("✅ Audit chain file exists")
        try:
            with open(audit_chain, 'r') as f:
                chain_data = json.load(f)
                entries = chain_data.get("entries", [])
                if len(entries) > 0:
                    print(f"✅ Audit chain has {len(entries)} entries")
                    # Verify hash chain integrity
                    prev_hash = "genesis"
                    for i, entry in enumerate(entries):
                        if entry["prev_hash"] == prev_hash:
                            prev_hash = entry["log_hash"]
                        else:
                            print(f"❌ Hash chain broken at entry {i}")
                            break
                    else:
                        print("✅ Hash chain integrity verified")
                else:
                    print("⚠️ Audit chain is empty")
        except json.JSONDecodeError:
            print("❌ Audit chain file is corrupted")
    else:
        print("❌ Audit chain file missing")

def check_configuration():
    """Check configuration files"""
    print("\n⚙️ Checking Configuration...")
    
    config_files = [
        ("config/.env.copilot", "Environment configuration"),
        ("config/allowlist.json", "Target allowlist"),
        ("config/modes.json", "Operational modes")
    ]
    
    for file_path, description in config_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {description}: Found")
            try:
                if file_path.endswith('.json'):
                    with open(path, 'r') as f:
                        data = json.load(f)
                        print(f"   Valid JSON with {len(data)} keys")
                else:
                    with open(path, 'r') as f:
                        lines = len(f.readlines())
                        print(f"   {lines} configuration lines")
            except Exception as e:
                print(f"   ⚠️ Error reading file: {e}")
        else:
            print(f"❌ {description}: Missing")

def check_branding():
    """Check branding files"""
    print("\n🎨 Checking DibTauroS Branding...")
    
    branding_files = [
        ("branding/splash.txt", "Text banner"),
        ("branding/html_banner.html", "HTML banner"),
        ("branding/telegram_intro.txt", "Telegram intro"),
        ("branding/README_DIBTAUROS.md", "DibTauroS manifesto")
    ]
    
    for file_path, description in branding_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {description}: Found")
            size = path.stat().st_size
            print(f"   Size: {size} bytes")
        else:
            print(f"❌ {description}: Missing")

def main():
    """Main verification function"""
    print_banner()
    
    print("\n" + "="*60)
    print("CopilotPrivateAgent Verification")
    print("Framework: DibTauroS/Ordo-ab-Chao")
    print("Owner: Dib Anouar")
    print("License: LUP v1.0")
    print("="*60)
    
    # Change to the copilot-agent directory
    os.chdir(Path(__file__).parent)
    
    check_configuration()
    check_branding()
    test_core_functionality()
    test_security_controls()
    test_audit_logging()
    
    print("\n" + "="*60)
    print("🎯 Verification Complete!")
    print("Framework ready for cybersecurity operations")
    print("Remember: Use responsibly and ethically")
    print("="*60)

if __name__ == "__main__":
    main()