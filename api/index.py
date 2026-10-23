# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from fastapi import FastAPI, Request

CUR_DIR = Path(__file__).resolve().parent
ROOT_DIR = CUR_DIR.parent
for p in [str(CUR_DIR), str(ROOT_DIR), str(CUR_DIR / "server"), str(ROOT_DIR / "server"), "/var/task", "/var/task/api"]:
    if p not in sys.path:
        sys.path.insert(0, p)

app = FastAPI()

@app.api_route("/{full_path:path}", methods=["GET", "POST"])
def catch_debug(request: Request, full_path: str):
    return {
        "scope_path": request.scope.get("path"),
        "full_path": full_path,
        "headers": dict(request.headers)
    }
