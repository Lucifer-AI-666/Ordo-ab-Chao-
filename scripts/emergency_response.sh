#!/bin/bash
#
# emergency_response.sh - Risposta emergenze security per Tauros/Lucy
# Creator: Lucifer-AI-666 (@Lucifer-AI-666)
# Ecosystem: Tauros/Lucy Intelligence Platform
# Deploy Time: 2025-08-16 09:40:35 UTC
#

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_DIR="/var/log/tauros-lucy"
readonly INSTALL_DIR="/opt/tauros-lucy"
readonly EMERGENCY_LOG="$LOG_DIR/emergency.log"
readonly INCIDENT_DIR="$LOG_DIR/incidents"
readonly BACKUP_DIR="/var/backups/tauros-lucy"
readonly OLLAMA_MODEL="copilot_private"

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly BOLD='\033[1m'
readonly NC='\033[0m'

# Emergency state
INCIDENT_ID=""
LOCKDOWN_ACTIVE=false
SERVICES_ISOLATED=false

# Logging functions
emergency_log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] [$level] $message" >> "$EMERGENCY_LOG" 2>/dev/null || true
    
    case $level in
        "CRITICAL")
            echo -e "${RED}${BOLD}🚨 [CRITICAL] $message${NC}" >&2
            ;;
        "ERROR")
            echo -e "${RED}❌ [ERROR] $message${NC}" >&2
            ;;
        "WARN")
            echo -e "${YELLOW}⚠️  [WARN] $message${NC}" >&2
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  [INFO] $message${NC}" >&2
            ;;
        "SUCCESS")
            echo -e "${GREEN}✅ [SUCCESS] $message${NC}" >&2
            ;;
    esac
}

# Usage
usage() {
    cat << EOF
🚨 CopilotPrivateAgent Emergency Response System

Usage: $0 [COMMAND] [OPTIONS]

COMMANDS:
    --lockdown              Immediate system lockdown
    --auto                  Automatic incident response
    --isolate               Isolate compromised services
    --restore               Restore from backup
    --status                Check emergency status
    --collect-evidence      Collect forensic evidence
    --reset                 Reset emergency state
    --notify                Send admin notifications

OPTIONS:
    --incident-id ID        Specify incident ID
    --services SERVICES     Comma-separated service list
    --notify-admin          Send admin notifications
    --force                 Force operation without confirmation
    --restore-from FILE     Specific backup file to restore
    --help, -h              Show this help

EXAMPLES:
    # Immediate lockdown
    $0 --lockdown --notify-admin
    
    # Automatic response with incident tracking
    $0 --auto --incident-id INCIDENT_001
    
    # Isolate specific services
    $0 --isolate --services "ollama,nginx"
    
    # Collect evidence for investigation
    $0 --collect-evidence --incident-id INCIDENT_001
    
    # Restore system from backup
    $0 --restore --restore-from /var/backups/tauros-lucy/backup_20250816.tar.gz

EMERGENCY CONTACT:
    - Security Team: security@tauros-lucy.local
    - Admin Console: http://tauros-lucy.local/emergency
    - Incident Portal: http://incident.tauros-lucy.local
EOF
}

# Banner
show_emergency_banner() {
    cat << 'EOF'
🚨 ══════════════════════════════════════════════════════════════════════════
   ███████ ███    ███ ███████ ██████   ██████  ███████ ███    ██  ██████ ██    ██ 
   ██      ████  ████ ██      ██   ██ ██       ██      ████   ██ ██       ██  ██  
   █████   ██ ████ ██ █████   ██████  ██   ███ █████   ██ ██  ██ ██        ████   
   ██      ██  ██  ██ ██      ██   ██ ██    ██ ██      ██  ██ ██ ██         ██    
   ███████ ██      ██ ███████ ██   ██  ██████  ███████ ██   ████  ██████    ██    
   
   EMERGENCY RESPONSE SYSTEM - TAUROS/LUCY
   Incident Response & Security Lockdown
   
   ACTIVATED: $(date '+%Y-%m-%d %H:%M:%S %Z')
══════════════════════════════════════════════════════════════════════════ 🚨
EOF
}

# Generate incident ID
generate_incident_id() {
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local random=$(openssl rand -hex 4 2>/dev/null || printf "%08x" $RANDOM)
    echo "INC_${timestamp}_${random^^}"
}

