# -*- coding: utf-8 -*-
"""
Vercel Serverless Function Entrypoint for ALL-TIME XI.
Exposes top-level 'app' and 'handler' for Vercel Python runtime.
"""
import os
import sys
from pathlib import Path

# Setup paths
CUR_DIR = Path(__file__).resolve().parent
ROOT_DIR = CUR_DIR.parent

for p in [str(CUR_DIR), str(ROOT_DIR), "/var/task", "/var/task/api"]:
    if p not in sys.path:
        sys.path.insert(0, p)

os.environ["VERCEL"] = "1"

try:
    from server.app import app as _app
except ImportError:
    from api.server.app import app as _app

# Explicit top-level assignments required by Vercel static AST parser
app = _app
handler = app
