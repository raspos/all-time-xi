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
        # Restore original path when Vercel sets scope["path"] to the function path
        # (e.g. /api/index instead of the original /api/bootstrap).
        # Try every header Vercel may send, preferring ones that look like the original URL.
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

        # Diagnostic endpoint
        if request.headers.get("x-debug") == "1":
            return JSONResponse({
                "scope_path": request.scope.get("path"),
                "url_path": str(request.url),
                "headers": dict(request.headers),
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

if init_error is None:
    from fastapi import Request as _Req
    from fastapi.responses import JSONResponse as _JSON

    @app.get("/__health")
    async def health_check(req: _Req):
        return _JSON({
            "ok": True,
            "commit": "c99f802",
            "scope_path": req.scope.get("path"),
            "url": str(req.url),
            "headers": {k: v for k, v in req.headers.items() if k.startswith("x-")},
        })

handler = app
