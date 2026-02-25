# 🎯 Esempi di Integrazione Mission Control

Questa guida mostra come integrare i nuovi progetti creati nel Mission Control di Ordo ab Chao.

## 📋 Modifiche Necessarie

Quando crei un nuovo progetto, aggiorna il file `docs/projects.html` per includerlo nel Mission Control.

## 🔧 Esempio 1: Progetto Python (Bot)

### Progetto Creato
```bash
./scripts/init-nuovo-progetto.sh tauros-ai "Bot Telegram con AI" python
```

### Integrazione Mission Control

Apri `docs/projects.html` e aggiungi nel array `projectsData`:

```javascript
{
    name: "🤖 TaurosAI Bot",
    path: "/Users/dib/Projects/tauros-ai",
    github: "https://github.com/Lucifer-AI-666/tauros-ai",
    description: "Bot Telegram con AI locale",
    status: "Development",
    language: "Python",
    actions: [
        {
            label: "🚀 Avvia Bot",
            command: "cd ~/Projects/tauros-ai && source venv/bin/activate && python src/main.py"
        },
        {
            label: "⚙️ Config",
            command: "code ~/Projects/tauros-ai/.env"
        },
        {
            label: "📊 Logs",
            command: "tail -f ~/Projects/tauros-ai/logs/bot.log"
        },
        {
            label: "🐙 GitHub",
            url: "https://github.com/Lucifer-AI-666/tauros-ai"
        }
    ]
}
```

### Aggiungi anche al tab GitHub Repos

Nel array `githubRepos`:

```javascript
{
    name: "tauros-ai",
    description: "Bot Telegram con AI locale e modelli Mistral",
    language: "Python",
    stars: 0,
    url: "https://github.com/Lucifer-AI-666/tauros-ai",
    status: "Development"
}
```

## 🌐 Esempio 2: Progetto Web (PWA)

### Progetto Creato
```bash
./scripts/init-nuovo-progetto.sh dashboard-admin "Dashboard amministrazione" web
```

### Integrazione Mission Control

```javascript
{
    name: "📊 Dashboard Admin",
    path: "/Users/dib/Projects/dashboard-admin",
    github: "https://github.com/Lucifer-AI-666/dashboard-admin",
    description: "Dashboard amministrazione web",
    status: "Active",
    language: "JavaScript",
    actions: [
        {
            label: "🚀 Avvia",
            command: "cd ~/Projects/dashboard-admin && python3 -m http.server 8080 &"
        },
        {
            label: "🌐 Apri Browser",
            url: "http://localhost:8080"
        },
        {
            label: "💻 VS Code",
            command: "code ~/Projects/dashboard-admin"
        },
        {
            label: "🚀 Deploy Vercel",
            command: "cd ~/Projects/dashboard-admin && vercel --prod"
        },
        {
            label: "🐙 GitHub",
            url: "https://github.com/Lucifer-AI-666/dashboard-admin"
        }
    ]
}
```

### Se deployato su Vercel

Aggiungi nel tab Vercel (array `vercelDeployments`):

```javascript
{
    name: "Dashboard Admin",
    domain: "dashboard-admin.vercel.app",
    github: "Lucifer-AI-666/dashboard-admin",
    status: "Active",
    lastDeploy: new Date().toISOString(),
    actions: [
        {
            label: "🌐 Visita",
            url: "https://dashboard-admin.vercel.app"
        },
        {
            label: "▲ Dashboard",
            url: "https://vercel.com/Lucifer-AI-666/dashboard-admin"
        },
        {
            label: "🚀 Deploy",
            command: "cd ~/Projects/dashboard-admin && vercel --prod"
        }
    ]
}
```

## 📦 Esempio 3: Progetto Node.js (API)

### Progetto Creato
```bash
./scripts/init-nuovo-progetto.sh api-server "REST API Server" nodejs
```

### Integrazione Mission Control

```javascript
{
    name: "🔌 API Server",
    path: "/Users/dib/Projects/api-server",
    github: "https://github.com/Lucifer-AI-666/api-server",
    description: "REST API Server con Express.js",
    status: "Development",
    language: "JavaScript",
    actions: [
        {
            label: "🚀 Avvia",
            command: "cd ~/Projects/api-server && npm start"
        },
        {
            label: "🧪 Test",
            command: "cd ~/Projects/api-server && npm test"
        },
        {
            label: "📝 Logs",
            command: "cd ~/Projects/api-server && npm run logs"
        },
        {
            label: "💻 VS Code",
            command: "code ~/Projects/api-server"
        },
        {
            label: "🐙 GitHub",
            url: "https://github.com/Lucifer-AI-666/api-server"
        }
    ]
}
```

