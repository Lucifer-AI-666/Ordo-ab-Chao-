# priv-cyber-agents — README Privato & Documentazione Operativa

Documento privato. Non condividere. Questo repository contiene un setup “privacy-by-default” per due agent locali di cybersecurity, un gateway locale e una mini app Android (APK) per controllo remoto sicuro.

Componenti
- primo (Copilot Private Agent): modello Ollama con guardrail via system prompt.
- secondo (Monica Private Agent): agente Python locale con policy rigorose, audit e catena d’integrità.
- gateway: FastAPI con token Bearer per orchestrare “secondo” da client esterni fidati.
- android-app: client Android minimale per invocare in modo sicuro le azioni consentite.
- scripts: setup/build e hardening (firewall).
- legal: licenze e modelli legali (LUP, DPA/GDPR).

Sicurezza by design
- Solo loopback: Ollama e gateway legati a 127.0.0.1.
- Gated actions: modalità DEFEND/TEST; keyword “Wassim”; allowlist; controllo privilegi; rate limit; dry-run; kill-switch (MONICA_DISABLE=1).
- Audit immutabili: JSONL + catena d’integrità SHA-256.
- Repo privata, secret handling e permessi file stretti.
- Licenza non-commerciale personalissima (LUP) e DPA/GDPR inclusi.

---

Indice
- 1. Struttura della repository
- 2. Prerequisiti
- 3. Setup rapido (Linux/macOS)
- 4. Uso degli agent (primo/secondo)
- 5. Gateway (API locali sicure)
- 6. App Android (APK) e build
- 7. Privacy & hardening operativo
- 8. Logging, audit e integrità
- 9. Gestione segreti e permessi
- 10. Licenza e legale (LUP, DPA/GDPR)
- 11. SOP operative (rotazioni, backup, incident response)
- 12. Troubleshooting

---

1) Struttura della repository
- primo/
  - CopilotPrivateAgent.Modelfile
  - README.md
- secondo/
  - MonicaPrivateAgent.Modelfile
  - monica_agent.py
  - monica.toml
  - requirements.txt
  - monica.service (systemd)
  - README.md
- gateway/
  - agent_gateway.py
  - requirements.txt
  - README.md
- android-app/
  - settings.gradle, build.gradle
  - app/ (manifest, MainActivity, Compose UI)
  - gradlew, gradlew.bat, gradle/wrapper/gradle-wrapper.properties
- scripts/
  - firewall_lock_linux.sh
  - build_apk.sh, build_apk.ps1
  - setup_all.sh
- systemd/
  - gateway.service
- docs/
  - IMPROVEMENTS.md
  - README_PRIVACY.md (separato)
- legal/
  - LICENSE.md (LUP v1.0 – uso personalissimo)
  - DPA_GDPR_Template_IT.md

---

2) Prerequisiti
- Sistema: Linux/macOS consigliati. Windows supportato per build APK e uso “primo”; per “secondo” è preferibile Linux.
- Software:
  - Ollama installato e in esecuzione (consigliato bind su 127.0.0.1:11434).
  - Python 3.10+ con pip.
  - Per gateway: fastapi/uvicorn (installati via requirements).
  - Per build APK: JDK 17+, Android SDK (ANDROID_HOME/ANDROID_SDK_ROOT), internet.
- Permessi: sudo per firewall, systemd, install di pacchetti in “secondo”.

---

3) Setup rapido (Linux/macOS)
Esegui il setup end-to-end (modelli, dipendenze, hardening, servizi):
- bash ./scripts/setup_all.sh

Cosa fa:
- Crea/aggiorna i modelli Ollama:
  - primo: copilot_private
  - secondo: monica_private
- Installa requirements Python per “secondo” e “gateway”.
- Applica hardening firewall (porta 11434 solo loopback).
- Sincronizza il progetto in /opt/priv-cyber-agents.
- Installa/abilita servizi systemd:
  - monica.service (se presente)
  - gateway.service (token generato automaticamente).

Note:
- Il gateway parte su 127.0.0.1:8787 con token Bearer sicuro (stampato a fine script). Conserva il token in modo sicuro.

---

4) Uso degli agent

4.1) primo (Copilot Private Agent, Ollama)
- Creazione modello:
  - cd primo
  - ollama create copilot_private -f CopilotPrivateAgent.Modelfile
- Esecuzione:
  - ollama run copilot_private
- Prompt:
  - DEFEND (sempre consentito): “Elenca i rischi principali per processi anomali e dammi comandi solo di ispezione.”
  - TEST (gated: richiede keyword + allowlist + privilegi): “Wassim esegui SUID check su localhost e proponi mitigazioni.”

4.2) secondo (Monica Private Agent, Python)
- Config: secondo/monica.toml
  - mode = "DEFEND" (default). Per azioni invasive serve TEST + keyword “Wassim”.
  - scope.allow_hosts e allow_cidrs (allowlist).
  - safety: rate_limit, timeout, dry_run, require_admin.
- Esempi:
  - Monitoraggio (DEFEND): python3 monica_agent.py --kind monitor
  - Install tool (TEST): python3 monica_agent.py --kind install_tool --tool nmap --prompt "Wassim install nmap"
  - Pen-test locale (TEST): python3 monica_agent.py --kind local_pentest --target 127.0.0.1 --prompt "Wassim pen test"

Kill-switch:
- Esporta MONICA_DISABLE=1 per bloccare qualsiasi azione invasiva.

---

5) Gateway (API locali sicure)
- Avvio manuale (sviluppo):
  - cd gateway
  - export AGENT_GATEWAY_TOKEN="$(python3 - <<<'import secrets;print(secrets.token_hex(24))')"
  - uvicorn gateway.agent_gateway:app --host 127.0.0.1 --port 8787
