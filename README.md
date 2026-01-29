# Ordo-ab-Chao - Minimal Android App + Webpage

Questo commit crea una app Android nativa minimale e una pagina web integrata negli assets.

Struttura proposta:
- app/: modulo Android minimale
  - src/main/AndroidManifest.xml
  - src/main/java/com/lucifer/ordoabchao/MainActivity.java
  - src/main/res/layout/activity_main.xml
  - src/main/assets/index.html
- build.gradle (root)
- settings.gradle
- web/index.html (opzionale, copia di assets)

Prerequisiti per build:
- JDK 11+ (o JDK compatibile con Gradle/AGP in uso)
- Android SDK (Android 34 platform se possibile)
- Gradle wrapper (opzionale; puoi usare il gradle installato o creare il wrapper)

Istruzioni rapide:
1. Posiziona i file nelle cartelle indicate.
2. Imposta `local.properties` con il percorso SDK (es. `sdk.dir=C:\Users\You\AppData\Local\Android\Sdk` su Windows).
3. Esegui (da root del progetto):
   - `./gradlew assembleDebug`  (o `gradlew.bat assembleDebug` su Windows)
4. APK risultante: `app/build/outputs/apk/debug/app-debug.apk`
5. Per testare la pagina web senza APK, apri `web/index.html` nel browser.

## Core Utilities

The project includes a comprehensive suite of Unix utilities for development and security operations:

```bash
# Quick access
./coreutils <command> [options]

# Common commands
./coreutils gitinfo          # Repository information
./coreutils sysinfo          # System information
./coreutils cleanup          # Clean temporary files
./coreutils search "*.py"    # Find Python files
./coreutils checksum verify  # Verify file integrity
```

See [docs/COREUTILS.md](docs/COREUTILS.md) and [utils/README.md](utils/README.md) for complete documentation.

## Verifica Repository

Per verificare lo stato del repository e dei commit:
```bash
# Verifica completa (Python - consigliato)
python3 controlla_commit.py

# Verifica rapida (Shell)
./controlla_commit.sh

# Verifica inizializzazione
python3 verifica.py

# Using coreutils
./coreutils gitinfo
```

Vedi [docs/COMMIT_VERIFICATION.md](docs/COMMIT_VERIFICATION.md) per dettagli.

Nota di sicurezza:
- Questa app è minimale e richiede poche dipendenze. Disabilita JavaScript nella WebView per sicurezza.
- Non eseguire l'APK su dispositivi che non controlli.