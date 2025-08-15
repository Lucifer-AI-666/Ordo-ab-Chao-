#!/usr/bin/env python3
"""
Threat Intelligence and Monitoring - cyber-intel.py
Intelligence gathering, threat feeds, and monitoring capabilities
"""

import argparse
import json
import sys
import os
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Add engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine.brain import CopilotBrain

class ThreatIntelligence:
    """Advanced threat intelligence and monitoring system"""
    
    def __init__(self):
        self.brain = CopilotBrain()
        self.results = {
            'intel_id': datetime.utcnow().strftime('%Y%m%d_%H%M%S'),
            'timestamp': datetime.utcnow().isoformat(),
            'intelligence_type': '',
            'findings': {}
        }
        
    def ioc_analysis(self, ioc: str, ioc_type: str = 'auto') -> Dict[str, Any]:
        """Analyze Indicators of Compromise"""
        result = {
            'type': 'ioc_analysis',
            'ioc': ioc,
            'ioc_type': ioc_type,
            'reputation': 'unknown',
            'threat_feeds': [],
            'analysis': {},
            'recommendations': []
        }
        
        try:
            # Auto-detect IOC type if not specified
            if ioc_type == 'auto':
                ioc_type = self._detect_ioc_type(ioc)
                
            result['ioc_type'] = ioc_type
            
            # Simulate threat intelligence analysis
            if ioc_type == 'ip':
                result['analysis'] = self._analyze_ip(ioc)
            elif ioc_type == 'domain':
                result['analysis'] = self._analyze_domain(ioc)
            elif ioc_type == 'hash':
                result['analysis'] = self._analyze_hash(ioc)
            elif ioc_type == 'url':
                result['analysis'] = self._analyze_url(ioc)
                
            # Generate reputation score
            result['reputation'] = self._calculate_reputation(result['analysis'])
            
            # Generate recommendations
            result['recommendations'] = self._generate_ioc_recommendations(result)
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def _detect_ioc_type(self, ioc: str) -> str:
        """Auto-detect IOC type"""
        import re
        
        # IP address pattern
        ip_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        if re.match(ip_pattern, ioc):
            return 'ip'
            
        # Hash patterns
        if len(ioc) == 32 and all(c in '0123456789abcdef' for c in ioc.lower()):
            return 'hash'  # MD5
        elif len(ioc) == 40 and all(c in '0123456789abcdef' for c in ioc.lower()):
            return 'hash'  # SHA1
        elif len(ioc) == 64 and all(c in '0123456789abcdef' for c in ioc.lower()):
            return 'hash'  # SHA256
            
        # URL pattern
        if ioc.startswith(('http://', 'https://')):
            return 'url'
            
        # Domain pattern (basic)
        if '.' in ioc and not ioc.startswith('.') and len(ioc) > 3:
            return 'domain'
            
        return 'unknown'
        
    def _analyze_ip(self, ip: str) -> Dict[str, Any]:
        """Analyze IP address"""
        analysis = {
            'geolocation': 'Unknown',
            'asn': 'Unknown',
            'reputation_sources': [],
            'malware_families': [],
            'first_seen': None,
            'last_seen': None
        }
        
        # Simulate geolocation lookup
        import random
        countries = ['US', 'CN', 'RU', 'DE', 'FR', 'GB', 'JP', 'BR']
        analysis['geolocation'] = random.choice(countries)
        
        # Simulate ASN
        analysis['asn'] = f'AS{random.randint(1000, 99999)}'
        
        # Simulate reputation check
        reputation_sources = ['VirusTotal', 'AbuseIPDB', 'ThreatFox', 'URLVoid']
        for source in reputation_sources:
            analysis['reputation_sources'].append({
                'source': source,
                'status': random.choice(['clean', 'malicious', 'suspicious', 'unknown']),
                'confidence': random.randint(60, 95)
            })
            
        return analysis
        
    def _analyze_domain(self, domain: str) -> Dict[str, Any]:
        """Analyze domain"""
        analysis = {
            'registrar': 'Unknown',
            'creation_date': None,
            'reputation_sources': [],
            'categories': [],
            'subdomains': []
        }
        
        # Simulate domain analysis
        import random
        registrars = ['GoDaddy', 'Namecheap', 'CloudFlare', 'Google Domains']
        analysis['registrar'] = random.choice(registrars)
        
        # Simulate reputation
        reputation_sources = ['URLVoid', 'VirusTotal', 'OpenPhish', 'PhishTank']
        for source in reputation_sources:
            analysis['reputation_sources'].append({
                'source': source,
                'status': random.choice(['clean', 'malicious', 'suspicious', 'unknown']),
                'confidence': random.randint(60, 95)
            })
            
        return analysis
        
    def _analyze_hash(self, hash_value: str) -> Dict[str, Any]:
        """Analyze file hash"""
        analysis = {
            'file_type': 'Unknown',
            'malware_family': 'Unknown',
            'detection_ratio': '0/0',
            'first_seen': None,
            'behavior': []
        }
        
        # Simulate hash analysis
        import random
        file_types = ['PE32', 'ELF', 'PDF', 'Office Document', 'JavaScript']
        analysis['file_type'] = random.choice(file_types)
        
        malware_families = ['Trojan.Generic', 'Backdoor.Agent', 'Ransomware.Wannacry', 'Clean']
        analysis['malware_family'] = random.choice(malware_families)
        
        detections = random.randint(0, 70)
        total = random.randint(60, 75)
        analysis['detection_ratio'] = f'{detections}/{total}'
        
        return analysis
        
    def _analyze_url(self, url: str) -> Dict[str, Any]:
        """Analyze URL"""
        analysis = {
            'domain_analysis': {},
            'categories': [],
            'reputation_sources': [],
            'redirect_chain': []
        }
        
        # Extract domain and analyze
        from urllib.parse import urlparse
        parsed = urlparse(url)
        if parsed.netloc:
            analysis['domain_analysis'] = self._analyze_domain(parsed.netloc)
            
        return analysis
        
    def _calculate_reputation(self, analysis: Dict[str, Any]) -> str:
        """Calculate overall reputation score"""
        malicious_count = 0
        clean_count = 0
        total_sources = 0
        
        for source in analysis.get('reputation_sources', []):
            status = source.get('status', 'unknown')
            if status == 'malicious':
                malicious_count += 1
            elif status == 'clean':
                clean_count += 1
            total_sources += 1
            
        if total_sources == 0:
            return 'unknown'
        elif malicious_count > total_sources * 0.5:
            return 'malicious'
        elif malicious_count > 0:
            return 'suspicious'
        else:
            return 'clean'
            
    def _generate_ioc_recommendations(self, ioc_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on IOC analysis"""
        recommendations = []
        reputation = ioc_result.get('reputation', 'unknown')
        
        if reputation == 'malicious':
            recommendations.extend([
                'Block this IOC immediately in firewall/proxy',
                'Search for additional related IOCs in environment',
                'Review logs for any connections to this IOC',
                'Consider threat hunting for related activities'
            ])
        elif reputation == 'suspicious':
            recommendations.extend([
                'Monitor this IOC closely',
                'Implement additional logging for related activities',
                'Consider temporary blocking if risk tolerance is low'
            ])
        else:
            recommendations.extend([
                'Continue monitoring as part of routine intelligence',
                'No immediate action required'
            ])
            
        return recommendations
        
    def threat_feed_monitoring(self) -> Dict[str, Any]:
        """Monitor threat intelligence feeds"""
        result = {
            'type': 'threat_feed_monitoring',
            'feeds_checked': [],
            'new_indicators': [],
            'feed_summary': {},
            'alerts': []
        }
        
        try:
            # Simulate threat feed sources
            feeds = [
                'MISP-Community',
                'AlienVault-OTX',
                'ThreatFox',
                'URLhaus',
                'MalwareBazaar'
            ]
            
            for feed in feeds:
                feed_result = self._check_threat_feed(feed)
                result['feeds_checked'].append(feed_result)
                
                # Aggregate new indicators
                new_iocs = feed_result.get('new_iocs', [])
                result['new_indicators'].extend(new_iocs)
                
                # Check for high-priority alerts
                if feed_result.get('high_priority_count', 0) > 0:
                    result['alerts'].append({
                        'feed': feed,
                        'alert_type': 'high_priority_indicators',
                        'count': feed_result['high_priority_count']
                    })
                    
            # Generate summary
            result['feed_summary'] = {
                'total_feeds': len(feeds),
                'total_new_indicators': len(result['new_indicators']),
                'total_alerts': len(result['alerts'])
            }
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def _check_threat_feed(self, feed_name: str) -> Dict[str, Any]:
        """Check individual threat feed"""
        result = {
            'feed': feed_name,
            'status': 'unknown',
            'new_iocs': [],
            'last_updated': datetime.utcnow().isoformat(),
            'high_priority_count': 0
        }
        
        try:
            # Simulate feed check
            import random
            
            result['status'] = random.choice(['online', 'online', 'offline', 'error'])
            
            if result['status'] == 'online':
                # Generate simulated IOCs
                ioc_count = random.randint(0, 20)
                for i in range(ioc_count):
                    ioc = {
                        'type': random.choice(['ip', 'domain', 'hash', 'url']),
                        'value': f'simulated-ioc-{i}',
                        'confidence': random.randint(60, 95),
                        'severity': random.choice(['low', 'medium', 'high', 'critical'])
                    }
                    result['new_iocs'].append(ioc)
                    
                    if ioc['severity'] in ['high', 'critical']:
                        result['high_priority_count'] += 1
                        
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            
        return result
        
    def attribution_analysis(self, indicators: List[str]) -> Dict[str, Any]:
        """Perform threat attribution analysis"""
        result = {
            'type': 'attribution_analysis',
            'indicators_analyzed': len(indicators),
            'potential_actors': [],
            'attack_patterns': [],
            'confidence_level': 'unknown'
        }
        
        try:
            # Simulate attribution analysis
            threat_actors = [
                {'name': 'APT1', 'country': 'CN', 'motivation': 'espionage'},
                {'name': 'Lazarus Group', 'country': 'KP', 'motivation': 'financial'},
                {'name': 'FIN7', 'country': 'Unknown', 'motivation': 'financial'},
                {'name': 'Turla', 'country': 'RU', 'motivation': 'espionage'},
                {'name': 'Carbanak', 'country': 'Unknown', 'motivation': 'financial'}
            ]
            
            attack_patterns = [
                'T1566.001 - Spearphishing Attachment',
                'T1071.001 - Web Protocols',
                'T1055 - Process Injection',
                'T1083 - File and Directory Discovery',
                'T1005 - Data from Local System'
            ]
            
            # Random attribution for simulation
            import random
            if len(indicators) > 5:
                result['potential_actors'] = random.sample(threat_actors, 2)
                result['attack_patterns'] = random.sample(attack_patterns, 3)
                result['confidence_level'] = 'medium'
            elif len(indicators) > 0:
                result['potential_actors'] = random.sample(threat_actors, 1)
                result['attack_patterns'] = random.sample(attack_patterns, 2)
                result['confidence_level'] = 'low'
            else:
                result['confidence_level'] = 'none'
                
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def intelligence(self, action: str = 'monitor', target: str = None, 
                    options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main intelligence interface"""
        options = options or {}
        
        # Analyze command
        command = f"intel {action}"
        if target:
            command += f" {target}"
        analysis = self.brain.analyze_command(command)
        
        if not analysis['safe_to_execute']:
            return {
                'error': 'Intelligence action blocked by security policy',
                'reason': analysis['explanation'],
                'suggestions': self.brain.get_command_suggestions(analysis)
            }
            
        self.results['intelligence_type'] = action
        
        intel_results = {
            'action_analysis': analysis,
            'intelligence_results': {}
        }
        
        # Execute appropriate intelligence actions
        if action == 'ioc_analysis':
            if not target:
                return {'error': 'IOC analysis requires a target IOC'}
            intel_results['intelligence_results']['ioc_analysis'] = \
                self.ioc_analysis(target, options.get('ioc_type', 'auto'))
                
        elif action == 'threat_feeds':
            intel_results['intelligence_results']['threat_feed_monitoring'] = \
                self.threat_feed_monitoring()
                
        elif action == 'attribution':
            indicators = options.get('indicators', [target] if target else [])
            intel_results['intelligence_results']['attribution_analysis'] = \
                self.attribution_analysis(indicators)
                
        elif action == 'monitor':
            # Comprehensive monitoring
            intel_results['intelligence_results']['threat_feed_monitoring'] = \
                self.threat_feed_monitoring()
            if target:
                intel_results['intelligence_results']['ioc_analysis'] = \
                    self.ioc_analysis(target)
                    
        else:
            return {
                'error': f'Unknown intelligence action: {action}',
                'available_actions': ['ioc_analysis', 'threat_feeds', 'attribution', 'monitor']
            }
            
        return intel_results
        
    def generate_report(self, results: Dict[str, Any], format_type: str = 'markdown') -> str:
        """Generate intelligence report"""
        if format_type == 'markdown':
            return self._generate_markdown_report(results)
        elif format_type == 'json':
            return json.dumps(results, indent=2)
        else:
            return str(results)
            
    def _generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate markdown formatted intelligence report"""
        report = f"""# Threat Intelligence Report

**Intel ID:** {self.results['intel_id']}
**Intelligence Type:** {self.results['intelligence_type']}
**Timestamp:** {self.results['timestamp']}

## Action Analysis
{results.get('action_analysis', {}).get('explanation', 'No analysis available')}

## Intelligence Results
"""
        
        for action_type, result in results.get('intelligence_results', {}).items():
            report += f"\n### {action_type.replace('_', ' ').title()}\n"
            
            if result.get('success'):
                if action_type == 'ioc_analysis':
                    ioc = result.get('ioc', 'Unknown')
                    ioc_type = result.get('ioc_type', 'Unknown')
                    reputation = result.get('reputation', 'Unknown')
                    
                    reputation_emoji = {
                        'clean': '🟢',
                        'suspicious': '🟡', 
                        'malicious': '🔴',
                        'unknown': '⚪'
                    }.get(reputation, '⚪')
                    
                    report += f"- **IOC:** {ioc}\n"
                    report += f"- **Type:** {ioc_type}\n"
                    report += f"- **Reputation:** {reputation_emoji} {reputation.upper()}\n"
                    
                    recommendations = result.get('recommendations', [])
                    if recommendations:
                        report += "- **Recommendations:**\n"
                        for rec in recommendations[:3]:  # Top 3
                            report += f"  - {rec}\n"
                            
                elif action_type == 'threat_feed_monitoring':
                    summary = result.get('feed_summary', {})
                    alerts = result.get('alerts', [])
                    
                    report += f"- **Feeds Monitored:** {summary.get('total_feeds', 0)}\n"
                    report += f"- **New Indicators:** {summary.get('total_new_indicators', 0)}\n"
                    report += f"- **High Priority Alerts:** {len(alerts)}\n"
                    
                    if alerts:
                        report += "- **Recent Alerts:**\n"
                        for alert in alerts[:3]:  # Top 3
                            feed = alert.get('feed', 'Unknown')
                            count = alert.get('count', 0)
                            report += f"  - {feed}: {count} high-priority indicators\n"
                            
                elif action_type == 'attribution_analysis':
                    indicators_count = result.get('indicators_analyzed', 0)
                    confidence = result.get('confidence_level', 'unknown')
                    actors = result.get('potential_actors', [])
                    
                    report += f"- **Indicators Analyzed:** {indicators_count}\n"
                    report += f"- **Confidence Level:** {confidence.upper()}\n"
                    
                    if actors:
                        report += "- **Potential Threat Actors:**\n"
                        for actor in actors:
                            name = actor.get('name', 'Unknown')
                            country = actor.get('country', 'Unknown')
                            motivation = actor.get('motivation', 'Unknown')
                            report += f"  - {name} ({country}) - {motivation}\n"
                            
            else:
                error = result.get('error', 'Unknown error')
                report += f"- **Error:** {error}\n"
                
        return report

def main():
    parser = argparse.ArgumentParser(description='Threat Intelligence and Monitoring Tool')
    parser.add_argument('action', choices=['ioc_analysis', 'threat_feeds', 'attribution', 'monitor'],
                       help='Intelligence action to perform')
    parser.add_argument('--target', help='Target for action (IOC, domain, etc.)')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Output format')
    parser.add_argument('--output', help='Output file (default: stdout)')
    parser.add_argument('--ioc-type', choices=['auto', 'ip', 'domain', 'hash', 'url'], 
                       default='auto', help='IOC type for analysis')
    parser.add_argument('--indicators', nargs='+', help='Multiple indicators for attribution analysis')
    
    args = parser.parse_args()
    
    intel = ThreatIntelligence()
    
    try:
        options = {}
        if args.ioc_type:
            options['ioc_type'] = args.ioc_type
        if args.indicators:
            options['indicators'] = args.indicators
            
        results = intel.intelligence(args.action, args.target, options)
        
        if 'error' in results:
            print(f"Error: {results['error']}", file=sys.stderr)
            if 'suggestions' in results:
                print("\nSuggested commands:", file=sys.stderr)
                for suggestion in results['suggestions']:
                    print(f"  {suggestion}", file=sys.stderr)
            sys.exit(1)
            
        report = intel.generate_report(results, args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)
            
    except KeyboardInterrupt:
        print("\nIntelligence operation interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()