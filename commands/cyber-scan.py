#!/usr/bin/env python3
"""
Universal Cyber Scanner - cyber-scan.py
Intelligent scanning system with adaptive capabilities
"""

import argparse
import json
import sys
import os
import subprocess
import socket
import ipaddress
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine.brain import CopilotBrain

class UniversalScanner:
    """Intelligent universal scanner with auto-detection and escalation"""
    
    def __init__(self):
        self.brain = CopilotBrain()
        self.results = {
            'scan_id': datetime.utcnow().strftime('%Y%m%d_%H%M%S'),
            'timestamp': datetime.utcnow().isoformat(),
            'targets': [],
            'results': {},
            'metadata': {}
        }
        
    def detect_target_type(self, target: str) -> Dict[str, Any]:
        """Auto-detect target type and characteristics"""
        detection = {
            'target': target,
            'type': 'unknown',
            'characteristics': [],
            'recommended_scans': []
        }
        
        # IP Address detection
        try:
            ip = ipaddress.ip_address(target)
            detection['type'] = 'ip_address'
            if ip.is_private:
                detection['characteristics'].append('private_network')
                detection['recommended_scans'] = ['port_scan', 'service_detection', 'vulnerability_scan']
            else:
                detection['characteristics'].append('public_ip')
                detection['recommended_scans'] = ['passive_scan', 'service_detection']
        except ValueError:
            pass
            
        # Network range detection
        try:
            network = ipaddress.ip_network(target, strict=False)
            detection['type'] = 'network_range'
            detection['characteristics'].append(f'network_size_{network.num_addresses}')
            detection['recommended_scans'] = ['host_discovery', 'port_scan']
        except ValueError:
            pass
            
        # Domain/hostname detection
        if '.' in target and detection['type'] == 'unknown':
            detection['type'] = 'domain'
            detection['characteristics'].append('requires_dns_resolution')
            detection['recommended_scans'] = ['dns_enum', 'subdomain_discovery', 'web_scan']
            
        # Localhost detection
        if target in ['localhost', '127.0.0.1', '::1']:
            detection['type'] = 'localhost'
            detection['characteristics'].append('local_system')
            detection['recommended_scans'] = ['local_enum', 'service_scan', 'process_scan']
            
        return detection
        
    def check_port_responsive(self, host: str, port: int, timeout: float = 3.0) -> bool:
        """Quick port responsiveness check"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                return result == 0
        except Exception:
            return False
            
    def perform_host_discovery(self, target: str, intensity: str = 'moderate') -> Dict[str, Any]:
        """Intelligent host discovery"""
        result = {
            'scan_type': 'host_discovery',
            'target': target,
            'alive_hosts': [],
            'total_hosts': 0,
            'scan_time': 0
        }
        
        start_time = datetime.utcnow()
        
        try:
            # Choose scan method based on intensity
            if intensity == 'passive':
                cmd = ['nmap', '-sn', '-PS22,80,443', target]
            elif intensity == 'aggressive':
                cmd = ['nmap', '-sn', '-PS22,80,443,993,995,3389,5900', target]
            else:  # moderate
                cmd = ['nmap', '-sn', target]
                
            # Execute scan
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if process.returncode == 0:
                # Parse nmap output for alive hosts
                lines = process.stdout.split('\n')
                for line in lines:
                    if 'Nmap scan report for' in line:
                        host = line.split()[-1].strip('()')
                        result['alive_hosts'].append(host)
                        
                result['total_hosts'] = len(result['alive_hosts'])
                
            result['scan_time'] = (datetime.utcnow() - start_time).total_seconds()
            result['command_executed'] = ' '.join(cmd)
            result['success'] = process.returncode == 0
            
        except subprocess.TimeoutExpired:
            result['error'] = 'Scan timeout'
            result['success'] = False
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def perform_port_scan(self, target: str, intensity: str = 'moderate', ports: str = None) -> Dict[str, Any]:
        """Intelligent port scanning with adaptive techniques"""
        result = {
            'scan_type': 'port_scan',
            'target': target,
            'open_ports': [],
            'filtered_ports': [],
            'services': {},
            'scan_time': 0
        }
        
        start_time = datetime.utcnow()
        
        try:
            # Build nmap command based on intensity
            cmd = ['nmap']
            
            if intensity == 'passive':
                cmd.extend(['-sS', '-Pn'])
                port_range = ports or '22,80,443'
            elif intensity == 'aggressive':
                cmd.extend(['-sS', '-sV', '-O', '-A'])
                port_range = ports or '1-65535'
            else:  # moderate
                cmd.extend(['-sS', '-sV'])
                port_range = ports or '1-1000'
                
            cmd.extend(['-p', port_range, target])
            
            # Execute scan
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if process.returncode == 0:
                # Parse results
                lines = process.stdout.split('\n')
                in_port_section = False
                
                for line in lines:
                    if '/tcp' in line or '/udp' in line:
                        in_port_section = True
                        parts = line.split()
                        if len(parts) >= 3:
                            port_info = parts[0]
                            state = parts[1]
                            service = parts[2] if len(parts) > 2 else 'unknown'
                            
                            port_num = port_info.split('/')[0]
                            
                            if state == 'open':
                                result['open_ports'].append(port_num)
                                result['services'][port_num] = service
                            elif state == 'filtered':
                                result['filtered_ports'].append(port_num)
                                
            result['scan_time'] = (datetime.utcnow() - start_time).total_seconds()
            result['command_executed'] = ' '.join(cmd)
            result['success'] = process.returncode == 0
            
        except subprocess.TimeoutExpired:
            result['error'] = 'Scan timeout'
            result['success'] = False
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def perform_vulnerability_scan(self, target: str, ports: List[str] = None) -> Dict[str, Any]:
        """Nuclei-based vulnerability scanning"""
        result = {
            'scan_type': 'vulnerability_scan', 
            'target': target,
            'vulnerabilities': [],
            'scan_time': 0
        }
        
        start_time = datetime.utcnow()
        
        try:
            cmd = ['nuclei', '-u', target, '-json']
            
            if ports:
                # Focus on specific ports if provided
                for port in ports:
                    port_target = f"{target}:{port}"
                    process = subprocess.run(
                        ['nuclei', '-u', port_target, '-json'],
                        capture_output=True, text=True, timeout=300
                    )
                    
                    if process.returncode == 0 and process.stdout:
                        for line in process.stdout.strip().split('\n'):
                            if line.strip():
                                try:
                                    vuln = json.loads(line)
                                    result['vulnerabilities'].append(vuln)
                                except json.JSONDecodeError:
                                    continue
            else:
                # General scan
                process = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if process.returncode == 0 and process.stdout:
                    for line in process.stdout.strip().split('\n'):
                        if line.strip():
                            try:
                                vuln = json.loads(line)
                                result['vulnerabilities'].append(vuln)
                            except json.JSONDecodeError:
                                continue
                                
            result['scan_time'] = (datetime.utcnow() - start_time).total_seconds()
            result['vulnerability_count'] = len(result['vulnerabilities'])
            result['success'] = True
            
        except subprocess.TimeoutExpired:
            result['error'] = 'Vulnerability scan timeout'
            result['success'] = False
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def perform_service_detection(self, target: str, ports: List[str]) -> Dict[str, Any]:
        """Detailed service detection and banner grabbing"""
        result = {
            'scan_type': 'service_detection',
            'target': target,
            'services': {},
            'banners': {},
            'scan_time': 0
        }
        
        start_time = datetime.utcnow()
        
        try:
            # Use nmap for service detection
            port_list = ','.join(ports)
            cmd = ['nmap', '-sV', '-sC', '-p', port_list, target]
            
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if process.returncode == 0:
                # Parse service information
                lines = process.stdout.split('\n')
                for line in lines:
                    if '/tcp' in line and 'open' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            port = parts[0].split('/')[0]
                            service = parts[2]
                            version_info = ' '.join(parts[3:]) if len(parts) > 3 else ''
                            
                            result['services'][port] = {
                                'service': service,
                                'version': version_info,
                                'state': 'open'
                            }
                            
            result['scan_time'] = (datetime.utcnow() - start_time).total_seconds()
            result['command_executed'] = ' '.join(cmd)
            result['success'] = process.returncode == 0
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def escalate_scan(self, initial_results: Dict[str, Any], target: str) -> Dict[str, Any]:
        """Intelligent scan escalation based on initial results"""
        escalation_result = {
            'escalation_triggered': True,
            'reason': '',
            'additional_scans': []
        }
        
        # Analyze initial results for escalation opportunities
        if 'open_ports' in initial_results and initial_results['open_ports']:
            open_ports = initial_results['open_ports']
            
            # Web services detected
            web_ports = [p for p in open_ports if p in ['80', '443', '8080', '8443']]
            if web_ports:
                escalation_result['reason'] = 'Web services detected'
                escalation_result['additional_scans'].append({
                    'type': 'web_scan',
                    'ports': web_ports
                })
                
            # SSH detected
            if '22' in open_ports:
                escalation_result['additional_scans'].append({
                    'type': 'ssh_enum',
                    'port': '22'
                })
                
            # Database ports detected
            db_ports = [p for p in open_ports if p in ['3306', '5432', '1433', '27017']]
            if db_ports:
                escalation_result['additional_scans'].append({
                    'type': 'database_enum',
                    'ports': db_ports
                })
                
        return escalation_result
        
    def scan(self, target: str, scan_type: str = 'auto', intensity: str = 'moderate', 
             ports: str = None, escalate: bool = True) -> Dict[str, Any]:
        """Main scanning interface with intelligent workflows"""
        
        # Analyze command and target
        command = f"scan {target}"
        analysis = self.brain.analyze_command(command)
        
        if not analysis['safe_to_execute']:
            return {
                'error': 'Scan blocked by security policy',
                'reason': analysis['explanation'],
                'suggestions': self.brain.get_command_suggestions(analysis)
            }
            
        # Detect target characteristics
        target_info = self.detect_target_type(target)
        
        scan_results = {
            'target_analysis': target_info,
            'security_analysis': analysis,
            'scan_results': {}
        }
        
        # Execute appropriate scans based on type and target
        if scan_type == 'auto':
            # Automatic scan selection based on target type
            recommended_scans = target_info['recommended_scans']
        else:
            recommended_scans = [scan_type]
            
        for scan_method in recommended_scans:
            if scan_method == 'host_discovery':
                result = self.perform_host_discovery(target, intensity)
            elif scan_method == 'port_scan':
                result = self.perform_port_scan(target, intensity, ports)
            elif scan_method == 'vulnerability_scan':
                result = self.perform_vulnerability_scan(target)
            elif scan_method == 'service_detection' and 'port_scan' in scan_results['scan_results']:
                # Use ports from previous scan
                open_ports = scan_results['scan_results']['port_scan'].get('open_ports', [])
                if open_ports:
                    result = self.perform_service_detection(target, open_ports)
                else:
                    continue
            else:
                continue
                
            scan_results['scan_results'][scan_method] = result
            
        # Escalation logic
        if escalate and 'port_scan' in scan_results['scan_results']:
            escalation = self.escalate_scan(scan_results['scan_results']['port_scan'], target)
            scan_results['escalation'] = escalation
            
        return scan_results
        
    def generate_report(self, results: Dict[str, Any], format_type: str = 'markdown') -> str:
        """Generate formatted scan report"""
        if format_type == 'markdown':
            return self._generate_markdown_report(results)
        elif format_type == 'json':
            return json.dumps(results, indent=2)
        else:
            return str(results)
            
    def _generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate markdown formatted report"""
        report = f"""# Cyber Scan Report
        
**Scan ID:** {self.results['scan_id']}
**Timestamp:** {self.results['timestamp']}

## Target Analysis
- **Target:** {results.get('target_analysis', {}).get('target', 'Unknown')}
- **Type:** {results.get('target_analysis', {}).get('type', 'Unknown')}
- **Characteristics:** {', '.join(results.get('target_analysis', {}).get('characteristics', []))}

## Security Assessment
{results.get('security_analysis', {}).get('explanation', 'No security analysis available')}

## Scan Results
"""
        
        for scan_type, scan_result in results.get('scan_results', {}).items():
            report += f"\n### {scan_type.replace('_', ' ').title()}\n"
            
            if scan_result.get('success'):
                if scan_type == 'port_scan':
                    open_ports = scan_result.get('open_ports', [])
                    report += f"- **Open Ports:** {', '.join(open_ports) if open_ports else 'None'}\n"
                    
                    services = scan_result.get('services', {})
                    if services:
                        report += "- **Services:**\n"
                        for port, service in services.items():
                            report += f"  - Port {port}: {service}\n"
                            
                elif scan_type == 'vulnerability_scan':
                    vuln_count = scan_result.get('vulnerability_count', 0)
                    report += f"- **Vulnerabilities Found:** {vuln_count}\n"
                    
                    if vuln_count > 0:
                        report += "- **Critical Issues:**\n"
                        for vuln in scan_result.get('vulnerabilities', [])[:5]:  # Top 5
                            severity = vuln.get('info', {}).get('severity', 'unknown')
                            name = vuln.get('info', {}).get('name', 'Unknown')
                            report += f"  - [{severity.upper()}] {name}\n"
                            
                scan_time = scan_result.get('scan_time', 0)
                report += f"- **Scan Time:** {scan_time:.2f} seconds\n"
            else:
                error = scan_result.get('error', 'Unknown error')
                report += f"- **Error:** {error}\n"
                
        # Escalation recommendations
        if 'escalation' in results and results['escalation']['escalation_triggered']:
            report += "\n## Recommended Next Steps\n"
            report += f"**Reason:** {results['escalation']['reason']}\n"
            for additional_scan in results['escalation']['additional_scans']:
                scan_type = additional_scan['type']
                report += f"- Execute {scan_type.replace('_', ' ')} scan\n"
                
        return report

