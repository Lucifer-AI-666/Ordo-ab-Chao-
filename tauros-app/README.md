# TAUROS App

**Companion app per il sistema Tauros AI Bot** - Interfaccia mobile React Native/Expo per la gestione e comunicazione con il backend AI.

## 📱 Funzionalità

### Chat
- Interfaccia per comunicare con l'AI via REST API `/chat`
- Persistenza locale delle conversazioni con AsyncStorage
- Supporto per diversi modelli AI (llama3, mistral, codellama, phi3, gemma)
- Cronologia chat con possibilità di cancellazione

### Status Dashboard
- Monitoraggio servizi: Telegram Bot, FastAPI, Redis, Ollama
- Pull-to-refresh per aggiornamento stato
- Indicatori visivi per stato servizi (Online/Offline/Sconosciuto)
- Latenza di risposta per ogni servizio

### Impostazioni
- Configurazione URL backend Tauros AI
- Selezione modello AI da utilizzare
- Test connessione con feedback visivo
- Notifiche push per avvisi servizi offline

## 🏗️ Architettura

L'app si integra con l'architettura del backend Tauros:

```
┌─────────────────┐     ┌──────────────┐
│  TAUROS App     │────▶│   FastAPI    │
│  (React Native) │     │   Backend    │
└─────────────────┘     └──────┬───────┘
                               │
                    ┌──────────┼──────────┐
                    │          │          │
               ┌────▼────┐ ┌───▼───┐ ┌────▼─────┐
               │  Redis  │ │ Ollama│ │ Telegram │
               │ Caching │ │  AI   │ │   Bot    │
               └─────────┘ └───────┘ └──────────┘
```

## 🚀 Getting Started

### Prerequisiti
- Node.js 18+
- npm o yarn
- Expo CLI (`npm install -g expo-cli`)
- Expo Go app sul dispositivo mobile (per testing)

### Installazione

```bash
# Entra nella directory dell'app
cd tauros-app

# Installa le dipendenze
npm install

# Avvia il server di sviluppo
npx expo start
```

### Sviluppo

```bash
# Avvia su iOS Simulator
npx expo start --ios

# Avvia su Android Emulator
npx expo start --android

# Avvia su web
npx expo start --web
```

## 📁 Struttura Progetto

```
tauros-app/
├── App.tsx                    # Entry point principale
├── app.json                   # Configurazione Expo
├── tsconfig.json              # Configurazione TypeScript
├── package.json               # Dipendenze
├── assets/                    # Icone e splash screen
│   ├── icon.png
│   └── splash.png
└── src/
    ├── components/            # Componenti riutilizzabili
    │   ├── Loading.tsx
    │   └── ErrorBoundary.tsx
    ├── constants/             # Costanti applicazione
    │   └── routes.ts
    ├── screens/               # Schermate
    │   ├── ChatScreen.tsx
    │   ├── StatusScreen.tsx
    │   └── SettingsScreen.tsx
    ├── theme/                 # Sistema di design
    │   ├── index.ts
    │   ├── colors.ts
    │   ├── typography.ts
    │   └── layout.ts
    ├── types/                 # Definizioni TypeScript
    │   └── navigation.ts
    └── utils/                 # Utility e API
        └── api.ts
```

## 🔧 Configurazione

### URL Backend
Configura l'URL del tuo backend Tauros AI nelle impostazioni dell'app:
- Apri l'app
- Vai su "Impostazioni"
- Inserisci l'URL del backend (es. `http://192.168.1.100:8000`)
- Premi "Salva" e "Test Connessione"

### Modelli AI Supportati
- **Llama 3**: Modello principale, bilanciato
- **Mistral**: Veloce e preciso
- **CodeLlama**: Ottimizzato per codice
- **Phi-3**: Compatto ed efficiente
- **Gemma**: Google AI

## 🔐 Sicurezza

### Prossimi passi suggeriti:
1. Aggiungere autenticazione con API key per gli endpoint admin (`/admin/stats`, `/admin/clear-cache`)
2. Implementare notifiche push per avvisi quando un servizio va offline
3. Aggiungere supporto per connessioni HTTPS

## 📦 Build

### Android APK
```bash
npx expo build:android
# oppure con EAS
eas build --platform android
```

### iOS IPA
```bash
npx expo build:ios
# oppure con EAS
eas build --platform ios
```

## 🛠️ Tecnologie

- **React Native** + **Expo** - Framework mobile cross-platform
- **TypeScript** - Type safety
- **React Navigation** - Navigazione
- **AsyncStorage** - Persistenza locale
- **Expo StatusBar** - Gestione barra di stato

## 📝 API Endpoints

L'app comunica con i seguenti endpoint del backend:

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/chat` | POST | Invia messaggio all'AI |
| `/health` | GET | Health check principale |
| `/health/redis` | GET | Stato Redis |
| `/health/ollama` | GET | Stato Ollama |
| `/health/telegram` | GET | Stato Telegram Bot |

## 📄 Licenza

LUP v1.0 (Personal & Non-Commercial Use Only)

---

**Framework**: DibTauroS/Ordo-ab-Chao  
**Companion App per**: Tauros AI Bot
