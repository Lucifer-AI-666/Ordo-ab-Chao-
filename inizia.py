#!/usr/bin/env python3
"""
Inizializzazione repository priv-cyber-agents
Organizza la struttura del progetto e configura l'ambiente base
Usage: python3 inizia.py
"""

import os
import sys
import shutil
import json
from datetime import datetime, timezone
from pathlib import Path

def print_emoji(emoji, message):
    """Print message with emoji (fallback for systems without emoji support)"""
    try:
        print(f"{emoji} {message}")
    except UnicodeEncodeError:
        print(f"[{emoji}] {message}")

def main():
    print_emoji("🚀", "Inizializzazione priv-cyber-agents...")
    print("   Titolare/Owner: Dib Anouar")
    print("   Licenza: LUP v1.0 (uso personale e non commerciale)")
    print("")

    # Create directory structure
    print_emoji("📁", "Creazione struttura directory...")
    directories = [
        "01-tauros", "02-lucy", "scripts", "docs", "legal", 
        "gateway", "tests", "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

    # Organize existing files
    print_emoji("📋", "Organizzazione file esistenti...")
    
    file_moves = [
        ("TaurosPrivateAgent_Version2.Modelfile", "01-tauros/TaurosPrivateAgent.Modelfile"),
        ("LucyPrivateAgent_Version2.Modelfile", "02-lucy/LucyPrivateAgent.Modelfile"),
        ("primo_CopilotPrivateAgent_Version3.Modelfile", "01-tauros/CopilotPrivateAgent.Modelfile"),
        ("scripts_make-zip_Version3.sh", "scripts/make-zip.sh"),
        ("scripts_make-zip_Version3.ps1", "scripts/make-zip.ps1"),
        ("legal_DPA_GDPR_Template_IT_Version3.md", "legal/DPA_GDPR_Template_IT.md"),
    ]
    
    for source, dest in file_moves:
        if Path(source).exists():
            shutil.move(source, dest)
            if dest.endswith('.sh'):
                os.chmod(dest, 0o755)  # Make executable
            print(f"   ✅ {Path(source).name} -> {Path(dest).parent}/")

    # Create allowlist.json if it doesn't exist
    allowlist_path = Path("allowlist.json")
    if not allowlist_path.exists():
        allowlist_data = {
            "allowed_targets": [
                "localhost",
                "127.0.0.1",
                "192.168.1.0/24"
            ],
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        with open(allowlist_path, 'w') as f:
            json.dump(allowlist_data, f, indent=2)
        print("   ✅ allowlist.json creato")

    # Create README files
    print_emoji("📝", "Creazione README per le directory...")

    readme_files = {
        "01-tauros/README.md": """# Tauros Private Agent

Modello Ollama con guardrail ferrei per uso personale/privato.

## Setup
```bash
cd 01-tauros
ollama create tauros_private -f TaurosPrivateAgent.Modelfile
ollama run tauros_private
```

## Utilizzo
- DEFEND (sempre consentito): comandi di ispezione e monitoraggio
- TEST (gated): richiede keyword "Wassim" + allowlist + privilegi admin
""",
        "02-lucy/README.md": """# Lucy Private Agent

Agente Python locale con policy rigorose, audit e catena d'integrità.

## Setup
```bash
cd 02-lucy
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp ../allowlist.json .
```

## Configurazione
- File config: lucy.toml
- Mode: DEFEND (default) o TEST (gated)
- Log: logs/lucy.log con catena SHA-256
""",
        "gateway/README.md": """# Gateway API Locale

FastAPI con token Bearer per orchestrare Lucy da client esterni fidati.

## Setup
```bash
cd gateway
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
export AGENT_GATEWAY_TOKEN=$(python3 -c "import secrets;print(secrets.token_hex(24))")
uvicorn gateway.agent_gateway:app --host 127.0.0.1 --port 8787
```

## Endpoint
- POST /monitor
- POST /install_tool
- POST /local_pentest
"""
    }

    for file_path, content in readme_files.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # Create requirements.txt files if they don't exist
    requirements_files = {
        "02-lucy/requirements.txt": [
            "toml>=0.10.2",
            "psutil>=5.9.0", 
            "requests>=2.28.0",
            "cryptography>=3.4.8"
        ],
        "gateway/requirements.txt": [
            "fastapi>=0.95.0",
            "uvicorn[standard]>=0.20.0",
            "python-multipart>=0.0.6"
        ]
    }

    for file_path, packages in requirements_files.items():
        if not Path(file_path).exists():
            with open(file_path, 'w') as f:
                f.write('\n'.join(packages) + '\n')
            print(f"   ✅ {file_path} creato")

    # Clean up temporary files
    print_emoji("🧹", "Pulizia file temporanei...")
    temp_files = [
        "Nuovo Documento di testo.txt",
        "invoice_*.pdf"
    ]
    
    for pattern in temp_files:
        for file_path in Path(".").glob(pattern):
            try:
                file_path.unlink()
            except OSError:
                pass

    # Clean up zip files
    for zip_file in Path(".").glob("files*.zip"):
        try:
            zip_file.unlink()
        except OSError:
            pass

    print("")
    print_emoji("✅", "Inizializzazione completata!")
    print("")
    print_emoji("📖", "Prossimi passi:")
    print("   1. Controlla allowlist.json e personalizza i target")
    print("   2. Setup Tauros: cd 01-tauros && ollama create tauros_private -f TaurosPrivateAgent.Modelfile")
    print("   3. Setup Lucy: cd 02-lucy && python3 -m venv .venv && pip install -r requirements.txt")
    print("   4. (Opzionale) Setup Gateway: cd gateway && python3 -m venv .venv && pip install -r requirements.txt")
    print("")
    print_emoji("🔒", "Sicurezza:")
    print("   - Tutti i servizi sono legati a 127.0.0.1 (solo loopback)")
    print("   - Azioni invasive richiedono modalità TEST + keyword 'Wassim'")
    print("   - Audit trail in logs/ con catena SHA-256")
    print("")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Inizializzazione interrotta dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Errore durante l'inizializzazione: {e}")
        sys.exit(1)