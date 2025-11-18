#!/usr/bin/env bash
# Crea un archivio zip della cartella del progetto, escludendo artefatti e cache.
# Uso:
#   bash scripts/make-zip.sh
# Output:
#   priv-cyber-agents-YYYYmmddHHMM.zip (nella directory superiore)

set -euo pipefail

# Calcola root repo (script in scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

STAMP="$(date -u +'%Y%m%d%H%M')"
OUT="../priv-cyber-agents-$STAMP.zip"

# Lista esclusioni
EXCLUDES=(
  ".git/*"
  "logs/*"
  ".venv/*"
  "venv/*"
  "dist/*"
  "build/*"
  ".gradle/*"
  "android-app/app/build/*"
  ".DS_Store"
  "Thumbs.db"
)

# Se zip non c'è, prova tar.gz
if ! command -v zip >/dev/null 2>&1; then
  echo "[info] 'zip' non trovato, uso tar.gz"
  TAR_OUT="../priv-cyber-agents-$STAMP.tar.gz"
  tar --exclude-vcs \
      $(printf -- "--exclude=%q " "${EXCLUDES[@]}") \
      -czf "$TAR_OUT" .
  echo "[ok] Creato: $TAR_OUT"
  exit 0
fi

# Prepara args -x per zip
XARGS=()
for p in "${EXCLUDES[@]}"; do
  XARGS+=(-x "$p")
done

# Crea zip
zip -r "$OUT" . "${XARGS[@]}"
echo "[ok] Creato: $OUT"