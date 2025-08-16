#!/bin/bash
#
# test_copilot_agent.sh - Test CopilotPrivateAgent functionality
# Creator: Lucifer-AI-666 (@Lucifer-AI-666)
# Ecosystem: Tauros/Lucy Intelligence Platform
# Deploy Time: 2025-08-16 09:40:35 UTC
#

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
readonly OLLAMA_MODEL="copilot_private"
readonly TEST_LOG="/tmp/copilot_test_$(date '+%Y%m%d_%H%M%S').log"

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly NC='\033[0m'

# Test results
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Logging functions
log_test() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" >> "$TEST_LOG"
    echo -e "${BLUE}[TEST] $message${NC}"
}

test_pass() {
    local test_name="$1"
    echo -e "${GREEN}✅ PASS: $test_name${NC}"
    ((TESTS_PASSED++))
    ((TESTS_TOTAL++))
    log_test "PASS: $test_name"
}

test_fail() {
    local test_name="$1"
    local error_msg="${2:-No error message}"
    echo -e "${RED}❌ FAIL: $test_name${NC}"
    echo -e "${RED}   Error: $error_msg${NC}"
    ((TESTS_FAILED++))
    ((TESTS_TOTAL++))
    log_test "FAIL: $test_name - $error_msg"
}

test_skip() {
    local test_name="$1"
    local reason="${2:-No reason provided}"
    echo -e "${YELLOW}⏭️  SKIP: $test_name (${reason})${NC}"
    ((TESTS_TOTAL++))
    log_test "SKIP: $test_name - $reason"
}

# Banner
show_test_banner() {
    cat << 'EOF'
🧪 ════════════════════════════════════════════════════════════════════════════
   ████████ ███████ ███████ ████████ 
   ██    ██ ██      ██         ██    
   ██    ██ █████   ███████    ██    
   ██    ██ ██           ██    ██    
   ████████ ███████ ███████    ██    
   
   CopilotPrivateAgent Testing Suite - Tauros/Lucy Ecosystem
   Creator: Lucifer-AI-666 (@Lucifer-AI-666)
   Test Time: $(date '+%Y-%m-%d %H:%M:%S %Z')
════════════════════════════════════════════════════════════════════════════ 🧪
EOF
}

# Test Ollama installation
test_ollama_installation() {
    log_test "Testing Ollama installation"
    
    if command -v ollama >/dev/null 2>&1; then
        local version
        version=$(ollama --version 2>/dev/null | head -1 || echo "unknown")
        test_pass "Ollama Installation ($version)"
    else
        test_fail "Ollama Installation" "Ollama command not found"
        return 1
    fi
}

# Test Ollama service
test_ollama_service() {
    log_test "Testing Ollama service"
    
    if systemctl is-active ollama >/dev/null 2>&1; then
        test_pass "Ollama Service Status"
    else
        test_fail "Ollama Service Status" "Service not active"
        return 1
    fi
    
    # Test API endpoint
    if curl -s --connect-timeout 5 http://127.0.0.1:11434/api/health >/dev/null 2>&1; then
        test_pass "Ollama API Connectivity"
    else
        test_fail "Ollama API Connectivity" "API not responding"
        return 1
    fi
}

# Test model availability
test_model_availability() {
    log_test "Testing CopilotPrivate model availability"
    
    if ollama list 2>/dev/null | grep -q "$OLLAMA_MODEL"; then
        test_pass "CopilotPrivate Model Availability"
    else
        test_fail "CopilotPrivate Model Availability" "Model not found in ollama list"
        return 1
    fi
}

