# Gateway API Locale

FastAPI con token Bearer per orchestrare Lucy da client esterni fidati.

## Setup
```bash
cd gateway
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export AGENT_GATEWAY_TOKEN=$(python3 -c "import secrets;print(secrets.token_hex(24))")
uvicorn gateway.agent_gateway:app --host 127.0.0.1 --port 8787
```

## Endpoint
- POST /monitor
- POST /install_tool
- POST /local_pentest
