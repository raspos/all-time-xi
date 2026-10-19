# -*- coding: utf-8 -*-
"""
Vercel Serverless Function Entrypoint for ALL-TIME XI.
Exposes top-level 'app' and 'handler' for Vercel Python runtime.
Includes full traceback reporting for zero-mystery debugging.
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
    @app.middleware("http")
    async def vercel_exception_reporter(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            return Response(
                f"VERCEL RUNTIME EXCEPTION:\n{traceback.format_exc()}",
                status_code=500,
                media_type="text/plain"
            )

handler = app
