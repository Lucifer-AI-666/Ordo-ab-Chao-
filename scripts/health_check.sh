#!/bin/bash
#
# health_check.sh - Verifica stato componenti ecosystem Tauros/Lucy
# Creator: Lucifer-AI-666 (@Lucifer-AI-666)
# Ecosystem: Tauros/Lucy Intelligence Platform
# Deploy Time: 2025-08-16 09:40:35 UTC
#

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_DIR="/var/log/tauros-lucy"
readonly INSTALL_DIR="/opt/tauros-lucy"
readonly OLLAMA_MODEL="copilot_private"
readonly HEALTH_LOG="$LOG_DIR/health_check.log"

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m'

# Global status
OVERALL_STATUS="HEALTHY"
ISSUES_COUNT=0
WARNINGS_COUNT=0

# Logging functions
log_health() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" >> "$HEALTH_LOG" 2>/dev/null || true
}

check_ok() {
    echo -e "${GREEN}✅ $*${NC}"
    log_health "OK: $*"
}

check_warn() {
    echo -e "${YELLOW}⚠️  $*${NC}"
    log_health "WARN: $*"
    ((WARNINGS_COUNT++))
}

check_error() {
    echo -e "${RED}❌ $*${NC}"
    log_health "ERROR: $*"
    OVERALL_STATUS="UNHEALTHY"
    ((ISSUES_COUNT++))
}

check_info() {
    echo -e "${BLUE}ℹ️  $*${NC}"
    log_health "INFO: $*"
}

section_header() {
    echo -e "\n${CYAN}🔍 $*${NC}"
    echo -e "${CYAN}$(printf '═%.0s' $(seq 1 50))${NC}"
}

# Usage
usage() {
    cat << EOF
🔍 CopilotPrivateAgent Tauros/Lucy Health Check Tool

Usage: $0 [OPTIONS]

OPTIONS:
    --verbose, -v       Verbose output with detailed information
    --quick, -q         Quick check (skip performance tests)
    --security, -s      Focus on security assessment
    --performance, -p   Focus on performance metrics
    --network, -n       Include network connectivity tests
    --json             Output results in JSON format
    --silent           Minimal output (errors only)
    --help, -h         Show this help

EXAMPLES:
    # Basic health check
    $0
    
    # Verbose security assessment
    $0 --verbose --security
    
    # Quick performance check
    $0 --quick --performance
    
    # JSON output for monitoring systems
    $0 --json

EXIT CODES:
    0    All checks passed
    1    Warnings found
    2    Critical issues found
EOF
}

# Parse arguments
VERBOSE=false
QUICK=false
SECURITY_FOCUS=false
PERFORMANCE_FOCUS=false
NETWORK_TESTS=false
JSON_OUTPUT=false
SILENT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --quick|-q)
            QUICK=true
            shift
            ;;
        --security|-s)
            SECURITY_FOCUS=true
            shift
            ;;
        --performance|-p)
            PERFORMANCE_FOCUS=true
            shift
            ;;
        --network|-n)
            NETWORK_TESTS=true
            shift
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --silent)
            SILENT=true
            shift
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

# Banner
show_banner() {
    if [[ "$SILENT" == "false" && "$JSON_OUTPUT" == "false" ]]; then
        cat << 'EOF'
🔍 ════════════════════════════════════════════════════════════════════════════
   ██   ██ ███████  █████  ██   ████████ ██   ██ 
   ██   ██ ██      ██   ██ ██      ██    ██   ██ 
   ███████ █████   ███████ ██      ██    ███████ 
   ██   ██ ██      ██   ██ ██      ██    ██   ██ 
   ██   ██ ███████ ██   ██ ███████ ██    ██   ██ 
   
   CopilotPrivateAgent Health Check - Tauros/Lucy Ecosystem
   Creator: Lucifer-AI-666 (@Lucifer-AI-666)
   Check Time: $(date '+%Y-%m-%d %H:%M:%S %Z')
════════════════════════════════════════════════════════════════════════════ 🔍
EOF
    fi
}

