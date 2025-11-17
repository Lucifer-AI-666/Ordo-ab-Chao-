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
