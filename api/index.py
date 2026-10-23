# -*- coding: utf-8 -*-
"""
Vercel Serverless Function Entrypoint for ALL-TIME XI.
Exposes top-level 'app' and 'handler' for Vercel Python runtime.
Handles Vercel URL rewrite path mapping and exception reporting.
"""
import os
import sys
import traceback
from pathlib import Path

# Setup paths
CUR_DIR = Path(__file__).resolve().parent
ROOT_DIR = CUR_DIR.parent

for p in [str(CUR_DIR), str(ROOT_DIR), str(CUR_DIR / "server"), str(ROOT_DIR / "server"), "/var/task", "/var/task/api"]:
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ["VERCEL"] = "1"

# Explicit top-level imports for Vercel AST analysis
try:
    from api.server.app import app
except Exception:
    from server.app import app

from fastapi import Request, Response
from fastapi.responses import JSONResponse

@app.middleware("http")
async def vercel_middleware(request: Request, call_next):
    # Restore original path from Vercel rewrite headers
    current_path = request.scope.get("path", "/")
    function_paths = ("/api/index", "/api/index.py")
    if current_path.rstrip("/") in (p.rstrip("/") for p in function_paths) or current_path in function_paths:
        for hdr in ["x-forwarded-uri", "x-original-url", "x-invoke-path", "x-matched-path"]:
            val = request.headers.get(hdr)
            if val and val.startswith("/"):
                candidate = val.split("?")[0]
                if not candidate.rstrip("/") in (p.rstrip("/") for p in function_paths):
                    request.scope["path"] = candidate
                    if "raw_path" in request.scope:
                        request.scope["raw_path"] = candidate.encode()
                    break

    try:
        return await call_next(request)
    except Exception:
        return Response(
            f"VERCEL RUNTIME EXCEPTION:\n{traceback.format_exc()}",
            status_code=500,
            media_type="text/plain"
        )

handler = app