# System checks
check_system_health() {
    section_header "SYSTEM HEALTH"
    
    # Operating system
    if [[ -f /etc/os-release ]]; then
        local os_info
        os_info=$(grep '^PRETTY_NAME=' /etc/os-release | cut -d'"' -f2)
        check_ok "Operating System: $os_info"
    else
        check_error "Operating System: Information not available"
    fi
    
    # System load
    local load_avg
    load_avg=$(uptime | awk -F'load average:' '{ print $2 }' | sed 's/^[ \t]*//')
    check_info "System Load: $load_avg"
    
    # Memory usage
    local mem_total mem_available mem_used_percent
    mem_total=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    mem_available=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
    mem_used_percent=$(( (mem_total - mem_available) * 100 / mem_total ))
    
    if [[ $mem_used_percent -gt 90 ]]; then
        check_warn "Memory Usage: ${mem_used_percent}% (HIGH)"
    elif [[ $mem_used_percent -gt 75 ]]; then
        check_warn "Memory Usage: ${mem_used_percent}% (MODERATE)"
    else
        check_ok "Memory Usage: ${mem_used_percent}%"
    fi
    
    # Disk space
    local disk_usage
    disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    
    if [[ $disk_usage -gt 90 ]]; then
        check_error "Disk Usage: ${disk_usage}% (CRITICAL)"
    elif [[ $disk_usage -gt 80 ]]; then
        check_warn "Disk Usage: ${disk_usage}% (HIGH)"
    else
        check_ok "Disk Usage: ${disk_usage}%"
    fi
    
    # Check if log directory exists and is writable
    if [[ -d "$LOG_DIR" && -w "$LOG_DIR" ]]; then
        check_ok "Log Directory: Accessible ($LOG_DIR)"
    else
        check_error "Log Directory: Not accessible ($LOG_DIR)"
    fi
    
    # Check if install directory exists
    if [[ -d "$INSTALL_DIR" ]]; then
        check_ok "Install Directory: Present ($INSTALL_DIR)"
    else
        check_error "Install Directory: Missing ($INSTALL_DIR)"
    fi
}

# Ollama service checks
check_ollama_service() {
    section_header "OLLAMA SERVICE"
    
    # Check if Ollama is installed
    if command -v ollama >/dev/null 2>&1; then
        local ollama_version
        ollama_version=$(ollama --version 2>/dev/null | head -1 || echo "unknown")
        check_ok "Ollama Installation: $ollama_version"
    else
        check_error "Ollama Installation: Not found"
        return 1
    fi
    
    # Check systemd service
    if systemctl is-active ollama >/dev/null 2>&1; then
        check_ok "Ollama Service: ACTIVE"
    else
        check_error "Ollama Service: INACTIVE"
    fi
    
    if systemctl is-enabled ollama >/dev/null 2>&1; then
        check_ok "Ollama Service: ENABLED"
    else
        check_warn "Ollama Service: NOT ENABLED"
    fi
    
    # Check API endpoint
    if curl -s --connect-timeout 5 http://127.0.0.1:11434/api/health >/dev/null 2>&1; then
        check_ok "Ollama API: RESPONSIVE"
    else
        check_error "Ollama API: UNRESPONSIVE"
    fi
    
    # Check configuration
    if [[ -f /etc/systemd/system/ollama.service.d/tauros-lucy.conf ]]; then
        check_ok "Tauros/Lucy Configuration: PRESENT"
        
        if [[ "$VERBOSE" == "true" ]]; then
            local config_host
            config_host=$(grep 'OLLAMA_HOST=' /etc/systemd/system/ollama.service.d/tauros-lucy.conf | cut -d'"' -f2)
            check_info "Configured Host: $config_host"
        fi
    else
        check_warn "Tauros/Lucy Configuration: MISSING"
    fi
}

