#!/usr/bin/env bash
# Inizializzazione repository priv-cyber-agents
# Organizza la struttura del progetto e configura l'ambiente base
# Usage: ./inizia.sh

set -euo pipefail

echo "🚀 Inizializzazione priv-cyber-agents..."
echo "   Titolare/Owner: Dib Anouar"
echo "   Licenza: LUP v1.0 (uso personale e non commerciale)"
echo ""

# Crea la struttura delle directory
echo "📁 Creazione struttura directory..."
mkdir -p {01-tauros,02-lucy,scripts,docs,legal,gateway,tests}
mkdir -p logs

# Organizza i file esistenti nella struttura corretta
echo "📋 Organizzazione file esistenti..."

# Sposta i Modelfile nella directory corretta
if [ -f "TaurosPrivateAgent_Version2.Modelfile" ]; then
    mv "TaurosPrivateAgent_Version2.Modelfile" "01-tauros/TaurosPrivateAgent.Modelfile"
    echo "   ✅ Tauros Modelfile -> 01-tauros/"
fi

if [ -f "LucyPrivateAgent_Version2.Modelfile" ]; then
    mv "LucyPrivateAgent_Version2.Modelfile" "02-lucy/LucyPrivateAgent.Modelfile"
    echo "   ✅ Lucy Modelfile -> 02-lucy/"
fi

if [ -f "primo_CopilotPrivateAgent_Version3.Modelfile" ]; then
    mv "primo_CopilotPrivateAgent_Version3.Modelfile" "01-tauros/CopilotPrivateAgent.Modelfile"
    echo "   ✅ Copilot Modelfile -> 01-tauros/"
fi

# Sposta script nella directory corretta
if [ -f "scripts_make-zip_Version3.sh" ]; then
    mv "scripts_make-zip_Version3.sh" "scripts/make-zip.sh"
    chmod +x "scripts/make-zip.sh"
    echo "   ✅ make-zip script -> scripts/"
fi

if [ -f "scripts_make-zip_Version3.ps1" ]; then
    mv "scripts_make-zip_Version3.ps1" "scripts/make-zip.ps1"
    echo "   ✅ make-zip PowerShell -> scripts/"
fi

# Sposta documentazione legale
if [ -f "legal_DPA_GDPR_Template_IT_Version3.md" ]; then
    mv "legal_DPA_GDPR_Template_IT_Version3.md" "legal/DPA_GDPR_Template_IT.md"
    echo "   ✅ DPA GDPR template -> legal/"
fi

# Crea allowlist.json dal template se non esiste
if [ ! -f "allowlist.json" ]; then
    cat > allowlist.json << 'EOF'
{
  "allowed_targets": [
    "localhost",
    "127.0.0.1",
    "192.168.1.0/24"
  ],
  "last_updated": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
}
EOF
    echo "   ✅ allowlist.json creato"
fi

# Crea README per ogni directory
echo "📝 Creazione README per le directory..."

cat > 01-tauros/README.md << 'EOF'
# Tauros Private Agent

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
EOF

cat > 02-lucy/README.md << 'EOF'
# Lucy Private Agent

Agente Python locale con policy rigorose, audit e catena d'integrità.

## Setup
```bash
cd 02-lucy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../allowlist.json .
```

## Configurazione
- File config: lucy.toml
- Mode: DEFEND (default) o TEST (gated)
- Log: logs/lucy.log con catena SHA-256
EOF

cat > gateway/README.md << 'EOF'
# Gateway API Locale

FastAPI con token Bearer per orchestrare Lucy da client esterni fidati.

## Setup
```bash
cd gateway
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export AGENT_GATEWAY_TOKEN=$(python3 -c "import secrets;print(secrets.token_hex(24))")
uvicorn gateway.agent_gateway:app --host 127.0.0.1 --port 8787
```

## Endpoint
- POST /monitor
- POST /install_tool
- POST /local_pentest
EOF

# Crea file requirements.txt di base se non esistono
if [ ! -f "02-lucy/requirements.txt" ]; then
    cat > 02-lucy/requirements.txt << 'EOF'
toml>=0.10.2
psutil>=5.9.0
requests>=2.28.0
cryptography>=3.4.8
EOF
    echo "   ✅ 02-lucy/requirements.txt creato"
fi

if [ ! -f "gateway/requirements.txt" ]; then
    cat > gateway/requirements.txt << 'EOF'
fastapi>=0.95.0
uvicorn[standard]>=0.20.0
python-multipart>=0.0.6
EOF
    echo "   ✅ gateway/requirements.txt creato"
fi

# Pulisci file temporanei e versioni multiple
echo "🧹 Pulizia file temporanei..."
rm -f "Nuovo Documento di testo.txt" 2>/dev/null || true
rm -f files*.zip 2>/dev/null || true
rm -f invoice_*.pdf 2>/dev/null || true

echo ""
echo "✅ Inizializzazione completata!"
echo ""
echo "📖 Prossimi passi:"
echo "   1. Controlla allowlist.json e personalizza i target"
echo "   2. Setup Tauros: cd 01-tauros && ollama create tauros_private -f TaurosPrivateAgent.Modelfile"
echo "   3. Setup Lucy: cd 02-lucy && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
echo "   4. (Opzionale) Setup Gateway: cd gateway && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
echo ""
echo "🔒 Sicurezza:"
echo "   - Tutti i servizi sono legati a 127.0.0.1 (solo loopback)"
echo "   - Azioni invasive richiedono modalità TEST + keyword 'Wassim'"
echo "   - Audit trail in logs/ con catena SHA-256"
echo ""