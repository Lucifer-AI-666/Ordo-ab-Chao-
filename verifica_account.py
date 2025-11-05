#!/usr/bin/env python3
"""
Verifica Account - DibTauroS/Ordo-ab-Chao
Verifica lo stato della configurazione account
Owner: Dib Anouar

Usage: python3 verifica_account.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def check_file(path, required=True):
    """Check if file exists and is readable"""
    p = Path(path)
    if p.exists():
        try:
            size = p.stat().st_size
            print(f"   ✅ {path} ({size} bytes)")
            return True
        except Exception as e:
            print(f"   ⚠️  {path} (errore lettura: {e})")
            return False
    else:
        if required:
            print(f"   ❌ {path} (mancante)")
        else:
            print(f"   ⚠️  {path} (opzionale, mancante)")
        return not required

def check_directory(path, required=True):
    """Check if directory exists"""
    p = Path(path)
    if p.exists() and p.is_dir():
        file_count = len(list(p.glob('*')))
        print(f"   ✅ {path}/ ({file_count} file)")
        return True
    else:
        if required:
            print(f"   ❌ {path}/ (mancante)")
        else:
            print(f"   ⚠️  {path}/ (opzionale, mancante)")
        return not required

def check_env_file():
    """Check .env.copilot file"""
    env_file = Path("copilot-agent/config/.env.copilot")
    if not env_file.exists():
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        
    checks = {
        "COPILOT_SECRET_KEY": "Secret key",
        "COPILOT_API_TOKEN": "API token",
        "COPILOT_OWNER": "Owner information",
        "MONICA_DISABLE": "Kill-switch"
    }
    
    all_ok = True
    for key, desc in checks.items():
        if key in content:
            print(f"   ✅ {desc}: configurato")
        else:
            print(f"   ❌ {desc}: mancante")
            all_ok = False
    
    return all_ok

def main():
    print("🔍 Verifica Configurazione Account DibTauroS/Ordo-ab-Chao")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check configuration files
    print("📋 File di configurazione:")
    all_ok &= check_file("copilot-agent/config/.env.copilot")
    all_ok &= check_file("copilot-agent/config/account.json", required=False)
    all_ok &= check_file("copilot-agent/config/modes.json")
    all_ok &= check_file("copilot-agent/config/allowlist.json", required=False)
    all_ok &= check_file("allowlist.json", required=False)
    print()
    
    # Check environment variables
    print("🔑 Variabili d'ambiente:")
    env_ok = check_env_file()
    all_ok &= env_ok
    print()
    
    # Check directory structure
    print("📁 Struttura directory:")
    all_ok &= check_directory("copilot-agent/config")
    all_ok &= check_directory("copilot-agent/logs")
    all_ok &= check_directory("logs")
    all_ok &= check_directory("01-tauros")
    all_ok &= check_directory("02-lucy")
    all_ok &= check_directory("gateway")
    print()
    
    # Check account configuration
    account_file = Path("copilot-agent/config/account.json")
    if account_file.exists():
        print("👤 Informazioni account:")
        try:
            with open(account_file, 'r') as f:
                account = json.load(f)
            print(f"   ✅ Owner: {account.get('owner', {}).get('name', 'N/A')}")
            print(f"   ✅ Framework: {account.get('owner', {}).get('framework', 'N/A')}")
            print(f"   ✅ Creato: {account.get('created_at', 'N/A')}")
            print(f"   ✅ Account ID: {account.get('account_id', 'N/A')}")
        except Exception as e:
            print(f"   ⚠️  Errore lettura account.json: {e}")
            all_ok = False
        print()
    
    # Final result
    print("=" * 60)
    if all_ok:
        print("🎉 Account correttamente configurato!")
        print()
        print("✅ Tutti i controlli superati")
        print("✅ Configurazione valida")
        print("✅ Pronto per l'uso")
        return 0
    else:
        print("⚠️  Account parzialmente configurato")
        print()
        print("💡 Eseguire ricostituzione:")
        print("   python3 ricostituzione_account.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