# Model checks
check_model_status() {
    section_header "MODEL STATUS"
    
    # Check if model exists
    if ollama list 2>/dev/null | grep -q "$OLLAMA_MODEL"; then
        check_ok "CopilotPrivate Model: AVAILABLE"
        
        if [[ "$VERBOSE" == "true" ]]; then
            local model_size
            model_size=$(ollama list 2>/dev/null | grep "$OLLAMA_MODEL" | awk '{print $2}')
            check_info "Model Size: $model_size"
        fi
    else
        check_error "CopilotPrivate Model: NOT FOUND"
        return 1
    fi
    
    # Test model functionality
    local test_response
    test_response=$(timeout 10 ollama run "$OLLAMA_MODEL" "test" 2>/dev/null | head -1 || echo "")
    
    if [[ -n "$test_response" ]]; then
        check_ok "Model Functionality: RESPONSIVE"
        if [[ "$VERBOSE" == "true" ]]; then
            check_info "Test Response: $(echo "$test_response" | cut -c1-50)..."
        fi
    else
        check_error "Model Functionality: UNRESPONSIVE"
    fi
    
    # Test DEFEND mode
    if ! [[ "$QUICK" == "true" ]]; then
        local defend_response
        defend_response=$(timeout 15 ollama run "$OLLAMA_MODEL" "Status check Tauros/Lucy" 2>/dev/null | head -3 || echo "")
        
        if [[ -n "$defend_response" ]]; then
            check_ok "DEFEND Mode: FUNCTIONAL"
        else
            check_warn "DEFEND Mode: LIMITED RESPONSE"
        fi
    fi
}

# Security assessment
check_security() {
    section_header "SECURITY ASSESSMENT"
    
    # Check Ollama binding
    local ollama_host
    if [[ -f /etc/systemd/system/ollama.service.d/tauros-lucy.conf ]]; then
        ollama_host=$(grep 'OLLAMA_HOST=' /etc/systemd/system/ollama.service.d/tauros-lucy.conf | cut -d'"' -f2)
        if [[ "$ollama_host" == "127.0.0.1:11434" ]]; then
            check_ok "Ollama Binding: LOCALHOST ONLY"
        else
            check_warn "Ollama Binding: NOT RESTRICTED ($ollama_host)"
        fi
    else
        check_warn "Ollama Binding: CONFIGURATION NOT FOUND"
    fi
    
    # Check firewall
    if command -v ufw >/dev/null 2>&1; then
        if ufw status | grep -q "Status: active"; then
            check_ok "Firewall (UFW): ACTIVE"
        else
            check_warn "Firewall (UFW): INACTIVE"
        fi
    elif command -v firewall-cmd >/dev/null 2>&1; then
        if systemctl is-active firewalld >/dev/null 2>&1; then
            check_ok "Firewall (firewalld): ACTIVE"
        else
            check_warn "Firewall (firewalld): INACTIVE"
        fi
    else
        check_warn "Firewall: NOT CONFIGURED"
    fi
    
    # Check allowlist configuration
    if [[ -f "$INSTALL_DIR/config/allowlist.json" ]]; then
        check_ok "Allowlist: CONFIGURED"
    elif [[ -f "$INSTALL_DIR/config/allowlist.example.json" ]]; then
        check_warn "Allowlist: EXAMPLE ONLY (need configuration)"
    else
        check_warn "Allowlist: NOT FOUND"
    fi
    
    # Check file permissions
    if [[ -d "$LOG_DIR" ]]; then
        local log_perms
        log_perms=$(stat -c %a "$LOG_DIR")
        if [[ "$log_perms" == "750" ]]; then
            check_ok "Log Directory Permissions: SECURE ($log_perms)"
        else
            check_warn "Log Directory Permissions: INSECURE ($log_perms)"
        fi
    fi
    
    # Test keyword authentication
    if [[ "$SECURITY_FOCUS" == "true" && "$QUICK" == "false" ]]; then
        local auth_test
        auth_test=$(timeout 10 ollama run "$OLLAMA_MODEL" "security assessment without keyword" 2>/dev/null | head -2)
        if [[ -n "$auth_test" ]]; then
            check_info "Keyword Authentication: Response generated (check manual)"
        fi
    fi
}

