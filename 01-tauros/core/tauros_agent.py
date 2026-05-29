#!/usr/bin/env python3
"""
TaurosPrivateAgent - Core Python Agent
Privacy-first cybersecurity agent for DibTauroS/Ordo-ab-Chao framework

Owner: Dib Anouar
License: LUP v1.0 (personal and non-commercial use only)
"""

import os
import sys
import json
import logging
import hashlib
import datetime
import subprocess
import ipaddress
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

class OperationMode(Enum):
    """Operational modes for the TaurosPrivateAgent"""
    DEFEND = "DEFEND"  # Default: defensive operations only
    TEST = "TEST"      # Advanced operations (requires Wassim keyword)

# Buffer size used when streaming log files for SHA-256 hashing
_LOG_CHUNK_SIZE = 65536

@dataclass
class SecurityContext:
    """Security context for operations"""
    mode: OperationMode
    has_wassim_keyword: bool
    target: str
    is_target_allowed: bool
    user_privileges: str
    timestamp: datetime.datetime

class TaurosPrivateAgent:
    """
    Main TaurosPrivateAgent class

    Provides cybersecurity and OSINT capabilities with strict security controls:
    - DEFEND mode: standard defensive operations
    - TEST mode: advanced operations (requires "Wassim" keyword + allowlist)
    - All operations logged with SHA-256 audit trail
    - Dry-run mode for safe testing
    """

    def __init__(self, config_dir: str = None):
        """Initialize the TaurosPrivateAgent"""
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent.parent / "config"
        self.logs_dir = Path(__file__).parent.parent.parent / "logs"
        self.logs_dir.mkdir(exist_ok=True)

        # Setup logging
        self._setup_logging()

        # Load configuration
        self.allowlist = self._load_allowlist()
        self.modes_config = self._load_modes_config()

        # Security state
        self.current_mode = OperationMode.DEFEND
        self.monica_disabled = os.getenv('MONICA_DISABLE', '0') == '1'

        # Cache for parsed IP networks (performance optimization)
        self._allowlist_cache = {}
        self._parse_allowlist_cache()

        self.logger.info("TaurosPrivateAgent initialized - DibTauroS/Ordo-ab-Chao")
        self.logger.info(f"Mode: {self.current_mode.value}, MONICA disabled: {self.monica_disabled}")

    def _setup_logging(self):
        """Setup secure logging with SHA-256 audit trail"""
        log_file = self.logs_dir / "tauros_agent.log"
        self.logger = logging.getLogger("TaurosPrivateAgent")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        has_file_handler = any(
            isinstance(handler, logging.FileHandler) and Path(handler.baseFilename) == log_file
            for handler in self.logger.handlers
        )
        if not has_file_handler:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        has_stdout_handler = any(
            isinstance(handler, logging.StreamHandler)
            and not isinstance(handler, logging.FileHandler)
            and getattr(handler, "stream", None) is sys.stdout
            for handler in self.logger.handlers
        )
        if not has_stdout_handler:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

        self._update_log_chain()

    def _load_allowlist(self) -> Dict:
        """Load target allowlist"""
        allowlist_file = self.config_dir / "allowlist.json"
        try:
            with open(allowlist_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            parent_allowlist = Path(__file__).parent.parent.parent / "allowlist.json"
            if parent_allowlist.exists():
                with open(parent_allowlist, 'r') as f:
                    return json.load(f)
            else:
                self.logger.warning("No allowlist found, using default safe targets")
                return {
                    "allowed_targets": ["localhost", "127.0.0.1"],
                    "last_updated": datetime.datetime.now().isoformat()
                }

    def _load_modes_config(self) -> Dict:
        """Load operational modes configuration"""
        modes_file = self.config_dir / "modes.json"
        default_config = {
            "DEFEND": {
                "description": "Defensive operations only",
                "allowed_actions": ["scan", "monitor", "analyze", "report"],
                "requires_authorization": False
            },
            "TEST": {
                "description": "Advanced testing operations",
                "allowed_actions": ["scan", "monitor", "analyze", "report", "install", "firewall", "suid_check"],
                "requires_authorization": True,
                "authorization_keyword": "Wassim"
            }
        }

        try:
            with open(modes_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.info("Creating default modes configuration")
            os.makedirs(self.config_dir, exist_ok=True)
            with open(modes_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config

    def _update_log_chain(self):
        """Update SHA-256 audit trail for log integrity (optimized with streaming)"""
        chain_file = self.logs_dir / "tauros_audit_chain.json"

        log_file = self.logs_dir / "tauros_agent.log"
        hasher = hashlib.sha256()

        if log_file.exists():
            try:
                with open(log_file, 'rb') as f:
                    for chunk in iter(lambda: f.read(_LOG_CHUNK_SIZE), b''):
                        hasher.update(chunk)
            except (IOError, OSError):
                pass

        current_hash = hasher.hexdigest()

        try:
            with open(chain_file, 'r') as f:
                chain = json.load(f)
        except FileNotFoundError:
            chain = {"entries": []}

        chain["entries"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "log_hash": current_hash,
            "prev_hash": chain["entries"][-1]["log_hash"] if chain["entries"] else "genesis"
        })

        chain["entries"] = chain["entries"][-100:]

        with open(chain_file, 'w') as f:
            json.dump(chain, f, indent=2)

    def _parse_allowlist_cache(self):
        """Parse and cache IP networks from allowlist (performance optimization)"""
        self._allowlist_cache = {
            'hostnames': [],
            'networks': []
        }

        allowed_targets = self.allowlist.get("allowed_targets", [])
        for target in allowed_targets:
            if '/' in target:
                try:
                    network = ipaddress.ip_network(target, strict=False)
                    self._allowlist_cache['networks'].append(network)
                except ValueError:
                    self._allowlist_cache['hostnames'].append(target)
            else:
                self._allowlist_cache['hostnames'].append(target)

    def _check_target_allowed(self, target: str) -> bool:
        """Check if target is in allowlist (optimized with caching)"""
        if target in self._allowlist_cache['hostnames']:
            return True

        try:
            target_ip = ipaddress.ip_address(target)
            for network in self._allowlist_cache['networks']:
                if target_ip in network:
                    return True
        except ValueError:
            pass

        return False

    def _create_security_context(self, prompt: str, target: str = "localhost") -> SecurityContext:
        """Create security context for operation"""
        has_wassim = "Wassim" in prompt or "wassim" in prompt
        is_allowed = self._check_target_allowed(target)

        mode = OperationMode.DEFEND
        if has_wassim and is_allowed:
            mode = OperationMode.TEST

        return SecurityContext(
            mode=mode,
            has_wassim_keyword=has_wassim,
            target=target,
            is_target_allowed=is_allowed,
            user_privileges=os.getenv('USER', 'unknown'),
            timestamp=datetime.datetime.now()
        )

    def execute_operation(self, prompt: str, target: str = "localhost", dry_run: bool = True) -> Dict:
        """
        Execute cybersecurity operation with security controls

        Args:
            prompt: User prompt/command
            target: Target system/IP
            dry_run: If True, only simulate the operation

        Returns:
            Dict with operation results and security info
        """
        if self.monica_disabled:
            return {
                "status": "blocked",
                "message": "MONICA system disabled (MONICA_DISABLE=1)",
                "timestamp": datetime.datetime.now().isoformat()
            }

        context = self._create_security_context(prompt, target)

        self.logger.info(
            f"Operation requested - Mode: {context.mode.value}, "
            f"Target: {target}, Wassim: {context.has_wassim_keyword}"
        )

        if context.mode == OperationMode.TEST and not context.has_wassim_keyword:
            return {
                "status": "denied",
                "message": "TEST mode operations require 'Wassim' keyword",
                "security_context": self._serialize_context(context),
                "timestamp": context.timestamp.isoformat()
            }

        if not context.is_target_allowed:
            return {
                "status": "denied",
                "message": f"Target '{target}' not in allowlist",
                "security_context": self._serialize_context(context),
                "timestamp": context.timestamp.isoformat()
            }

        try:
            if dry_run:
                result = self._simulate_operation(prompt, context)
            else:
                result = self._execute_real_operation(prompt, context)

            self.logger.info(f"Operation completed - Status: {result.get('status', 'unknown')}")
            self._update_log_chain()

            return result

        except Exception as e:
            error_msg = "Operation failed due to an internal error"
            self.logger.error("execute_operation error: %s", e, exc_info=True)
            return {
                "status": "error",
                "message": error_msg,
                "security_context": self._serialize_context(context),
                "timestamp": context.timestamp.isoformat()
            }

    def _serialize_context(self, context: SecurityContext) -> Dict:
        """Serialize SecurityContext to dict"""
        return {
            "mode": context.mode.value,
            "has_wassim_keyword": context.has_wassim_keyword,
            "target": context.target,
            "is_target_allowed": context.is_target_allowed,
            "user_privileges": context.user_privileges,
            "timestamp": context.timestamp.isoformat()
        }

    def _simulate_operation(self, prompt: str, context: SecurityContext) -> Dict:
        """Simulate operation without actual execution"""
        operation_type = "unknown"
        if any(keyword in prompt.lower() for keyword in ["scan", "nmap", "port"]):
            operation_type = "network_scan"
        elif any(keyword in prompt.lower() for keyword in ["monitor", "ps", "process"]):
            operation_type = "system_monitor"
        elif any(keyword in prompt.lower() for keyword in ["install", "apt", "yum"]):
            operation_type = "package_install"
        elif any(keyword in prompt.lower() for keyword in ["suid", "privilege"]):
            operation_type = "privilege_check"
        elif any(keyword in prompt.lower() for keyword in ["firewall", "iptables", "ufw"]):
            operation_type = "firewall_check"

        commands = []
        if operation_type == "network_scan":
            commands = [f"nmap -sn {context.target}", f"nmap -sS -O {context.target}"]
        elif operation_type == "system_monitor":
            commands = ["ps aux", "netstat -tuln", "ss -tuln"]
        elif operation_type == "package_install":
            commands = ["apt list --upgradable", "apt update"]
        elif operation_type == "privilege_check":
            commands = ["find / -perm -4000 2>/dev/null", "sudo -l"]
        elif operation_type == "firewall_check":
            commands = ["iptables -L -n", "ufw status verbose"]

        return {
            "status": "simulated",
            "operation_type": operation_type,
            "mode": context.mode.value,
            "target": context.target,
            "commands_would_run": commands,
            "dry_run": True,
            "security_context": self._serialize_context(context),
            "timestamp": context.timestamp.isoformat()
        }

    def _execute_real_operation(self, prompt: str, context: SecurityContext) -> Dict:
        """Execute real operation with proper security checks"""
        if context.mode == OperationMode.DEFEND:
            safe_commands = {
                "ps": ["ps", "aux"],
                "netstat": ["netstat", "-tuln"],
                "ss": ["ss", "-tuln"],
                "df": ["df", "-h"],
                "uptime": ["uptime"],
                "who": ["who"],
                "w": ["w"],
                "last": ["last", "-n", "10"]
            }

            command_key = None
            for key in safe_commands:
                if key in prompt.lower():
                    command_key = key
                    break

            if command_key:
                try:
                    result = subprocess.run(
                        safe_commands[command_key],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    return {
                        "status": "success",
                        "command": " ".join(safe_commands[command_key]),
                        "output": result.stdout,
                        "error": result.stderr,
                        "return_code": result.returncode,
                        "mode": context.mode.value,
                        "timestamp": context.timestamp.isoformat()
                    }
                except subprocess.TimeoutExpired:
                    return {
                        "status": "timeout",
                        "message": "Command execution timed out",
                        "timestamp": context.timestamp.isoformat()
                    }
            else:
                return {
                    "status": "not_implemented",
                    "message": "Command not implemented in DEFEND mode",
                    "available_commands": list(safe_commands.keys()),
                    "timestamp": context.timestamp.isoformat()
                }

        elif context.mode == OperationMode.TEST:
            return {
                "status": "not_implemented",
                "message": "TEST mode real operations not yet implemented",
                "note": "Use dry_run=True for testing advanced operations",
                "timestamp": context.timestamp.isoformat()
            }

    def get_status(self) -> Dict:
        """Get current agent status"""
        return {
            "agent": "TaurosPrivateAgent",
            "version": "1.0.0",
            "owner": "Dib Anouar",
            "framework": "DibTauroS/Ordo-ab-Chao",
            "current_mode": self.current_mode.value,
            "monica_disabled": self.monica_disabled,
            "allowlist_targets": len(self.allowlist.get("allowed_targets", [])),
            "logs_dir": str(self.logs_dir),
            "config_dir": str(self.config_dir),
            "timestamp": datetime.datetime.now().isoformat()
        }


def main():
    """Main CLI interface for TaurosPrivateAgent"""
    import argparse

    parser = argparse.ArgumentParser(
        description="TaurosPrivateAgent - DibTauroS Cybersecurity Framework"
    )
    parser.add_argument("--prompt", "-p", help="Operation prompt/command")
    parser.add_argument("--target", "-t", default="localhost", help="Target system (default: localhost)")
    parser.add_argument("--real", action="store_true", help="Execute real operation (default: dry-run)")
    parser.add_argument("--status", action="store_true", help="Show agent status")
    parser.add_argument("--config-dir", help="Configuration directory path")

    args = parser.parse_args()

    agent = TaurosPrivateAgent(config_dir=args.config_dir)

    if args.status:
        status = agent.get_status()
        print(json.dumps(status, indent=2))
        return

    if not args.prompt:
        parser.error("--prompt is required when not using --status")

    result = agent.execute_operation(
        prompt=args.prompt,
        target=args.target,
        dry_run=not args.real
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
