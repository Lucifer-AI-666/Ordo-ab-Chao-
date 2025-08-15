#!/usr/bin/env python3
"""
Cyber Defense and Hardening Tool - cyber-defend.py
Defensive security, monitoring, and hardening capabilities
"""

import argparse
import json
import sys
import os
import subprocess
import psutil
import socket
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine.brain import CopilotBrain

class CyberDefense:
    """Comprehensive defensive security and monitoring system"""
    
    def __init__(self):
        self.brain = CopilotBrain()
        self.results = {
            'defense_id': datetime.utcnow().strftime('%Y%m%d_%H%M%S'),
            'timestamp': datetime.utcnow().isoformat(),
            'action_type': '',
            'findings': {}
        }
        
    def system_monitoring(self) -> Dict[str, Any]:
        """Comprehensive system monitoring and health check"""
        result = {
            'type': 'system_monitoring',
            'timestamp': datetime.utcnow().isoformat(),
            'system_health': {},
            'network_connections': [],
            'running_processes': [],
            'suspicious_activities': [],
            'resource_usage': {}
        }
        
        try:
            # System resource monitoring
            result['resource_usage'] = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': {p.mountpoint: psutil.disk_usage(p.mountpoint).percent 
                              for p in psutil.disk_partitions()},
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None
            }
            
            # Network connections monitoring
            connections = psutil.net_connections(kind='inet')
            for conn in connections:
                if conn.status == 'ESTABLISHED':
                    try:
                        process = psutil.Process(conn.pid) if conn.pid else None
                        result['network_connections'].append({
                            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
                            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                            'status': conn.status,
                            'pid': conn.pid,
                            'process_name': process.name() if process else 'Unknown'
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                        
            # Process monitoring
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'connections']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] > 50 or proc_info['memory_percent'] > 50:
                        result['running_processes'].append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            # Suspicious activity detection
            suspicious_processes = [
                'nc', 'netcat', 'ncat', 'telnet', 'ssh', 'ftp', 'wget', 'curl'
            ]
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    proc_info = proc.info
                    if any(susp in proc_info['name'].lower() for susp in suspicious_processes):
                        result['suspicious_activities'].append({
                            'type': 'suspicious_process',
                            'process': proc_info['name'],
                            'pid': proc_info['pid'],
                            'cmdline': ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else ''
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def security_audit(self) -> Dict[str, Any]:
        """Comprehensive security audit of the system"""
        result = {
            'type': 'security_audit',
            'timestamp': datetime.utcnow().isoformat(),
            'user_accounts': [],
            'suid_binaries': [],
            'world_writable_files': [],
            'listening_services': [],
            'firewall_status': {},
            'security_findings': []
        }
        
        try:
            # User account audit
            with open('/etc/passwd', 'r') as f:
                for line in f:
                    parts = line.strip().split(':')
                    if len(parts) >= 7:
                        uid = int(parts[2])
                        shell = parts[6]
                        if uid >= 1000 or (uid == 0 and parts[0] == 'root'):
                            result['user_accounts'].append({
                                'username': parts[0],
                                'uid': uid,
                                'shell': shell,
                                'home': parts[5]
                            })
                            
            # SUID binary detection
            try:
                suid_process = subprocess.run(['find', '/', '-perm', '-4000', '-type', 'f'], 
                                            capture_output=True, text=True, timeout=60)
                if suid_process.returncode == 0:
                    result['suid_binaries'] = suid_process.stdout.strip().split('\n')
            except subprocess.TimeoutExpired:
                result['suid_binaries'] = ['Search timeout']
                
            # World-writable files (dangerous)
            try:
                writable_process = subprocess.run(['find', '/', '-perm', '-002', '-type', 'f', '!', '-path', '/proc/*'], 
                                                capture_output=True, text=True, timeout=60)
                if writable_process.returncode == 0:
                    result['world_writable_files'] = writable_process.stdout.strip().split('\n')[:20]  # Limit output
            except subprocess.TimeoutExpired:
                result['world_writable_files'] = ['Search timeout']
                
            # Listening services
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'LISTEN':
                    try:
                        process = psutil.Process(conn.pid) if conn.pid else None
                        result['listening_services'].append({
                            'address': f"{conn.laddr.ip}:{conn.laddr.port}",
                            'pid': conn.pid,
                            'process': process.name() if process else 'Unknown'
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                        
            # Firewall status check
            try:
                ufw_status = subprocess.run(['ufw', 'status'], capture_output=True, text=True, timeout=10)
                if ufw_status.returncode == 0:
                    result['firewall_status']['ufw'] = ufw_status.stdout.strip()
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
                
            try:
                iptables_status = subprocess.run(['iptables', '-L'], capture_output=True, text=True, timeout=10)
                if iptables_status.returncode == 0:
                    rules_count = len(iptables_status.stdout.strip().split('\n'))
                    result['firewall_status']['iptables_rules'] = rules_count
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
                
            # Generate security findings
            if len(result['suid_binaries']) > 50:
                result['security_findings'].append('High number of SUID binaries detected')
                
            if result['world_writable_files']:
                result['security_findings'].append('World-writable files detected')
                
            external_listeners = [s for s in result['listening_services'] if not s['address'].startswith('127.')]
            if external_listeners:
                result['security_findings'].append(f'{len(external_listeners)} services listening on external interfaces')
                
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def network_hardening(self) -> Dict[str, Any]:
        """Apply network hardening measures"""
        result = {
            'type': 'network_hardening',
            'timestamp': datetime.utcnow().isoformat(),
            'actions_taken': [],
            'recommendations': [],
            'before_state': {},
            'after_state': {}
        }
        
        try:
            # Record current state
            result['before_state'] = {
                'listening_ports': len([c for c in psutil.net_connections() if c.status == 'LISTEN']),
                'external_connections': len([c for c in psutil.net_connections() if c.status == 'ESTABLISHED'])
            }
            
            # Hardening actions (dry-run mode for safety)
            hardening_commands = [
                {
                    'description': 'Disable IP forwarding',
                    'command': 'echo 0 > /proc/sys/net/ipv4/ip_forward',
                    'check': 'cat /proc/sys/net/ipv4/ip_forward'
                },
                {
                    'description': 'Enable SYN flood protection',
                    'command': 'echo 1 > /proc/sys/net/ipv4/tcp_syncookies',
                    'check': 'cat /proc/sys/net/ipv4/tcp_syncookies'
                },
                {
                    'description': 'Disable ICMP redirects',
                    'command': 'echo 0 > /proc/sys/net/ipv4/conf/all/accept_redirects',
                    'check': 'cat /proc/sys/net/ipv4/conf/all/accept_redirects'
                }
            ]
            
            for action in hardening_commands:
                try:
                    # Check current value
                    check_result = subprocess.run(action['check'].split(), capture_output=True, text=True, timeout=5)
                    current_value = check_result.stdout.strip()
                    
                    result['actions_taken'].append({
                        'description': action['description'],
                        'current_value': current_value,
                        'recommended_command': action['command'],
                        'status': 'checked'
                    })
                except Exception as e:
                    result['actions_taken'].append({
                        'description': action['description'],
                        'error': str(e),
                        'status': 'failed'
                    })
                    
            # Generate recommendations
            result['recommendations'] = [
                'Review and close unnecessary listening ports',
                'Implement fail2ban for intrusion prevention',
                'Configure firewall rules for specific services only',
                'Enable logging for security events',
                'Regular security updates and patches',
                'Network segmentation for critical services'
            ]
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def incident_detection(self) -> Dict[str, Any]:
        """Active incident detection and alerting"""
        result = {
            'type': 'incident_detection',
            'timestamp': datetime.utcnow().isoformat(),
            'incidents': [],
            'indicators': [],
            'risk_level': 'low'
        }
        
        try:
            # Check for common attack indicators
            indicators = []
            
            # High CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 90:
                indicators.append({
                    'type': 'resource_exhaustion',
                    'description': f'High CPU usage: {cpu_percent}%',
                    'severity': 'medium'
                })
                
            # Unusual network connections
            external_connections = []
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    if not conn.raddr.ip.startswith(('127.', '192.168.', '10.', '172.')):
                        external_connections.append(conn.raddr.ip)
                        
            if len(external_connections) > 10:
                indicators.append({
                    'type': 'suspicious_network_activity',
                    'description': f'High number of external connections: {len(external_connections)}',
                    'severity': 'high'
                })
                
            # Failed login attempts (if auth.log exists)
            auth_log_paths = ['/var/log/auth.log', '/var/log/secure']
            for log_path in auth_log_paths:
                if os.path.exists(log_path):
                    try:
                        with open(log_path, 'r') as f:
                            recent_lines = f.readlines()[-100:]  # Last 100 lines
                            failed_logins = [line for line in recent_lines if 'Failed password' in line]
                            if len(failed_logins) > 5:
                                indicators.append({
                                    'type': 'brute_force_attempt',
                                    'description': f'Multiple failed login attempts: {len(failed_logins)}',
                                    'severity': 'high'
                                })
                    except PermissionError:
                        pass
                        
            # Check for suspicious processes
            suspicious_patterns = ['nc ', 'netcat', 'bash -i', 'sh -i', '/dev/tcp']
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if any(pattern in cmdline for pattern in suspicious_patterns):
                        indicators.append({
                            'type': 'suspicious_process',
                            'description': f'Suspicious command: {cmdline[:100]}',
                            'severity': 'high'
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            result['indicators'] = indicators
            
            # Determine risk level
            high_severity = len([i for i in indicators if i['severity'] == 'high'])
            medium_severity = len([i for i in indicators if i['severity'] == 'medium'])
            
            if high_severity > 0:
                result['risk_level'] = 'high'
            elif medium_severity > 2:
                result['risk_level'] = 'medium'
            else:
                result['risk_level'] = 'low'
                
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def log_analysis(self, log_file: str = None) -> Dict[str, Any]:
        """Analyze system logs for security events"""
        result = {
            'type': 'log_analysis',
            'timestamp': datetime.utcnow().isoformat(),
            'analyzed_logs': [],
            'security_events': [],
            'summary': {}
        }
        
        try:
            # Default log files to analyze
            if not log_file:
                log_files = [
                    '/var/log/syslog',
                    '/var/log/auth.log',
                    '/var/log/secure',
                    '/var/log/messages'
                ]
            else:
                log_files = [log_file]
                
            security_patterns = [
                'Failed password',
                'Invalid user',
                'refused connect',
                'attack',
                'intrusion',
                'violation',
                'denied',
                'blocked',
                'suspicious'
            ]
            
            for log_path in log_files:
                if os.path.exists(log_path):
                    try:
                        with open(log_path, 'r') as f:
                            lines = f.readlines()[-1000:]  # Last 1000 lines
                            
                        log_events = []
                        for line in lines:
                            for pattern in security_patterns:
                                if pattern.lower() in line.lower():
                                    log_events.append({
                                        'pattern': pattern,
                                        'line': line.strip(),
                                        'timestamp': datetime.utcnow().isoformat()
                                    })
                                    
                        result['analyzed_logs'].append({
                            'file': log_path,
                            'events_found': len(log_events),
                            'events': log_events[:10]  # Top 10 events
                        })
                        
                        result['security_events'].extend(log_events)
                        
                    except PermissionError:
                        result['analyzed_logs'].append({
                            'file': log_path,
                            'error': 'Permission denied'
                        })
                        
            # Generate summary
            result['summary'] = {
                'total_events': len(result['security_events']),
                'files_analyzed': len([log for log in result['analyzed_logs'] if 'error' not in log]),
                'most_common_patterns': {}
            }
            
            # Count pattern occurrences
            pattern_counts = {}
            for event in result['security_events']:
                pattern = event['pattern']
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
                
            result['summary']['most_common_patterns'] = pattern_counts
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def defend(self, action: str = 'monitor', target: str = None, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main defense interface"""
        options = options or {}
        
        # Analyze command
        command = f"defend {action}"
        if target:
            command += f" {target}"
        analysis = self.brain.analyze_command(command)
        
        if not analysis['safe_to_execute']:
            return {
                'error': 'Defense action blocked by security policy',
                'reason': analysis['explanation'],
                'suggestions': self.brain.get_command_suggestions(analysis)
            }
            
        self.results['action_type'] = action
        
        defense_results = {
            'action_analysis': analysis,
            'defense_results': {}
        }
        
        # Execute appropriate defense actions
        if action == 'monitor':
            defense_results['defense_results']['monitoring'] = self.system_monitoring()
            
        elif action == 'audit':
            defense_results['defense_results']['security_audit'] = self.security_audit()
            
        elif action == 'harden':
            defense_results['defense_results']['network_hardening'] = self.network_hardening()
            
        elif action == 'detect':
            defense_results['defense_results']['incident_detection'] = self.incident_detection()
            
        elif action == 'analyze_logs':
            defense_results['defense_results']['log_analysis'] = self.log_analysis(target)
            
        elif action == 'all':
            # Comprehensive defense assessment
            defense_results['defense_results']['monitoring'] = self.system_monitoring()
            defense_results['defense_results']['security_audit'] = self.security_audit()
            defense_results['defense_results']['incident_detection'] = self.incident_detection()
            
        else:
            return {
                'error': f'Unknown defense action: {action}',
                'available_actions': ['monitor', 'audit', 'harden', 'detect', 'analyze_logs', 'all']
            }
            
        return defense_results
        
    def generate_report(self, results: Dict[str, Any], format_type: str = 'markdown') -> str:
        """Generate defense report"""
        if format_type == 'markdown':
            return self._generate_markdown_report(results)
        elif format_type == 'json':
            return json.dumps(results, indent=2)
        else:
            return str(results)
            
    def _generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate markdown formatted defense report"""
        report = f"""# Cyber Defense Report

**Defense ID:** {self.results['defense_id']}
**Action Type:** {self.results['action_type']}
**Timestamp:** {self.results['timestamp']}

## Action Analysis
{results.get('action_analysis', {}).get('explanation', 'No analysis available')}

## Defense Results
"""
        
        for action_type, result in results.get('defense_results', {}).items():
            report += f"\n### {action_type.replace('_', ' ').title()}\n"
            
            if result.get('success'):
                if action_type == 'monitoring':
                    resource_usage = result.get('resource_usage', {})
                    suspicious = result.get('suspicious_activities', [])
                    
                    report += f"- **CPU Usage:** {resource_usage.get('cpu_percent', 'N/A')}%\n"
                    report += f"- **Memory Usage:** {resource_usage.get('memory_percent', 'N/A')}%\n"
                    report += f"- **Network Connections:** {len(result.get('network_connections', []))}\n"
                    
                    if suspicious:
                        report += f"- **Suspicious Activities:** {len(suspicious)}\n"
                        for activity in suspicious[:3]:  # Top 3
                            report += f"  - {activity.get('type', 'Unknown')}: {activity.get('process', 'Unknown')}\n"
                            
                elif action_type == 'security_audit':
                    findings = result.get('security_findings', [])
                    suid_count = len(result.get('suid_binaries', []))
                    listeners = len(result.get('listening_services', []))
                    
                    report += f"- **SUID Binaries:** {suid_count}\n"
                    report += f"- **Listening Services:** {listeners}\n"
                    report += f"- **Security Findings:** {len(findings)}\n"
                    
                    for finding in findings:
                        report += f"  - ⚠️ {finding}\n"
                        
                elif action_type == 'incident_detection':
                    risk_level = result.get('risk_level', 'unknown')
                    indicators = result.get('indicators', [])
                    
                    risk_emoji = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}.get(risk_level, '⚪')
                    report += f"- **Risk Level:** {risk_emoji} {risk_level.upper()}\n"
                    report += f"- **Security Indicators:** {len(indicators)}\n"
                    
                    for indicator in indicators:
                        severity_emoji = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}.get(indicator.get('severity'), '⚪')
                        report += f"  - {severity_emoji} {indicator.get('description', 'Unknown')}\n"
                        
                elif action_type == 'log_analysis':
                    total_events = result.get('summary', {}).get('total_events', 0)
                    files_analyzed = result.get('summary', {}).get('files_analyzed', 0)
                    
                    report += f"- **Files Analyzed:** {files_analyzed}\n"
                    report += f"- **Security Events Found:** {total_events}\n"
                    
                    patterns = result.get('summary', {}).get('most_common_patterns', {})
                    if patterns:
                        report += "- **Common Patterns:**\n"
                        for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:5]:
                            report += f"  - {pattern}: {count} occurrences\n"
                            
                elif action_type == 'network_hardening':
                    actions = result.get('actions_taken', [])
                    recommendations = result.get('recommendations', [])
                    
                    report += f"- **Hardening Checks:** {len(actions)}\n"
                    report += f"- **Recommendations:** {len(recommendations)}\n"
                    
                    if recommendations:
                        report += "- **Key Recommendations:**\n"
                        for rec in recommendations[:3]:  # Top 3
                            report += f"  - {rec}\n"
                            
            else:
                error = result.get('error', 'Unknown error')
                report += f"- **Error:** {error}\n"
                
        return report

def main():
    parser = argparse.ArgumentParser(description='Cyber Defense and Hardening Tool')
    parser.add_argument('action', choices=['monitor', 'audit', 'harden', 'detect', 'analyze_logs', 'all'],
                       help='Defense action to perform')
    parser.add_argument('--target', help='Target for action (e.g., log file for analyze_logs)')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Output format')
    parser.add_argument('--output', help='Output file (default: stdout)')
    parser.add_argument('--continuous', action='store_true', help='Continuous monitoring mode')
    
    args = parser.parse_args()
    
    defense = CyberDefense()
    
    try:
        if args.continuous and args.action == 'monitor':
            # Continuous monitoring mode
            import time
            print("Starting continuous monitoring (Ctrl+C to stop)...")
            while True:
                results = defense.defend(args.action, args.target)
                
                if 'error' in results:
                    print(f"Error: {results['error']}", file=sys.stderr)
                    break
                    
                # Print summary
                monitoring_result = results.get('defense_results', {}).get('monitoring', {})
                if monitoring_result.get('success'):
                    cpu = monitoring_result.get('resource_usage', {}).get('cpu_percent', 'N/A')
                    mem = monitoring_result.get('resource_usage', {}).get('memory_percent', 'N/A')
                    connections = len(monitoring_result.get('network_connections', []))
                    suspicious = len(monitoring_result.get('suspicious_activities', []))
                    
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] CPU: {cpu}% | MEM: {mem}% | Connections: {connections} | Suspicious: {suspicious}")
                    
                time.sleep(10)  # Monitor every 10 seconds
        else:
            # Single execution mode
            results = defense.defend(args.action, args.target)
            
            if 'error' in results:
                print(f"Error: {results['error']}", file=sys.stderr)
                if 'suggestions' in results:
                    print("\nSuggested commands:", file=sys.stderr)
                    for suggestion in results['suggestions']:
                        print(f"  {suggestion}", file=sys.stderr)
                sys.exit(1)
                
            report = defense.generate_report(results, args.format)
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(report)
                print(f"Report saved to {args.output}")
            else:
                print(report)
                
    except KeyboardInterrupt:
        print("\nDefense operation interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()