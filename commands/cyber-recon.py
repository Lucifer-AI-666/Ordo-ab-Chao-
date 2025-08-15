#!/usr/bin/env python3
"""
Advanced Reconnaissance Tool - cyber-recon.py
OSINT and reconnaissance capabilities with intelligence
"""

import argparse
import json
import sys
import os
import subprocess
import socket
import dns.resolver
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

# Add engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine.brain import CopilotBrain

class AdvancedRecon:
    """Advanced reconnaissance with OSINT capabilities"""
    
    def __init__(self):
        self.brain = CopilotBrain()
        self.results = {
            'recon_id': datetime.utcnow().strftime('%Y%m%d_%H%M%S'),
            'timestamp': datetime.utcnow().isoformat(),
            'target': '',
            'recon_type': '',
            'findings': {}
        }
        
    def passive_dns_lookup(self, domain: str) -> Dict[str, Any]:
        """Passive DNS reconnaissance"""
        result = {
            'type': 'dns_lookup',
            'domain': domain,
            'records': {},
            'subdomains': [],
            'mail_servers': [],
            'name_servers': []
        }
        
        try:
            # A records
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                result['records']['A'] = [str(r) for r in a_records]
            except dns.resolver.NXDOMAIN:
                result['records']['A'] = []
            except Exception:
                pass
                
            # AAAA records (IPv6)
            try:
                aaaa_records = dns.resolver.resolve(domain, 'AAAA')
                result['records']['AAAA'] = [str(r) for r in aaaa_records]
            except:
                result['records']['AAAA'] = []
                
            # MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                result['mail_servers'] = [str(r) for r in mx_records]
            except:
                pass
                
            # NS records
            try:
                ns_records = dns.resolver.resolve(domain, 'NS')
                result['name_servers'] = [str(r) for r in ns_records]
            except:
                pass
                
            # TXT records
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                result['records']['TXT'] = [str(r) for r in txt_records]
            except:
                result['records']['TXT'] = []
                
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def subdomain_enumeration(self, domain: str, method: str = 'passive') -> Dict[str, Any]:
        """Subdomain discovery using various methods"""
        result = {
            'type': 'subdomain_enumeration',
            'domain': domain,
            'method': method,
            'subdomains': [],
            'tools_used': []
        }
        
        try:
            if method in ['passive', 'all']:
                # Use subfinder for passive enumeration
                cmd = ['subfinder', '-d', domain, '-silent']
                try:
                    process = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    if process.returncode == 0:
                        subdomains = process.stdout.strip().split('\n')
                        result['subdomains'].extend([s for s in subdomains if s])
                        result['tools_used'].append('subfinder')
                except subprocess.TimeoutExpired:
                    pass
                except FileNotFoundError:
                    pass
                    
            if method in ['active', 'all']:
                # Use amass for active enumeration  
                cmd = ['amass', 'enum', '-d', domain, '-passive']
                try:
                    process = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
                    if process.returncode == 0:
                        subdomains = process.stdout.strip().split('\n')
                        new_subdomains = [s for s in subdomains if s and s not in result['subdomains']]
                        result['subdomains'].extend(new_subdomains)
                        result['tools_used'].append('amass')
                except subprocess.TimeoutExpired:
                    pass
                except FileNotFoundError:
                    pass
                    
            # Remove duplicates and sort
            result['subdomains'] = sorted(list(set(result['subdomains'])))
            result['subdomain_count'] = len(result['subdomains'])
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def web_reconnaissance(self, target: str) -> Dict[str, Any]:
        """Web application reconnaissance"""
        result = {
            'type': 'web_reconnaissance',
            'target': target,
            'technologies': [],
            'headers': {},
            'status_code': 0,
            'response_size': 0,
            'server_info': {},
            'security_headers': {}
        }
        
        try:
            # Ensure target has protocol
            if not target.startswith(('http://', 'https://')):
                target = f"http://{target}"
                
            # Basic HTTP request
            response = requests.get(target, timeout=10, allow_redirects=True)
            result['status_code'] = response.status_code
            result['response_size'] = len(response.content)
            result['headers'] = dict(response.headers)
            
            # Extract server information
            result['server_info'] = {
                'server': response.headers.get('Server', 'Unknown'),
                'powered_by': response.headers.get('X-Powered-By', 'Unknown'),
                'technology': response.headers.get('X-Technology', 'Unknown')
            }
            
            # Security headers analysis
            security_headers = [
                'Strict-Transport-Security',
                'Content-Security-Policy', 
                'X-Frame-Options',
                'X-Content-Type-Options',
                'X-XSS-Protection',
                'Referrer-Policy'
            ]
            
            for header in security_headers:
                result['security_headers'][header] = response.headers.get(header, 'Missing')
                
            # Technology detection from headers and content
            content = response.text.lower()
            
            # Common technology signatures
            tech_signatures = {
                'WordPress': ['wp-content', 'wp-includes'],
                'Drupal': ['drupal', 'sites/all'],
                'Joomla': ['joomla', 'administrator'],
                'Apache': ['apache'],
                'Nginx': ['nginx'],
                'PHP': ['php'],
                'ASP.NET': ['asp.net', '__viewstate'],
                'Django': ['django', 'csrftoken'],
                'React': ['react', '__react'],
                'Angular': ['angular', 'ng-'],
                'Vue.js': ['vue.js', 'vue ']
            }
            
            for tech, signatures in tech_signatures.items():
                if any(sig in content for sig in signatures) or any(sig in str(response.headers) for sig in signatures):
                    result['technologies'].append(tech)
                    
            result['success'] = True
            
        except requests.RequestException as e:
            result['error'] = str(e)
            result['success'] = False
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def directory_enumeration(self, target: str, wordlist: str = None) -> Dict[str, Any]:
        """Directory and file enumeration"""
        result = {
            'type': 'directory_enumeration',
            'target': target,
            'found_paths': [],
            'interesting_files': [],
            'status_codes': {}
        }
        
        try:
            # Use gobuster for directory enumeration
            cmd = ['gobuster', 'dir', '-u', target, '-q']
            
            if wordlist:
                cmd.extend(['-w', wordlist])
            else:
                # Try common wordlists
                common_wordlists = [
                    '/usr/share/wordlists/dirb/common.txt',
                    '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
                    '/opt/SecLists/Discovery/Web-Content/common.txt'
                ]
                
                for wl in common_wordlists:
                    if os.path.exists(wl):
                        cmd.extend(['-w', wl])
                        break
                        
            cmd.extend(['-t', '50', '--timeout', '10s'])
            
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if process.returncode == 0:
                lines = process.stdout.strip().split('\n')
                for line in lines:
                    if 'Status:' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            path = parts[0]
                            status = parts[1].replace('(Status:', '').replace(')', '')
                            result['found_paths'].append(path)
                            result['status_codes'][path] = status
                            
                            # Identify interesting files
                            interesting_extensions = ['.php', '.asp', '.jsp', '.do', '.action', '.cgi']
                            interesting_names = ['admin', 'login', 'config', 'backup', 'test']
                            
                            if any(ext in path for ext in interesting_extensions) or \
                               any(name in path.lower() for name in interesting_names):
                                result['interesting_files'].append(path)
                                
            result['total_found'] = len(result['found_paths'])
            result['success'] = True
            
        except subprocess.TimeoutExpired:
            result['error'] = 'Directory enumeration timeout'
            result['success'] = False
        except FileNotFoundError:
            result['error'] = 'Gobuster not found'
            result['success'] = False
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def port_service_enumeration(self, target: str) -> Dict[str, Any]:
        """Detailed port and service enumeration"""
        result = {
            'type': 'port_service_enumeration',
            'target': target,
            'open_ports': {},
            'services': {},
            'banners': {},
            'vulnerabilities': []
        }
        
        try:
            # Use nmap for detailed service enumeration
            cmd = ['nmap', '-sV', '-sC', '-O', '--script=vuln', target]
            
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if process.returncode == 0:
                lines = process.stdout.split('\n')
                current_port = None
                
                for line in lines:
                    # Parse port information
                    if '/tcp' in line and ('open' in line or 'filtered' in line):
                        parts = line.split()
                        if len(parts) >= 3:
                            port_proto = parts[0]
                            state = parts[1]
                            service = parts[2]
                            version = ' '.join(parts[3:]) if len(parts) > 3 else ''
                            
                            port_num = port_proto.split('/')[0]
                            current_port = port_num
                            
                            result['open_ports'][port_num] = state
                            result['services'][port_num] = {
                                'service': service,
                                'version': version,
                                'state': state
                            }
                            
                    # Parse vulnerability information
                    elif current_port and ('CVE-' in line or 'VULNERABLE' in line):
                        result['vulnerabilities'].append({
                            'port': current_port,
                            'description': line.strip()
                        })
                        
            result['total_open_ports'] = len(result['open_ports'])
            result['success'] = True
            
        except subprocess.TimeoutExpired:
            result['error'] = 'Service enumeration timeout'
            result['success'] = False
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def social_media_osint(self, target: str) -> Dict[str, Any]:
        """Basic social media and OSINT reconnaissance"""
        result = {
            'type': 'social_media_osint',
            'target': target,
            'social_profiles': [],
            'email_addresses': [],
            'phone_numbers': [],
            'locations': []
        }
        
        try:
            # Basic search patterns (passive only)
            social_platforms = {
                'LinkedIn': f"https://www.linkedin.com/search/results/people/?keywords={target}",
                'Twitter': f"https://twitter.com/search?q={target}",
                'Facebook': f"https://www.facebook.com/search/people/?q={target}",
                'Instagram': f"https://www.instagram.com/{target}/",
                'GitHub': f"https://github.com/{target}"
            }
            
            for platform, url in social_platforms.items():
                try:
                    response = requests.get(url, timeout=5, allow_redirects=True)
                    if response.status_code == 200:
                        result['social_profiles'].append({
                            'platform': platform,
                            'url': url,
                            'found': True
                        })
                except:
                    result['social_profiles'].append({
                        'platform': platform,
                        'url': url,
                        'found': False
                    })
                    
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def reconnaissance(self, target: str, recon_type: str = 'auto', intensity: str = 'moderate') -> Dict[str, Any]:
        """Main reconnaissance interface"""
        
        # Analyze command and target
        command = f"recon {target}"
        analysis = self.brain.analyze_command(command)
        
        if not analysis['safe_to_execute']:
            return {
                'error': 'Reconnaissance blocked by security policy',
                'reason': analysis['explanation'],
                'suggestions': self.brain.get_command_suggestions(analysis)
            }
            
        self.results['target'] = target
        self.results['recon_type'] = recon_type
        
        recon_results = {
            'target_analysis': analysis,
            'reconnaissance_results': {}
        }
        
        # Determine reconnaissance methods based on target type
        target_type = analysis.get('target_type', 'unknown')
        
        if recon_type == 'auto':
            if target_type == 'domain':
                methods = ['dns_lookup', 'subdomain_enumeration', 'web_reconnaissance']
                if intensity in ['aggressive', 'all']:
                    methods.extend(['directory_enumeration', 'port_service_enumeration'])
            elif target_type in ['ip_address', 'localhost']:
                methods = ['port_service_enumeration']
                if intensity in ['moderate', 'aggressive']:
                    methods.append('web_reconnaissance')
            else:
                methods = ['dns_lookup']
        else:
            methods = [recon_type]
            
        # Execute reconnaissance methods
        for method in methods:
            try:
                if method == 'dns_lookup':
                    result = self.passive_dns_lookup(target)
                elif method == 'subdomain_enumeration':
                    result = self.subdomain_enumeration(target, 'passive' if intensity == 'passive' else 'all')
                elif method == 'web_reconnaissance':
                    result = self.web_reconnaissance(target)
                elif method == 'directory_enumeration':
                    result = self.directory_enumeration(target)
                elif method == 'port_service_enumeration':
                    result = self.port_service_enumeration(target)
                elif method == 'social_media_osint':
                    result = self.social_media_osint(target)
                else:
                    continue
                    
                recon_results['reconnaissance_results'][method] = result
                
            except Exception as e:
                recon_results['reconnaissance_results'][method] = {
                    'error': str(e),
                    'success': False
                }
                
        return recon_results
        
    def generate_report(self, results: Dict[str, Any], format_type: str = 'markdown') -> str:
        """Generate reconnaissance report"""
        if format_type == 'markdown':
            return self._generate_markdown_report(results)
        elif format_type == 'json':
            return json.dumps(results, indent=2)
        else:
            return str(results)
            
    def _generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate markdown formatted reconnaissance report"""
        report = f"""# Reconnaissance Report

