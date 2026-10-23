# -*- coding: utf-8 -*-
"""
Vercel Serverless Function Entrypoint for ALL-TIME XI.
Directly instantiates top-level 'app = FastAPI()' for Vercel AST analysis.
Mounts full backend FastAPI application.
"""
import os
import sys
from pathlib import Path
from fastapi import FastAPI, Request, Response

CUR_DIR = Path(__file__).resolve().parent
ROOT_DIR = CUR_DIR.parent
for p in [str(CUR_DIR), str(ROOT_DIR), str(CUR_DIR / "server"), str(ROOT_DIR / "server"), "/var/task", "/var/task/api"]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from api.server.app import app as backend_app
except ImportError:
    from server.app import app as backend_app

app = FastAPI(title="ALL-TIME XI API")

@app.middleware("http")
async def vercel_path_rewrite_middleware(request: Request, call_next):
    current_path = request.scope.get("path", "/")
    function_prefixes = ("/api/index", "/api/index.py")
    if current_path == "/api" or current_path == "/api/" or any(current_path.startswith(p) for p in function_prefixes):
        for hdr in ["x-forwarded-uri", "x-original-url", "x-invoke-path", "x-matched-path"]:
            val = request.headers.get(hdr)
            if val and val.startswith("/"):
                candidate = val.split("?")[0]
                if not any(candidate.startswith(p) for p in function_prefixes):
                    request.scope["path"] = candidate
                    if "raw_path" in request.scope:
                        request.scope["raw_path"] = candidate.encode()
                    break

    try:
        return await call_next(request)
    except Exception:
        import traceback
        return Response(
            f"VERCEL RUNTIME ERROR:\n{traceback.format_exc()}",
            status_code=500,
            media_type="text/plain"
        )

app.mount("/", backend_app)
handler = app
