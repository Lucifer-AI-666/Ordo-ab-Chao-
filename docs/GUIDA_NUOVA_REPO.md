# 🚀 Guida: Creare una Nuova Repository

## 📋 Indice
1. [Prerequisiti](#prerequisiti)
2. [Creazione Repository su GitHub](#creazione-repository-su-github)
3. [Inizializzazione Locale](#inizializzazione-locale)
4. [Struttura Progetto Consigliata](#struttura-progetto-consigliata)
5. [Configurazione Base](#configurazione-base)
6. [Integrazione con Ordo ab Chao](#integrazione-con-ordo-ab-chao)
7. [Deploy e CI/CD](#deploy-e-cicd)

---

## 📚 Prerequisiti

Prima di creare una nuova repository, assicurati di avere:

- ✅ Account GitHub configurato (@Lucifer-AI-666)
- ✅ Git installato e configurato localmente
- ✅ SSH keys configurate per GitHub
- ✅ Accesso al Mission Control di Ordo ab Chao
- ✅ Python 3.9+ e/o Node.js (secondo il tipo di progetto)

### Verifica Configurazione Git

```bash
# Verifica configurazione
git config --global user.name
git config --global user.email

# Se necessario, configura
git config --global user.name "Lucifer-AI-666"
git config --global user.email "your-email@example.com"
```

---

## 🐙 Creazione Repository su GitHub

### Metodo 1: Via Web (Consigliato)

1. **Vai su GitHub**
   - Apri: https://github.com/new
   - Oppure: Mission Control → GitHub Repos → "New Repository"

2. **Compila il Form**
   - **Repository name**: Nome del progetto (es. `nuovo-progetto`)
   - **Description**: Descrizione breve e chiara
   - **Public/Private**: Scegli visibilità
   - **Initialize with**:
     - ✅ Add a README file (consigliato)
     - ✅ Add .gitignore (scegli template appropriato)
     - ✅ Choose a license (MIT consigliato per open source)

3. **Crea Repository**
   - Clicca "Create repository"
   - Copia l'URL SSH/HTTPS della repo

### Metodo 2: Via GitHub CLI

```bash
# Installa GitHub CLI se non presente
brew install gh  # macOS
# oppure
sudo apt install gh  # Linux

# Login
gh auth login

# Crea repository
gh repo create Lucifer-AI-666/nuovo-progetto \
  --public \
  --description "Descrizione del progetto" \
  --clone
```

---

## 💻 Inizializzazione Locale

### Opzione A: Clone Repository Esistente

Se hai già creato la repo su GitHub:

```bash
# Clone via SSH (consigliato)
git clone git@github.com:Lucifer-AI-666/nuovo-progetto.git
cd nuovo-progetto

# Oppure via HTTPS
git clone https://github.com/Lucifer-AI-666/nuovo-progetto.git
cd nuovo-progetto
```

### Opzione B: Inizializzazione da Zero

Se vuoi creare prima il progetto localmente:

```bash
# Crea cartella progetto
mkdir nuovo-progetto
cd nuovo-progetto

# Inizializza Git
git init

# Crea README
echo "# Nuovo Progetto" > README.md

# Primo commit
git add README.md
git commit -m "Initial commit"

# Collega a repository remota (crea prima su GitHub)
git remote add origin git@github.com:Lucifer-AI-666/nuovo-progetto.git
git branch -M main
git push -u origin main
```

### Opzione C: Usa Script di Inizializzazione

Usa lo script incluso in Ordo ab Chao:

```bash
# Torna alla cartella Ordo ab Chao
cd ~/Ordo-ab-Chao-

# Esegui script di inizializzazione
./scripts/init-nuovo-progetto.sh nuovo-progetto "Descrizione progetto"
```

---

## 📁 Struttura Progetto Consigliata

### Progetto Python

```
nuovo-progetto/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── setup.py (opzionale)
├── .env.example
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
│   └── README.md
└── scripts/
    └── deploy.sh
```

### Progetto Node.js/JavaScript

```
nuovo-progetto/
├── README.md
├── LICENSE
├── .gitignore
├── package.json
├── .env.example
├── .eslintrc.js (opzionale)
├── .prettierrc (opzionale)
├── src/
│   ├── index.js
│   └── components/
├── public/
│   └── index.html
├── tests/
│   └── index.test.js
└── docs/
    └── API.md
```

### Progetto Web/PWA

```
nuovo-progetto/
├── README.md
├── LICENSE
├── .gitignore
├── index.html
├── manifest.json
├── service-worker.js
├── css/
│   └── style.css
├── js/
│   └── app.js
├── images/
│   └── icon-192.png
└── docs/
    └── INSTALL.md
```

---

## ⚙️ Configurazione Base

### .gitignore

**Per Python:**
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv
pip-log.txt
pip-delete-this-directory.txt

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Build
dist/
build/
*.egg-info/
```

**Per Node.js:**
```gitignore
# Node
node_modules/
npm-debug.log
yarn-error.log
.npm
.yarn

# Build
dist/
build/
.next/
out/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.production

# Testing
coverage/
.nyc_output/
```

### README.md Template

```markdown
# Nome Progetto

Breve descrizione del progetto (1-2 righe).

## 🎯 Caratteristiche

- Feature 1
- Feature 2
- Feature 3

## 🚀 Installazione

\`\`\`bash
# Clone repository
git clone https://github.com/Lucifer-AI-666/nome-progetto.git
cd nome-progetto

# Installa dipendenze
npm install  # oppure pip install -r requirements.txt

# Configura environment
cp .env.example .env
# Modifica .env con le tue configurazioni

# Avvia progetto
npm start  # oppure python src/main.py
\`\`\`

## 📖 Utilizzo

Istruzioni base per utilizzare il progetto.

## 🧪 Testing

\`\`\`bash
npm test  # oppure pytest
\`\`\`

## 📝 License

MIT License - vedi [LICENSE](LICENSE)

## 👤 Autore

**Lucifer-AI-666**
- GitHub: [@Lucifer-AI-666](https://github.com/Lucifer-AI-666)
- WhatsApp: +39 333 525 5525
```

### LICENSE (MIT)

```
MIT License

Copyright (c) 2025 Lucifer-AI-666

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🔗 Integrazione con Ordo ab Chao

### 1. Aggiungi Progetto al Mission Control

Modifica il file `docs/projects.html` per aggiungere il nuovo progetto:

```javascript
// Aggiungi a projectsData array
{
    name: "🆕 Nuovo Progetto",
    path: "/path/to/nuovo-progetto",
    github: "https://github.com/Lucifer-AI-666/nuovo-progetto",
    description: "Descrizione breve",
    status: "Development",
    actions: [
        {
            label: "🚀 Avvia",
            command: "npm start"  // o comando appropriato
        },
        {
            label: "🐙 GitHub",
            url: "https://github.com/Lucifer-AI-666/nuovo-progetto"
        }
    ]
}
```

### 2. Aggiungi alla Lista GitHub Repos

Nel tab "GitHub Repos" del Mission Control:

```javascript
// Aggiungi a githubRepos array
{
    name: "nuovo-progetto",
    description: "Descrizione del progetto",
    language: "JavaScript",  // o Python, TypeScript, etc.
    stars: 0,
    url: "https://github.com/Lucifer-AI-666/nuovo-progetto",
    status: "Development"  // Active, Development, Archived
}
```

### 3. Crea Primo Snapshot

```bash
# Vai alla root di Ordo ab Chao
cd ~/Ordo-ab-Chao-

# Crea snapshot con il nuovo progetto
python3 scatola-nera.py snapshot "Aggiunto nuovo progetto: nuovo-progetto"
```

---

## 🚀 Deploy e CI/CD

### Deploy su Vercel

1. **Installa Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login**
   ```bash
   vercel login
   ```

3. **Deploy Progetto**
   ```bash
   cd nuovo-progetto
   vercel
   ```

4. **Deploy in Produzione**
   ```bash
   vercel --prod
   ```

5. **Aggiungi al Mission Control**
   Aggiorna `docs/projects.html` con il deployment:
   ```javascript
   {
       name: "Nuovo Progetto",
       domain: "nuovo-progetto.vercel.app",
       status: "Active",
       lastDeploy: new Date().toISOString()
   }
   ```

### GitHub Actions (CI/CD)

Crea `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm install
    
    - name: Run tests
      run: npm test
    
    - name: Build
      run: npm run build
```

---

## 🎯 Checklist Completamento

Dopo aver creato la nuova repository, verifica:

- [ ] ✅ Repository creata su GitHub
- [ ] ✅ Clone locale effettuato
- [ ] ✅ README.md compilato
- [ ] ✅ LICENSE aggiunta
- [ ] ✅ .gitignore configurato
- [ ] ✅ .env.example creato
- [ ] ✅ Dipendenze installate
- [ ] ✅ Primo commit pushato
- [ ] ✅ Aggiunto al Mission Control
- [ ] ✅ Snapshot creato con scatola-nera
- [ ] ✅ Deploy configurato (se applicabile)
- [ ] ✅ CI/CD configurato (opzionale)

---

## 🛠️ Comandi Utili

```bash
# Clone repository
git clone git@github.com:Lucifer-AI-666/nuovo-progetto.git

# Status e informazioni
git status
git log --oneline -10
git remote -v

# Commit e push
git add .
git commit -m "Descrizione modifiche"
git push origin main

# Branch
git branch nuovo-feature
git checkout nuovo-feature
git checkout -b altro-branch

# Pull e sync
git pull origin main
git fetch --all

# Tags
git tag v1.0.0
git push origin v1.0.0
```

---

## 📚 Risorse Utili

- **GitHub Docs**: https://docs.github.com
- **Git Book**: https://git-scm.com/book/it/v2
- **Vercel Docs**: https://vercel.com/docs
- **GitHub Actions**: https://docs.github.com/en/actions

---

## 💡 Tips & Best Practices

1. **Commit Frequenti**: Fai commit piccoli e frequenti con messaggi chiari
2. **Branch Strategy**: Usa branch per features, `main` per produzione
3. **Semantic Versioning**: Usa versioni semantiche (v1.0.0)
4. **Documentazione**: Mantieni README e docs aggiornati
5. **Testing**: Scrivi test prima di pushare
6. **Security**: Non committare mai credenziali o API keys
7. **Backup**: Usa scatola-nera per backup regolari
8. **Code Review**: Usa PR per revisione codice

---

## 📞 Supporto

Per problemi o domande:

- 💬 **WhatsApp**: +39 333 525 5525
- 🐙 **GitHub**: @Lucifer-AI-666
- 📧 **Email**: contact@lucifer-ai.dev

---

**Creato da Lucifer-AI-666**  
**Parte del progetto Ordo ab Chao**  
**2025**
