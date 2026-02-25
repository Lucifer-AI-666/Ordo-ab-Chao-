# 📦 Template per Nuovi Progetti

Questa directory contiene template predefiniti per creare nuovi progetti rapidamente.

## 🚀 Utilizzo

### Metodo 1: Script Automatico (Consigliato)

Usa lo script di inizializzazione dalla root di Ordo ab Chao:

```bash
./scripts/init-nuovo-progetto.sh <nome-progetto> [descrizione] [tipo]
```

**Esempi:**
```bash
# Crea progetto Python
./scripts/init-nuovo-progetto.sh mio-bot "Bot Telegram" python

# Crea progetto Node.js
./scripts/init-nuovo-progetto.sh mia-app "App fantastica" nodejs

# Crea progetto Web/PWA
./scripts/init-nuovo-progetto.sh mia-pwa "PWA moderna" web
```

## 📝 Template Disponibili

Lo script genera automaticamente la struttura corretta in base al tipo scelto.

### Python Template
- Struttura src/tests/docs
- requirements.txt
- .gitignore configurato

### Node.js Template
- package.json configurato
- Struttura src/tests/public
- .gitignore configurato

### Web/PWA Template
- HTML/CSS/JS structure
- manifest.json (PWA)
- service-worker.js

## 🔗 Risorse

- [Guida completa creazione repository](../docs/GUIDA_NUOVA_REPO.md)
- [Script inizializzazione](../scripts/init-nuovo-progetto.sh)

---

**Parte del progetto Ordo ab Chao**
**by Lucifer-AI-666**
