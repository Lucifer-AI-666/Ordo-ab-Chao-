# Guida alla Ricostituzione Account

## DibTauroS/Ordo-ab-Chao Framework
**Owner**: Dib Anouar  
**License**: LUP v1.0 (uso personale e non commerciale)

---

## Panoramica

La ricostituzione account è un processo completo che ricrea tutta la configurazione dell'account utente per il framework DibTauroS/Ordo-ab-Chao. Questo processo è utile per:

- **Setup iniziale**: Configurare l'account per la prima volta
- **Reset completo**: Ripristinare l'account a uno stato pulito
- **Rotazione token**: Generare nuovi token di sicurezza
- **Ripristino da backup**: Ricreare la configurazione dopo un problema

## Componenti Ricostituiti

La ricostituzione account crea e configura:

### 1. Configurazione Account
- **File**: `copilot-agent/config/account.json`
- **Contiene**: Informazioni owner, framework, versione, account ID univoco
- **Permessi**: 600 (read/write solo per owner)

### 2. Environment Configuration
- **File**: `copilot-agent/config/.env.copilot`
- **Contiene**: Token di sicurezza, configurazione servizi, feature flags
- **Permessi**: 600 (read/write solo per owner)
- **Backup**: Automatico con timestamp prima di ogni ricostituzione

### 3. Allowlist
- **File**: `allowlist.json` e `copilot-agent/config/allowlist.json`
- **Contiene**: Lista dei target autorizzati per operazioni di sicurezza
- **Default**: localhost, 127.0.0.1, 192.168.1.0/24

### 4. Struttura Directory
```
├── logs/
│   ├── copilot/
│   ├── tauros/
│   └── lucy/
├── copilot-agent/
│   ├── config/
│   └── logs/
├── 01-tauros/
│   └── logs/
├── 02-lucy/
│   └── logs/
├── gateway/
│   └── logs/
├── tests/
│   └── results/
└── docs/
    └── account/
```

### 5. Documentazione
- **File**: `docs/account/README_ACCOUNT.md`
- **Contiene**: Guida completa alla gestione account

## Utilizzo

### Ricostituzione Completa

```bash
python3 ricostituzione_account.py
```

**Output**:
- Nuovi token di sicurezza generati (Secret Key e API Token)
- Backup automatico della configurazione precedente
- Configurazione account completa creata
- Allowlist configurata
- Struttura directory completa
- Documentazione aggiornata

### Verifica Account

```bash
python3 verifica_account.py
```

Verifica:
- ✅ File di configurazione presenti
- ✅ Variabili d'ambiente configurate
- ✅ Struttura directory completa
- ✅ Informazioni account valide

### Backup Account

```bash
python3 backup_account.py
```

Crea:
- Backup completo della configurazione
- Archivio compresso `.tar.gz`
- Manifest con elenco file e dimensioni
- README con istruzioni ripristino

## Token di Sicurezza

### Generazione

I token vengono generati automaticamente durante la ricostituzione:

```python
# Secret Key: 64 caratteri esadecimali
COPILOT_SECRET_KEY=eb5aebd902f90f7c0114b3d199fcc5599ec2df0077a91d462e928e66fb8d4e8e

# API Token: 64 caratteri esadecimali
COPILOT_API_TOKEN=a0e17bc10af70ff5f96b4c8f2335a26a5202cad154015e615a9ec549f8117f65
```

### Sicurezza Token

⚠️ **IMPORTANTE**:
1. I token sono **generati casualmente** con `secrets.token_hex(32)`
2. Ogni ricostituzione genera **nuovi token univoci**
3. I vecchi token vengono salvati in **backup con timestamp**
4. **NON condividere mai** i token
5. **NON committare** il file `.env.copilot` in Git

### Rotazione Token

Per ruotare i token:

```bash
# Metodo 1: Ricostituzione completa (raccomandato)
python3 ricostituzione_account.py

# Metodo 2: Generazione manuale
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
python3 -c "import secrets; print('API_TOKEN=' + secrets.token_hex(32))"
```

Dopo la rotazione:
1. Aggiornare tutti i servizi che usano i token
2. Riavviare i servizi (gateway, copilot-agent, etc.)
3. Verificare che tutto funzioni: `python3 verifica_account.py`

## Backup e Ripristino

### Creare Backup

```bash
python3 backup_account.py
```

Output:
- `backups/account_backup_YYYYMMDD_HHMMSS/` - Directory backup
- `backups/account_backup_YYYYMMDD_HHMMSS.tar.gz` - Archivio compresso

### Protezione Backup

⚠️ **Il backup contiene token sensibili!**

Raccomandazioni:
1. **Cifrare** l'archivio:
   ```bash
   gpg -c backups/account_backup_YYYYMMDD_HHMMSS.tar.gz
   ```

2. **Spostare** in posizione sicura:
   ```bash
   mv backups/account_backup_*.tar.gz /percorso/sicuro/
   ```

