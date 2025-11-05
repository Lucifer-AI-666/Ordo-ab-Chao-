#!/usr/bin/env python3
"""
CopilotPrivateAgent Web Server
Simple FastAPI server to demonstrate the JavaScript integration

Owner: Dib Anouar
License: LUP v1.0 (personal and non-commercial use only)
"""

import os
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from copilot_agent import CopilotPrivateAgent

# Initialize FastAPI app
app = FastAPI(
    title="CopilotPrivateAgent API",
    description="DibTauroS/Ordo-ab-Chao cybersecurity framework web interface",
    version="1.0.0"
)

# Initialize agent
agent = CopilotPrivateAgent()

# Request models
class OperationRequest(BaseModel):
    prompt: str
    target: str = "localhost"
    dry_run: bool = True

@app.get("/", response_class=HTMLResponse)
async def web_interface():
    """Serve the main web interface"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CopilotPrivateAgent - DibTauroS Framework</title>
</head>
<body>
    <div id="copilot-auto-init"></div>
    <script src="/static/copilot_integration.js"></script>
    
    <script>
        // Auto-initialize the agent with local API configuration
        window.copilotAgent = new CopilotPrivateAgent({
            baseUrl: window.location.origin,
            enableLogging: true
        });
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.get("/copilot/status")
async def get_status():
    """Get agent status"""
    try:
        return agent.get_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/copilot/execute")
async def execute_operation(request: OperationRequest):
    """Execute cybersecurity operation"""
    try:
        result = agent.execute_operation(
            prompt=request.prompt,
            target=request.target,
            dry_run=request.dry_run
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/static/copilot_integration.js")
async def serve_js():
    """Serve the JavaScript integration file"""
    js_file = Path(__file__).parent / "copilot_integration.js"
    if js_file.exists():
        return FileResponse(js_file, media_type="application/javascript")
    else:
        raise HTTPException(status_code=404, detail="JavaScript file not found")

@app.get("/branding/banner")
async def get_banner():
    """Get HTML banner for branding (optimized with async I/O)"""
    import aiofiles
    banner_file = Path(__file__).parent.parent / "branding" / "html_banner.html"
    if banner_file.exists():
        try:
            async with aiofiles.open(banner_file, 'r') as f:
                content = await f.read()
            return HTMLResponse(content=content)
        except ImportError:
            # Fallback to sync I/O if aiofiles not available
            with open(banner_file, 'r') as f:
                return HTMLResponse(content=f.read())
    else:
        return {"message": "Banner not found"}

@app.get("/branding/splash")
async def get_splash():
    """Get text splash banner (optimized with async I/O)"""
    import aiofiles
    splash_file = Path(__file__).parent.parent / "branding" / "splash.txt"
    if splash_file.exists():
        try:
            async with aiofiles.open(splash_file, 'r') as f:
                content = await f.read()
            return {"splash": content}
        except ImportError:
            # Fallback to sync I/O if aiofiles not available
            with open(splash_file, 'r') as f:
                return {"splash": f.read()}
    else:
        return {"splash": "CopilotPrivateAgent - DibTauroS Framework"}

if __name__ == "__main__":
    import uvicorn
    
    # Security: only bind to localhost
    host = os.getenv("COPILOT_HOST", "127.0.0.1")
    port = int(os.getenv("COPILOT_PORT", "8787"))
    
    print(f"Starting CopilotPrivateAgent web server on {host}:{port}")
    print("Framework: DibTauroS/Ordo-ab-Chao")
    print("Owner: Dib Anouar")
    print("License: LUP v1.0")
    
    uvicorn.run(app, host=host, port=port, log_level="info")