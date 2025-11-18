#!/bin/bash
# Ordo ab Chao - Script Avvio PWA
# Avvia il server web e apre il browser

echo "🔥 ORDO AB CHAO - Avvio PWA 🔥"
echo ""
echo "📂 Directory: /Users/dib/Ordo-ab-Chao-/web"
echo "🌐 URL: http://localhost:8000"
echo ""

# Controlla se porta 8000 è già in uso
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Porta 8000 già in uso!"
    echo "🔄 Fermando processo esistente..."
    kill -9 $(lsof -t -i:8000)
    sleep 1
fi

# Vai nella cartella web
cd /Users/dib/Ordo-ab-Chao-/web

echo "🚀 Avvio server web..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🔐 CREDENZIALI LOGIN:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Admin:   admin / ordo2025"
echo "  Lucifer: lucifer / chaos666"
echo "  User:    user / user123"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Server in esecuzione su http://localhost:8000"
echo "🌐 Apertura browser automatica..."
echo ""
echo "⚠️  Premi CTRL+C per fermare il server"
echo ""

# Aspetta un secondo prima di aprire il browser
sleep 2

# Apri browser
open http://localhost:8000/login.html

# Avvia server Python
python3 -m http.server 8000
