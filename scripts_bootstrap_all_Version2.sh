#!/usr/bin/env bash
# Crea l'intera struttura "priv-cyber-agents" con TUTTI i file e genera uno .zip finale.
# Uso:
#   bash scripts/bootstrap_all.sh [DEST_DIR]
# Default DEST_DIR: ./priv-cyber-agents

set -euo pipefail

DEST="${1:-priv-cyber-agents}"
STAMP="$(date -u +'%Y%m%d%H%M')"
OUT_ZIP="../priv-cyber-agents-$STAMP.zip"

mkdir -p "$DEST"
mkdir -p "$DEST"/{01-tauros,02-lucy,scripts,docs,legal,gateway,.github/workflows,tests}

write() {
  local path="$1"
  shift
  mkdir -p "$(dirname "$path")"
  cat > "$path" <<'EOF'
'"$@"'
EOF
}

# ---------------- Root files ----------------
write "$DEST/.gitignore" '```gitignore
# Secrets & credenziali
*.env
*.key
allowlist.json
systemd/*.env
keystore.jks
*.keystore
keystore.properties

# Log
logs/
*.log
02-lucy/*.jsonl
02-lucy/*chain*.sha256

# Cache & temp
__pycache__/
*.pyc
*.pyo
*.tmp
.venv/
venv/

# Output modello
*.bin
*.gguf

# Build output
.dist/
dist/
build/
.gradle/

# Android (se presente)
android-app/app/build/
android-app/.gradle/
android-app/.cxx/
android-app/.idea/
android-app/local.properties

# Editor/OS
.vscode/
.idea/
.DS_Store
Thumbs.db
```'

write "$DEST/allowlist.example.json" '```json
{
  "allowed_targets": [
    "localhost",
    "127.0.0.1",
    "192.168.1.10"
  ]
}
```'

write "$DEST/README.md" '````markdown
# priv-cyber-agents

Setup locale “privacy-by-default” per due agent di cybersecurity:
- 01-tauros: modello Ollama con guardrail.
- 02-lucy: agente Python locale con policy, audit e allowlist.
- scripts/: hardening firewall per Linux/Windows.
- legal/: DPA_B2B (uso enterprise) + Licenza Enterprise.
- README_PRIVACY.md: principi di sicurezza e uso consentito.

Titolare/Owner: Dib Anouar
Licenza: LUP v1.0 (uso personale e non commerciale) o Licenza Enterprise per uso B2B.

Struttura
- 01-tauros/
  - TaurosPrivateAgent.Modelfile
  - README.md
- 02-lucy/
  - LucyPrivateAgent.Modelfile
  - lucy.toml
  - lucy_agent.py
  - lucy.service
  - requirements.txt
  - README.md
- scripts/
  - firewall_lock_linux.sh
  - firewall_lock_windows.ps1
  - make-zip.sh
  - make-zip.ps1
- legal/
  - DPA_B2B_IT.md
  - LICENSE_ENTERPRISE_IT.md
  - LUP_LICENSE_IT.md
- docs/
  - ARCHITETTURA.md
  - MAPPA_MENTALE.md
- gateway/ (opzionale)
  - README.md
  - agent_gateway.py
  - requirements.txt
  - SYSTEMD.md
- .github/workflows/ci.yml
- tests/test_policy.py
- README_PRIVACY.md

Note rapide
- Allowlist: usa allowlist.json (non committato, vedi allowlist.example.json).
- Loopback: mantieni Ollama e gateway su 127.0.0.1, proteggi con firewall.
- Gated actions: richiedono “TEST” + keyword “Wassim” + allowlist + privilegi admin.

Istruzioni base (offline)
- Lucy:
  - cd 02-lucy
  - python3 -m venv .venv && source .venv/bin/activate
  - pip install -r requirements.txt
  - cp ../allowlist.example.json ../allowlist.json
  - python3 lucy_agent.py --kind monitor
- Tauros (Ollama):
  - cd 01-tauros
  - ollama create tauros_private -f TaurosPrivateAgent.Modelfile
  - ollama run tauros_private
- Firewall:
  - Linux: sudo bash scripts/firewall_lock_linux.sh
  - Windows (Admin): ./scripts/firewall_lock_windows.ps1
- Gateway (opzionale, sempre 127.0.0.1 di default):
  - cd gateway && python3 -m venv .venv && source .venv/bin/activate
  - pip install -r requirements.txt
  - export AGENT_GATEWAY_TOKEN=$(python3 - <<<'import secrets;print(secrets.token_hex(16))')
  - uvicorn gateway.agent_gateway:app --host 127.0.0.1 --port 8787
````'

write "$DEST/README_PRIVACY.md" '````markdown
# README Privacy & Sicurezza — priv-cyber-agents
Titolare/Owner: Dib Anouar
Licenza: LUP v1.0 (uso personale e non commerciale) oppure Licenza Enterprise (uso B2B) — vedi legal/

Principi di sicurezza (privacy-by-default)
- Tutto in locale: nessun dato inviato a terzi per impostazione predefinita.
- Least privilege: azioni invasive eseguite solo quando strettamente necessario.
- Gated actions: modalità TEST richiede keyword “Wassim”, allowlist valida e privilegi adeguati.
- Allowlist centralizzata: file condiviso allowlist.json controllato dagli agenti per target invasivi.
- Audit e integrità: log append-only, rotazione e catena di integrità SHA-256/HMAC (Lucy).
- Gestione segreti: token/chiavi fuori VCS, in env o file protetti (chmod 600).
- Superficie di rete minima: servizi vincolati a 127.0.0.1. Su LAN solo con firewall e, preferibilmente, TLS/mTLS.

Uso consentito (LUP v1.0/Enterprise)
- Personale: uso privato non commerciale.
- Enterprise: uso interno al Cliente come da LICENSE_ENTERPRISE_IT.md e DPA_B2B_IT.md.
- Vietato: distribuzione pubblica, SaaS, addestramento AI, text/data mining.

Operativa chiave
- Allowlist: copia allowlist.example.json in allowlist.json e personalizza i target.
- Modalità: DEFEND di default; per TEST includi “Wassim” nel prompt.
- Log: file locali (es. logs/lucy.log), con rotazione e catena SHA-256/HMAC (LUCY_HMAC_KEY opzionale).
- Firewall: usa scripts/firewall_lock_* con logging su logs/firewall.log.
````'

# ---------------- Tauros ----------------
write "$DEST/01-tauros/README.md" '````markdown
# Tauros Private Agent

Modello Ollama con guardrail ferrei per uso personale/privato di Dib Anouar.

Creazione modello
```bash
cd 01-tauros
ollama create tauros_private -f TaurosPrivateAgent.Modelfile