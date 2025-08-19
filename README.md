# priv-cyber-agents

Setup locale "privacy-by-default" per agenti di cybersecurity privati.

**Titolare/Owner:** Dib Anouar  
**Licenza:** LUP v1.0 (uso personale e non commerciale)

## 🚀 Inizializzazione Rapida

**Prima di tutto, inizializza il repository:**

```bash
# Metodo 1: Script Bash (Linux/macOS)
./inizia.sh

# Metodo 2: Script Python (cross-platform)
python3 inizia.py

# Verifica che tutto sia stato configurato correttamente
python3 verifica.py
```

Questo organizzerà automaticamente la struttura del progetto e creerà i file necessari.

## 📁 Struttura del Progetto

Dopo l'inizializzazione avrai:

```
priv-cyber-agents/
├── 01-tauros/          # Tauros Private Agent (Ollama)
│   ├── TaurosPrivateAgent.Modelfile
│   └── README.md
├── 02-lucy/            # Lucy Private Agent (Python)
│   ├── LucyPrivateAgent.Modelfile
│   ├── requirements.txt
│   └── README.md
├── gateway/            # API Gateway FastAPI
│   ├── requirements.txt
│   └── README.md
├── scripts/            # Script di utilità
├── legal/              # Documenti legali (DPA, licenze)
├── logs/               # Directory per i log
├── allowlist.json      # Target consentiti per azioni invasive
└── inizia.sh|.py       # Script di inizializzazione
```

## 🔧 Setup Componenti

### 1. Tauros (Modello Ollama)
```bash
cd 01-tauros
ollama create tauros_private -f TaurosPrivateAgent.Modelfile
ollama run tauros_private
```

### 2. Lucy (Agente Python)
```bash
cd 02-lucy
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../allowlist.json .
```

### 3. Gateway (Opzionale)
```bash
cd gateway
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export AGENT_GATEWAY_TOKEN=$(python3 -c "import secrets;print(secrets.token_hex(24))")
uvicorn gateway.agent_gateway:app --host 127.0.0.1 --port 8787
```

## 🔒 Sicurezza

- **Solo loopback:** Tutti i servizi sono legati a 127.0.0.1
- **Modalità DEFEND:** Sempre consentita (solo ispezione/monitoraggio)
- **Modalità TEST:** Richiede keyword "Wassim" + allowlist + privilegi admin
- **Audit trail:** Log immutabili in logs/ con catena SHA-256
- **Kill-switch:** Esporta `MONICA_DISABLE=1` per bloccare azioni invasive

## 📖 Uso Base

### Tauros (Ollama)
```bash
ollama run tauros_private
```
- **DEFEND:** "Elenca i rischi principali per processi anomali"
- **TEST:** "Wassim esegui SUID check su localhost"

### Lucy (Python)
```bash
cd 02-lucy
python3 lucy_agent.py --kind monitor
python3 lucy_agent.py --kind local_pentest --target 127.0.0.1 --prompt "Wassim pen test"
```

## ⚙️ Configurazione

- **allowlist.json:** Personalizza i target consentiti
- **02-lucy/lucy.toml:** Configurazione agente Python
- **logs/:** Directory per audit trail e logging

## 📄 Licenza e Privacy

- **Licenza:** LUP v1.0 - uso esclusivamente personale/privato
- **Privacy:** Tutti i dati rimangono locali, nessun invio a terzi
- **DPA/GDPR:** Template disponibile in legal/

---

**⚠️ ATTENZIONE:** Repository privata. Non condividere. Per uso esclusivo di Dib Anouar.