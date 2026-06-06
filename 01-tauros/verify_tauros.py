#!/usr/bin/env python3
"""
TaurosPrivateAgent Verification Script
Comprehensive testing of the DibTauroS/Ordo-ab-Chao Tauros framework

Owner: Dib Anouar
License: LUP v1.0 (personal and non-commercial use only)
"""

import os
import sys
import json
import subprocess
from pathlib import Path


def print_banner():
    """Display the Tauros banner"""
    banner_file = Path(__file__).parent / "branding" / "splash.txt"
    if banner_file.exists():
        with open(banner_file, 'r') as f:
            print(f.read())
    else:
        print("TaurosPrivateAgent - DibTauroS Framework")
        print("Ordo ab Chao")


def test_core_functionality():
    """Test core agent functionality"""
    print("\n🧪 Testing Core Functionality...")

    tests = [
        {
            "name": "Agent Status Check",
            "command": ["python3", "core/tauros_agent.py", "--status"],
            "expect_success": True
        },
        {
            "name": "DEFEND Mode Operation (Dry Run)",
            "command": ["python3", "core/tauros_agent.py", "--prompt", "check processes", "--target", "localhost"],
            "expect_success": True
        },
        {
            "name": "TEST Mode Operation (Dry Run)",
            "command": ["python3", "core/tauros_agent.py", "--prompt", "Wassim scan network", "--target", "localhost"],
            "expect_success": True
        },
        {
            "name": "Real Operation Test",
            "command": ["python3", "core/tauros_agent.py", "--prompt", "uptime", "--target", "localhost", "--real"],
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


def _parse_json_from_output(output: str):
    """Extract the last JSON object from mixed log+JSON output"""
    import re
    # Find all JSON-looking blocks (starting with { and ending with })
    matches = list(re.finditer(r'^\{', output, re.MULTILINE))
    if not matches:
        return None
    # Try from last match backwards
    for m in reversed(matches):
        candidate = output[m.start():]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass
    return None


def test_security_controls():
    """Test security controls"""
    print("\n🔒 Testing Security Controls...")

    # Test MONICA disable
    print("Testing MONICA emergency disable...")
    env = os.environ.copy()
    env["MONICA_DISABLE"] = "1"

    try:
        result = subprocess.run(
            ["python3", "core/tauros_agent.py", "--prompt", "test", "--target", "localhost"],
            capture_output=True,
            text=True,
            env=env,
            timeout=10
        )

        if result.returncode == 0:
            json_data = _parse_json_from_output(result.stdout)
            if json_data and json_data.get("status") == "blocked":
                print("✅ MONICA disable: PASSED")
            else:
                print("❌ MONICA disable: FAILED - Not blocked")
                print(f"   Output: {result.stdout[:200]}")
        else:
            print("❌ MONICA disable: FAILED - Command error")
    except Exception as e:
        print(f"❌ MONICA disable: ERROR - {e}")

    # Test target not in allowlist
    print("Testing allowlist enforcement (target not in allowlist)...")
    try:
        result = subprocess.run(
            ["python3", "core/tauros_agent.py", "--prompt", "scan", "--target", "8.8.8.8"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            json_data = _parse_json_from_output(result.stdout)
            if json_data and json_data.get("status") == "denied":
                print("✅ Allowlist enforcement: PASSED")
            else:
                print("❌ Allowlist enforcement: FAILED - Not denied")
        else:
            print("❌ Allowlist enforcement: FAILED - Command error")
    except Exception as e:
        print(f"❌ Allowlist enforcement: ERROR - {e}")


def test_audit_logging():
    """Test audit logging functionality"""
    print("\n📝 Testing Audit Logging...")

    logs_dir = Path("../logs")
    agent_log = logs_dir / "tauros_agent.log"
    audit_chain = logs_dir / "tauros_audit_chain.json"

    if agent_log.exists():
        print("✅ Agent log file exists")
        with open(agent_log, 'r') as f:
            lines = f.readlines()
            print(f"   Log has {len(lines)} entries")
    else:
        print("❌ Agent log file missing (run an operation first)")

    if audit_chain.exists():
        print("✅ Audit chain file exists")
        try:
            with open(audit_chain, 'r') as f:
                chain_data = json.load(f)
                entries = chain_data.get("entries", [])
                print(f"   Audit chain has {len(entries)} entries")
                # Verify hash chain integrity
                prev_hash = "genesis"
                for i, entry in enumerate(entries):
                    if entry["prev_hash"] == prev_hash:
                        prev_hash = entry["log_hash"]
                    else:
                        print(f"❌ Hash chain broken at entry {i}")
                        break
                else:
                    if entries:
                        print("✅ Hash chain integrity verified")
        except json.JSONDecodeError:
            print("❌ Audit chain file is corrupted")
    else:
        print("❌ Audit chain file missing (run an operation first)")


def check_configuration():
    """Check configuration files"""
    print("\n⚙️ Checking Configuration...")

    config_files = [
        ("config/.env.tauros", "Environment configuration"),
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
            print(f"❌ {description}: Missing ({file_path})")


def check_branding():
    """Check branding files"""
    print("\n🎨 Checking DibTauroS Branding...")

    branding_files = [
        ("branding/splash.txt", "Text banner"),
        ("branding/html_banner.html", "HTML banner"),
        ("branding/telegram_intro.txt", "Telegram intro"),
        ("branding/README_TAUROS.md", "Tauros manifesto")
    ]

    for file_path, description in branding_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {description}: Found ({size} bytes)")
        else:
            print(f"❌ {description}: Missing ({file_path})")


def check_core_files():
    """Check core implementation files"""
    print("\n🔧 Checking Core Files...")

    core_files = [
        ("core/tauros_agent.py", "Main Python agent"),
        ("core/tauros_integration.js", "Web integration"),
        ("core/web_server.py", "FastAPI web server"),
        ("TaurosPrivateAgent.Modelfile", "Ollama model config"),
        ("infrastructure/requirements.txt", "Python requirements"),
        ("infrastructure/Dockerfile.tauros", "Docker configuration"),
        ("infrastructure/docker-compose.yml", "Docker Compose"),
        ("infrastructure/setup_tauros.sh", "Setup script"),
        ("docs/INSTALLATION.md", "Installation guide")
    ]

    for file_path, description in core_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {description}: Found ({size} bytes)")
        else:
            print(f"❌ {description}: Missing ({file_path})")


def main():
    """Main verification function"""
    print_banner()

    print("\n" + "=" * 60)
    print("TaurosPrivateAgent Verification")
    print("Framework: DibTauroS/Ordo-ab-Chao")
    print("Owner: Dib Anouar")
    print("License: LUP v1.0")
    print("=" * 60)

    # Change to the 01-tauros directory
    os.chdir(Path(__file__).parent)

    check_core_files()
    check_configuration()
    check_branding()
    test_core_functionality()
    test_security_controls()
    test_audit_logging()

    print("\n" + "=" * 60)
    print("🎯 Verification Complete!")
    print("Framework ready for cybersecurity operations")
    print("Remember: Use responsibly and ethically")
    print("=" * 60)


if __name__ == "__main__":
    main()
