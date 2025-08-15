#!/usr/bin/env python3
"""
Core Intelligence Engine - Brain Module
Copilot Private Agent Decision Making System
"""

import json
import os
import sys
import logging
import ipaddress
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class CopilotBrain:
    """Central intelligence for decision making and command coordination"""
    
    def __init__(self, config_dir: str = None):
        self.config_dir = Path(config_dir or os.path.join(os.path.dirname(__file__), '..', 'config'))
        self.setup_logging()
        self.load_configurations()
        
    def setup_logging(self):
        """Setup intelligent logging system"""
        log_dir = Path(os.path.dirname(__file__)).parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'brain.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('CopilotBrain')
        
    def load_configurations(self):
        """Load all configuration files with error handling"""
        try:
            # Load allowlist with fallback to example
            allowlist_file = self.config_dir / 'allowlist.json'
            if not allowlist_file.exists():
                allowlist_file = self.config_dir / 'allowlist.example.json'
            
            with open(allowlist_file) as f:
                self.allowlist = json.load(f)
                
            with open(self.config_dir / 'privileges.json') as f:
                self.privileges = json.load(f)
                
            with open(self.config_dir / 'profiles.json') as f:
                self.profiles = json.load(f)
                
            with open(self.config_dir / 'tools.json') as f:
                self.tools = json.load(f)
                
            self.logger.info("Configuration loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            raise
            
    def analyze_command(self, command: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Intelligent command analysis and decision making"""
        context = context or {}
        
        # Extract key information from command
        analysis = {
            'command': command,
            'timestamp': datetime.utcnow().isoformat(),
            'risk_level': 'unknown',
            'requires_wassim': False,
            'requires_admin': False,
            'target_type': 'unknown',
            'action_type': 'unknown',
            'recommended_profile': 'DEFEND',
            'safe_to_execute': False,
            'explanation': '',
            'suggested_escalation': None
        }
        
        # Keyword detection
        wassim_detected = 'wassim' in command.lower()
        analysis['wassim_keyword_detected'] = wassim_detected
        
        # Command type classification
        if any(word in command.lower() for word in ['scan', 'nmap', 'port']):
            analysis['action_type'] = 'scanning'
            analysis['risk_level'] = 'medium'
        elif any(word in command.lower() for word in ['attack', 'exploit', 'pentest']):
            analysis['action_type'] = 'penetration_testing'
            analysis['risk_level'] = 'high'
            analysis['requires_wassim'] = True
            analysis['requires_admin'] = True
        elif any(word in command.lower() for word in ['monitor', 'check', 'status']):
            analysis['action_type'] = 'monitoring'
            analysis['risk_level'] = 'low'
        elif any(word in command.lower() for word in ['recon', 'enumerate', 'discover']):
            analysis['action_type'] = 'reconnaissance'
            analysis['risk_level'] = 'medium'
        
        # Target detection and validation
        targets = self.extract_targets(command)
        analysis['targets'] = targets
        
        if targets:
            target_analysis = self.analyze_targets(targets)
            analysis.update(target_analysis)
        
        # Profile recommendation
        analysis['recommended_profile'] = self.recommend_profile(analysis)
        
        # Safety assessment
        analysis['safe_to_execute'] = self.assess_safety(analysis, wassim_detected)
        
        # Generate explanation
        analysis['explanation'] = self.generate_explanation(analysis)
        
        self.logger.info(f"Command analysis completed: {analysis['action_type']} with risk {analysis['risk_level']}")
        
        return analysis
        
    def extract_targets(self, command: str) -> List[str]:
        """Extract potential targets from command"""
        targets = []
        words = command.split()
        
        for word in words:
            # IP address detection
            try:
                ipaddress.ip_address(word)
                targets.append(word)
            except ValueError:
                pass
                
            # CIDR detection  
            try:
                ipaddress.ip_network(word, strict=False)
                targets.append(word)
            except ValueError:
                pass
                
            # Domain/hostname detection (simple)
            if '.' in word and not word.startswith('.') and len(word) > 3:
                targets.append(word)
        
        return targets
        
    def analyze_targets(self, targets: List[str]) -> Dict[str, Any]:
        """Analyze if targets are allowed and their characteristics"""
        allowed_targets = []
        blocked_targets = []
        
        for target in targets:
            if self.is_target_allowed(target):
                allowed_targets.append(target)
            else:
                blocked_targets.append(target)
                
        return {
            'allowed_targets': allowed_targets,
            'blocked_targets': blocked_targets,
            'target_allowed': len(blocked_targets) == 0,
            'target_type': self.classify_target_type(targets[0] if targets else '')
        }
        
    def is_target_allowed(self, target: str) -> bool:
        """Check if target is in allowlist"""
        try:
            # Check localhost variants
            localhost_hosts = self.allowlist.get('allowed_targets', {}).get('localhost', {}).get('hosts', [])
            if target in localhost_hosts:
                return True
                
            # Check specific hosts
            for category in self.allowlist.get('allowed_targets', {}).values():
                if isinstance(category, dict):
                    hosts = category.get('hosts', [])
                    if target in hosts:
                        return True
                        
                    # Check CIDR ranges
                    cidrs = category.get('cidrs', [])
                    for cidr in cidrs:
                        try:
                            if ipaddress.ip_address(target) in ipaddress.ip_network(cidr):
                                return True
                        except ValueError:
                            continue
                            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking target allowlist: {e}")
            return False
            
    def classify_target_type(self, target: str) -> str:
        """Classify the type of target"""
        if not target:
            return 'unknown'
            
        if target in ['localhost', '127.0.0.1', '::1']:
            return 'localhost'
        
        try:
            ip = ipaddress.ip_address(target)
            if ip.is_private:
                return 'private_ip'
            elif ip.is_global:
                return 'public_ip'
        except ValueError:
            pass
            
        if '.' in target and not target.replace('.', '').isdigit():
            return 'domain'
            
        return 'unknown'
        
    def recommend_profile(self, analysis: Dict[str, Any]) -> str:
        """Recommend operational profile based on analysis"""
        action_type = analysis.get('action_type', 'unknown')
        risk_level = analysis.get('risk_level', 'unknown')
        
        if action_type == 'monitoring':
            return 'DEFEND'
        elif action_type == 'penetration_testing':
            return 'TEST'
        elif risk_level == 'high':
            return 'STEALTH'
        elif analysis.get('target_type') == 'localhost':
            return 'AGGRESSIVE'
        else:
            return 'DEFEND'
            
    def assess_safety(self, analysis: Dict[str, Any], wassim_detected: bool) -> bool:
        """Assess if command is safe to execute"""
        # Check basic requirements
        if analysis['requires_wassim'] and not wassim_detected:
            return False
            
        if analysis.get('blocked_targets'):
            return False
            
        # Check risk level vs permissions
        risk_level = analysis['risk_level']
        if risk_level == 'high' and not wassim_detected:
            return False
            
        return True
        
    def generate_explanation(self, analysis: Dict[str, Any]) -> str:
        """Generate human-readable explanation of the analysis"""
        explanations = []
        
        explanations.append(f"Action Type: {analysis['action_type'].title()}")
        explanations.append(f"Risk Level: {analysis['risk_level'].upper()}")
        
        if analysis['targets']:
            explanations.append(f"Targets: {', '.join(analysis['targets'])}")
            if analysis.get('blocked_targets'):
                explanations.append(f"⚠️  Blocked targets: {', '.join(analysis['blocked_targets'])}")
                
        if analysis['requires_wassim']:
            if analysis['wassim_keyword_detected']:
                explanations.append("✅ Wassim keyword detected")
            else:
                explanations.append("❌ Wassim keyword required but not found")
                
        if analysis['safe_to_execute']:
            explanations.append("✅ Safe to execute")
        else:
            explanations.append("❌ Blocked - requirements not met")
            
        explanations.append(f"Recommended Profile: {analysis['recommended_profile']}")
        
        return " | ".join(explanations)
        
    def get_command_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate command suggestions based on analysis"""
        suggestions = []
        action_type = analysis.get('action_type', 'unknown')
        
        if action_type == 'scanning':
            suggestions.extend([
                "nmap -sn <target>  # Ping scan",
                "nmap -sS <target>  # SYN scan", 
                "nmap -sV <target>  # Version detection"
            ])
        elif action_type == 'monitoring':
            suggestions.extend([
                "netstat -tulpn  # Active connections",
                "ss -tulpn       # Socket statistics",
                "ps aux          # Running processes"
            ])
        elif action_type == 'reconnaissance':
            suggestions.extend([
                "subfinder -d <domain>  # Subdomain enumeration",
                "amass enum -d <domain> # Active reconnaissance",
                "nuclei -u <target>     # Vulnerability scan"
            ])
            
        return suggestions
        
    def auto_detect_environment(self) -> Dict[str, Any]:
        """Auto-detect current environment and network configuration"""
        environment = {
            'detected_networks': [],
            'system_info': {},
            'security_tools': {},
            'environment_type': 'unknown'
        }
        
        try:
            # Detect local networks
            result = subprocess.run(['ip', 'route'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'default via' in line:
                        # Extract default gateway and network
                        parts = line.split()
                        if len(parts) >= 3:
                            gateway = parts[2]
                            environment['detected_networks'].append({
                                'type': 'default_route',
                                'gateway': gateway
                            })
        except Exception as e:
            self.logger.warning(f"Network detection failed: {e}")
            
        return environment

if __name__ == "__main__":
    # Test the brain
    brain = CopilotBrain()
    
    test_commands = [
        "scan my network",
        "Wassim pentest 192.168.1.1", 
        "monitor localhost processes",
        "nmap -sS 8.8.8.8"
    ]
    
    for cmd in test_commands:
        print(f"\n=== Analyzing: {cmd} ===")
        analysis = brain.analyze_command(cmd)
        print(f"Result: {analysis['explanation']}")
        print(f"Safe: {'Yes' if analysis['safe_to_execute'] else 'No'}")