# Test DEFEND mode functionality
test_defend_mode() {
    log_test "Testing DEFEND mode functionality"
    
    local test_prompt="Status check Tauros/Lucy ecosystem"
    local response
    
    # Test basic response
    response=$(timeout 30 ollama run "$OLLAMA_MODEL" "$test_prompt" 2>/dev/null | head -10 || echo "")
    
    if [[ -n "$response" ]]; then
        test_pass "DEFEND Mode Basic Response"
        
        # Check if response contains expected sections
        if echo "$response" | grep -qi "analisi\|analysis"; then
            test_pass "DEFEND Mode Output Format (Analysis section)"
        else
            test_fail "DEFEND Mode Output Format" "Missing Analysis section"
        fi
        
        # Test ecosystem awareness
        if echo "$response" | grep -qi "tauros\|lucy"; then
            test_pass "DEFEND Mode Ecosystem Awareness"
        else
            test_fail "DEFEND Mode Ecosystem Awareness" "No ecosystem references found"
        fi
        
    else
        test_fail "DEFEND Mode Basic Response" "No response received"
    fi
}

# Test security controls
test_security_controls() {
    log_test "Testing security controls"
    
    # Test unauthorized action (should work but with warnings)
    local unauthorized_prompt="Execute system scan without authorization"
    local response
    
    response=$(timeout 15 ollama run "$OLLAMA_MODEL" "$unauthorized_prompt" 2>/dev/null | head -5 || echo "")
    
    if [[ -n "$response" ]]; then
        # Check if response mentions security or authorization
        if echo "$response" | grep -qi "sicurezza\|security\|autorizzazione\|authorization\|wassim"; then
            test_pass "Security Controls - Unauthorized Action Recognition"
        else
            test_fail "Security Controls" "No security warnings in response"
        fi
    else
        test_skip "Security Controls" "No response to test prompt"
    fi
}

# Test keyword authentication awareness
test_keyword_authentication() {
    log_test "Testing keyword authentication awareness"
    
    # Test with keyword
    local auth_prompt="Wassim - status check for security assessment"
    local response
    
    response=$(timeout 20 ollama run "$OLLAMA_MODEL" "$auth_prompt" 2>/dev/null | head -10 || echo "")
    
    if [[ -n "$response" ]]; then
        if echo "$response" | grep -qi "wassim\|authentication\|authorized\|test.*mode"; then
            test_pass "Keyword Authentication Awareness"
        else
            test_fail "Keyword Authentication" "No authentication recognition"
        fi
    else
        test_skip "Keyword Authentication" "No response to keyword prompt"
    fi
}

# Test configuration files
test_configuration_files() {
    log_test "Testing configuration files"
    
    # Test systemd service file
    if [[ -f "$PROJECT_ROOT/config/ollama-tauros-lucy.service" ]]; then
        if grep -q "OLLAMA_HOST=127.0.0.1:11434" "$PROJECT_ROOT/config/ollama-tauros-lucy.service"; then
            test_pass "Systemd Service Configuration"
        else
            test_fail "Systemd Service Configuration" "Missing localhost binding"
        fi
    else
        test_fail "Systemd Service Configuration" "Service file not found"
    fi
    
    # Test nginx configuration
    if [[ -f "$PROJECT_ROOT/config/nginx-tauros-lucy.conf" ]]; then
        if grep -q "listen 443 ssl" "$PROJECT_ROOT/config/nginx-tauros-lucy.conf"; then
            test_pass "Nginx SSL Configuration"
        else
            test_fail "Nginx SSL Configuration" "SSL not configured"
        fi
    else
        test_fail "Nginx Configuration" "Nginx config file not found"
    fi
    
    # Test LOCCHIO monitoring configuration
    if [[ -f "$PROJECT_ROOT/config/locchio-tauros-lucy.yml" ]]; then
        if grep -q "copilot_private" "$PROJECT_ROOT/config/locchio-tauros-lucy.yml"; then
            test_pass "LOCCHIO Monitoring Configuration"
        else
            test_fail "LOCCHIO Monitoring Configuration" "Model reference not found"
        fi
    else
        test_fail "LOCCHIO Configuration" "Monitoring config file not found"
    fi
    
    # Test allowlist template
    if [[ -f "$PROJECT_ROOT/config/allowlist.example.json" ]]; then
        if grep -q "127.0.0.1" "$PROJECT_ROOT/config/allowlist.example.json"; then
            test_pass "Allowlist Template Configuration"
        else
            test_fail "Allowlist Template" "Localhost not in allowlist"
        fi
    else
        test_fail "Allowlist Template" "Allowlist template not found"
    fi
}