# Performance metrics
check_performance() {
    section_header "PERFORMANCE METRICS"
    
    if [[ "$QUICK" == "true" ]]; then
        check_info "Performance checks skipped (quick mode)"
        return 0
    fi
    
    # API response time
    local start_time end_time response_time
    start_time=$(date +%s.%N)
    if curl -s --connect-timeout 10 http://127.0.0.1:11434/api/health >/dev/null 2>&1; then
        end_time=$(date +%s.%N)
        response_time=$(echo "$end_time - $start_time" | bc 2>/dev/null || echo "unknown")
        
        if [[ "$response_time" != "unknown" ]]; then
            if (( $(echo "$response_time < 1.0" | bc -l) )); then
                check_ok "API Response Time: ${response_time}s"
            elif (( $(echo "$response_time < 3.0" | bc -l) )); then
                check_warn "API Response Time: ${response_time}s (SLOW)"
            else
                check_error "API Response Time: ${response_time}s (VERY SLOW)"
            fi
        fi
    fi
    
    # Model inference time
    start_time=$(date +%s.%N)
    if timeout 30 ollama run "$OLLAMA_MODEL" "test" >/dev/null 2>&1; then
        end_time=$(date +%s.%N)
        local inference_time
        inference_time=$(echo "$end_time - $start_time" | bc 2>/dev/null || echo "unknown")
        
        if [[ "$inference_time" != "unknown" ]]; then
            if (( $(echo "$inference_time < 5.0" | bc -l) )); then
                check_ok "Model Inference Time: ${inference_time}s"
            elif (( $(echo "$inference_time < 15.0" | bc -l) )); then
                check_warn "Model Inference Time: ${inference_time}s (SLOW)"
            else
                check_warn "Model Inference Time: ${inference_time}s (VERY SLOW)"
            fi
        fi
    else
        check_error "Model Inference: TIMEOUT"
    fi
    
    # Resource usage
    if command -v pidof >/dev/null 2>&1; then
        local ollama_pid
        ollama_pid=$(pidof ollama || echo "")
        if [[ -n "$ollama_pid" ]]; then
            local cpu_usage mem_usage
            cpu_usage=$(ps -p "$ollama_pid" -o %cpu --no-headers 2>/dev/null | tr -d ' ')
            mem_usage=$(ps -p "$ollama_pid" -o %mem --no-headers 2>/dev/null | tr -d ' ')
            
            check_info "Ollama CPU Usage: ${cpu_usage}%"
            check_info "Ollama Memory Usage: ${mem_usage}%"
        fi
    fi
}

# Network connectivity
check_network() {
    section_header "NETWORK CONNECTIVITY"
    
    # Local connectivity
    if curl -s --connect-timeout 5 http://127.0.0.1:11434/api/health >/dev/null 2>&1; then
        check_ok "Local API Access: AVAILABLE"
    else
        check_error "Local API Access: FAILED"
    fi
    
    # External connectivity (for updates)
    if ping -c 1 -W 5 8.8.8.8 >/dev/null 2>&1; then
        check_ok "External Connectivity: AVAILABLE"
    else
        check_warn "External Connectivity: LIMITED"
    fi
    
    # DNS resolution
    if nslookup ollama.ai >/dev/null 2>&1; then
        check_ok "DNS Resolution: WORKING"
    else
        check_warn "DNS Resolution: ISSUES"
    fi
    
    # Port accessibility
    if netstat -tln 2>/dev/null | grep -q ":11434"; then
        check_ok "Ollama Port 11434: LISTENING"
    else
        check_error "Ollama Port 11434: NOT LISTENING"
    fi
}

# Ecosystem integration
check_ecosystem_integration() {
    section_header "ECOSYSTEM INTEGRATION"
    
    # Tauros platform integration
    if [[ -f "$INSTALL_DIR/config/tauros_integration.json" ]]; then
        check_ok "Tauros Platform: CONFIGURED"
    else
        check_info "Tauros Platform: READY FOR INTEGRATION"
    fi
    
    # Lucy AI suite coordination
    if [[ -f "$INSTALL_DIR/config/lucy_coordination.json" ]]; then
        check_ok "Lucy AI Suite: CONFIGURED"
    else
        check_info "Lucy AI Suite: READY FOR COORDINATION"
    fi
    
    # LOCCHIO monitoring
    if [[ -f "$INSTALL_DIR/config/locchio_monitor.yml" ]]; then
        check_ok "LOCCHIO Monitoring: CONFIGURED"
    else
        check_info "LOCCHIO Monitoring: READY FOR SYNC"
    fi
    
    # NEA network
    if [[ -f "$INSTALL_DIR/config/nea_network.conf" ]]; then
        check_ok "NEA Network: CONFIGURED"
    else
        check_info "NEA Network: READY FOR REGISTRATION"
    fi
    
    # Check for ecosystem scripts
    local integration_scripts=("tauros_sync.sh" "lucy_coord.sh" "locchio_sync.sh" "nea_register.sh")
    for script in "${integration_scripts[@]}"; do
        if [[ -f "$INSTALL_DIR/scripts/$script" ]]; then
            check_ok "Integration Script: $script PRESENT"
        else
            check_info "Integration Script: $script PENDING"
        fi
    done
}