- Endpoint:
  - POST /monitor
  - POST /install_tool { prompt, tool }
  - POST /local_pentest { prompt, target }
- Autenticazione: Header Authorization: Bearer <TOKEN>
- Esempi:
  - curl -s -X POST http://127.0.0.1:8787/monitor -H "Authorization: Bearer $AGENT_GATEWAY_TOKEN"
  - curl -s -X POST http://127.0.0.1:8787/install_tool -H "Authorization: Bearer $AGENT_GATEWAY_TOKEN" -H "Content-Type: application/json" -d '{"prompt":"Wassim install nmap","tool":"nmap"}'

Systemd (produzione locale):
- gateway.service usa WorkingDirectory=/opt/priv-cyber-agents e token in Environment= (sostituito da setup_all.sh).
- Comandi:
  - sudo systemctl status gateway
  - sudo systemctl restart gateway

Importante:
- Mantieni il bind su 127.0.0.1. Se devi accedere da un dispositivo nella stessa LAN, usa un reverse proxy con firewall e, se possibile, TLS e mutual auth.

---

6) App Android (APK) e build
- Config di base (android-app):
  - Compose UI minimale
  - OkHttp client
  - Manifest con INTERNET e networkSecurityConfig per chiaro (sviluppo)
- Build APK:
  - Linux/macOS: ./scripts/build_apk.sh
  - Windows (PowerShell): ./scripts/build_apk.ps1
- Output: dist/PrivCyberAgent-debug-YYYYmmdd_HHMMSS.apk
- Collegamento all’host:
  - Emulatore: URL default http://10.0.2.2:8787
  - Dispositivo reale: usa l’IP del PC nella LAN (solo per test, con firewall stretto). Inserisci il token Bearer generato.
- Sicurezza app:
  - Non hardcodare token/URL sensibili nella app.
  - Per release, usa firma con keystore protetto; abilita R8/obfuscation; conserva il keystore fuori repo.

---

7) Privacy & hardening operativo
- Loopback binding per Ollama:
  - Systemd override (Linux): OLLAMA_HOST=127.0.0.1:11434
- Firewall porta 11434 (Linux):
  - ./scripts/firewall_lock_linux.sh
- Permessi file:
  - chmod 600 per monica.toml, log e chain; ACL ridotte su Windows.
- Repo privata, forking disattivato, 2FA obbligatoria, secret scanning attivo.
- Niente upload automatici dei log; i log restano locali.

---

8) Logging, audit e integrità
- Log JSONL: secondo/monica_agent.jsonl
- Catena d’integrità: secondo/monica_chain.sha256
- Ogni record include _ts e _prev_hash; la chain è SHA-256 append-only.
- Opzionale: sostituire/integrare con HMAC-SHA256 (chiave locale non committata).

---

9) Gestione segreti e permessi
- Non committare: keystore Android, token del gateway, .env, PAT/SSH private.
- .gitignore suggerito:
  - .env, *.keystore, keystore.jks, keystore.properties, dist/, secondi log/chain
- Permessi:
  - Linux: chmod 600 su config/log/chain; proprietario root o utente di servizio.
  - Windows: ACL NTFS per limitare a Administrators e all’utente corrente.
- GitHub:
  - Repository privata, forking off, branch protection, signed commits (se possibile).
  - Secrets di CI limitati ai job necessari; artifact privati.

---

10) Licenza e legale
- Licenza: legal/LICENSE.md (LUP v1.0 — Licenza d’Uso Personalissimo)
  - Uso esclusivamente personale/privato e non commerciale.
  - Vietata la distribuzione/pubblicazione senza consenso scritto.
- DPA/GDPR: legal/DPA_GDPR_Template_IT.md
  - Modello conforme art. 28 GDPR, con allegati TOM, SCC e sub-responsabili.
  - Personalizzare con il consulente legale.

---

11) SOP operative (rotazioni, backup, incident response)
- Rotazione token gateway:
  - Genera nuovo token; aggiorna Environment del servizio; systemctl daemon-reload && restart; comunica il token ai client in modo sicuro.
- Aggiornamento modelli:
  - Aggiorna i Modelfile; ollama create <name> -f <file>; test in ambiente locale; poi switchare i client.
- Backup:
  - Backup cifrati di config e log (senza includere token in chiaro). Conserva separato il keystore Android.
- Incident response:
  - Kill-switch: export MONICA_DISABLE=1
  - Offload: stop gateway (systemctl stop gateway), disabilita TEST in monica.toml, abilita logging esteso.
  - Review: verifica chain, compara hash; estrai evidenze.

---

12) Troubleshooting
- Ollama non risponde:
  - Verifica OLLAMA_HOST=127.0.0.1:11434, firewall e service status; prova con curl http://127.0.0.1:11434/api/tags
- Azioni bloccate:
  - Controlla: mode=TEST, keyword “Wassim”, allowlist, privilegi admin/sudo, rate limit, kill-switch.
- Gateway 401/403:
  - Header Authorization mancante/errato; token non aggiornato; unit file non ricaricata.
- APK non builda:
  - JDK 17+; Android SDK e variabili ANDROID_HOME; usa scripts/build_apk.sh; controlla proxy/firewall aziendale.
- Permessi file:
  - Ripristina chmod 600 (Linux) o ACL (Windows); verifica ownership del servizio.

Contatti e responsabilità
- Titolare/Owner: [Inserire nominativo e contatti]
- Manutentore tecnico: [Inserire nominativo e contatti]
- Questo documento è riservato. L’uso è regolato dalla LUP v1.0 in legal/LICENSE.md.