# Test script functionality
test_scripts() {
    log_test "Testing deployment scripts"
    
    # Test script existence and permissions
    local scripts=("deploy_tauros_lucy.sh" "final_deployment.sh" "health_check.sh" "emergency_response.sh")
    
    for script in "${scripts[@]}"; do
        if [[ -f "$PROJECT_ROOT/scripts/$script" ]]; then
            if [[ -x "$PROJECT_ROOT/scripts/$script" ]]; then
                test_pass "Script $script (executable)"
            else
                test_fail "Script $script" "Not executable"
            fi
        else
            test_fail "Script $script" "File not found"
        fi
    done
    
    # Test health check script functionality
    if [[ -x "$PROJECT_ROOT/scripts/health_check.sh" ]]; then
        # Run health check in dry-run mode if possible
        if "$PROJECT_ROOT/scripts/health_check.sh" --help >/dev/null 2>&1; then
            test_pass "Health Check Script Functionality"
        else
            test_skip "Health Check Script" "Help option not working"
        fi
    fi
    
    # Test emergency response script
    if [[ -x "$PROJECT_ROOT/scripts/emergency_response.sh" ]]; then
        if "$PROJECT_ROOT/scripts/emergency_response.sh" --help >/dev/null 2>&1; then
            test_pass "Emergency Response Script Functionality"
        else
            test_skip "Emergency Response Script" "Help option not working"
        fi
    fi
}

# Test response time
test_response_time() {
    log_test "Testing response time performance"
    
    local start_time end_time response_time
    local test_prompt="test"
    
    start_time=$(date +%s.%N)
    if timeout 30 ollama run "$OLLAMA_MODEL" "$test_prompt" >/dev/null 2>&1; then
        end_time=$(date +%s.%N)
        response_time=$(echo "$end_time - $start_time" | bc 2>/dev/null || echo "unknown")
        
        if [[ "$response_time" != "unknown" ]]; then
            if (( $(echo "$response_time < 15.0" | bc -l 2>/dev/null || echo 0) )); then
                test_pass "Response Time Performance (${response_time}s)"
            else
                test_fail "Response Time Performance" "Too slow: ${response_time}s"
            fi
        else
            test_skip "Response Time Performance" "Could not measure time"
        fi
    else
        test_fail "Response Time Performance" "Model timeout"
    fi
}

# Test ecosystem integration readiness
test_ecosystem_readiness() {
    log_test "Testing ecosystem integration readiness"
    
    # Test for ecosystem-aware prompts
    local ecosystem_prompt="Report status of Tauros platform and Lucy AI coordination"
    local response
    
    response=$(timeout 25 ollama run "$OLLAMA_MODEL" "$ecosystem_prompt" 2>/dev/null | head -10 || echo "")
    
    if [[ -n "$response" ]]; then
        local ecosystem_mentions=0
        
        if echo "$response" | grep -qi "tauros"; then
            ((ecosystem_mentions++))
        fi
        if echo "$response" | grep -qi "lucy"; then
            ((ecosystem_mentions++))
        fi
        if echo "$response" | grep -qi "ecosystem\|integration\|coordination"; then
            ((ecosystem_mentions++))
        fi
        
        if [[ $ecosystem_mentions -ge 2 ]]; then
            test_pass "Ecosystem Integration Readiness"
        else
            test_fail "Ecosystem Integration" "Limited ecosystem awareness"
        fi
    else
        test_skip "Ecosystem Integration" "No response to ecosystem prompt"
    fi
}