def main():
    parser = argparse.ArgumentParser(description='Universal Cyber Scanner')
    parser.add_argument('target', help='Target to scan (IP, domain, or network)')
    parser.add_argument('--type', choices=['auto', 'host_discovery', 'port_scan', 'vulnerability_scan'], 
                       default='auto', help='Scan type')
    parser.add_argument('--intensity', choices=['passive', 'moderate', 'aggressive'], 
                       default='moderate', help='Scan intensity')
    parser.add_argument('--ports', help='Port specification (e.g., 22,80,443 or 1-1000)')
    parser.add_argument('--no-escalate', action='store_true', help='Disable automatic escalation')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Output format')
    parser.add_argument('--output', help='Output file (default: stdout)')
    
    args = parser.parse_args()
    
    scanner = UniversalScanner()
    
    try:
        results = scanner.scan(
            target=args.target,
            scan_type=args.type,
            intensity=args.intensity,
            ports=args.ports,
            escalate=not args.no_escalate
        )
        
        if 'error' in results:
            print(f"Error: {results['error']}", file=sys.stderr)
            if 'suggestions' in results:
                print("\nSuggested commands:", file=sys.stderr)
                for suggestion in results['suggestions']:
                    print(f"  {suggestion}", file=sys.stderr)
            sys.exit(1)
            
        report = scanner.generate_report(results, args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)
            
    except KeyboardInterrupt:
        print("\nScan interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()