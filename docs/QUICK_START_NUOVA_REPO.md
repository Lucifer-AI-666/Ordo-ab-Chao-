# 🚀 Quick Start: Creare una Nuova Repository

Guida rapida per iniziare subito con un nuovo progetto.

## ⚡ Metodo Veloce (1 minuto)

```bash
# 1. Vai nella cartella Ordo ab Chao
cd ~/Ordo-ab-Chao-

# 2. Esegui lo script
./scripts/init-nuovo-progetto.sh nome-progetto "Descrizione" tipo

# 3. Il progetto è pronto in ~/Projects/nome-progetto
```

### Tipi Disponibili
- `python` - Per bot, script, API backend
- `nodejs` - Per applicazioni Node.js, API REST
- `web` - Per PWA, siti web, dashboard

## 📝 Esempi Pratici

### Esempio 1: Bot Telegram Python
```bash
./scripts/init-nuovo-progetto.sh tauros-bot "Bot Telegram con AI" python
cd ~/Projects/tauros-bot
python3 -m venv venv
source venv/bin/activate
pip install python-telegram-bot
```

### Esempio 2: Web App Node.js
```bash
./scripts/init-nuovo-progetto.sh my-api "REST API Server" nodejs
cd ~/Projects/my-api
npm install express
npm start
```

### Esempio 3: Progressive Web App
```bash
./scripts/init-nuovo-progetto.sh dashboard "Dashboard Admin" web
cd ~/Projects/dashboard
python3 -m http.server 8000
# Apri http://localhost:8000
```

## 🔗 Collegare a GitHub

Dopo aver creato il progetto:

```bash
# 1. Crea repository su GitHub
# Vai su: https://github.com/new
# Nome: nome-progetto (stesso nome usato nello script)

# 2. Collega repository locale
cd ~/Projects/nome-progetto
git remote add origin git@github.com:Lucifer-AI-666/nome-progetto.git
git push -u origin main

# ✅ Fatto!
```

## 📦 Aggiungere al Mission Control

Modifica `~/Ordo-ab-Chao-/docs/projects.html`:

```javascript
// Trova projectsData array e aggiungi:
{
    name: "🆕 Nome Progetto",
    path: "/Users/dib/Projects/nome-progetto",
    github: "https://github.com/Lucifer-AI-666/nome-progetto",
    description: "Descrizione breve",
    status: "Development",
    actions: [
        {
            label: "🚀 Avvia",
            command: "npm start"  // o il comando appropriato
        },
        {
            label: "🐙 GitHub",
            url: "https://github.com/Lucifer-AI-666/nome-progetto"
        }
    ]
}
```

## 💾 Backup con Scatola Nera

```bash
cd ~/Ordo-ab-Chao-
python3 scatola-nera.py snapshot "Aggiunto nuovo progetto: nome-progetto"
```

## 🎯 Workflow Completo (3 minuti)

```bash
# 1. Crea progetto
cd ~/Ordo-ab-Chao-
./scripts/init-nuovo-progetto.sh awesome-bot "Bot fantastico" python

# 2. Crea repo su GitHub
open https://github.com/new

# 3. Collega e push
cd ~/Projects/awesome-bot
git remote add origin git@github.com:Lucifer-AI-666/awesome-bot.git
git push -u origin main

# 4. Sviluppa
python3 -m venv venv
source venv/bin/activate
# ... sviluppo ...

# 5. Backup
cd ~/Ordo-ab-Chao-
python3 scatola-nera.py snapshot "Progetto awesome-bot inizializzato"

# ✅ Tutto fatto!
```

## 📚 Risorse

- **Guida Completa**: [docs/GUIDA_NUOVA_REPO.md](GUIDA_NUOVA_REPO.md)
- **Template**: [../templates/README.md](../templates/README.md)
- **Script**: [../scripts/init-nuovo-progetto.sh](../scripts/init-nuovo-progetto.sh)

## 💡 Tips

1. **Nome semplice**: Usa nomi brevi senza spazi (usa trattini)
2. **Descrizione chiara**: Spiega cosa fa il progetto in 5-10 parole
3. **Tipo giusto**: Scegli il tipo appropriato per il progetto
4. **Git config**: Verifica che git sia configurato con `git config --global user.name`
5. **SSH keys**: Configura SSH per GitHub per push senza password

## 🆘 Problemi Comuni

**Script non eseguibile:**
```bash
chmod +x ~/Ordo-ab-Chao-/scripts/init-nuovo-progetto.sh
```

**Git non configurato:**
```bash
git config --global user.name "Lucifer-AI-666"
git config --global user.email "your-email@example.com"
```

**Directory Projects non esiste:**
Lo script la crea automaticamente in `~/Projects`

---

**Creato da Lucifer-AI-666**  
**Parte di Ordo ab Chao** 🚀
