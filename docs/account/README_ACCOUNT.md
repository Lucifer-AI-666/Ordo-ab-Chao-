# Account Dib Anouar - DibTauroS/Ordo-ab-Chao

## Informazioni Account

- **Owner**: Dib Anouar
- **Framework**: DibTauroS/Ordo-ab-Chao
- **License**: LUP v1.0 (uso personale e non commerciale)
- **Ricostituito**: 2025-11-05T19:49:17.689814+00:00

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
python3 ricostituzione_account.py --rotate-tokens
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
