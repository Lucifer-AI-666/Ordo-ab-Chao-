# 🚀 CopilotPrivateAgent - Ecosistema Tauros/Lucy

## 🎯 Overview

**CopilotPrivateAgent** è un agente di cybersecurity privato specializzato per l'ecosistema Tauros/Lucy, progettato con controlli di sicurezza multi-livello e modalità operative distinte. Sviluppato per la macchina di Dib Anouar con focus su "meta intelligence, non forza bruta".

### 🌟 Caratteristiche Principali

- **🛡️ Dual Mode Operation**: DEFEND (passivo) / TEST (attivo con autorizzazione)
- **🔐 Security-First**: Keyword authentication, allowlist, privilege verification
- **📊 Complete Audit Trail**: Logging completo dry-run e real-run
- **🔗 Ecosystem Integration**: Coordinamento seamless con Tauros/Lucy platform
- **⚡ Emergency Response**: Procedura automatica di lockdown e incident response

---

## 🏗️ Architettura del Sistema

### Core Components

```
Tauros/Lucy Ecosystem
├── 🤖 CopilotPrivateAgent (Ollama Model)
├── 🌐 Tauros Platform (Web/API/Database Layer)
├── 🧠 Lucy AI Suite (AI Agents Coordination)
├── 👁️ LOCCHIO Monitoring (Surveillance System)
├── 🌐 NEA Network (Network Communications)
└── 🔒 Security Stack (Crypto/Stego Tools)
```

### Security Framework

```
Request → Keyword Check → Allowlist Validation → Privilege Verification → Execution → Audit Log
```

---

## 🚀 Quick Start

### Prerequisiti

- **Ollama**: Installato e configurato
- **Sistema**: Linux/macOS con privilegi admin
- **Network**: Accesso SSH per deployment remoto (opzionale)
- **Monitoring**: LOCCHIO system configurato (opzionale)

### Installazione Base

```bash
# 1. Clone repository
git clone https://github.com/Lucifer-AI-666/priv-cyber-agents-private.git
cd priv-cyber-agents-private

# 2. Deploy locale
./scripts/final_deployment.sh

# 3. Verifica installazione
./scripts/health_check.sh
```

### Deployment Rapido

```bash
# Deploy automatico completo
ollama create copilot_private -f CopilotPrivateAgent.Modelfile
ollama run copilot_private
```

---

## 📖 Modalità Operative

### 🛡️ DEFEND Mode (Default)

Modalità **passiva** sempre disponibile per:
- Analisi di sicurezza non-invasiva
- Monitoraggio processi e rete
- Identificazione vulnerabilità
- Raccomandazioni di hardening

**Esempio**:
```bash
# Prompt DEFEND
"Status check Tauros/Lucy ecosystem"
"Elenca i rischi principali per processi anomali"
"Analizza configurazione firewall attuale"
```

### ⚡ TEST Mode (Keyword Required)

Modalità **attiva** con controlli rigorosi per:
- Scan di sicurezza intensivi
- Installazione tool di penetration testing
- Modifica configurazioni sistema
- Test invasivi su target autorizzati

**Requisiti**:
- 🔑 Keyword "Wassim" nel prompt
- 📋 Target in allowlist autorizzata
- 👑 Privilegi admin/sudo disponibili
- 📝 Pre-check automatici superati

**Esempio**:
```bash
# Prompt TEST
"Wassim - security assessment su localhost"
"Wassim esegui SUID check e proponi mitigazioni"
"Wassim install nmap per scan rete autorizzata"
```

---

## 🔧 Deployment Guide

### Deployment Locale

```bash
# Setup completo automatico
./scripts/final_deployment.sh

# Configurazione manuale step-by-step
sudo systemctl enable ollama-tauros-lucy
sudo systemctl start ollama-tauros-lucy
```

### Deployment SSH Remoto

```bash
# Deploy su host remoto via SSH
./scripts/deploy_tauros_lucy.sh user@remote-host

# Multi-host deployment
./scripts/deploy_tauros_lucy.sh --hosts hosts.txt
```

### Deployment Multi-Host

```bash
# Configurazione cluster
./scripts/deploy_tauros_lucy.sh --cluster \
  --primary primary.host.com \
  --secondaries "secondary1.host.com,secondary2.host.com"
```

---

## ⚙️ Configuration Files

### Systemd Service