# Test documentation completeness
test_documentation() {
    log_test "Testing documentation completeness"
    
    if [[ -f "$PROJECT_ROOT/README.md" ]]; then
        local doc_content
        doc_content=$(cat "$PROJECT_ROOT/README.md")
        
        local required_sections=("Installation" "Configuration" "Security" "Tauros" "Lucy")
        local found_sections=0
        
        for section in "${required_sections[@]}"; do
            if echo "$doc_content" | grep -qi "$section"; then
                ((found_sections++))
            fi
        done
        
        if [[ $found_sections -ge 4 ]]; then
            test_pass "Documentation Completeness ($found_sections/${#required_sections[@]} sections)"
        else
            test_fail "Documentation Completeness" "Missing required sections ($found_sections/${#required_sections[@]})"
        fi
    else
        test_fail "Documentation" "README.md not found"
    fi
}

# Generate test report
generate_test_report() {
    local report_file="/tmp/copilot_test_report_$(date '+%Y%m%d_%H%M%S').txt"
    
    cat > "$report_file" << EOF
🧪 COPILOTPRIVATEAGENT TEST REPORT
═══════════════════════════════════════════════════════════════

Test Time: $(date '+%Y-%m-%d %H:%M:%S %Z')
Creator: Lucifer-AI-666 (@Lucifer-AI-666)
Ecosystem: Tauros/Lucy Intelligence Platform

📊 TEST SUMMARY
━━━━━━━━━━━━━━━
Total Tests: $TESTS_TOTAL
Passed: $TESTS_PASSED
Failed: $TESTS_FAILED
Skipped: $((TESTS_TOTAL - TESTS_PASSED - TESTS_FAILED))

Success Rate: $(( TESTS_PASSED * 100 / TESTS_TOTAL ))%

🎯 DEPLOYMENT READINESS
━━━━━━━━━━━━━━━━━━━━━━━
$(if [[ $TESTS_FAILED -eq 0 ]]; then
    echo "✅ READY FOR DEPLOYMENT"
    echo "All critical tests passed successfully."
elif [[ $TESTS_FAILED -le 2 ]]; then
    echo "⚠️  DEPLOYMENT WITH CAUTION"
    echo "Minor issues detected, review failed tests."
else
    echo "❌ NOT READY FOR DEPLOYMENT"
    echo "Critical issues detected, fix required."
fi)

📋 DETAILED RESULTS
━━━━━━━━━━━━━━━━━━━
$(cat "$TEST_LOG")

🔗 NEXT STEPS
━━━━━━━━━━━━━
$(if [[ $TESTS_FAILED -eq 0 ]]; then
    echo "1. Deploy with: ./scripts/final_deployment.sh"
    echo "2. Run health check: ./scripts/health_check.sh"
    echo "3. Test live: ollama run copilot_private 'Status check Tauros/Lucy'"
else
    echo "1. Review failed tests above"
    echo "2. Fix identified issues"
    echo "3. Re-run tests: ./scripts/test_copilot_agent.sh"
fi)

═══════════════════════════════════════════════════════════════
EOF
    
    # Display report
    cat "$report_file"
    
    echo -e "\n${BLUE}📄 Full test report saved to: $report_file${NC}"
    echo -e "${BLUE}📄 Test log saved to: $TEST_LOG${NC}"
    
    # Return appropriate exit code
    if [[ $TESTS_FAILED -eq 0 ]]; then
        return 0
    elif [[ $TESTS_FAILED -le 2 ]]; then
        return 1
    else
        return 2
    fi
}

# Main test execution
main() {
    show_test_banner
    
    log_test "Starting CopilotPrivateAgent test suite"
    
    # Core functionality tests
    test_ollama_installation
    test_ollama_service
    test_model_availability
    test_defend_mode
    test_security_controls
    test_keyword_authentication
    
    # Configuration tests
    test_configuration_files
    test_scripts
    
    # Performance tests
    test_response_time
    
    # Integration tests
    test_ecosystem_readiness
    test_documentation
    
    # Generate final report
    generate_test_report
}

# Execute main function
main "$@"