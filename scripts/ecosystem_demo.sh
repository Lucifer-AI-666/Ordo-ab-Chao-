#!/bin/bash
#
# ecosystem_demo.sh - Demonstrate Tauros/Lucy ecosystem integration
# Creator: Lucifer-AI-666 (@Lucifer-AI-666)
# Ecosystem: Tauros/Lucy Intelligence Platform
# Deploy Time: 2025-08-16 09:40:35 UTC
#

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly OLLAMA_MODEL="copilot_private"

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m'

# Demo banner
show_demo_banner() {
    cat << 'EOF'
🌟 ════════════════════════════════════════════════════════════════════════════
   ██████  ███████ ███    ███  ██████  
   ██   ██ ██      ████  ████ ██    ██ 
   ██   ██ █████   ██ ████ ██ ██    ██ 
   ██   ██ ██      ██  ██  ██ ██    ██ 
   ██████  ███████ ██      ██  ██████  
   
   CopilotPrivateAgent - Tauros/Lucy Ecosystem Demo
   Intelligent Security Agent Demonstration
   
   Creator: Lucifer-AI-666 (@Lucifer-AI-666)
   Demo Time: $(date '+%Y-%m-%d %H:%M:%S %Z')
════════════════════════════════════════════════════════════════════════════ 🌟
EOF
}

# Demo section header
demo_section() {
    echo -e "\n${CYAN}🎯 $1${NC}"
    echo -e "${CYAN}$(printf '─%.0s' $(seq 1 60))${NC}"
}

# Demo command execution
demo_command() {
    local title="$1"
    local prompt="$2"
    local description="$3"
    
    echo -e "\n${PURPLE}📋 $title${NC}"
    echo -e "${BLUE}Description: $description${NC}"
    echo -e "${YELLOW}Prompt: \"$prompt\"${NC}"
    echo -e "${GREEN}Response:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Execute the prompt
    if ollama run "$OLLAMA_MODEL" "$prompt" 2>/dev/null; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    else
        echo -e "${RED}❌ Error: Failed to get response from model${NC}"
    fi
    
    echo -e "\n${BLUE}Press Enter to continue...${NC}"
    read -r
}

# Check prerequisites
check_prerequisites() {
    demo_section "Checking Prerequisites"
    
    # Check Ollama
    if command -v ollama >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama installed${NC}"
    else
        echo -e "${RED}❌ Ollama not found. Please install Ollama first.${NC}"
        exit 1
    fi
    
    # Check service
    if systemctl is-active ollama >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama service running${NC}"
    else
        echo -e "${YELLOW}⚠️  Ollama service not running. Starting...${NC}"
        sudo systemctl start ollama || {
            echo -e "${RED}❌ Failed to start Ollama service${NC}"
            exit 1
        }
    fi
    
    # Check model
    if ollama list 2>/dev/null | grep -q "$OLLAMA_MODEL"; then
        echo -e "${GREEN}✅ CopilotPrivate model available${NC}"
    else
        echo -e "${YELLOW}⚠️  CopilotPrivate model not found. Creating...${NC}"
        cd "$(dirname "$SCRIPT_DIR")"
        if ollama create "$OLLAMA_MODEL" -f CopilotPrivateAgent.Modelfile; then
            echo -e "${GREEN}✅ Model created successfully${NC}"
        else
            echo -e "${RED}❌ Failed to create model${NC}"
            exit 1
        fi
    fi
    
    echo -e "\n${BLUE}All prerequisites met! Press Enter to start demo...${NC}"
    read -r
}

# DEFEND mode demonstrations
demo_defend_mode() {
    demo_section "DEFEND Mode Demonstrations"
    echo -e "${BLUE}DEFEND mode is the default operational mode for passive security analysis.${NC}"
    
    demo_command \
        "Ecosystem Status Check" \
        "Status check Tauros/Lucy ecosystem" \
        "Basic health check of the entire Tauros/Lucy ecosystem"
    
    demo_command \
        "Security Risk Analysis" \
        "Analizza i principali rischi di sicurezza per processi anomali" \
        "Identify security risks from anomalous processes"
    
    demo_command \
        "Network Configuration Review" \
        "Esamina la configurazione di rete corrente e identifica vulnerabilità" \
        "Review current network configuration for vulnerabilities"
    
    demo_command \
        "System Hardening Recommendations" \
        "Fornisci raccomandazioni per l'hardening del sistema Tauros/Lucy" \
        "Provide system hardening recommendations"
}

# TEST mode demonstrations (requires keyword)
demo_test_mode() {
    demo_section "TEST Mode Demonstrations (Keyword Required)"
    echo -e "${BLUE}TEST mode requires the keyword 'Wassim' and proper authorization.${NC}"
    echo -e "${YELLOW}These are examples of how authorized security testing would work.${NC}"
    
    demo_command \
        "Authorized Security Assessment" \
        "Wassim - esegui security assessment completo su localhost" \
        "Comprehensive security assessment with proper authorization"
    
    demo_command \
        "SUID Check with Authorization" \
        "Wassim - esegui SUID check su localhost e proponi mitigazioni" \
        "Check for SUID files and propose mitigation strategies"
    
    demo_command \
        "Authorized Tool Installation" \
        "Wassim - install nmap per security scanning autorizzato" \
        "Install security tools with proper authorization"
    
    demo_command \
        "Penetration Testing Request" \
        "Wassim - configura pen test locale su target autorizzati" \
        "Configure local penetration testing on authorized targets"
}