# Initialize incident
initialize_incident() {
    local custom_id="$1"
    
    if [[ -n "$custom_id" ]]; then
        INCIDENT_ID="$custom_id"
    else
        INCIDENT_ID=$(generate_incident_id)
    fi
    
    # Create incident directory
    mkdir -p "$INCIDENT_DIR/$INCIDENT_ID"
    
    # Initialize incident log
    local incident_log="$INCIDENT_DIR/$INCIDENT_ID/incident.log"
    cat > "$incident_log" << EOF
INCIDENT ID: $INCIDENT_ID
START TIME: $(date '+%Y-%m-%d %H:%M:%S %Z')
SYSTEM: $(hostname)
USER: $USER
SCRIPT: $0
ARGS: $*

INCIDENT TIMELINE:
==================
EOF
    
    emergency_log "INFO" "Incident $INCIDENT_ID initialized"
}

# Log incident activity
log_incident() {
    local activity="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [[ -n "$INCIDENT_ID" ]]; then
        echo "[$timestamp] $activity" >> "$INCIDENT_DIR/$INCIDENT_ID/incident.log"
    fi
    
    emergency_log "INFO" "INCIDENT $INCIDENT_ID: $activity"
}

# System lockdown
emergency_lockdown() {
    emergency_log "CRITICAL" "INITIATING EMERGENCY LOCKDOWN"
    log_incident "Emergency lockdown initiated"
    
    # Stop Ollama service immediately
    emergency_log "INFO" "Stopping Ollama service..."
    if systemctl is-active ollama >/dev/null 2>&1; then
        sudo systemctl stop ollama
        emergency_log "SUCCESS" "Ollama service stopped"
    else
        emergency_log "WARN" "Ollama service was not running"
    fi
    
    # Block Ollama port
    emergency_log "INFO" "Blocking Ollama port 11434..."
    if command -v iptables >/dev/null 2>&1; then
        sudo iptables -I INPUT -p tcp --dport 11434 -j DROP
        emergency_log "SUCCESS" "Port 11434 blocked via iptables"
    elif command -v ufw >/dev/null 2>&1; then
        sudo ufw deny 11434
        emergency_log "SUCCESS" "Port 11434 blocked via UFW"
    else
        emergency_log "WARN" "No firewall available to block port"
    fi
    
    # Set emergency environment variables
    export COPILOT_EMERGENCY_MODE=1
    export COPILOT_DISABLE_TEST=1
    echo "export COPILOT_EMERGENCY_MODE=1" | sudo tee -a /etc/environment
    echo "export COPILOT_DISABLE_TEST=1" | sudo tee -a /etc/environment
    
    # Create lockdown indicator
    echo "EMERGENCY LOCKDOWN ACTIVE - $(date)" > "$INSTALL_DIR/.emergency_lockdown"
    chmod 644 "$INSTALL_DIR/.emergency_lockdown"
    
    LOCKDOWN_ACTIVE=true
    log_incident "System lockdown completed"
    emergency_log "CRITICAL" "EMERGENCY LOCKDOWN COMPLETED"
}

# Isolate services
isolate_services() {
    local services="$1"
    
    emergency_log "WARN" "Isolating services: $services"
    log_incident "Service isolation initiated for: $services"
    
    IFS=',' read -ra SERVICE_ARRAY <<< "$services"
    
    for service in "${SERVICE_ARRAY[@]}"; do
        service=$(echo "$service" | xargs)  # trim whitespace
        
        emergency_log "INFO" "Isolating service: $service"
        
        if systemctl is-active "$service" >/dev/null 2>&1; then
            sudo systemctl stop "$service"
            sudo systemctl disable "$service"
            emergency_log "SUCCESS" "Service $service stopped and disabled"
        else
            emergency_log "WARN" "Service $service was not running"
        fi
        
        # Create isolation marker
        echo "ISOLATED - $(date)" > "$INSTALL_DIR/.isolated_$service"
    done
    
    SERVICES_ISOLATED=true
    log_incident "Service isolation completed"
    emergency_log "WARN" "Service isolation completed"
}

