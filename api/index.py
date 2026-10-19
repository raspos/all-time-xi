# -*- coding: utf-8 -*-
"""
Vercel Serverless Function Entrypoint for ALL-TIME XI.
"""
import os
import sys
import traceback
from pathlib import Path

# Add possible root directories to sys.path
CUR_DIR = Path(__file__).resolve().parent
ROOT_DIR = CUR_DIR.parent

for p in [str(CUR_DIR), str(ROOT_DIR), "/var/task", "/var/task/api"]:
    if p not in sys.path and os.path.exists(p):
        sys.path.insert(0, p)

os.environ["VERCEL"] = "1"

try:
    try:
        from server.app import app
    except ImportError:
        from api.server.app import app
except Exception:
    err_tb = traceback.format_exc()
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse

    app = FastAPI(title="ALL-TIME XI Vercel Error")

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
    def debug_error(full_path: str):
        return HTMLResponse(
            f"<html><head><title>Vercel Startup Error</title></head>"
            f"<body style='font-family:monospace;padding:2rem;background:#090d16;color:#f87171;'>"
            f"<h2 style='color:#ef4444;'>Vercel Serverless Function Startup Error</h2>"
            f"<pre style='background:#1e293b;color:#f1f5f9;padding:1.5rem;border-radius:12px;overflow:auto;'>{err_tb}</pre>"
            f"<p style='color:#94a3b8;font-size:12px;'>sys.path: {sys.path}</p>"
            f"</body></html>",
            status_code=500
        )