**File**: `/etc/systemd/system/ollama-tauros-lucy.service`
```ini
[Unit]
Description=Ollama Tauros/Lucy CopilotPrivateAgent
After=network-online.target

[Service]
Type=notify
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_ORIGINS=http://127.0.0.1:*"
Environment="TAUROS_LUCY_MODE=DEFEND"
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Nginx Reverse Proxy

**File**: `/etc/nginx/sites-available/tauros-lucy`
```nginx
server {
    listen 443 ssl http2;
    server_name tauros-lucy.local;

    ssl_certificate /etc/ssl/certs/tauros-lucy.crt;
    ssl_certificate_key /etc/ssl/private/tauros-lucy.key;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://127.0.0.1:11434;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
    }
}
```

### LOCCHIO Monitoring Integration

**File**: `/etc/locchio/tauros-lucy-monitor.yml`
```yaml
monitor:
  name: "TaurosLucy-CopilotAgent"
  type: "ollama-service"
  
endpoints:
  - url: "http://127.0.0.1:11434/api/health"
    interval: 30s
    timeout: 10s
    
alerts:
  - name: "Service Down"
    condition: "response_time > 5s OR status != 200"
    action: "emergency_response"
    
  - name: "High Load"
    condition: "cpu_usage > 80% AND duration > 5m"
    action: "scale_notification"

security:
  audit_logs: "/var/log/tauros-lucy/audit.log"
  performance_logs: "/var/log/tauros-lucy/performance.log"
  retain_days: 30
```

---

## 🔐 Security Features

### Target Allowlist

**File**: `allowlist.json` (non committato)
```json
{
  "version": "1.0",
  "last_updated": "2025-08-16T09:40:35Z",
  "authorized_targets": {
    "hosts": [
      "127.0.0.1",
      "localhost",
      "192.168.1.100-192.168.1.110"
    ],
    "cidrs": [
      "10.0.0.0/24",
      "192.168.1.0/24"
    ],
    "excluded": [
      "192.168.1.1",
      "10.0.0.1"
    ]
  },
  "permissions": {
    "scan_intensive": ["192.168.1.0/24"],
    "install_tools": ["127.0.0.1"],
    "firewall_modify": ["localhost"]
  }
}
```

### Privilege Verification

```bash
# Check automatici prima di operazioni invasive
- Verifica utente in gruppo admin/sudo
- Test disponibilità comandi richiesti  
- Controllo permessi di scrittura
- Validazione spazio disco disponibile
```

### Emergency Lockdown

```bash
# Attivazione automatica lockdown
export COPILOT_EMERGENCY_MODE=1

# Disattivazione modalità TEST
export COPILOT_DISABLE_TEST=1

# Kill-switch completo
./scripts/emergency_response.sh --lockdown
```

---

## 🧪 Testing & Validation

### Test Funzionalità Base

```bash
# Test DEFEND mode
ollama run copilot_private "Status check Tauros/Lucy"

# Test sistema di logging
tail -f /var/log/tauros-lucy/audit.log

# Test health check
./scripts/health_check.sh --verbose
```

### Test Sicurezza

```bash
# Test autorizzazione keyword
ollama run copilot_private "Security assessment localhost"
# Dovrebbe richiedere keyword "Wassim"

# Test allowlist
ollama run copilot_private "Wassim scan 8.8.8.8"
# Dovrebbe rifiutare target non autorizzato

# Test privilegi
ollama run copilot_private "Wassim modify firewall rules"
# Dovrebbe verificare privilegi admin
```

### Test Integrazione

```bash
# Test coordinamento con LOCCHIO
curl -X POST http://localhost:8080/locchio/api/agents/status

# Test comunicazione NEA network
./scripts/test_nea_integration.sh

# Test Tauros platform sync
./scripts/test_tauros_sync.sh
```

### Performance Test

```bash
# Benchmark prestazioni
./scripts/performance_benchmark.sh

# Test load concurrent
ab -n 1000 -c 10 http://127.0.0.1:11434/api/health

# Monitor resource usage
./scripts/monitor_resources.sh --duration 300
```

---

## 📊 Advanced Features

### Executive Reporting

```bash
# Report formato business
ollama run copilot_private "Generate executive security report for last 30 days"

# Dashboard metrics
./scripts/generate_dashboard.sh --format html --output /var/www/tauros-lucy/
```

### Technical Deep Dive

```bash
# Analisi tecnica dettagliata
ollama run copilot_private "Wassim - complete technical assessment with forensics"