3. **Eliminare** backup obsoleti in modo sicuro:
   ```bash
   shred -u backups/account_backup_*.tar.gz
   ```

### Ripristinare da Backup

```bash
# 1. Estrarre backup
tar -xzf backups/account_backup_YYYYMMDD_HHMMSS.tar.gz

# 2. Copiare file di configurazione
cp account_backup_YYYYMMDD_HHMMSS/configuration_files/copilot-agent/config/.env.copilot \
   copilot-agent/config/.env.copilot

# 3. Verificare
python3 verifica_account.py

# 4. Riavviare servizi
# systemctl restart gateway
# etc.
```

## File di Configurazione

### .env.copilot

Variabili principali:

```bash
# Security
MONICA_DISABLE=0                    # Kill-switch (0=enabled, 1=disabled)
COPILOT_MODE=DEFEND                 # Modalità operativa default

# Network
COPILOT_HOST=127.0.0.1             # Bind solo a localhost
COPILOT_PORT=8787                   # Porta web interface

# Logging
LOG_LEVEL=INFO                      # Livello logging
LOG_RETENTION_DAYS=30               # Giorni ritenzione log

# Ollama
OLLAMA_HOST=127.0.0.1
OLLAMA_PORT=11434
OLLAMA_MODEL=mistral:7b-instruct

# Security Keys (GENERATED)
COPILOT_SECRET_KEY=...              # Generato automaticamente
COPILOT_API_TOKEN=...               # Generato automaticamente
```

### account.json

```json
{
  "owner": {
    "name": "Dib Anouar",
    "framework": "DibTauroS/Ordo-ab-Chao",
    "license": "LUP v1.0"
  },
  "created_at": "2025-11-05T19:49:17.688822+00:00",
  "version": "1.0.0",
  "account_id": "3e2030099f8cab1b"
}
```

### allowlist.json

```json
{
  "allowed_targets": [
    "localhost",
    "127.0.0.1",
    "192.168.1.0/24"
  ],
  "last_updated": "2025-11-05T19:49:17.689500+00:00",
  "owner": "Dib Anouar"
}
```

## Sicurezza

### Protezione File

I file sensibili sono protetti:

```bash
# Permessi restrittivi
chmod 600 copilot-agent/config/.env.copilot
chmod 600 copilot-agent/config/account.json

# .gitignore automatico
.env.copilot                        # File con token
*.backup.*                          # Tutti i backup
copilot-agent/config/account.json   # Configurazione account
backups/                            # Directory backup
```

### Best Practices

1. **Non committare** file sensibili in Git
2. **Usare** `.env.copilot.example` come template
3. **Ruotare** i token periodicamente (es. ogni 3 mesi)
4. **Verificare** l'account dopo ogni modifica
5. **Creare backup** prima di modifiche importanti
6. **Cifrare** i backup con GPG o simili
7. **Eliminare** in modo sicuro i backup obsoleti

### Emergency Kill-Switch

Per disabilitare tutte le operazioni immediatamente:

```bash
# Metodo 1: Variabile d'ambiente
export MONICA_DISABLE=1

# Metodo 2: File .env.copilot
# Modifica: MONICA_DISABLE=1

# Metodo 3: Stop servizi
systemctl stop gateway
systemctl stop copilot-agent
```

## Troubleshooting

### Account non configurato

**Sintomo**: `verifica_account.py` riporta file mancanti

**Soluzione**:
```bash
python3 ricostituzione_account.py
python3 verifica_account.py
```

### Token non validi

**Sintomo**: Errori di autenticazione

**Soluzione**:
```bash
# Ricostituzione genera nuovi token
python3 ricostituzione_account.py

# Riavvia servizi
systemctl restart gateway
```

### Permessi file errati

**Sintomo**: Errori di accesso ai file

**Soluzione**:
```bash
# Fix permessi
chmod 600 copilot-agent/config/.env.copilot
chmod 600 copilot-agent/config/account.json
chmod 644 copilot-agent/config/.env.copilot.example
```

### Backup corrotto

**Sintomo**: Impossibile estrarre backup

**Soluzione**:
```bash
# Verifica integrità
tar -tzf backups/account_backup_*.tar.gz

# Se corrotto, usa backup precedente o ricostituzione
python3 ricostituzione_account.py
```

## Riferimenti

- **Setup**: `ricostituzione_account.py` - Script ricostituzione completa
- **Verifica**: `verifica_account.py` - Script verifica configurazione
- **Backup**: `backup_account.py` - Script backup account
- **Documentazione**: `docs/account/README_ACCOUNT.md` - Guida dettagliata

## Supporto

Per problemi o domande:
1. Consulta questa documentazione
2. Esegui `python3 verifica_account.py` per diagnostica
3. Controlla i log in `logs/`
4. Riferisci il README principale del progetto

---

**Framework**: DibTauroS/Ordo-ab-Chao  
**Owner**: Dib Anouar  
**License**: LUP v1.0 (Personal & Non-Commercial Use Only)  
**Versione**: 1.0.0
