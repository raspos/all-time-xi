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

for p in [str(CUR_DIR), str(ROOT_DIR), "/var/task", "/var/task/api"]:
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ["VERCEL"] = "1"

init_error = None
try:
    try:
        from server.app import app as _app
    except Exception as e1:
        try:
            from api.server.app import app as _app
        except Exception as e2:
            raise RuntimeError(f"server.app fail: {e1}\napi.server.app fail: {e2}\nTraceback:\n{traceback.format_exc()}")
    app = _app
except Exception:
    init_error = traceback.format_exc()
    from fastapi import FastAPI, Response
    app = FastAPI()

    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    def show_init_error(path: str):
        return Response(f"VERCEL STARTUP EXCEPTION:\n{init_error}", status_code=500, media_type="text/plain")

if init_error is None:
    from fastapi import Request, Response
    from fastapi.responses import JSONResponse

    @app.middleware("http")
    async def vercel_middleware(request: Request, call_next):
        # 1. Restore original path from Vercel rewrite headers if rewritten
        for hdr in ["x-matched-path", "x-invoke-path", "x-forwarded-uri", "x-original-url"]:
            val = request.headers.get(hdr)
            if val and val.startswith("/") and not val.startswith("/api/index"):
                clean_path = val.split("?")[0]
                request.scope["path"] = clean_path
                break

        # 2. Diagnostic endpoint: if x-debug header is 1
        if request.headers.get("x-debug") == "1":
            return JSONResponse({
                "scope_path": request.scope.get("path"),
                "url_path": request.url.path,
                "headers": dict(request.headers),
                "matched_path": request.headers.get("x-matched-path"),
                "routes": [r.path for r in app.routes if hasattr(r, "path")]
            })

        try:
            return await call_next(request)
        except Exception:
            return Response(
                f"VERCEL RUNTIME EXCEPTION:\n{traceback.format_exc()}",
                status_code=500,
                media_type="text/plain"
            )

handler = app