# Custom compliance check
ollama run copilot_private "Wassim - PCI-DSS compliance verification"
```

### Lucifer Mode (Creator Personality)

```bash
# Debug con personalità creator
ollama run copilot_private "Lucifer - debug Tauros/Lucy integration issues"

# Advanced troubleshooting
ollama run copilot_private "Lucifer - analyze performance bottlenecks"
```

---

## 🚨 Emergency Response

### Automatic Incident Response

```bash
# Risposta automatica emergenze
./scripts/emergency_response.sh --auto

# Lockdown immediato
./scripts/emergency_response.sh --lockdown --notify-admin

# Isolamento servizi compromessi
./scripts/emergency_response.sh --isolate --services "ollama,nginx"
```

### Manual Emergency Procedures

1. **Immediate Lockdown**:
   ```bash
   sudo systemctl stop ollama-tauros-lucy
   sudo iptables -A INPUT -p tcp --dport 11434 -j DROP
   ```

2. **Evidence Collection**:
   ```bash
   ./scripts/collect_evidence.sh --incident-id INCIDENT_001
   ```

3. **System Recovery**:
   ```bash
   ./scripts/recovery_mode.sh --restore-from-backup
   ```

---

## 🔍 Health Check & Monitoring

### Health Check Script

```bash
#!/bin/bash
# health_check.sh - Verifica stato ecosystem

echo "🔍 Tauros/Lucy Ecosystem Health Check"
echo "====================================="

# Check Ollama service
systemctl is-active ollama-tauros-lucy && echo "✅ Ollama service: RUNNING" || echo "❌ Ollama service: STOPPED"

# Check model availability
ollama list | grep -q "copilot_private" && echo "✅ CopilotPrivate model: AVAILABLE" || echo "❌ Model: NOT FOUND"

# Security assessment
./scripts/security_assessment.sh --quick && echo "✅ Security: OK" || echo "⚠️ Security: ISSUES FOUND"

# Network connectivity
curl -s http://127.0.0.1:11434/api/health >/dev/null && echo "✅ Network: REACHABLE" || echo "❌ Network: UNREACHABLE"

# Performance check
load=$(uptime | awk '{print $NF}')
echo "📊 System Load: $load"

# Disk space
df -h | grep -E "(/$|/opt)" | awk '{print "💾 Disk " $6 ": " $5 " used"}'

echo "====================================="
echo "🎯 Health Check Complete"
```

### Performance Metrics

```bash
# Monitor real-time performance
watch -n 1 './scripts/performance_metrics.sh'

# Log analysis
./scripts/analyze_logs.sh --period "last 24h" --format json
```

---

## 🛠️ Troubleshooting

### Common Issues

#### Ollama Service Not Starting

```bash
# Check service logs
sudo journalctl -u ollama-tauros-lucy -f

# Verify configuration
sudo systemctl cat ollama-tauros-lucy

# Reset and restart
sudo systemctl daemon-reload
sudo systemctl restart ollama-tauros-lucy
```

#### Model Not Responding

```bash
# Recreate model
ollama rm copilot_private
ollama create copilot_private -f CopilotPrivateAgent.Modelfile

# Test basic functionality
ollama run copilot_private "test connection"
```

#### Azioni Bloccate

```bash
# Verifica modalità corrente
echo $COPILOT_EMERGENCY_MODE $COPILOT_DISABLE_TEST

# Check allowlist
cat allowlist.json | jq '.authorized_targets'

# Verifica privilegi
groups $USER | grep -E "(sudo|admin|wheel)"
```

#### Performance Issues

```bash
# Check resource usage
htop
iotop
nethogs

# Optimize configuration
./scripts/optimize_performance.sh --auto
```

---

## 🤝 Ecosystem Integration

### Tauros Platform Integration

```python
# tauros_integration.py
import requests
import json

class TaurosClient:
    def __init__(self, base_url="http://tauros.local:8080"):
        self.base_url = base_url
        
    def sync_agent_status(self, agent_id, status):
        return requests.post(
            f"{self.base_url}/api/agents/{agent_id}/status",
            json={"status": status, "timestamp": time.time()}
        )
    
    def get_security_policy(self):
        return requests.get(f"{self.base_url}/api/security/policy").json()
