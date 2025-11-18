# Lucy Private Agent

Agente Python locale con policy rigorose, audit e catena d'integrità.

## Setup
```bash
cd 02-lucy
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../allowlist.json .
```

## Configurazione
- File config: lucy.toml
- Mode: DEFEND (default) o TEST (gated)
- Log: logs/lucy.log con catena SHA-256
