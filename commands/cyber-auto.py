#!/usr/bin/env python3
"""
Automation and Orchestration Tool - cyber-auto.py
Automated workflows, responses, and orchestration capabilities
"""

import argparse
import json
import sys
import os
import time
import schedule
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable

# Add engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine.brain import CopilotBrain

class CyberAutomation:
    """Advanced automation and orchestration system"""
    
    def __init__(self):
        self.brain = CopilotBrain()
        self.results = {
            'automation_id': datetime.utcnow().strftime('%Y%m%d_%H%M%S'),
            'timestamp': datetime.utcnow().isoformat(),
            'automation_type': '',
            'status': 'initialized'
        }
        self.running_automations = {}
        self.automation_history = []
        
    def create_workflow(self, workflow_name: str, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create automated workflow"""
        result = {
            'type': 'workflow_creation',
            'workflow_name': workflow_name,
            'steps_count': len(steps),
            'workflow_id': f"wf_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'status': 'created'
        }
        
        try:
            # Validate workflow steps
            validated_steps = []
            for i, step in enumerate(steps):
                validated_step = self._validate_workflow_step(step, i)
                if validated_step.get('valid'):
                    validated_steps.append(validated_step)
                else:
                    result['error'] = f"Invalid step {i}: {validated_step.get('error')}"
                    result['status'] = 'failed'
                    return result
                    
            # Store workflow
            workflow = {
                'id': result['workflow_id'],
                'name': workflow_name,
                'steps': validated_steps,
                'created_at': datetime.utcnow().isoformat(),
                'status': 'ready'
            }
            
            # Save workflow to file
            workflow_dir = Path(__file__).parent.parent / 'logs' / 'workflows'
            workflow_dir.mkdir(exist_ok=True)
            
            with open(workflow_dir / f"{result['workflow_id']}.json", 'w') as f:
                json.dump(workflow, f, indent=2)
                
            result['workflow'] = workflow
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def _validate_workflow_step(self, step: Dict[str, Any], step_index: int) -> Dict[str, Any]:
        """Validate individual workflow step"""
        required_fields = ['action', 'type']
        
        for field in required_fields:
            if field not in step:
                return {'valid': False, 'error': f"Missing required field: {field}"}
                
        valid_actions = ['scan', 'recon', 'defend', 'monitor', 'alert', 'wait']
        if step['action'] not in valid_actions:
            return {'valid': False, 'error': f"Invalid action: {step['action']}"}
            
        # Add step metadata
        validated_step = step.copy()
        validated_step.update({
            'step_id': f"step_{step_index}",
            'valid': True,
            'estimated_duration': step.get('timeout', 300),  # Default 5 minutes
            'dependencies': step.get('dependencies', [])
        })
        
        return validated_step
        
    def execute_workflow(self, workflow_id: str, dry_run: bool = False) -> Dict[str, Any]:
        """Execute automated workflow"""
        result = {
            'type': 'workflow_execution',
            'workflow_id': workflow_id,
            'dry_run': dry_run,
            'execution_id': f"exec_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'steps_executed': [],
            'status': 'running'
        }
        
        try:
            # Load workflow
            workflow_dir = Path(__file__).parent.parent / 'logs' / 'workflows'
            workflow_file = workflow_dir / f"{workflow_id}.json"
            
            if not workflow_file.exists():
                return {'error': f'Workflow {workflow_id} not found', 'success': False}
                
            with open(workflow_file, 'r') as f:
                workflow = json.load(f)
                
            result['workflow_name'] = workflow.get('name', 'Unknown')
            
            # Execute workflow steps
            for step in workflow.get('steps', []):
                step_result = self._execute_workflow_step(step, dry_run)
                result['steps_executed'].append(step_result)
                
                # Check if step failed
                if not step_result.get('success', False):
                    result['status'] = 'failed'
                    result['failed_step'] = step.get('step_id')
                    break
                    
                # Wait between steps if specified
                wait_time = step.get('wait_after', 0)
                if wait_time > 0 and not dry_run:
                    time.sleep(wait_time)
                    
            if result['status'] == 'running':
                result['status'] = 'completed'
                
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            result['status'] = 'error'
            
        return result
        
    def _execute_workflow_step(self, step: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
        """Execute individual workflow step"""
        step_result = {
            'step_id': step.get('step_id'),
            'action': step.get('action'),
            'start_time': datetime.utcnow().isoformat(),
            'dry_run': dry_run
        }
        
        try:
            action = step['action']
            
            if dry_run:
                # Simulate step execution
                step_result.update({
                    'simulated': True,
                    'would_execute': step.get('command', f"{action} operation"),
                    'estimated_time': step.get('estimated_duration', 60),
                    'success': True
                })
            else:
                # Actually execute the step
                if action == 'scan':
                    step_result.update(self._execute_scan_step(step))
                elif action == 'recon':
                    step_result.update(self._execute_recon_step(step))
                elif action == 'defend':
                    step_result.update(self._execute_defend_step(step))
                elif action == 'monitor':
                    step_result.update(self._execute_monitor_step(step))
                elif action == 'alert':
                    step_result.update(self._execute_alert_step(step))
                elif action == 'wait':
                    step_result.update(self._execute_wait_step(step))
                else:
                    step_result.update({'error': f'Unknown action: {action}', 'success': False})
                    
            step_result['end_time'] = datetime.utcnow().isoformat()
            
        except Exception as e:
            step_result.update({
                'error': str(e),
                'success': False,
                'end_time': datetime.utcnow().isoformat()
            })
            
        return step_result
        
    def _execute_scan_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute scan step"""
        try:
            from commands.cyber_scan import UniversalScanner
            
            scanner = UniversalScanner()
            target = step.get('target', 'localhost')
            scan_type = step.get('scan_type', 'auto')
            intensity = step.get('intensity', 'moderate')
            
            scan_result = scanner.scan(target, scan_type, intensity)
            
            return {
                'success': True,
                'result_summary': f"Scanned {target}",
                'full_result': scan_result
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def _execute_recon_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute reconnaissance step"""
        try:
            from commands.cyber_recon import AdvancedRecon
            
            recon = AdvancedRecon()
            target = step.get('target', 'example.com')
            recon_type = step.get('recon_type', 'auto')
            
            recon_result = recon.reconnaissance(target, recon_type)
            
            return {
                'success': True,
                'result_summary': f"Reconnaissance of {target}",
                'full_result': recon_result
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def _execute_defend_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute defense step"""
        try:
            from commands.cyber_defend import CyberDefense
            
            defense = CyberDefense()
            action = step.get('defense_action', 'monitor')
            
            defense_result = defense.defend(action)
            
            return {
                'success': True,
                'result_summary': f"Defense action: {action}",
                'full_result': defense_result
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def _execute_monitor_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute monitoring step"""
        duration = step.get('duration', 60)  # Monitor for 60 seconds
        
        # Simplified monitoring
        import psutil
        
        monitoring_data = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'network_connections': len(psutil.net_connections())
        }
        
        return {
            'success': True,
            'result_summary': f"Monitored system for {duration}s",
            'monitoring_data': monitoring_data
        }
        
    def _execute_alert_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute alert step"""
        message = step.get('message', 'Automation alert')
        severity = step.get('severity', 'info')
        
        # Log alert (in production, could send to SIEM, email, etc.)
        alert_data = {
            'message': message,
            'severity': severity,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Write to alert log
        log_dir = Path(__file__).parent.parent / 'logs'
        with open(log_dir / 'alerts.log', 'a') as f:
            f.write(f"{json.dumps(alert_data)}\n")
            
        return {
            'success': True,
            'result_summary': f"Alert sent: {message}",
            'alert_data': alert_data
        }
        
    def _execute_wait_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute wait step"""
        duration = step.get('duration', 10)
        time.sleep(duration)
        
        return {
            'success': True,
            'result_summary': f"Waited {duration} seconds"
        }
        
    def schedule_automation(self, workflow_id: str, schedule_config: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule automated workflow execution"""
        result = {
            'type': 'automation_scheduling',
            'workflow_id': workflow_id,
            'schedule_id': f"sched_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'status': 'scheduled'
        }
        
        try:
            schedule_type = schedule_config.get('type', 'once')
            
            if schedule_type == 'once':
                # One-time execution
                execution_time = schedule_config.get('execute_at')
                if execution_time:
                    # In production, would use proper scheduler
                    result['scheduled_for'] = execution_time
                    
            elif schedule_type == 'recurring':
                # Recurring execution
                interval = schedule_config.get('interval', 'daily')
                time_of_day = schedule_config.get('time', '00:00')
                
                if interval == 'daily':
                    schedule.every().day.at(time_of_day).do(
                        self._scheduled_execution, workflow_id
                    )
                elif interval == 'hourly':
                    schedule.every().hour.do(
                        self._scheduled_execution, workflow_id
                    )
                    
                result['interval'] = interval
                result['time'] = time_of_day
                
            # Store schedule info
            self.running_automations[result['schedule_id']] = {
                'workflow_id': workflow_id,
                'schedule_config': schedule_config,
                'created_at': datetime.utcnow().isoformat(),
                'status': 'active'
            }
            
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            
        return result
        
    def _scheduled_execution(self, workflow_id: str):
        """Execute scheduled workflow"""
        try:
            execution_result = self.execute_workflow(workflow_id, dry_run=False)
            
            # Log execution
            log_entry = {
                'workflow_id': workflow_id,
                'execution_result': execution_result,
                'timestamp': datetime.utcnow().isoformat(),
                'type': 'scheduled_execution'
            }
            
            self.automation_history.append(log_entry)
            
            # Write to log file
            log_dir = Path(__file__).parent.parent / 'logs'
            with open(log_dir / 'automation.log', 'a') as f:
                f.write(f"{json.dumps(log_entry)}\n")
                
        except Exception as e:
            print(f"Scheduled execution failed: {e}")
            
    def incident_response_automation(self, incident_type: str, 
                                   severity: str = 'medium') -> Dict[str, Any]:
        """Automated incident response"""
        result = {
            'type': 'incident_response',
            'incident_type': incident_type,
            'severity': severity,
            'response_id': f"ir_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'actions_taken': []
        }
        
        try:
            # Define response workflows based on incident type
            response_workflows = {
                'malware_detected': [
                    {'action': 'defend', 'defense_action': 'detect'},
                    {'action': 'scan', 'target': 'localhost', 'intensity': 'aggressive'},
                    {'action': 'alert', 'message': f'Malware incident response - {severity}', 'severity': severity}
                ],
                'unauthorized_access': [
                    {'action': 'defend', 'defense_action': 'audit'},
                    {'action': 'monitor', 'duration': 300},
                    {'action': 'alert', 'message': f'Unauthorized access incident - {severity}', 'severity': severity}
                ],
                'network_anomaly': [
                    {'action': 'defend', 'defense_action': 'monitor'},
                    {'action': 'scan', 'target': 'localhost', 'scan_type': 'port_scan'},
                    {'action': 'alert', 'message': f'Network anomaly detected - {severity}', 'severity': severity}
                ]
            }
            
            workflow_steps = response_workflows.get(incident_type, [
                {'action': 'alert', 'message': f'Unknown incident type: {incident_type}', 'severity': 'high'}
            ])
            
            # Execute response workflow
            for step in workflow_steps:
                step_result = self._execute_workflow_step(step, dry_run=False)
                result['actions_taken'].append(step_result)
                
            result['status'] = 'completed'
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
            result['status'] = 'failed'
            
        return result
        
    def automation(self, action: str = 'status', target: str = None, 
                  options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main automation interface"""
        options = options or {}
        
        # Analyze command
        command = f"auto {action}"
        if target:
            command += f" {target}"
        analysis = self.brain.analyze_command(command)
        
        if not analysis['safe_to_execute']:
            return {
                'error': 'Automation action blocked by security policy',
                'reason': analysis['explanation'],
                'suggestions': self.brain.get_command_suggestions(analysis)
            }
            
        self.results['automation_type'] = action
        
        automation_results = {
            'action_analysis': analysis,
            'automation_results': {}
        }
        
        # Execute appropriate automation actions
        if action == 'create_workflow':
            workflow_name = options.get('name', 'unnamed_workflow')
            steps = options.get('steps', [])
            automation_results['automation_results']['workflow_creation'] = \
                self.create_workflow(workflow_name, steps)
                
        elif action == 'execute_workflow':
            if not target:
                return {'error': 'Execute workflow requires workflow ID'}
            dry_run = options.get('dry_run', False)
            automation_results['automation_results']['workflow_execution'] = \
                self.execute_workflow(target, dry_run)
                
        elif action == 'schedule':
            if not target:
                return {'error': 'Schedule requires workflow ID'}
            schedule_config = options.get('schedule', {})
            automation_results['automation_results']['automation_scheduling'] = \
                self.schedule_automation(target, schedule_config)
                
        elif action == 'incident_response':
            incident_type = target or 'unknown'
            severity = options.get('severity', 'medium')
            automation_results['automation_results']['incident_response'] = \
                self.incident_response_automation(incident_type, severity)
                
        elif action == 'status':
            automation_results['automation_results']['status'] = {
                'running_automations': len(self.running_automations),
                'history_entries': len(self.automation_history),
                'active_schedules': list(self.running_automations.keys()),
                'success': True
            }
            
        else:
            return {
                'error': f'Unknown automation action: {action}',
                'available_actions': ['create_workflow', 'execute_workflow', 'schedule', 'incident_response', 'status']
            }
            
        return automation_results
        
    def generate_report(self, results: Dict[str, Any], format_type: str = 'markdown') -> str:
        """Generate automation report"""
        if format_type == 'markdown':
            return self._generate_markdown_report(results)
        elif format_type == 'json':
            return json.dumps(results, indent=2)
        else:
            return str(results)
            
    def _generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate markdown formatted automation report"""
        report = f"""# Automation Report

**Automation ID:** {self.results['automation_id']}
**Automation Type:** {self.results['automation_type']}
**Timestamp:** {self.results['timestamp']}

## Action Analysis
{results.get('action_analysis', {}).get('explanation', 'No analysis available')}

## Automation Results
"""
        
        for action_type, result in results.get('automation_results', {}).items():
            report += f"\n### {action_type.replace('_', ' ').title()}\n"
            
            if result.get('success'):
                if action_type == 'workflow_creation':
                    workflow_name = result.get('workflow_name', 'Unknown')
                    steps_count = result.get('steps_count', 0)
                    workflow_id = result.get('workflow_id', 'Unknown')
                    
                    report += f"- **Workflow Name:** {workflow_name}\n"
                    report += f"- **Steps:** {steps_count}\n"
                    report += f"- **Workflow ID:** {workflow_id}\n"
                    report += f"- **Status:** ✅ Created successfully\n"
                    
                elif action_type == 'workflow_execution':
                    workflow_id = result.get('workflow_id', 'Unknown')
                    execution_id = result.get('execution_id', 'Unknown')
                    status = result.get('status', 'Unknown')
                    steps_executed = len(result.get('steps_executed', []))
                    
                    status_emoji = {'completed': '✅', 'failed': '❌', 'running': '🔄'}.get(status, '⚪')
                    
                    report += f"- **Workflow ID:** {workflow_id}\n"
                    report += f"- **Execution ID:** {execution_id}\n"
                    report += f"- **Status:** {status_emoji} {status.upper()}\n"
                    report += f"- **Steps Executed:** {steps_executed}\n"
                    
                elif action_type == 'incident_response':
                    incident_type = result.get('incident_type', 'Unknown')
                    severity = result.get('severity', 'Unknown')
                    actions_count = len(result.get('actions_taken', []))
                    
                    report += f"- **Incident Type:** {incident_type}\n"
                    report += f"- **Severity:** {severity.upper()}\n"
                    report += f"- **Actions Taken:** {actions_count}\n"
                    report += f"- **Status:** ✅ Response completed\n"
                    
                elif action_type == 'status':
                    running = result.get('running_automations', 0)
                    history = result.get('history_entries', 0)
                    schedules = result.get('active_schedules', [])
                    
                    report += f"- **Running Automations:** {running}\n"
                    report += f"- **History Entries:** {history}\n"
                    report += f"- **Active Schedules:** {len(schedules)}\n"
                    
                    if schedules:
                        report += "- **Schedule IDs:**\n"
                        for schedule_id in schedules[:5]:  # Top 5
                            report += f"  - {schedule_id}\n"
                            
            else:
                error = result.get('error', 'Unknown error')
                report += f"- **Error:** {error}\n"
                
        return report

def main():
    parser = argparse.ArgumentParser(description='Automation and Orchestration Tool')
    parser.add_argument('action', choices=['create_workflow', 'execute_workflow', 'schedule', 'incident_response', 'status'],
                       help='Automation action to perform')
    parser.add_argument('--target', help='Target for action (workflow ID, incident type, etc.)')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Output format')
    parser.add_argument('--output', help='Output file (default: stdout)')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode for workflow execution')
    parser.add_argument('--workflow-file', help='JSON file containing workflow definition')
    parser.add_argument('--severity', choices=['low', 'medium', 'high', 'critical'], 
                       default='medium', help='Incident severity')
    
    args = parser.parse_args()
    
    automation = CyberAutomation()
    
    try:
        options = {}
        
        if args.dry_run:
            options['dry_run'] = True
            
        if args.severity:
            options['severity'] = args.severity
            
        if args.workflow_file and args.action == 'create_workflow':
            with open(args.workflow_file, 'r') as f:
                workflow_data = json.load(f)
            options['name'] = workflow_data.get('name', 'imported_workflow')
            options['steps'] = workflow_data.get('steps', [])
            
        results = automation.automation(args.action, args.target, options)
        
        if 'error' in results:
            print(f"Error: {results['error']}", file=sys.stderr)
            if 'suggestions' in results:
                print("\nSuggested commands:", file=sys.stderr)
                for suggestion in results['suggestions']:
                    print(f"  {suggestion}", file=sys.stderr)
            sys.exit(1)
            
        report = automation.generate_report(results, args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)
            
    except KeyboardInterrupt:
        print("\nAutomation interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()