```

### Lucy AI Suite Coordination

```bash
# Coordinamento con altri agenti AI
curl -X POST http://lucy.local:8081/api/coordination \
  -H "Content-Type: application/json" \
  -d '{"agent": "copilot_private", "action": "security_scan", "target": "network"}'
```

### LOCCHIO Monitoring Sync

```bash
# Sincronizzazione con sistema surveillance
./scripts/sync_locchio.sh --agent copilot_private --metrics security
```

### NEA Network Integration

```bash
# Gestione comunicazioni di rete
./scripts/nea_sync.sh --register-agent --type security --priority high
```

---

## 📝 Compliance & Legal

### Compliance Checklist

- [x] **Privacy by Design**: Dati processati localmente
- [x] **Least Privilege**: Accesso minimale necessario  
- [x] **Audit Trail**: Logging completo operazioni
- [x] **Data Retention**: Policy di retention configurata
- [x] **Access Control**: Autenticazione e autorizzazione
- [x] **Incident Response**: Procedure emergency definite

### Security Standards

- **ISO 27001**: Information Security Management
- **NIST Framework**: Cybersecurity guidelines
- **PCI-DSS**: Payment card security (se applicabile)
- **GDPR**: Privacy compliance per dati EU

---

## 🚀 Deployment Timeline

### Deploy Time: 2025-08-16 09:40:35 UTC

#### Phase 1: Core Setup (0-30 min)
- [x] ✅ Repository preparation
- [x] ✅ CopilotPrivateAgent.Modelfile optimization
- [ ] ⏳ Ollama model creation and testing

#### Phase 2: Infrastructure (30-60 min)
- [ ] ⏳ Systemd service configuration
- [ ] ⏳ Nginx reverse proxy setup
- [ ] ⏳ LOCCHIO monitoring integration

#### Phase 3: Security (60-90 min)
- [ ] ⏳ Allowlist configuration
- [ ] ⏳ Emergency response procedures
- [ ] ⏳ Security testing validation

#### Phase 4: Integration (90-120 min)
- [ ] ⏳ Tauros platform sync
- [ ] ⏳ Lucy AI suite coordination
- [ ] ⏳ NEA network registration

---

## 🎯 Success Criteria

### ✅ Deployment Success
```bash
# Model deployment test
ollama create copilot_private -f CopilotPrivateAgent.Modelfile
# Expected: Success, no errors

# Functionality test
ollama run copilot_private "Status check Tauros/Lucy"
# Expected: Structured markdown response with ecosystem status

# Security test
ollama run copilot_private "Wassim - security assessment"
# Expected: Authorization check, then security analysis
```

### 🔍 Integration Verification
```bash
# Ecosystem communication test
./scripts/test_ecosystem_integration.sh
# Expected: All components responding correctly

# Performance benchmark
./scripts/performance_test.sh --duration 60
# Expected: Response time < 2s, throughput > 10 req/s
```

---

## 👥 Team & Contacts

### Project Information
- **Creator**: Lucifer-AI-666 (@Lucifer-AI-666)
- **Organization**: @lasuperbia  
- **Ecosystem**: Tauros/Lucy Intelligence Platform
- **Repository**: Lucifer-AI-666/priv-cyber-agents-private

### Support & Maintenance
- **Technical Lead**: Dib Anouar
- **Security Team**: Tauros/Lucy Security Division
- **Monitoring**: LOCCHIO Operations Center

---

## 📄 License & Legal

Questo progetto è rilasciato sotto **LUP v1.0** (Lucifer Use Private) per uso personale e non commerciale.

Per uso enterprise/commerciale, contattare il team per licenza appropriata.

### Note Legali
- Repository pubblico per condivisione community
- Codice ottimizzato per "meta intelligence, non forza bruta"
- Focus su automazione e smart deployment
- Integrazione seamless con ecosystem esistente
- Security-first approach con controlli rigorosi

---

## 🔗 Quick Links

- 📊 [Dashboard Monitoring](http://tauros-lucy.local/dashboard)
- 🔧 [Admin Panel](http://tauros-lucy.local/admin)  
- 📈 [Performance Metrics](http://tauros-lucy.local/metrics)
- 🚨 [Emergency Console](http://tauros-lucy.local/emergency)
- 📖 [API Documentation](http://tauros-lucy.local/docs)

---

*Documento generato automaticamente il 2025-08-16 09:40:35 UTC per il deploy del CopilotPrivateAgent ecosystem.*