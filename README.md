# Ordo-ab-Chao

App Android minimale con pagina web locale integrata negli asset.

## Contenuto del progetto

```
app/
  src/main/AndroidManifest.xml
  src/main/java/com/lucifer/ordoabchao/MainActivity.java
  src/main/res/layout/activity_main.xml
  src/main/assets/index.html
build.gradle
settings.gradle
```

## Requisiti

- JDK 11+
- Android SDK (compileSdk/targetSdk 34)
- Gradle installato nel sistema (in questo repository non è presente il wrapper `gradlew`)

## Build APK (debug)

1. Crea/aggiorna `local.properties` nella root del repo con il path SDK:

   ```properties
   sdk.dir=/percorso/al/tuo/Android/Sdk
   ```

2. Esegui la build dalla root:

   ```bash
   gradle assembleDebug
   ```

3. APK generato in:

   `app/build/outputs/apk/debug/app-debug.apk`

## Comportamento app

- `MainActivity` carica `file:///android_asset/index.html`
- WebView con JavaScript disabilitato per default
- Permesso Internet presente nel manifest

## Script utili repository

```bash
python3 controlla_commit.py
./controlla_commit.sh
python3 verifica.py
```

Dettagli in `docs/COMMIT_VERIFICATION.md`.

## Sicurezza

- Mantieni JavaScript disabilitato in WebView se non strettamente necessario
- Installa ed esegui l’APK solo su dispositivi fidati