# Generate JSON output
generate_json_output() {
    local timestamp
    timestamp=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    
    cat << EOF
{
  "timestamp": "$timestamp",
  "overall_status": "$OVERALL_STATUS",
  "issues_count": $ISSUES_COUNT,
  "warnings_count": $WARNINGS_COUNT,
  "checks": {
    "system_health": "completed",
    "ollama_service": "completed",
    "model_status": "completed",
    "security": "completed",
    "performance": "$([ "$QUICK" == "true" ] && echo "skipped" || echo "completed")",
    "network": "$([ "$NETWORK_TESTS" == "true" ] && echo "completed" || echo "skipped")",
    "ecosystem": "completed"
  },
  "recommendations": [
    $([ $ISSUES_COUNT -gt 0 ] && echo '"Address critical issues immediately",' || echo '')
    $([ $WARNINGS_COUNT -gt 0 ] && echo '"Review warnings for potential improvements",' || echo '')
    "Monitor system regularly with automated health checks"
  ]
}
EOF
}

# Summary
show_summary() {
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        generate_json_output
        return 0
    fi
    
    if [[ "$SILENT" == "true" ]]; then
        if [[ $ISSUES_COUNT -gt 0 ]]; then
            echo "UNHEALTHY: $ISSUES_COUNT critical issues found"
            return 2
        elif [[ $WARNINGS_COUNT -gt 0 ]]; then
            echo "WARNINGS: $WARNINGS_COUNT warnings found"
            return 1
        else
            echo "HEALTHY: All checks passed"
            return 0
        fi
    fi
    
    section_header "HEALTH CHECK SUMMARY"
    
    echo -e "\n${PURPLE}📊 FINAL RESULTS${NC}"
    echo -e "${PURPLE}$(printf '─%.0s' $(seq 1 30))${NC}"
    
    if [[ "$OVERALL_STATUS" == "HEALTHY" ]]; then
        echo -e "${GREEN}🎉 Overall Status: HEALTHY${NC}"
    else
        echo -e "${RED}⚠️  Overall Status: UNHEALTHY${NC}"
    fi
    
    echo -e "${BLUE}Issues Found: $ISSUES_COUNT${NC}"
    echo -e "${YELLOW}Warnings: $WARNINGS_COUNT${NC}"
    
    if [[ $ISSUES_COUNT -gt 0 ]]; then
        echo -e "\n${RED}🚨 CRITICAL ISSUES DETECTED${NC}"
        echo -e "${RED}Please address these issues immediately${NC}"
    fi
    
    if [[ $WARNINGS_COUNT -gt 0 ]]; then
        echo -e "\n${YELLOW}⚠️  WARNINGS FOUND${NC}"
        echo -e "${YELLOW}Consider reviewing these for optimization${NC}"
    fi
    
    echo -e "\n${CYAN}📝 Health check completed at $(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo -e "${CYAN}Log saved to: $HEALTH_LOG${NC}"
    
    # Exit code based on results
    if [[ $ISSUES_COUNT -gt 0 ]]; then
        return 2
    elif [[ $WARNINGS_COUNT -gt 0 ]]; then
        return 1
    else
        return 0
    fi
}

# Main execution
main() {
    # Initialize log
    mkdir -p "$LOG_DIR" 2>/dev/null || true
    log_health "Health check started by $USER"
    
    show_banner
    
    # Execute checks based on options
    check_system_health
    check_ollama_service
    check_model_status
    
    if [[ "$SECURITY_FOCUS" == "true" ]] || [[ "$SECURITY_FOCUS" == "false" && "$PERFORMANCE_FOCUS" == "false" ]]; then
        check_security
    fi
    
    if [[ "$PERFORMANCE_FOCUS" == "true" ]] || [[ "$SECURITY_FOCUS" == "false" && "$PERFORMANCE_FOCUS" == "false" ]]; then
        check_performance
    fi
    
    if [[ "$NETWORK_TESTS" == "true" ]]; then
        check_network
    fi
    
    check_ecosystem_integration
    
    log_health "Health check completed with status: $OVERALL_STATUS"
    
    show_summary
}

# Execute main function
main "$@"