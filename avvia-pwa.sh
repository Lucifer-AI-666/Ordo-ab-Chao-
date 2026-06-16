#!/usr/bin/env bash
# Ordo ab Chao - Script Avvio PWA
# Avvia il server web e apre il browser

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="${SCRIPT_DIR}/docs"
PORT="${PORT:-8000}"
URL="http://localhost:${PORT}/login.html"

echo "🔥 ORDO AB CHAO - Avvio PWA 🔥"
echo ""
echo "📂 Directory: ${DOCS_DIR}"
echo "🌐 URL: ${URL}"
echo ""

if [ ! -d "${DOCS_DIR}" ]; then
    echo "❌ Directory docs non trovata: ${DOCS_DIR}"
    exit 1
fi

# Controlla se la porta è già in uso
if command -v lsof >/dev/null 2>&1 && lsof -iTCP:"${PORT}" -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Porta ${PORT} già in uso!"
    echo "🔄 Fermando processo esistente..."
    existing_pid="$(lsof -t -iTCP:"${PORT}" -sTCP:LISTEN | head -n 1)"
    if [ -n "${existing_pid}" ]; then
        if ! kill "${existing_pid}"; then
            echo "❌ Impossibile fermare il processo ${existing_pid} sulla porta ${PORT}."
            exit 1
        fi
        sleep 1
    fi

    if lsof -iTCP:"${PORT}" -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "❌ La porta ${PORT} è ancora occupata. Chiudi il processo esistente e riprova."
        exit 1
    fi
fi

open_browser() {
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "${URL}" >/dev/null 2>&1 &
    elif command -v open >/dev/null 2>&1; then
        open "${URL}" >/dev/null 2>&1 &
    elif command -v start >/dev/null 2>&1; then
        start "${URL}" >/dev/null 2>&1 &
    else
        echo "ℹ️  Apri manualmente: ${URL}"
    fi
}

echo "🚀 Avvio server web..."
echo ""
echo "✅ Server in esecuzione su ${URL}"
echo "🌐 Apertura browser automatica..."
echo ""
echo "⚠️  Premi CTRL+C per fermare il server"
echo ""

# Aspetta un secondo prima di aprire il browser
sleep 2

# Apri browser
open_browser

# Avvia server Python
python3 -m http.server "${PORT}" --directory "${DOCS_DIR}"
