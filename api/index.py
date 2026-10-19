# -*- coding: utf-8 -*-
"""
Vercel Serverless Function entrypoint for ALL-TIME XI FastAPI backend.
"""
import os
import sys
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Signal Vercel environment
os.environ["VERCEL"] = "1"

from server.app import app