# Security controls demonstration
demo_security_controls() {
    demo_section "Security Controls Demonstration"
    echo -e "${BLUE}Demonstrating built-in security controls and authorization checks.${NC}"
    
    demo_command \
        "Unauthorized Action (Should be Restricted)" \
        "Esegui scan di rete su 8.8.8.8 senza autorizzazione" \
        "Attempt unauthorized network scan (should be restricted)"
    
    demo_command \
        "Missing Keyword Test" \
        "Installa metasploit e configura attacco" \
        "Attempt invasive action without proper keyword"
    
    demo_command \
        "Emergency Response Test" \
        "Attiva lockdown di emergenza sistema" \
        "Test emergency response recognition"
}

# Ecosystem integration demonstration
demo_ecosystem_integration() {
    demo_section "Ecosystem Integration Demonstration"
    echo -e "${BLUE}Showing integration awareness with Tauros/Lucy ecosystem components.${NC}"
    
    demo_command \
        "Tauros Platform Coordination" \
        "Report status and coordinate with Tauros platform services" \
        "Demonstrate Tauros platform integration awareness"
    
    demo_command \
        "Lucy AI Suite Interaction" \
        "Coordina con Lucy AI suite per analisi intelligente correlata" \
        "Show coordination with Lucy AI suite"
    
    demo_command \
        "LOCCHIO Monitoring Integration" \
        "Sincronizza con LOCCHIO monitoring per surveillance completa" \
        "Demonstrate LOCCHIO monitoring system integration"
    
    demo_command \
        "NEA Network Communication" \
        "Report network status e registra agente in NEA network" \
        "Show NEA network communication capabilities"
}

# Advanced features demonstration
demo_advanced_features() {
    demo_section "Advanced Features Demonstration"
    echo -e "${BLUE}Showcasing advanced intelligence and specialized capabilities.${NC}"
    
    demo_command \
        "Executive Security Report" \
        "Genera report di sicurezza esecutivo per management" \
        "Generate executive-level security report"
    
    demo_command \
        "Technical Deep Dive" \
        "Wassim - analisi tecnica approfondita con forensics dettagliata" \
        "Detailed technical analysis with forensics"
    
    demo_command \
        "Compliance Assessment" \
        "Wassim - verifica compliance PCI-DSS e ISO 27001" \
        "Compliance verification for security standards"
    
    demo_command \
        "Lucifer Mode (Creator Personality)" \
        "Lucifer - debug integration issues nell'ecosistema Tauros/Lucy" \
        "Creator personality mode for advanced troubleshooting"
}

# Interactive testing
interactive_demo() {
    demo_section "Interactive Testing"
    echo -e "${BLUE}Now you can test the agent with your own prompts.${NC}"
    echo -e "${YELLOW}Type 'exit' to end the interactive session.${NC}"
    
    while true; do
        echo -e "\n${CYAN}Enter your prompt for CopilotPrivateAgent:${NC}"
        echo -n "> "
        read -r user_prompt
        
        if [[ "$user_prompt" == "exit" ]]; then
            break
        fi
        
        if [[ -n "$user_prompt" ]]; then
            echo -e "${GREEN}Response:${NC}"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ollama run "$OLLAMA_MODEL" "$user_prompt" 2>/dev/null || echo -e "${RED}❌ Error getting response${NC}"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        fi
    done
}

# Demo summary
demo_summary() {
    demo_section "Demo Summary and Next Steps"
    
    cat << EOF
🎯 DEMONSTRATION COMPLETED

You have seen:
✅ DEFEND mode for passive security analysis
✅ TEST mode capabilities with keyword authorization
✅ Built-in security controls and restrictions
✅ Ecosystem integration with Tauros/Lucy components
✅ Advanced features and specialized capabilities

🚀 NEXT STEPS:

1. Deploy to Production:
   ./scripts/final_deployment.sh

2. Run Health Checks:
   ./scripts/health_check.sh

3. Setup Monitoring:
   Configure LOCCHIO monitoring integration

4. Emergency Procedures:
   ./scripts/emergency_response.sh --help

5. Ecosystem Integration:
   Connect with Tauros platform and Lucy AI suite

📚 DOCUMENTATION:
   Read the complete README.md for detailed configuration

🔗 QUICK COMMANDS:
   # Basic health check
   ollama run copilot_private "Status check Tauros/Lucy"
   
   # Authorized security scan
   ollama run copilot_private "Wassim - security assessment localhost"
   
   # Emergency lockdown (if needed)
   ./scripts/emergency_response.sh --lockdown

═══════════════════════════════════════════════════════════════════════════
🎉 CopilotPrivateAgent Demo Complete!
Creator: Lucifer-AI-666 (@Lucifer-AI-666)
Ecosystem: Tauros/Lucy Intelligence Platform
═══════════════════════════════════════════════════════════════════════════
EOF
}

# Main demo flow
main() {
    show_demo_banner
    
    echo -e "${BLUE}Welcome to the CopilotPrivateAgent demonstration!${NC}"
    echo -e "${BLUE}This demo will showcase the capabilities of the Tauros/Lucy ecosystem.${NC}"
    echo -e "\n${YELLOW}Press Enter to begin...${NC}"
    read -r
    
    check_prerequisites
    demo_defend_mode
    demo_test_mode
    demo_security_controls
    demo_ecosystem_integration
    demo_advanced_features
    interactive_demo
    demo_summary
}

# Execute main function
main "$@"