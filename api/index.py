# -*- coding: utf-8 -*-
"""
Vercel Serverless Function Entrypoint for ALL-TIME XI.
Guaranteed bulletproof startup with lazy/resilient backend mounting
and full diagnostic reporting.
"""
import os
import sys
import traceback
from pathlib import Path
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

CUR_DIR = Path(__file__).resolve().parent
ROOT_DIR = CUR_DIR.parent
for p in [str(CUR_DIR), str(ROOT_DIR), str(CUR_DIR / "server"), str(ROOT_DIR / "server"), "/var/task", "/var/task/api"]:
    if p not in sys.path:
        sys.path.insert(0, p)

app = FastAPI(title="ALL-TIME XI API")

backend_app = None
import_error = None

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
        import_error = f"Primary Import Error:\n{err1}\n\nFallback Import Error:\n{err2}"

@app.middleware("http")
async def vercel_path_rewrite_middleware(request: Request, call_next):
    current_path = request.scope.get("path", "/")
    function_prefixes = ("/api/index", "/api/index.py")
    if current_path in ("/api", "/api/") or any(current_path.startswith(p) for p in function_prefixes):
        for hdr in ["x-forwarded-uri", "x-original-url", "x-invoke-path", "x-matched-path"]:
            val = request.headers.get(hdr)
            if val and val.startswith("/"):
                candidate = val.split("?")[0]
                if not any(candidate.startswith(p) for p in function_prefixes):
                    request.scope["path"] = candidate
                    if "raw_path" in request.scope:
                        request.scope["raw_path"] = candidate.encode()
                    break
    return await call_next(request)

@app.get("/api/ping")
def ping():
    files = []
    if Path("/var/task").exists():
        files = [str(p) for p in Path("/var/task").rglob("*")][:80]
    return {
        "status": "ok",
        "has_backend": backend_app is not None,
        "import_error": import_error,
        "files_count": len(files),
        "files_preview": files[:30]
    }

if backend_app is not None:
    app.mount("/", backend_app)
else:
    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    def catch_all_error(full_path: str):
        return Response(
            f"BACKEND INITIALIZATION FAILED:\n{import_error}",
            status_code=500,
            media_type="text/plain"
        )

handler = app