## 🎨 Customizzazione Icone

Per aggiungere icone personalizzate ai progetti:

```javascript
{
    name: "🎨 Nome Progetto",  // Usa emoji Unicode
    // oppure
    name: "Nome Progetto",
    icon: "path/to/icon.png",  // Path relativo a docs/
    // ...
}
```

## 📊 Status Disponibili

Usa questi status per indicare lo stato del progetto:

- `"Active"` - Progetto attivo e in produzione
- `"Development"` - In sviluppo attivo
- `"Archived"` - Archiviato, non più mantenuto
- `"Maintenance"` - Solo manutenzione, feature freeze
- `"Planning"` - In fase di pianificazione

## 🔍 Filtri e Ricerca

I progetti nel Mission Control possono essere filtrati per:
- Status
- Linguaggio
- Nome

Assicurati di impostare correttamente questi campi:

```javascript
{
    name: "Nome Progetto",
    language: "Python",  // Python, JavaScript, TypeScript, Go, etc.
    status: "Development",
    // ...
}
```

## 💡 Best Practices

1. **Comandi assoluti**: Usa path completi nei comandi
   ```javascript
   command: "cd ~/Projects/nome-progetto && npm start"
   ```

2. **Descrizioni chiare**: Spiega cosa fa il progetto
   ```javascript
   description: "Bot Telegram per gestione task con AI"
   ```

3. **Actions utili**: Aggiungi azioni che usi frequentemente
   ```javascript
   actions: [
       { label: "Avvia", command: "..." },
       { label: "Test", command: "..." },
       { label: "Logs", command: "..." },
       { label: "GitHub", url: "..." }
   ]
   ```

4. **Mantieni sincronizzato**: Aggiorna status quando cambia
   ```javascript
   status: "Development"  // → "Active" quando rilasci in produzione
   ```

## 🔄 Template Completo

```javascript
{
    // Info base
    name: "🎯 Nome Progetto",
    description: "Descrizione breve e chiara",
    path: "/Users/dib/Projects/nome-progetto",
    
    // GitHub
    github: "https://github.com/Lucifer-AI-666/nome-progetto",
    
    // Metadata
    status: "Development",  // Active, Development, Archived, Maintenance
    language: "Python",     // Python, JavaScript, TypeScript, Go, etc.
    
    // Azioni rapide
    actions: [
        {
            label: "🚀 Avvia",
            command: "cd ~/Projects/nome-progetto && comando-avvio"
        },
        {
            label: "🧪 Test",
            command: "cd ~/Projects/nome-progetto && comando-test"
        },
        {
            label: "💻 VS Code",
            command: "code ~/Projects/nome-progetto"
        },
        {
            label: "🌐 Apri",
            url: "http://localhost:8000"  // Se applicabile
        },
        {
            label: "🐙 GitHub",
            url: "https://github.com/Lucifer-AI-666/nome-progetto"
        }
    ]
}
```

## 🔗 File da Modificare

1. **docs/projects.html** - Mission Control principale
   - Array `projectsData` (tab Progetti)
   - Array `githubRepos` (tab GitHub Repos)
   - Array `vercelDeployments` (tab Vercel, se applicabile)

2. **Scatola Nera** - Crea snapshot dopo le modifiche
   ```bash
   cd ~/Ordo-ab-Chao-
   python3 scatola-nera.py snapshot "Aggiunto progetto nome-progetto al Mission Control"
   ```

3. **Git** - Commit e push
   ```bash
   cd ~/Ordo-ab-Chao-
   git add docs/projects.html
   git commit -m "Aggiunto progetto nome-progetto al Mission Control"
   git push
   ```

## ✅ Checklist Integrazione

Dopo aver creato un nuovo progetto:

- [ ] Aggiunto a `projectsData` in docs/projects.html
- [ ] Aggiunto a `githubRepos` in docs/projects.html
- [ ] Se deployato, aggiunto a `vercelDeployments`
- [ ] Testato che le azioni funzionino
- [ ] Creato snapshot con scatola-nera
- [ ] Commit e push su GitHub
- [ ] Verificato nel Mission Control (apri docs/projects.html)

---

**Parte di Ordo ab Chao**  
**by Lucifer-AI-666** 🚀
