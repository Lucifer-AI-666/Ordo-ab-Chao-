#!/bin/bash

# 🚀 Script di Inizializzazione Nuovo Progetto
# Parte del sistema Ordo ab Chao
# Autore: Lucifer-AI-666

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║         🚀 ORDO AB CHAO - Nuovo Progetto 🚀            ║"
echo "║                                                          ║"
echo "║              Inizializzazione Repository                ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Funzione per mostrare help
show_help() {
    echo -e "${CYAN}Utilizzo:${NC}"
    echo "  ./init-nuovo-progetto.sh <nome-progetto> [descrizione] [tipo]"
    echo ""
    echo -e "${CYAN}Parametri:${NC}"
    echo "  nome-progetto  : Nome del progetto (richiesto)"
    echo "  descrizione    : Descrizione breve (opzionale)"
    echo "  tipo           : python|nodejs|web (default: web)"
    echo ""
    echo -e "${CYAN}Esempi:${NC}"
    echo "  ./init-nuovo-progetto.sh mio-bot"
    echo "  ./init-nuovo-progetto.sh mio-bot \"Bot Telegram AI\" python"
    echo "  ./init-nuovo-progetto.sh mia-pwa \"PWA fantastica\" web"
    echo ""
    exit 0
}

# Check parametri
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    show_help
fi

if [ -z "$1" ]; then
    echo -e "${RED}❌ ERRORE: Nome progetto richiesto${NC}"
    show_help
fi

# Variabili
PROJECT_NAME=$1
PROJECT_DESC=${2:-"Nuovo progetto creato con Ordo ab Chao"}
PROJECT_TYPE=${3:-"web"}
PROJECTS_DIR="$HOME/Projects"
PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"
GITHUB_USER="Lucifer-AI-666"

echo -e "${BLUE}📋 Configurazione:${NC}"
echo -e "  Nome:        ${GREEN}$PROJECT_NAME${NC}"
echo -e "  Descrizione: ${GREEN}$PROJECT_DESC${NC}"
echo -e "  Tipo:        ${GREEN}$PROJECT_TYPE${NC}"
echo -e "  Path:        ${GREEN}$PROJECT_PATH${NC}"
echo ""

# Verifica se il progetto esiste già
if [ -d "$PROJECT_PATH" ]; then
    echo -e "${RED}❌ ERRORE: Il progetto $PROJECT_NAME esiste già in $PROJECT_PATH${NC}"
    exit 1
fi

# Crea directory progetti se non esiste
if [ ! -d "$PROJECTS_DIR" ]; then
    echo -e "${YELLOW}📁 Creazione directory Projects...${NC}"
    mkdir -p "$PROJECTS_DIR"
fi

# Crea directory progetto
echo -e "${YELLOW}📁 Creazione directory progetto...${NC}"
mkdir -p "$PROJECT_PATH"
cd "$PROJECT_PATH"

# Inizializza Git
echo -e "${YELLOW}🔧 Inizializzazione Git...${NC}"
git init
git branch -M main