# Collect evidence
collect_evidence() {
    emergency_log "INFO" "Starting evidence collection"
    log_incident "Forensic evidence collection started"
    
    local evidence_dir="$INCIDENT_DIR/$INCIDENT_ID/evidence"
    mkdir -p "$evidence_dir"
    
    # System information
    emergency_log "INFO" "Collecting system information..."
    {
        echo "=== SYSTEM INFORMATION ==="
        uname -a
        echo -e "\n=== DATE ==="
        date
        echo -e "\n=== UPTIME ==="
        uptime
        echo -e "\n=== USERS ==="
        who
        echo -e "\n=== PROCESSES ==="
        ps aux
        echo -e "\n=== NETWORK CONNECTIONS ==="
        netstat -tulpn 2>/dev/null || ss -tulpn
        echo -e "\n=== MEMORY ==="
        free -h
        echo -e "\n=== DISK ==="
        df -h
    } > "$evidence_dir/system_info.txt"
    
    # Service status
    emergency_log "INFO" "Collecting service status..."
    {
        echo "=== SYSTEMD SERVICES ==="
        systemctl list-units --type=service --state=running
        echo -e "\n=== OLLAMA SERVICE ==="
        systemctl status ollama || true
        echo -e "\n=== OLLAMA LOGS ==="
        journalctl -u ollama --since "1 hour ago" --no-pager
    } > "$evidence_dir/services.txt"
    
    # Ollama specific data
    if command -v ollama >/dev/null 2>&1; then
        emergency_log "INFO" "Collecting Ollama evidence..."
        {
            echo "=== OLLAMA VERSION ==="
            ollama --version
            echo -e "\n=== OLLAMA MODELS ==="
            ollama list
            echo -e "\n=== OLLAMA PROCESSES ==="
            pgrep -fl ollama || echo "No ollama processes found"
        } > "$evidence_dir/ollama.txt"
    fi
    
    # Configuration files
    emergency_log "INFO" "Collecting configuration files..."
    if [[ -d /etc/systemd/system/ollama.service.d/ ]]; then
        cp -r /etc/systemd/system/ollama.service.d/ "$evidence_dir/systemd_config/"
    fi
    
    if [[ -d "$INSTALL_DIR/config" ]]; then
        cp -r "$INSTALL_DIR/config" "$evidence_dir/tauros_config/"
    fi
    
    # Log files
    emergency_log "INFO" "Collecting recent logs..."
    if [[ -d "$LOG_DIR" ]]; then
        find "$LOG_DIR" -name "*.log" -mtime -1 -exec cp {} "$evidence_dir/" \;
    fi
    
    # Create evidence archive
    local evidence_archive="$INCIDENT_DIR/$INCIDENT_ID/evidence_$(date '+%Y%m%d_%H%M%S').tar.gz"
    tar -czf "$evidence_archive" -C "$evidence_dir" .
    
    # Generate evidence hash
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$evidence_archive" > "$evidence_archive.sha256"
        emergency_log "SUCCESS" "Evidence archive created with checksum"
    fi
    
    log_incident "Evidence collection completed: $evidence_archive"
    emergency_log "SUCCESS" "Evidence collection completed"
    
    echo "$evidence_archive"
}

# Backup system state
create_emergency_backup() {
    emergency_log "INFO" "Creating emergency backup"
    log_incident "Emergency backup started"
    
    local backup_file="$BACKUP_DIR/emergency_backup_$(date '+%Y%m%d_%H%M%S').tar.gz"
    mkdir -p "$BACKUP_DIR"
    
    # Create backup with critical data
    tar -czf "$backup_file" \
        "$INSTALL_DIR" \
        "$LOG_DIR" \
        /etc/systemd/system/ollama.service.d/ \
        /etc/tauros-lucy/ \
        2>/dev/null
    
    if [[ -f "$backup_file" ]]; then
        emergency_log "SUCCESS" "Emergency backup created: $backup_file"
        log_incident "Emergency backup completed: $backup_file"
        echo "$backup_file"
    else
        emergency_log "ERROR" "Emergency backup failed"
        return 1
    fi
}