**Target:** {self.results['target']}
**Recon ID:** {self.results['recon_id']}
**Timestamp:** {self.results['timestamp']}

## Target Analysis
{results.get('target_analysis', {}).get('explanation', 'No analysis available')}

## Reconnaissance Results
"""
        
        for method, result in results.get('reconnaissance_results', {}).items():
            report += f"\n### {method.replace('_', ' ').title()}\n"
            
            if result.get('success'):
                if method == 'dns_lookup':
                    records = result.get('records', {})
                    for record_type, values in records.items():
                        if values:
                            report += f"- **{record_type} Records:** {', '.join(values)}\n"
                            
                elif method == 'subdomain_enumeration':
                    count = result.get('subdomain_count', 0)
                    report += f"- **Subdomains Found:** {count}\n"
                    if count > 0:
                        subdomains = result.get('subdomains', [])[:10]  # Top 10
                        report += f"- **Sample Subdomains:** {', '.join(subdomains)}\n"
                        
                elif method == 'web_reconnaissance':
                    server_info = result.get('server_info', {})
                    technologies = result.get('technologies', [])
                    report += f"- **Server:** {server_info.get('server', 'Unknown')}\n"
                    if technologies:
                        report += f"- **Technologies:** {', '.join(technologies)}\n"
                        
                    # Security headers
                    security_headers = result.get('security_headers', {})
                    missing_headers = [h for h, v in security_headers.items() if v == 'Missing']
                    if missing_headers:
                        report += f"- **Missing Security Headers:** {', '.join(missing_headers)}\n"
                        
                elif method == 'directory_enumeration':
                    total_found = result.get('total_found', 0)
                    interesting = result.get('interesting_files', [])
                    report += f"- **Directories/Files Found:** {total_found}\n"
                    if interesting:
                        report += f"- **Interesting Files:** {', '.join(interesting[:5])}\n"
                        
                elif method == 'port_service_enumeration':
                    open_ports = result.get('open_ports', {})
                    vulnerabilities = result.get('vulnerabilities', [])
                    report += f"- **Open Ports:** {len(open_ports)}\n"
                    if vulnerabilities:
                        report += f"- **Potential Vulnerabilities:** {len(vulnerabilities)}\n"
                        
            else:
                error = result.get('error', 'Unknown error')
                report += f"- **Error:** {error}\n"
                
        return report

def main():
    parser = argparse.ArgumentParser(description='Advanced Reconnaissance Tool')
    parser.add_argument('target', help='Target for reconnaissance (domain, IP, or organization)')
    parser.add_argument('--type', choices=['auto', 'dns_lookup', 'subdomain_enumeration', 'web_reconnaissance', 
                                          'directory_enumeration', 'port_service_enumeration', 'social_media_osint'],
                       default='auto', help='Reconnaissance type')
    parser.add_argument('--intensity', choices=['passive', 'moderate', 'aggressive'], 
                       default='moderate', help='Reconnaissance intensity')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Output format')
    parser.add_argument('--output', help='Output file (default: stdout)')
    
    args = parser.parse_args()
    
    recon = AdvancedRecon()
    
    try:
        results = recon.reconnaissance(
            target=args.target,
            recon_type=args.type,
            intensity=args.intensity
        )
        
        if 'error' in results:
            print(f"Error: {results['error']}", file=sys.stderr)
            if 'suggestions' in results:
                print("\nSuggested commands:", file=sys.stderr)
                for suggestion in results['suggestions']:
                    print(f"  {suggestion}", file=sys.stderr)
            sys.exit(1)
            
        report = recon.generate_report(results, args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)
            
    except KeyboardInterrupt:
        print("\nReconnaissance interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()