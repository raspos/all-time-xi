# -*- coding: utf-8 -*-
"""
Vercel Serverless Function Entrypoint for ALL-TIME XI.
Routes requests cleanly using _route query parameter restoration.
"""
import os
import sys
import traceback
from pathlib import Path
from fastapi import FastAPI, Request, Response

CUR_DIR = Path(__file__).resolve().parent
ROOT_DIR = CUR_DIR.parent
for p in [str(CUR_DIR), str(ROOT_DIR), str(CUR_DIR / "server"), str(ROOT_DIR / "server"), "/var/task", "/var/task/api"]:
    if p not in sys.path:
        sys.path.insert(0, p)

import_error = None
backend_app = None

try:
    from api.server.app import app as _backend
    backend_app = _backend
except Exception:
    err1 = traceback.format_exc()
    try:
        from server.app import app as _backend
        backend_app = _backend
    except Exception:
        err2 = traceback.format_exc()
        import_error = f"Primary:\n{err1}\n\nFallback:\n{err2}"

app = FastAPI(title="ALL-TIME XI API")

@app.middleware("http")
async def vercel_route_restore_middleware(request: Request, call_next):
    route = request.query_params.get("_route")
    if route:
        if route.startswith(("api/", "team/", "match/")):
            restored_path = f"/{route}"
        else:
            restored_path = f"/api/{route}"
        request.scope["path"] = restored_path
        if "raw_path" in request.scope:
            request.scope["raw_path"] = restored_path.encode()

    try:
        return await call_next(request)
    except Exception:
        return Response(
            f"BACKEND RUNTIME ERROR:\n{traceback.format_exc()}",
            status_code=500,
            media_type="text/plain"
        )

if backend_app is not None:
    app.mount("/", backend_app)
else:
    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    def import_failure_fallback(full_path: str):
        return Response(
            f"BACKEND IMPORT FAILED:\n{import_error}",
            status_code=500,
            media_type="text/plain"
        )

handler = app