# Restore from backup
restore_from_backup() {
    local backup_file="$1"
    
    if [[ ! -f "$backup_file" ]]; then
        emergency_log "ERROR" "Backup file not found: $backup_file"
        return 1
    fi
    
    emergency_log "WARN" "Starting system restore from: $backup_file"
    log_incident "System restore initiated from: $backup_file"
    
    # Verify backup integrity
    if ! tar -tzf "$backup_file" >/dev/null 2>&1; then
        emergency_log "ERROR" "Backup file is corrupted: $backup_file"
        return 1
    fi
    
    # Stop services before restore
    emergency_log "INFO" "Stopping services for restore..."
    sudo systemctl stop ollama 2>/dev/null || true
    
    # Create pre-restore backup
    local pre_restore_backup="$BACKUP_DIR/pre_restore_$(date '+%Y%m%d_%H%M%S').tar.gz"
    tar -czf "$pre_restore_backup" "$INSTALL_DIR" "$LOG_DIR" 2>/dev/null || true
    
    # Extract backup
    emergency_log "INFO" "Extracting backup..."
    if tar -xzf "$backup_file" -C / 2>/dev/null; then
        emergency_log "SUCCESS" "Backup extracted successfully"
    else
        emergency_log "ERROR" "Backup extraction failed"
        return 1
    fi
    
    # Reload systemd and restart services
    sudo systemctl daemon-reload
    sudo systemctl enable ollama
    sudo systemctl start ollama
    
    # Remove emergency state
    rm -f "$INSTALL_DIR/.emergency_lockdown"
    rm -f "$INSTALL_DIR/.isolated_"*
    
    # Reset environment variables
    sudo sed -i '/COPILOT_EMERGENCY_MODE/d' /etc/environment
    sudo sed -i '/COPILOT_DISABLE_TEST/d' /etc/environment
    
    log_incident "System restore completed from: $backup_file"
    emergency_log "SUCCESS" "System restore completed"
}

# Send admin notifications
send_admin_notification() {
    local subject="$1"
    local message="$2"
    
    emergency_log "INFO" "Sending admin notification: $subject"
    
    # Log notification to file
    local notification_file="$INCIDENT_DIR/$INCIDENT_ID/notifications.log"
    {
        echo "NOTIFICATION: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "SUBJECT: $subject"
        echo "MESSAGE: $message"
        echo "SYSTEM: $(hostname)"
        echo "INCIDENT: $INCIDENT_ID"
        echo "----------------------------------------"
    } >> "$notification_file"
    
    # Try multiple notification methods
    local notification_sent=false
    
    # System logger
    logger -t "TAUROS_LUCY_EMERGENCY" "[$INCIDENT_ID] $subject: $message"
    
    # Wall message for logged in users
    if command -v wall >/dev/null 2>&1; then
        echo "🚨 TAUROS/LUCY EMERGENCY [$INCIDENT_ID]: $subject - $message" | wall
        notification_sent=true
    fi
    
    # Email if available
    if command -v mail >/dev/null 2>&1; then
        {
            echo "Subject: [TAUROS/LUCY EMERGENCY] $subject"
            echo "Incident ID: $INCIDENT_ID"
            echo "System: $(hostname)"
            echo "Time: $(date '+%Y-%m-%d %H:%M:%S %Z')"
            echo ""
            echo "$message"
        } | mail root 2>/dev/null && notification_sent=true
    fi
    
    # Webhook notification (if configured)
    if [[ -f "$INSTALL_DIR/config/webhook_url.txt" ]]; then
        local webhook_url
        webhook_url=$(cat "$INSTALL_DIR/config/webhook_url.txt")
        if curl -s -X POST "$webhook_url" \
            -H "Content-Type: application/json" \
            -d "{\"incident_id\":\"$INCIDENT_ID\",\"subject\":\"$subject\",\"message\":\"$message\",\"system\":\"$(hostname)\",\"timestamp\":\"$(date -u '+%Y-%m-%dT%H:%M:%SZ')\"}" \
            >/dev/null 2>&1; then
            notification_sent=true
        fi
    fi
    
    if [[ "$notification_sent" == "true" ]]; then
        emergency_log "SUCCESS" "Admin notification sent"
    else
        emergency_log "WARN" "Admin notification failed - check notification methods"
    fi
}

