#!/usr/bin/env python3
"""
Ricostituzione Account - DibTauroS/Ordo-ab-Chao
Ricostituisce completamente la configurazione dell'account utente
Owner: Dib Anouar
License: LUP v1.0 (uso personale e non commerciale)

Usage: python3 ricostituzione_account.py
"""

import os
import sys
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
import secrets
import hashlib

def print_emoji(emoji, message):
    """Print message with emoji (fallback for systems without emoji support)"""
    try:
        print(f"{emoji} {message}")
    except UnicodeEncodeError:
        print(f"[{emoji}] {message}")

def generate_secure_token(length=32):
    """Generate a secure random token"""
    return secrets.token_hex(length)

def create_account_config():
    """Create complete account configuration"""
    print_emoji("🔐", "Creazione configurazione account...")
    
    account_config = {
        "owner": {
            "name": "Dib Anouar",
            "framework": "DibTauroS/Ordo-ab-Chao",
            "license": "LUP v1.0"
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
        "account_id": hashlib.sha256(f"DibAnouar{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()[:16]
    }
    
    config_dir = Path("copilot-agent/config")
    config_dir.mkdir(parents=True, exist_ok=True)
    
    account_file = config_dir / "account.json"
    with open(account_file, 'w', encoding='utf-8') as f:
        json.dump(account_config, f, indent=2)
    
    os.chmod(account_file, 0o600)
    print(f"   ✅ Configurazione account creata: {account_file}")
    return account_config

def reconstitute_env_file():
    """Reconstitute .env.copilot with fresh secure tokens"""
    print_emoji("🔑", "Ricostituzione file ambiente con nuovi token di sicurezza...")
    
    env_file = Path("copilot-agent/config/.env.copilot")
    backup_file = Path("copilot-agent/config/.env.copilot.backup")
    
    # Backup existing file if it exists
    if env_file.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = Path(f"copilot-agent/config/.env.copilot.backup.{timestamp}")
        shutil.copy(env_file, backup_file)
        print(f"   📦 Backup creato: {backup_file}")
    
    # Generate new secure tokens
    secret_key = generate_secure_token(32)
    api_token = generate_secure_token(32)
    
    env_content = f"""# CopilotPrivateAgent Environment Configuration
# DibTauroS/Ordo-ab-Chao framework
# Owner: Dib Anouar
# License: LUP v1.0 (personal and non-commercial use only)
# Ricostituito: {datetime.now(timezone.utc).isoformat()}

# Security Settings
MONICA_DISABLE=0
COPILOT_MODE=DEFEND

# Network Configuration  
COPILOT_HOST=127.0.0.1
COPILOT_PORT=8787

# Logging Configuration
LOG_LEVEL=INFO
LOG_RETENTION_DAYS=30

# Ollama Configuration
OLLAMA_HOST=127.0.0.1
OLLAMA_PORT=11434
OLLAMA_MODEL=mistral:7b-instruct

# Security Keys (GENERATED - Keep these secure!)
COPILOT_SECRET_KEY={secret_key}
COPILOT_API_TOKEN={api_token}

# Owner Information
COPILOT_OWNER="Dib Anouar"
COPILOT_LICENSE="LUP v1.0"
COPILOT_FRAMEWORK="DibTauroS/Ordo-ab-Chao"

# Database Configuration (if using database features)
DATABASE_URL=sqlite:///copilot_agent.db

# Feature Flags
ENABLE_WEB_INTERFACE=true
ENABLE_TELEGRAM_BOT=false
ENABLE_REAL_TIME_LOGGING=true
ENABLE_AUDIT_CHAIN=true

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=60
MAX_CONCURRENT_OPERATIONS=5

# Timeout Settings
OPERATION_TIMEOUT_SECONDS=300
NETWORK_TIMEOUT_SECONDS=30

# Account Settings
ACCOUNT_RECONSTITUTED=true
RECONSTITUTION_DATE={datetime.now(timezone.utc).isoformat()}
"""
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    os.chmod(env_file, 0o600)
    print(f"   ✅ File ambiente ricostituito con nuovi token di sicurezza")
    print(f"   🔒 Secret Key: {secret_key[:8]}...{secret_key[-8:]}")
    print(f"   🔒 API Token: {api_token[:8]}...{api_token[-8:]}")
    
    return {"secret_key": secret_key, "api_token": api_token}

def setup_allowlist():
    """Setup allowlist.json from example"""
    print_emoji("📋", "Configurazione allowlist...")
    
    allowlist_file = Path("allowlist.json")
    example_file = Path("allowlist.example.json")
    
    if not allowlist_file.exists() and example_file.exists():
        allowlist_data = {
            "allowed_targets": [
                "localhost",
                "127.0.0.1",
                "192.168.1.0/24"
            ],
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "owner": "Dib Anouar",
            "_comment": "Lista dei target autorizzati per operazioni di sicurezza"
        }
        
        with open(allowlist_file, 'w', encoding='utf-8') as f:
            json.dump(allowlist_data, f, indent=2)
        
        print(f"   ✅ Allowlist creata: {allowlist_file}")
    else:
        print(f"   ℹ️  Allowlist esistente mantenuta")
    
    # Also create allowlist in copilot-agent/config
    copilot_allowlist = Path("copilot-agent/config/allowlist.json")
    if not copilot_allowlist.exists():
        copilot_allowlist.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(allowlist_file, copilot_allowlist)
        print(f"   ✅ Allowlist copiata in: {copilot_allowlist}")

def setup_directory_structure():
    """Create complete directory structure for account"""
    print_emoji("📁", "Creazione struttura directory completa...")
    
    directories = [
        "logs",
        "logs/copilot",
        "logs/tauros",
        "logs/lucy",
        "copilot-agent/config",
        "copilot-agent/logs",
        "01-tauros/logs",
        "02-lucy/logs",
        "gateway/logs",
        "tests/results",
        "docs/account"
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        
        # Create .gitkeep to preserve empty directories
        gitkeep = path / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
    
    print(f"   ✅ {len(directories)} directory create/verificate")

def create_account_readme():
    """Create README for account configuration"""
    print_emoji("📝", "Creazione documentazione account...")
    
    readme_content = """# Account Dib Anouar - DibTauroS/Ordo-ab-Chao

## Informazioni Account

- **Owner**: Dib Anouar
- **Framework**: DibTauroS/Ordo-ab-Chao
- **License**: LUP v1.0 (uso personale e non commerciale)
- **Ricostituito**: {timestamp}

## Configurazione Account

### File di Configurazione

- `copilot-agent/config/.env.copilot` - Variabili d'ambiente e token di sicurezza
- `copilot-agent/config/account.json` - Configurazione account principale
- `copilot-agent/config/allowlist.json` - Target autorizzati
- `copilot-agent/config/modes.json` - Modalità operative (DEFEND/TEST)

### Struttura Directory

```
├── copilot-agent/          # Agente principale
│   ├── config/             # Configurazioni
│   └── logs/               # Log operazioni
├── 01-tauros/              # Tauros Private Agent
│   └── logs/               # Log Tauros
├── 02-lucy/                # Lucy Private Agent
│   └── logs/               # Log Lucy
├── gateway/                # API Gateway
│   └── logs/               # Log Gateway
└── logs/                   # Log centrali
    ├── copilot/
    ├── tauros/
    └── lucy/
```

## Sicurezza Account

### Token e Chiavi

- **Secret Key**: Generata automaticamente (64 caratteri hex)
- **API Token**: Generato automaticamente (64 caratteri hex)
- **Backup**: File `.env.copilot.backup.*` con timestamp

⚠️ **IMPORTANTE**: Non condividere mai i token di sicurezza!

### Modalità Operative

1. **DEFEND** (Default)
   - Operazioni di monitoraggio e analisi
   - Sempre disponibile
   - Comandi read-only

2. **TEST** (Gated)
   - Operazioni avanzate
   - Richiede keyword "Wassim"
   - Richiede target in allowlist

### Emergency Kill-Switch

Per disabilitare tutte le operazioni:
```bash
export MONICA_DISABLE=1
```

## Utilizzo

### Verifica Account
```bash
python3 verifica_account.py
```

### Backup Account
```bash
python3 backup_account.py
```

### Ripristino Account
```bash
python3 ricostituzione_account.py
```

## Manutenzione

### Rotazione Token

I token di sicurezza dovrebbero essere ruotati periodicamente:
```bash
# Ricostituzione completa genera nuovi token
python3 ricostituzione_account.py
```

### Pulizia Log

Per pulire i log più vecchi di 30 giorni:
```bash
find logs/ -name "*.log" -mtime +30 -delete
```

## Supporto

Per problemi o domande:
- Consulta la documentazione in `docs/`
- Verifica i log in `logs/`
- Esegui `python3 verifica.py` per diagnostica

---

**Framework**: DibTauroS/Ordo-ab-Chao  
**Owner**: Dib Anouar  
**License**: LUP v1.0 (Personal & Non-Commercial Use Only)
""".format(timestamp=datetime.now(timezone.utc).isoformat())
    
    readme_file = Path("docs/account/README_ACCOUNT.md")
    readme_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"   ✅ Documentazione account creata: {readme_file}")

def create_gitignore_entries():
    """Add sensitive files to .gitignore"""
    print_emoji("🔒", "Aggiornamento .gitignore per file sensibili...")
    
    gitignore_file = Path(".gitignore")
    
    sensitive_patterns = [
        "\n# Account sensitive files (added by ricostituzione_account.py)",
        "*.backup.*",
        ".env",
        ".env.local",
        ".env.copilot",
        "copilot-agent/config/.env*",
        "copilot-agent/config/account.json",
        "**/logs/*.log",
        "**/logs/*.jsonl",
        "**/*.db",
        "**/*.sqlite",
        "**/*.sqlite3"
    ]
    
    # Read existing .gitignore
    existing_content = ""
    if gitignore_file.exists():
        with open(gitignore_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # Add new patterns if not already present
    new_patterns = []
    for pattern in sensitive_patterns:
        if pattern.strip() and pattern.strip() not in existing_content:
            new_patterns.append(pattern)
    
    if new_patterns:
        with open(gitignore_file, 'a', encoding='utf-8') as f:
            f.write("\n")
            f.write("\n".join(new_patterns))
            f.write("\n")
        print(f"   ✅ Aggiunti {len(new_patterns)} pattern a .gitignore")
    else:
        print(f"   ℹ️  .gitignore già aggiornato")

def ensure_verification_script():
    """Ensure verification script exists"""
    print_emoji("🧪", "Verifica script di verifica account...")
    
    verification_file = Path("verifica_account.py")
    if verification_file.exists():
        print(f"   ✅ Script di verifica già presente: {verification_file}")
    else:
        print(f"   ⚠️  Script di verifica non trovato")
        print(f"   💡 Usa verifica_account.py dalla repository")

def main():
    """Main reconstitution process"""
    print()
    print("=" * 70)
    print_emoji("🔄", "RICOSTITUZIONE ACCOUNT - DibTauroS/Ordo-ab-Chao")
    print("=" * 70)
    print()
    print("   Owner: Dib Anouar")
    print("   Framework: DibTauroS/Ordo-ab-Chao")
    print("   License: LUP v1.0 (uso personale e non commerciale)")
    print()
    
    try:
        # Step 1: Create directory structure
        setup_directory_structure()
        print()
        
        # Step 2: Create account configuration
        account_config = create_account_config()
        print()
        
        # Step 3: Reconstitute environment file with new tokens
        tokens = reconstitute_env_file()
        print()
        
        # Step 4: Setup allowlist
        setup_allowlist()
        print()
        
        # Step 5: Create account documentation
        create_account_readme()
        print()
        
        # Step 6: Update .gitignore
        create_gitignore_entries()
        print()
        
        # Step 7: Ensure verification script exists
        ensure_verification_script()
        print()
        
        print("=" * 70)
        print_emoji("✅", "RICOSTITUZIONE COMPLETATA CON SUCCESSO!")
        print("=" * 70)
        print()
        
        print_emoji("📊", "Riepilogo:")
        print(f"   ✅ Account ID: {account_config['account_id']}")
        print(f"   ✅ Configurazione creata: copilot-agent/config/account.json")
        print(f"   ✅ Nuovi token di sicurezza generati")
        print(f"   ✅ Allowlist configurata")
        print(f"   ✅ Struttura directory completa")
        print(f"   ✅ Documentazione aggiornata")
        print()
        
        print_emoji("🔒", "Sicurezza:")
        print(f"   🔑 Secret Key: {tokens['secret_key'][:16]}...{tokens['secret_key'][-16:]}")
        print(f"   🔑 API Token: {tokens['api_token'][:16]}...{tokens['api_token'][-16:]}")
        print(f"   ⚠️  CONSERVARE QUESTI TOKEN IN MODO SICURO!")
        print()
        
        print_emoji("📖", "Prossimi passi:")
        print("   1. Verifica configurazione: python3 verifica_account.py")
        print("   2. Personalizza allowlist: edit allowlist.json")
        print("   3. Avvia Copilot Agent: cd copilot-agent && python3 core/copilot_agent.py --status")
        print("   4. Consulta documentazione: docs/account/README_ACCOUNT.md")
        print()
        
        print_emoji("💾", "Backup:")
        backup_files = list(Path("copilot-agent/config").glob(".env.copilot.backup.*"))
        if backup_files:
            print(f"   📦 {len(backup_files)} file di backup creati")
            for backup in backup_files[-3:]:  # Show last 3
                print(f"      - {backup.name}")
        print()
        
        return 0
        
    except KeyboardInterrupt:
        print()
        print_emoji("❌", "Ricostituzione interrotta dall'utente")
        return 1
    except Exception as e:
        print()
        print_emoji("❌", f"Errore durante la ricostituzione: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