# Funzione per creare struttura Python
create_python_structure() {
    echo -e "${YELLOW}🐍 Creazione struttura Python...${NC}"
    
    # Directories
    mkdir -p src tests docs scripts
    
    # Files
    touch src/__init__.py
    touch src/main.py
    touch tests/__init__.py
    touch tests/test_main.py
    touch requirements.txt
    touch .env.example
    
    # src/main.py
    cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Main module for the project
"""

def main():
    """Main entry point"""
    print("🚀 Hello from Ordo ab Chao!")

if __name__ == "__main__":
    main()
EOF
    
    # requirements.txt
    cat > requirements.txt << 'EOF'
# Dipendenze base
python-dotenv>=1.0.0

# Aggiungi altre dipendenze qui
EOF
    
    # .gitignore
    cat > .gitignore << 'EOF'
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
EOF
}

# Funzione per creare struttura Node.js
create_nodejs_structure() {
    echo -e "${YELLOW}📦 Creazione struttura Node.js...${NC}"
    
    # Directories
    mkdir -p src tests docs public
    
    # Files
    touch src/index.js
    touch tests/index.test.js
    
    # package.json
    cat > package.json << EOF
{
  "name": "$PROJECT_NAME",
  "version": "1.0.0",
  "description": "$PROJECT_DESC",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "test": "echo \\"Error: no test specified\\" && exit 1"
  },
  "keywords": [],
  "author": "$GITHUB_USER",
  "license": "MIT"
}
EOF
    
    # src/index.js
    cat > src/index.js << 'EOF'
/**
 * Main entry point
 */

console.log('🚀 Hello from Ordo ab Chao!');

module.exports = {};
EOF
    
    # .gitignore
    cat > .gitignore << 'EOF'
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
EOF
}

# Funzione per creare struttura Web/PWA
create_web_structure() {
    echo -e "${YELLOW}🌐 Creazione struttura Web/PWA...${NC}"
    
    # Directories
    mkdir -p css js images docs
    
    # index.html
    cat > index.html << EOF
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="$PROJECT_DESC">
    <title>$PROJECT_NAME</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#6366f1">
</head>
<body>
    <header>
        <h1>⚡ $PROJECT_NAME ⚡</h1>
        <p>$PROJECT_DESC</p>
    </header>
    
    <main>
        <div class="container">
            <h2>🚀 Benvenuto!</h2>
            <p>Progetto creato con Ordo ab Chao</p>
        </div>
    </main>
    
    <footer>
        <p>Creato da $GITHUB_USER - 2025</p>
    </footer>
    
    <script src="js/app.js"></script>
</body>
</html>
EOF
    
    # css/style.css
    cat > css/style.css << 'EOF'
/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

header {
    text-align: center;
    padding: 2rem;
    color: white;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

main {
    padding: 2rem;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

footer {
    text-align: center;
    padding: 2rem;
    color: white;
    font-size: 0.9rem;
}
EOF
    
    # js/app.js
    cat > js/app.js << 'EOF'
/**
 * Main application JavaScript
 */

console.log('🚀 App initialized');

// Service Worker registration (PWA)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then(reg => console.log('✅ Service Worker registered'))
            .catch(err => console.error('❌ Service Worker registration failed:', err));
    });
}
EOF
    
    # manifest.json
    cat > manifest.json << EOF
{
  "name": "$PROJECT_NAME",
  "short_name": "$PROJECT_NAME",
  "description": "$PROJECT_DESC",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#6366f1",
  "theme_color": "#6366f1",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "images/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "images/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
EOF
    
    # service-worker.js
    cat > service-worker.js << 'EOF'
const CACHE_NAME = 'v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/css/style.css',
    '/js/app.js'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});
EOF
    
    # .gitignore
    cat > .gitignore << 'EOF'
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

# Build (se usi bundler)
dist/
build/
node_modules/
EOF
}

# Crea struttura in base al tipo
case $PROJECT_TYPE in
    python)
        create_python_structure
        ;;
    nodejs|node)
        create_nodejs_structure
        ;;
    web|pwa)
        create_web_structure
        ;;
    *)
        echo -e "${RED}❌ ERRORE: Tipo progetto non valido. Usa: python, nodejs, o web${NC}"
        exit 1
        ;;
esac

# README.md
echo -e "${YELLOW}📝 Creazione README.md...${NC}"
cat > README.md << EOF
# $PROJECT_NAME

$PROJECT_DESC

## 🎯 Caratteristiche

- Feature 1
- Feature 2
- Feature 3

## 🚀 Installazione

\`\`\`bash
# Clone repository
git clone https://github.com/$GITHUB_USER/$PROJECT_NAME.git
cd $PROJECT_NAME
EOF

if [ "$PROJECT_TYPE" == "python" ]; then
    cat >> README.md << 'EOF'

# Crea virtual environment
python3 -m venv venv
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Configura environment
cp .env.example .env
# Modifica .env con le tue configurazioni

# Avvia progetto
python src/main.py
EOF
elif [ "$PROJECT_TYPE" == "nodejs" ] || [ "$PROJECT_TYPE" == "node" ]; then
    cat >> README.md << 'EOF'

# Installa dipendenze
npm install

# Avvia progetto
npm start
EOF
else
    cat >> README.md << 'EOF'

# Avvia server locale
python3 -m http.server 8000
# Oppure usa Live Server in VS Code
EOF
fi

cat >> README.md << EOF
\`\`\`

## 📖 Utilizzo

Istruzioni per utilizzare il progetto.

## 🧪 Testing

\`\`\`bash
# Aggiungi comandi di test qui
\`\`\`

## 📝 License

MIT License - vedi [LICENSE](LICENSE)

## 👤 Autore

**$GITHUB_USER**
- GitHub: [@$GITHUB_USER](https://github.com/$GITHUB_USER)
- WhatsApp: +39 333 525 5525

---

**Creato con Ordo ab Chao** 🚀
EOF

# LICENSE
echo -e "${YELLOW}📄 Creazione LICENSE...${NC}"
cat > LICENSE << EOF
MIT License

Copyright (c) $(date +%Y) $GITHUB_USER

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
EOF

# Primo commit
echo -e "${YELLOW}📦 Creazione commit iniziale...${NC}"
git add .
git commit -m "🎉 Initial commit - Progetto creato con Ordo ab Chao"

# Riepilogo
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                          ║${NC}"
echo -e "${GREEN}║              ✅ PROGETTO CREATO CON SUCCESSO! ✅         ║${NC}"
echo -e "${GREEN}║                                                          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📊 Riepilogo:${NC}"
echo -e "  Nome:     ${GREEN}$PROJECT_NAME${NC}"
echo -e "  Tipo:     ${GREEN}$PROJECT_TYPE${NC}"
echo -e "  Path:     ${GREEN}$PROJECT_PATH${NC}"
echo -e "  Commit:   ${GREEN}✅ Initial commit creato${NC}"
echo ""
echo -e "${CYAN}🔗 Prossimi passi:${NC}"
echo ""
echo -e "  1️⃣  Vai al progetto:"
echo -e "      ${YELLOW}cd $PROJECT_PATH${NC}"
echo ""
echo -e "  2️⃣  Crea repository su GitHub:"
echo -e "      ${YELLOW}https://github.com/new${NC}"
echo -e "      Nome: ${GREEN}$PROJECT_NAME${NC}"
echo ""
echo -e "  3️⃣  Collega repository remota:"
echo -e "      ${YELLOW}git remote add origin git@github.com:$GITHUB_USER/$PROJECT_NAME.git${NC}"
echo -e "      ${YELLOW}git push -u origin main${NC}"
echo ""
echo -e "  4️⃣  Aggiungi al Mission Control:"
echo -e "      Modifica: ${YELLOW}~/Ordo-ab-Chao-/docs/projects.html${NC}"
echo ""
echo -e "  5️⃣  Crea snapshot con Scatola Nera:"
echo -e "      ${YELLOW}cd ~/Ordo-ab-Chao-${NC}"
echo -e "      ${YELLOW}python3 scatola-nera.py snapshot \"Aggiunto $PROJECT_NAME\"${NC}"
echo ""
echo -e "${PURPLE}🚀 Buon lavoro fratello! 🚀${NC}"
echo ""