# Check emergency status
check_emergency_status() {
    emergency_log "INFO" "Checking emergency status"
    
    echo -e "${CYAN}🔍 Emergency Status Report${NC}"
    echo -e "${CYAN}$(printf '═%.0s' $(seq 1 40))${NC}"
    
    # Lockdown status
    if [[ -f "$INSTALL_DIR/.emergency_lockdown" ]]; then
        echo -e "${RED}🚨 Emergency Lockdown: ACTIVE${NC}"
        echo -e "   Since: $(cat "$INSTALL_DIR/.emergency_lockdown")"
    else
        echo -e "${GREEN}✅ Emergency Lockdown: INACTIVE${NC}"
    fi
    
    # Service status
    if systemctl is-active ollama >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama Service: RUNNING${NC}"
    else
        echo -e "${RED}❌ Ollama Service: STOPPED${NC}"
    fi
    
    # Isolated services
    local isolated_services=($(ls "$INSTALL_DIR"/.isolated_* 2>/dev/null | sed 's/.*\.isolated_//' || true))
    if [[ ${#isolated_services[@]} -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  Isolated Services: ${isolated_services[*]}${NC}"
    else
        echo -e "${GREEN}✅ Service Isolation: NONE${NC}"
    fi
    
    # Environment variables
    if [[ "${COPILOT_EMERGENCY_MODE:-0}" == "1" ]]; then
        echo -e "${RED}🚨 Emergency Mode: ENABLED${NC}"
    else
        echo -e "${GREEN}✅ Emergency Mode: DISABLED${NC}"
    fi
    
    # Recent incidents
    echo -e "\n${CYAN}📋 Recent Incidents:${NC}"
    if [[ -d "$INCIDENT_DIR" ]]; then
        find "$INCIDENT_DIR" -maxdepth 1 -type d -name "INC_*" | head -5 | while read -r incident_path; do
            local incident_name=$(basename "$incident_path")
            echo -e "   📄 $incident_name"
        done
    else
        echo -e "   ${GREEN}No recent incidents${NC}"
    fi
}

# Reset emergency state
reset_emergency_state() {
    emergency_log "INFO" "Resetting emergency state"
    
    # Remove lockdown indicators
    rm -f "$INSTALL_DIR/.emergency_lockdown"
    rm -f "$INSTALL_DIR"/.isolated_*
    
    # Reset environment variables
    unset COPILOT_EMERGENCY_MODE
    unset COPILOT_DISABLE_TEST
    sudo sed -i '/COPILOT_EMERGENCY_MODE/d' /etc/environment
    sudo sed -i '/COPILOT_DISABLE_TEST/d' /etc/environment
    
    # Remove firewall blocks
    if command -v iptables >/dev/null 2>&1; then
        sudo iptables -D INPUT -p tcp --dport 11434 -j DROP 2>/dev/null || true
    elif command -v ufw >/dev/null 2>&1; then
        sudo ufw delete deny 11434 2>/dev/null || true
    fi
    
    # Restart services
    sudo systemctl daemon-reload
    sudo systemctl enable ollama
    sudo systemctl start ollama
    
    emergency_log "SUCCESS" "Emergency state reset completed"
}

# Automatic incident response
automatic_response() {
    emergency_log "CRITICAL" "AUTOMATIC INCIDENT RESPONSE INITIATED"
    
    # Create emergency backup first
    local backup_file
    backup_file=$(create_emergency_backup)
    
    # Collect evidence
    local evidence_file
    evidence_file=$(collect_evidence)
    
    # Activate lockdown
    emergency_lockdown
    
    # Send notification
    send_admin_notification "Automatic Emergency Response Activated" \
        "Incident $INCIDENT_ID - System locked down automatically. Evidence collected: $evidence_file. Backup created: $backup_file"
    
    log_incident "Automatic response completed"
    emergency_log "CRITICAL" "AUTOMATIC RESPONSE COMPLETED"
}

# Main execution
main() {
    # Parse arguments
    local command=""
    local force=false
    local services=""
    local notify_admin=false
    local restore_file=""
    local custom_incident_id=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --lockdown)
                command="lockdown"
                shift
                ;;
            --auto)
                command="auto"
                shift
                ;;
            --isolate)
                command="isolate"
                shift
                ;;
            --restore)
                command="restore"
                shift
                ;;
            --status)
                command="status"
                shift
                ;;
            --collect-evidence)
                command="evidence"
                shift
                ;;
            --reset)
                command="reset"
                shift
                ;;
            --notify)
                command="notify"
                shift
                ;;
            --services)
                services="$2"
                shift 2
                ;;
            --incident-id)
                custom_incident_id="$2"
                shift 2
                ;;
            --notify-admin)
                notify_admin=true
                shift
                ;;
            --force)
                force=true
                shift
                ;;
            --restore-from)
                restore_file="$2"
                shift 2
                ;;
            --help|-h)
                usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Initialize logging
    mkdir -p "$LOG_DIR" "$INCIDENT_DIR" "$BACKUP_DIR" 2>/dev/null || true
    
    # Show banner for critical operations
    if [[ "$command" =~ ^(lockdown|auto|isolate)$ ]]; then
        show_emergency_banner
    fi
    
    # Initialize incident if needed
    if [[ "$command" != "status" && "$command" != "reset" ]]; then
        initialize_incident "$custom_incident_id"
    fi
    
    # Execute command
    case $command in
        "lockdown")
            if [[ "$force" == "false" ]]; then
                echo -e "${YELLOW}⚠️  This will immediately stop all Ollama services and block access.${NC}"
                echo -n "Are you sure? [y/N]: "
                read -r confirmation
                if [[ ! "$confirmation" =~ ^[Yy]$ ]]; then
                    echo "Operation cancelled"
                    exit 0
                fi
            fi
            
            emergency_lockdown
            
            if [[ "$notify_admin" == "true" ]]; then
                send_admin_notification "Emergency Lockdown Activated" \
                    "System has been placed in emergency lockdown mode by $USER on $(hostname)"
            fi
            ;;
            
        "auto")
            automatic_response
            ;;
            
        "isolate")
            if [[ -z "$services" ]]; then
                emergency_log "ERROR" "No services specified for isolation"
                exit 1
            fi
            
            isolate_services "$services"
            
            if [[ "$notify_admin" == "true" ]]; then
                send_admin_notification "Services Isolated" \
                    "Services isolated: $services on $(hostname)"
            fi
            ;;
            
        "restore")
            if [[ -z "$restore_file" ]]; then
                # Find latest backup
                restore_file=$(find "$BACKUP_DIR" -name "*.tar.gz" -type f -exec ls -1t {} + | head -1)
                if [[ -z "$restore_file" ]]; then
                    emergency_log "ERROR" "No backup file found and none specified"
                    exit 1
                fi
                emergency_log "INFO" "Using latest backup: $restore_file"
            fi
            
            if [[ "$force" == "false" ]]; then
                echo -e "${YELLOW}⚠️  This will restore system state from backup.${NC}"
                echo -e "Backup file: $restore_file"
                echo -n "Continue? [y/N]: "
                read -r confirmation
                if [[ ! "$confirmation" =~ ^[Yy]$ ]]; then
                    echo "Operation cancelled"
                    exit 0
                fi
            fi
            
            restore_from_backup "$restore_file"
            ;;
            
        "evidence")
            evidence_file=$(collect_evidence)
            echo -e "${GREEN}Evidence collected: $evidence_file${NC}"
            ;;
            
        "status")
            check_emergency_status
            ;;
            
        "reset")
            if [[ "$force" == "false" ]]; then
                echo -e "${YELLOW}⚠️  This will reset all emergency states and restart services.${NC}"
                echo -n "Continue? [y/N]: "
                read -r confirmation
                if [[ ! "$confirmation" =~ ^[Yy]$ ]]; then
                    echo "Operation cancelled"
                    exit 0
                fi
            fi
            
            reset_emergency_state
            ;;
            
        "notify")
            send_admin_notification "Test Notification" \
                "Emergency notification system test from $(hostname)"
            ;;
            
        "")
            echo "No command specified"
            usage
            exit 1
            ;;
            
        *)
            echo "Unknown command: $command"
            usage
            exit 1
            ;;
    esac
    
    # Final status
    if [[ "$command" != "status" ]]; then
        emergency_log "INFO" "Emergency response command '$command' completed"
        
        if [[ -n "$INCIDENT_ID" ]]; then
            echo -e "\n${CYAN}📋 Incident ID: $INCIDENT_ID${NC}"
            echo -e "${CYAN}📁 Incident Dir: $INCIDENT_DIR/$INCIDENT_ID${NC}"
        fi
    fi
}

# Execute main function
main "$@"