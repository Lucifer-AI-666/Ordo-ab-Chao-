#!/usr/bin/env python3
"""
TaurosPrivateAgent Web Server
FastAPI server to expose the Tauros agent over a local HTTP interface

Owner: Dib Anouar
License: LUP v1.0 (personal and non-commercial use only)
"""

import os
import secrets
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

try:
    import aiofiles
    HAS_AIOFILES = True
except ImportError:
    HAS_AIOFILES = False

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from tauros_agent import TaurosPrivateAgent

CONFIG_DIR = Path(__file__).parent.parent / "config"
ENV_FILE = CONFIG_DIR / ".env.tauros"

if load_dotenv and ENV_FILE.exists():
    load_dotenv(ENV_FILE)

app = FastAPI(
    title="TaurosPrivateAgent API",
    description="DibTauroS/Ordo-ab-Chao cybersecurity framework web interface",
    version="1.0.0"
)

agent = TaurosPrivateAgent()
_server_log = logging.getLogger("TaurosWebServer")

def _is_placeholder_token(token: str) -> bool:
    normalized = token.strip().lower()
    return not normalized or "change_this_in_production" in normalized

def _require_real_operation_token(request: Request):
    token = os.getenv("TAUROS_API_TOKEN", "").strip()
    if _is_placeholder_token(token):
        raise HTTPException(
            status_code=503,
            detail="Real execution is disabled until TAUROS_API_TOKEN is configured"
        )

    authorization = request.headers.get("Authorization", "")
    scheme, _, provided_token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not secrets.compare_digest(provided_token.strip(), token):
        raise HTTPException(status_code=401, detail="Unauthorized")

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
    <title>TaurosPrivateAgent - DibTauroS Framework</title>
</head>
<body>
    <div id="tauros-auto-init"></div>
    <script src="/static/tauros_integration.js"></script>

    <script>
        window.taurosAgent = new TaurosPrivateAgent({
            baseUrl: window.location.origin,
            enableLogging: true
        });
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.get("/tauros/status")
async def get_status():
    """Get agent status"""
    try:
        return agent.get_status()
    except Exception as e:
        _server_log.error("get_status failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/tauros/execute")
async def execute_operation(operation: OperationRequest, request: Request):
    """Execute cybersecurity operation"""
    try:
        if not operation.dry_run:
            _require_real_operation_token(request)

        result = agent.execute_operation(
            prompt=operation.prompt,
            target=operation.target,
            dry_run=operation.dry_run
        )
        return result
    except Exception as e:
        # Log full error internally; return only a generic message to callers
        _server_log.error("execute_operation failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/static/tauros_integration.js")
async def serve_js():
    """Serve the JavaScript integration file"""
    js_file = Path(__file__).parent / "tauros_integration.js"
    if js_file.exists():
        return FileResponse(js_file, media_type="application/javascript")
    else:
        raise HTTPException(status_code=404, detail="JavaScript file not found")

@app.get("/branding/banner")
async def get_banner():
    """Get HTML banner for branding"""
    banner_file = Path(__file__).parent.parent / "branding" / "html_banner.html"
    if banner_file.exists():
        if HAS_AIOFILES:
            async with aiofiles.open(banner_file, 'r') as f:
                content = await f.read()
            return HTMLResponse(content=content)
        else:
            with open(banner_file, 'r') as f:
                return HTMLResponse(content=f.read())
    else:
        return {"message": "Banner not found"}

@app.get("/branding/splash")
async def get_splash():
    """Get text splash banner"""
    splash_file = Path(__file__).parent.parent / "branding" / "splash.txt"
    if splash_file.exists():
        if HAS_AIOFILES:
            async with aiofiles.open(splash_file, 'r') as f:
                content = await f.read()
            return {"splash": content}
        else:
            with open(splash_file, 'r') as f:
                return {"splash": f.read()}
    else:
        return {"splash": "TaurosPrivateAgent - DibTauroS Framework"}

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("TAUROS_HOST", "127.0.0.1")
    port = int(os.getenv("TAUROS_PORT", "8788"))

    print(f"Starting TaurosPrivateAgent web server on {host}:{port}")
    print("Framework: DibTauroS/Ordo-ab-Chao")
    print("Owner: Dib Anouar")
    print("License: LUP v1.0")

    uvicorn.run(app, host=host, port=port, log_level="info")
