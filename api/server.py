#!/usr/bin/env python3
"""
Copilot Private Agent API Server
RESTful API for controlling and monitoring the cybersecurity agent
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine.brain import CopilotBrain

# Security
security = HTTPBearer()

class CopilotAPIServer:
    """FastAPI server for Copilot Private Agent"""
    
    def __init__(self):
        self.app = FastAPI(
            title="Copilot Private Agent API",
            description="RESTful API for cybersecurity operations",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # CORS middleware (localhost only)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://127.0.0.1:*", "http://localhost:*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self.brain = CopilotBrain()
        self.api_token = os.environ.get('COPILOT_API_TOKEN')
        
        if not self.api_token:
            # Try to load from .env file
            env_file = Path(__file__).parent.parent / '.env'
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('COPILOT_API_TOKEN='):
                            self.api_token = line.split('=', 1)[1].strip()
                            break
                            
        if not self.api_token:
            raise ValueError("COPILOT_API_TOKEN not found in environment or .env file")
            
        self.setup_routes()
        self.setup_logging()
        
    def setup_logging(self):
        """Setup API logging"""
        log_dir = Path(__file__).parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'api.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('CopilotAPI')
        
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Security(security)):
        """Verify API token"""
        token = credentials.credentials
        if token != self.api_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token
        
    def setup_routes(self):
        """Setup API routes"""
        
        # Pydantic models
        class CommandRequest(BaseModel):
            command: str = Field(..., description="Command to execute")
            context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
            
        class ScanRequest(BaseModel):
            target: str = Field(..., description="Target to scan")
            scan_type: str = Field(default="auto", description="Type of scan")
            intensity: str = Field(default="moderate", description="Scan intensity")
            ports: Optional[str] = Field(None, description="Port specification")
            
        class ReconRequest(BaseModel):
            target: str = Field(..., description="Target for reconnaissance")
            recon_type: str = Field(default="auto", description="Type of reconnaissance")
            intensity: str = Field(default="moderate", description="Reconnaissance intensity")
            
        class DefenseRequest(BaseModel):
            action: str = Field(..., description="Defense action")
            target: Optional[str] = Field(None, description="Target for action")
            options: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional options")
            
        # Health check
        @self.app.get("/")
        async def root():
            return {"message": "Copilot Private Agent API", "status": "operational", "version": "1.0.0"}
            
        @self.app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "components": {
                    "brain": "operational",
                    "api": "operational"
                }
            }
            
        @self.app.get("/status")
        async def status():
            """Get system status"""
            try:
                # Check brain functionality
                test_analysis = self.brain.analyze_command("test command")
                brain_status = "operational" if test_analysis else "error"
                
                return {
                    "status": "operational",
                    "timestamp": datetime.utcnow().isoformat(),
                    "components": {
                        "brain": brain_status,
                        "api": "operational",
                        "authentication": "enabled"
                    },
                    "uptime": "unknown"  # Could be enhanced
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")
                
        # Command analysis
        @self.app.post("/analyze")
        async def analyze_command(request: CommandRequest, token: str = Depends(self.verify_token)):
            """Analyze a command for safety and requirements"""
            try:
                analysis = self.brain.analyze_command(request.command, request.context)
                
                self.logger.info(f"Command analyzed: {request.command} -> {analysis['risk_level']}")
                
                return {
                    "status": "success",
                    "analysis": analysis,
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                self.logger.error(f"Command analysis failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
                
        # Scanning operations
        @self.app.post("/scan")
        async def perform_scan(request: ScanRequest, token: str = Depends(self.verify_token)):
            """Perform network scanning"""
            try:
                # Import here to avoid circular dependencies
                from commands.cyber_scan import UniversalScanner
                
                scanner = UniversalScanner()
                results = scanner.scan(
                    target=request.target,
                    scan_type=request.scan_type,
                    intensity=request.intensity,
                    ports=request.ports
                )
                
                self.logger.info(f"Scan completed: {request.target} ({request.scan_type})")
                
                return {
                    "status": "success",
                    "results": results,
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                self.logger.error(f"Scan failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")
                
        # Reconnaissance operations
        @self.app.post("/recon")
        async def perform_reconnaissance(request: ReconRequest, token: str = Depends(self.verify_token)):
            """Perform reconnaissance"""
            try:
                from commands.cyber_recon import AdvancedRecon
                
                recon = AdvancedRecon()
                results = recon.reconnaissance(
                    target=request.target,
                    recon_type=request.recon_type,
                    intensity=request.intensity
                )
                
                self.logger.info(f"Reconnaissance completed: {request.target} ({request.recon_type})")
                
                return {
                    "status": "success",
                    "results": results,
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                self.logger.error(f"Reconnaissance failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Reconnaissance failed: {str(e)}")
                
        # Defense operations
        @self.app.post("/defend")
        async def perform_defense(request: DefenseRequest, token: str = Depends(self.verify_token)):
            """Perform defensive operations"""
            try:
                from commands.cyber_defend import CyberDefense
                
                defense = CyberDefense()
                results = defense.defend(
                    action=request.action,
                    target=request.target,
                    options=request.options
                )
                
                self.logger.info(f"Defense action completed: {request.action}")
                
                return {
                    "status": "success",
                    "results": results,
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                self.logger.error(f"Defense action failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Defense action failed: {str(e)}")
                
        # Configuration management
        @self.app.get("/config")
        async def get_configuration(token: str = Depends(self.verify_token)):
            """Get current configuration (sanitized)"""
            try:
                config = {
                    "allowlist_summary": {
                        "targets": len(self.brain.allowlist.get('allowed_targets', {})),
                        "auto_detection": self.brain.allowlist.get('auto_detection', {}).get('enabled', False)
                    },
                    "profiles": list(self.brain.profiles.get('profiles', {}).keys()),
                    "tools_configured": len(self.brain.tools.get('tool_categories', {}))
                }
                
                return {
                    "status": "success",
                    "configuration": config,
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Configuration retrieval failed: {str(e)}")
                
        # Logs and monitoring
        @self.app.get("/logs")
        async def get_logs(token: str = Depends(self.verify_token), limit: int = 100):
            """Get recent log entries"""
            try:
                log_dir = Path(__file__).parent.parent / 'logs'
                logs = []
                
                # Read recent API logs
                api_log_file = log_dir / 'api.log'
                if api_log_file.exists():
                    with open(api_log_file, 'r') as f:
                        lines = f.readlines()
                        for line in lines[-limit:]:
                            logs.append({
                                'source': 'api',
                                'content': line.strip(),
                                'timestamp': datetime.utcnow().isoformat()
                            })
                            
                return {
                    "status": "success",
                    "logs": logs,
                    "total": len(logs),
                    "timestamp": datetime.utcnow().isoformat()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Log retrieval failed: {str(e)}")
                
        # Dashboard
        @self.app.get("/dashboard", response_class=HTMLResponse)
        async def dashboard():
            """Serve the web dashboard"""
            dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Copilot Private Agent Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f0f0; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .status { padding: 10px; border-radius: 3px; margin: 10px 0; }
        .status.good { background: #d4edda; color: #155724; }
        .status.warning { background: #fff3cd; color: #856404; }
        .status.error { background: #f8d7da; color: #721c24; }
        button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background: #2980b9; }
        .form-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; }
        input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 3px; }
        #results { background: #f8f9fa; padding: 15px; border-radius: 3px; margin-top: 15px; white-space: pre-wrap; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Copilot Private Agent</h1>
            <p>Universal Cybersecurity Command & Control Dashboard</p>
        </div>
        
        <div class="card">
            <h2>System Status</h2>
            <div id="status" class="status">Loading...</div>
            <button onclick="checkStatus()">Refresh Status</button>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>🔍 Network Scanning</h3>
                <div class="form-group">
                    <label>Target:</label>
                    <input type="text" id="scan-target" placeholder="IP, domain, or network">
                </div>
                <div class="form-group">
                    <label>Scan Type:</label>
                    <select id="scan-type">
                        <option value="auto">Auto-detect</option>
                        <option value="host_discovery">Host Discovery</option>
                        <option value="port_scan">Port Scan</option>
                        <option value="vulnerability_scan">Vulnerability Scan</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Intensity:</label>
                    <select id="scan-intensity">
                        <option value="passive">Passive</option>
                        <option value="moderate" selected>Moderate</option>
                        <option value="aggressive">Aggressive</option>
                    </select>
                </div>
                <button onclick="performScan()">Start Scan</button>
            </div>
            
            <div class="card">
                <h3>🕵️ Reconnaissance</h3>
                <div class="form-group">
                    <label>Target:</label>
                    <input type="text" id="recon-target" placeholder="Domain or organization">
                </div>
                <div class="form-group">
                    <label>Recon Type:</label>
                    <select id="recon-type">
                        <option value="auto">Auto-detect</option>
                        <option value="dns_lookup">DNS Lookup</option>
                        <option value="subdomain_enumeration">Subdomain Enum</option>
                        <option value="web_reconnaissance">Web Recon</option>
                    </select>
                </div>
                <button onclick="performRecon()">Start Reconnaissance</button>
            </div>
            
            <div class="card">
                <h3>🛡️ Defense & Monitoring</h3>
                <div class="form-group">
                    <label>Action:</label>
                    <select id="defense-action">
                        <option value="monitor">System Monitor</option>
                        <option value="audit">Security Audit</option>
                        <option value="detect">Incident Detection</option>
                        <option value="analyze_logs">Log Analysis</option>
                    </select>
                </div>
                <button onclick="performDefense()">Execute Defense</button>
            </div>
        </div>
        
        <div class="card">
            <h3>📊 Results</h3>
            <div id="results">Results will appear here...</div>
        </div>
    </div>
    
    <script>
        const API_BASE = '';
        let authToken = localStorage.getItem('copilot_token');
        
        if (!authToken) {
            authToken = prompt('Enter API Token:');
            if (authToken) {
                localStorage.setItem('copilot_token', authToken);
            }
        }
        
        function makeRequest(url, method = 'GET', data = null) {
            const options = {
                method: method,
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                    'Content-Type': 'application/json'
                }
            };
            
            if (data) {
                options.body = JSON.stringify(data);
            }
            
            return fetch(url, options).then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            });
        }
        
        function updateResults(data) {
            document.getElementById('results').textContent = JSON.stringify(data, null, 2);
        }
        
        function checkStatus() {
            makeRequest('/status')
                .then(data => {
                    const statusElement = document.getElementById('status');
                    if (data.status === 'operational') {
                        statusElement.className = 'status good';
                        statusElement.textContent = '✅ System Operational - All components healthy';
                    } else {
                        statusElement.className = 'status warning';
                        statusElement.textContent = '⚠️ System Issues Detected';
                    }
                })
                .catch(error => {
                    const statusElement = document.getElementById('status');
                    statusElement.className = 'status error';
                    statusElement.textContent = `❌ Connection Error: ${error.message}`;
                });
        }
        
        function performScan() {
            const target = document.getElementById('scan-target').value;
            const scanType = document.getElementById('scan-type').value;
            const intensity = document.getElementById('scan-intensity').value;
            
            if (!target) {
                alert('Please enter a target');
                return;
            }
            
            updateResults({status: 'Scanning...', target: target});
            
            makeRequest('/scan', 'POST', {
                target: target,
                scan_type: scanType,
                intensity: intensity
            })
            .then(data => updateResults(data))
            .catch(error => updateResults({error: error.message}));
        }
        
        function performRecon() {
            const target = document.getElementById('recon-target').value;
            const reconType = document.getElementById('recon-type').value;
            
            if (!target) {
                alert('Please enter a target');
                return;
            }
            
            updateResults({status: 'Reconnaissance in progress...', target: target});
            
            makeRequest('/recon', 'POST', {
                target: target,
                recon_type: reconType,
                intensity: 'moderate'
            })
            .then(data => updateResults(data))
            .catch(error => updateResults({error: error.message}));
        }
        
        function performDefense() {
            const action = document.getElementById('defense-action').value;
            
            updateResults({status: 'Executing defense action...', action: action});
            
            makeRequest('/defend', 'POST', {
                action: action
            })
            .then(data => updateResults(data))
            .catch(error => updateResults({error: error.message}));
        }
        
        // Load status on page load
        checkStatus();
    </script>
</body>
</html>
            """
            return HTMLResponse(content=dashboard_html)

def create_app():
    """Create and configure the FastAPI app"""
    server = CopilotAPIServer()
    return server.app

# For uvicorn
app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "api.server:app",
        host="127.0.0.1",
        port=8787,
        reload=False,
        access_log=True
    )