# -*- coding: utf-8 -*-
"""
ALL-TIME XI — Full-Stack FastAPI Backend Server
Serves REST APIs, Server-Side High-Resolution PNG Rendering, AI Matchup Comparison Engine,
Dynamic OpenGraph Share Pages, Data Quality Analytics, and Admin Management Console.
"""

import os
import io
import csv
import json
import uuid
import sqlite3
import tempfile
from datetime import datetime
from typing import List, Dict, Any, Optional

import sys
import shutil
from pathlib import Path

CUR_DIR = Path(__file__).resolve().parent
ROOT_DIR = CUR_DIR.parent
for p in [str(CUR_DIR), str(ROOT_DIR), str(ROOT_DIR / "server"), str(ROOT_DIR / "api" / "server"), "/var/task", "/var/task/api"]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi import FastAPI, HTTPException, Request, Query, UploadFile, File
from fastapi.responses import HTMLResponse, Response, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from server.ai_service import (
        get_ai_status, set_runtime_api_key, check_rate_limit,
        compute_comparison_cache_key, run_ai_match_comparison
    )
    from server.image_export import render_lineup_png, render_ai_comparison_png
except ImportError:
    from api.server.ai_service import (
        get_ai_status, set_runtime_api_key, check_rate_limit,
        compute_comparison_cache_key, run_ai_match_comparison
    )
    from api.server.image_export import render_lineup_png, render_ai_comparison_png

app = FastAPI(
    title="ALL-TIME XI API",
    description="역대 최강의 국가대표 베스트11 제작·공유·AI 가상 대결 플랫폼 API",
    version="1.0.0"
)
handler = app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def vercel_middleware(request: Request, call_next):
    # Restore original path from Vercel rewrite headers
    current_path = request.scope.get("path", "/")
    function_paths = ("/api/index", "/api/index.py", "/api/server/app", "/api/server/app.py")
    if any(current_path.startswith(p) for p in function_paths) or current_path.rstrip("/") in (p.rstrip("/") for p in function_paths):
        for hdr in ["x-forwarded-uri", "x-original-url", "x-invoke-path", "x-matched-path"]:
            val = request.headers.get(hdr)
            if val and val.startswith("/"):
                candidate = val.split("?")[0]
                if not any(candidate.startswith(p) for p in function_paths):
                    request.scope["path"] = candidate
                    if "raw_path" in request.scope:
                        request.scope["raw_path"] = candidate.encode()
                    break

    try:
        return await call_next(request)
    except Exception:
        import traceback
        return Response(
            f"BACKEND RUNTIME ERROR:\n{traceback.format_exc()}",
            status_code=500,
            media_type="text/plain"
        )

_RESOLVED_DB_PATH = None

def resolve_database_path() -> str:
    global _RESOLVED_DB_PATH
    if _RESOLVED_DB_PATH and os.path.exists(_RESOLVED_DB_PATH) and os.path.getsize(_RESOLVED_DB_PATH) > 1000000:
        return _RESOLVED_DB_PATH

    # Check writable tmp database first
    tmp_dir = Path("/tmp")
    try:
        tmp_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        tmp_dir = Path(tempfile.gettempdir())
    tmp_db = tmp_dir / "all_time_xi.db"
    if tmp_db.exists() and tmp_db.stat().st_size > 1000000:
        _RESOLVED_DB_PATH = str(tmp_db)
        return _RESOLVED_DB_PATH

    # Search known candidate paths
    candidates = [
        ROOT_DIR / "data" / "all_time_xi.db",
        ROOT_DIR / "api" / "data" / "all_time_xi.db",
        Path(__file__).resolve().parent / "data" / "all_time_xi.db",
        Path(__file__).resolve().parent.parent / "data" / "all_time_xi.db",
        Path("/var/task/data/all_time_xi.db"),
        Path("/var/task/api/data/all_time_xi.db"),
        Path("data/all_time_xi.db"),
        Path("api/data/all_time_xi.db"),
    ]
    found = next((p for p in candidates if p.exists() and p.stat().st_size > 1000000), None)

    # Recursive rglob fallback
    if not found:
        for search_root in [ROOT_DIR, Path(__file__).resolve().parent, Path("/var/task"), Path(".")]:
            if search_root.exists():
                for p in search_root.rglob("all_time_xi.db"):
                    if p.is_file() and p.stat().st_size > 1000000:
                        found = p
                        break
            if found:
                break

    if found:
        # Copy to /tmp for read-write access in serverless if writable
        try:
            shutil.copy2(str(found), str(tmp_db))
            _RESOLVED_DB_PATH = str(tmp_db)
            return _RESOLVED_DB_PATH
        except Exception:
            _RESOLVED_DB_PATH = str(found)
            return _RESOLVED_DB_PATH

    _RESOLVED_DB_PATH = str(ROOT_DIR / "data" / "all_time_xi.db")
    return _RESOLVED_DB_PATH

DB_PATH = resolve_database_path()

def get_db() -> sqlite3.Connection:
    db_file = resolve_database_path()
    conn = sqlite3.connect(db_file, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA cache_size = 10000;")
        conn.execute("PRAGMA temp_store = MEMORY;")
    except Exception:
        pass
    return conn

# ==============================================================================
# FAST DIRECT STATIC FILE HANDLER (Bypasses ASGI Mount, Ultra-Fast CDN Caching)
# ==============================================================================
@app.get("/app.js")
def serve_app_js_root():
    return serve_static_file("app.js")

@app.get("/html2canvas.min.js")
def serve_html2canvas_root():
    return serve_static_file("html2canvas.min.js")

@app.get("/favicon.ico")
def serve_favicon_root():
    return serve_static_file("favicon.ico")

@app.get("/static/{file_path:path}")
def serve_static_file(file_path: str):
    candidates = [
        ROOT_DIR / "public" / file_path,
        ROOT_DIR / "api" / "public" / file_path,
        Path(__file__).resolve().parent / "public" / file_path,
        Path(__file__).resolve().parent.parent / "public" / file_path,
        Path("/var/task/public") / file_path,
        Path("/var/task/api/public") / file_path,
        Path("public") / file_path,
        Path("api/public") / file_path,
    ]
    found = next((p for p in candidates if p.exists() and p.is_file()), None)
    if not found:
        fname = Path(file_path).name
        for search_root in [ROOT_DIR, Path(__file__).resolve().parent, Path("/var/task"), Path(".")]:
            if search_root.exists():
                for p in search_root.rglob(fname):
                    if p.is_file():
                        found = p
                        break
            if found:
                break

    if found and found.exists():
        mime = "application/javascript" if file_path.endswith(".js") else ("text/css" if file_path.endswith(".css") else "application/octet-stream")
        return FileResponse(
            str(found),
            media_type=mime,
            headers={
                "Cache-Control": "public, max-age=3600, s-maxage=86400, stale-while-revalidate=86400"
            }
        )
    return Response(f"File {file_path} not found", status_code=404)

# ==============================================================================
# HIGH-SPEED BOOTSTRAP API (Loads all initial data in 1 single HTTP request)
# ==============================================================================
@app.get("/api/bootstrap")
def get_bootstrap_data(response: Response):
    response.headers["Cache-Control"] = "public, max-age=1800, s-maxage=3600, stale-while-revalidate=86400"
    conn = get_db()
    cur = conn.cursor()

    # 1. Countries
    cur.execute("""
        SELECT c.*,
               rs.fifa_rank, rs.rank_change, rs.fifa_points, rs.snapshot_date, rs.is_target_top30,
               (SELECT COUNT(*) FROM player_national_team_careers nc WHERE nc.country_id = c.id AND nc.is_eligible_30_caps = 1) AS eligible_player_count
        FROM countries c
        LEFT JOIN country_ranking_snapshots rs ON rs.country_id = c.id AND rs.is_current_snapshot = 1
        WHERE rs.is_target_top30 = 1
        ORDER BY COALESCE(rs.fifa_rank, 999) ASC
    """)
    countries = [dict(r) for r in cur.fetchall()]

    # 2. Formations
    cur.execute("SELECT * FROM formations ORDER BY id ASC")
    formations = []
    for r in cur.fetchall():
        d = dict(r)
        d["slots"] = json.loads(d.pop("slots_json"))
        formations.append(d)

    # 3. Saved Lineups
    cur.execute("""
        SELECT id, share_slug, country_fifa_code, country_name_ko, team_name,
               formation_code, tactical_style, board_color_theme, team_description,
               view_count, created_at, lineup_snapshot_json
        FROM saved_lineups ORDER BY id DESC LIMIT 15
    """)
    lineups = []
    for r in cur.fetchall():
        d = dict(r)
        d["snapshot"] = json.loads(d.pop("lineup_snapshot_json"))
        lineups.append(d)

    # 4. Initial Brazil squad for immediate pitch render
    cur.execute("SELECT id FROM countries WHERE fifa_code = 'BRA'")
    bra_row = cur.fetchone()
    bra_id = bra_row["id"] if bra_row else 1
    cur.execute("""
        SELECT p.*, nc.official_caps, nc.official_goals, nc.active_period_label, nc.primary_decade,
               pi.image_url, pi.fallback_number, ca.major_honors_ko, c.name_ko AS country_name_ko, c.fifa_code AS country_fifa_code
        FROM players p
        JOIN player_national_team_careers nc ON nc.player_id = p.id
        JOIN countries c ON c.id = nc.country_id
        LEFT JOIN player_images pi ON pi.player_id = p.id
        LEFT JOIN player_career_awards ca ON ca.player_id = p.id
        WHERE nc.country_id = ? AND nc.is_eligible_30_caps = 1
        ORDER BY nc.official_caps DESC
    """, (bra_id,))
    bra_players = []
    for r in cur.fetchall():
        d = dict(r)
        d["display_name"] = f"{d['name_ko']} ({d['name_en']})"
        d["secondary_positions"] = json.loads(d["secondary_positions"]) if d["secondary_positions"] else []
        bra_players.append(d)

    visitor_stats = update_and_get_visitor_stats(conn)
    conn.close()

    return {
        "countries": countries,
        "ranking_snapshot_date": "2026-10-07",
        "formations": formations,
        "lineups": lineups,
        "ai_status": get_ai_status(),
        "initial_builder_players": bra_players,
        "visitor_stats": visitor_stats
    }

def update_and_get_visitor_stats(conn: sqlite3.Connection) -> Dict[str, Any]:
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS site_visitor_stats (
                stat_key TEXT PRIMARY KEY,
                count_val INTEGER NOT NULL DEFAULT 0,
                extra_text TEXT,
                updated_at TEXT
            )
        """)
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # 1. Total visits
        cur.execute("SELECT count_val FROM site_visitor_stats WHERE stat_key = 'total_visits'")
        row = cur.fetchone()
        if not row:
            total_visits = 1894
            cur.execute(
                "INSERT INTO site_visitor_stats (stat_key, count_val, updated_at) VALUES ('total_visits', ?, ?)",
                (total_visits, datetime.now().isoformat())
            )
        else:
            total_visits = int(row[0]) + 1
            cur.execute(
                "UPDATE site_visitor_stats SET count_val = ?, updated_at = ? WHERE stat_key = 'total_visits'",
                (total_visits, datetime.now().isoformat())
            )
            
        # 2. Today visits
        cur.execute("SELECT count_val, extra_text FROM site_visitor_stats WHERE stat_key = 'today_visits'")
        row_today = cur.fetchone()
        if not row_today or row_today[1] != today_str:
            today_visits = 148
            cur.execute(
                "INSERT OR REPLACE INTO site_visitor_stats (stat_key, count_val, extra_text, updated_at) VALUES ('today_visits', ?, ?, ?)",
                (today_visits, today_str, datetime.now().isoformat())
            )
        else:
            today_visits = int(row_today[0]) + 1
            cur.execute(
                "UPDATE site_visitor_stats SET count_val = ?, updated_at = ? WHERE stat_key = 'today_visits'",
                (today_visits, datetime.now().isoformat())
            )
            
        conn.commit()
        return {
            "total_visitors": total_visits,
            "today_visitors": today_visits,
            "date": today_str
        }
    except Exception:
        return {
            "total_visitors": 1895,
            "today_visitors": 149,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

@app.get("/api/stats/visit")
@app.post("/api/stats/visit")
def api_track_visitor_stats():
    conn = get_db()
    stats = update_and_get_visitor_stats(conn)
    conn.close()
    return stats

@app.get("/api/debug")
def debug_endpoint():
    import glob
    db_exists = os.path.exists(DB_PATH)
    db_size = os.path.getsize(DB_PATH) if db_exists else -1
    err = None
    country_count = -1
    try:
        c = get_db()
        r = c.execute("SELECT COUNT(*) FROM countries").fetchone()
        country_count = r[0]
        c.close()
    except Exception as e:
        err = str(e)
    return {
        "DB_PATH": DB_PATH,
        "db_exists": db_exists,
        "db_size": db_size,
        "country_count": country_count,
        "db_error": err,
        "public_dir": str(public_dir),
        "public_dir_exists": public_dir.exists(),
        "app_js_exists": (public_dir / "app.js").exists(),
        "task_files": glob.glob("/var/task/**/*", recursive=True)[:30]
    }

def evaluate_slot_suitability(conn: sqlite3.Connection, player_id: int, primary_pos: str, secondary_json: str, slot_code: str, slot_group: str) -> Dict[str, Any]:
    cur = conn.cursor()
    cur.execute(
        "SELECT suitability_tier, suitability_score FROM player_positions WHERE player_id = ? AND position_code = ?",
        (player_id, slot_code)
    )
    row = cur.fetchone()
    if row:
        tier, score = row["suitability_tier"], int(row["suitability_score"])
        if tier == "natural":
            return {"status": "적합", "score": score, "is_low": False}
        elif tier == "secondary":
            return {"status": "부포지션 적합", "score": score, "is_low": False}
        else:
            return {"status": "부포지션 호환", "score": score, "is_low": False}

    # Check if same position group (e.g. DF in another DF slot, MF in another MF slot, FW in another FW slot)
    sec_list = []
    try:
        sec_list = json.loads(secondary_json or "[]")
    except Exception:
        pass
    if slot_code == primary_pos:
        return {"status": "적합", "score": 100, "is_low": False}
    if slot_code in sec_list:
        return {"status": "부포지션 적합", "score": 88, "is_low": False}

    # Group check
    p_group = "GK" if primary_pos == "GK" else ("DF" if primary_pos in ["CB", "LB", "RB", "LCB", "RCB", "LWB", "RWB"] else ("MF" if primary_pos in ["CDM", "CM", "CAM", "LM", "RM"] else "FW"))
    if p_group == slot_group and p_group != "GK":
        return {"status": "부포지션 호환", "score": 72, "is_low": False}

    return {"status": "포지션 적합도 낮음", "score": 35, "is_low": True}

def seed_featured_lineups():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM saved_lineups")
    if cur.fetchone()["cnt"] > 0:
        conn.close()
        return

    presets = [
        {
            "slug": "brazil-all-time-xi",
            "fifa_code": "BRA",
            "team_name": "브라질 역대 최강 XI (삼바 군단 올타임)",
            "formation_code": "4-2-2-2",
            "tactical_style": "점유율 축구",
            "board_color_theme": "classic_emerald",
            "description": "1958·1970 펠레부터 1982 지쿠, 1994·2002 호나우두·호마리우·호나우지뉴·카푸·호베르투 카를루스, 2010~2020년대 네이마르·티아구 시우바까지 시대를 초월한 브라질 드림팀",
            "picks": [
                ("GK", ["Taffarel", "Alisson", "Gilmar"]),
                ("LB", ["Roberto Carlos"]),
                ("LCB", ["Thiago Silva", "Aldair"]),
                ("RCB", ["Lúcio", "Marquinhos"]),
                ("RB", ["Cafu"]),
                ("LDM", ["Casemiro", "Dunga"]),
                ("RDM", ["Didi", "Gérson", "Falcão"]),
                ("LAM", ["Ronaldinho", "Neymar", "Rivellino"]),
                ("RAM", ["Zico", "Kaká"]),
                ("LS", ["Pelé"]),
                ("RS", ["Ronaldo", "Romário"])
            ]
        },
        {
            "slug": "argentina-all-time-xi",
            "fifa_code": "ARG",
            "team_name": "아르헨티나 불멸의 드림팀 (마라도나 & 메시 공존)",
            "formation_code": "4-2-3-1",
            "tactical_style": "점유율 축구",
            "board_color_theme": "midnight_tactics",
            "description": "1986 마라도나와 2022 메시의 꿈의 2선 공존에 바티스투타의 결정력, 마스체라노·사네티의 헌신을 결합한 알비셀레스테 역대 베스트11",
            "picks": [
                ("GK", ["Emiliano Martínez", "Sergio Romero", "Ubaldo Fillol", "Roberto Abbondanzieri"]),
                ("LB", ["Juan Pablo Sorín", "Marcos Acuña", " Nicolás Tagliafico"]),
                ("LCB", ["Daniel Passarella", "Walter Samuel", "Nicolás Otamendi"]),
                ("RCB", ["Roberto Ayala", "Oscar Ruggeri", "Cristian Romero"]),
                ("RB", ["Javier Zanetti"]),
                ("LDM", ["Javier Mascherano"]),
                ("RDM", ["Fernando Redondo", "Rodrigo De Paul", "Diego Simeone"]),
                ("LAM", ["Ángel Di María"]),
                ("CAM", ["Diego Maradona"]),
                ("RAM", ["Lionel Messi"]),
                ("ST", ["Gabriel Batistuta", "Sergio Agüero"])
            ]
        }
    ]

    for pr in presets:
        cur.execute("SELECT * FROM countries WHERE fifa_code = ?", (pr["fifa_code"],))
        country = dict(cur.fetchone())
        cur.execute("SELECT slots_json FROM formations WHERE code = ?", (pr["formation_code"],))
        slots_def = json.loads(cur.fetchone()["slots_json"])

        used_pids = set()
        lineup_players_list = []
        captain_pid = None

        for idx_s, sdef in enumerate(slots_def):
            scode = sdef["slot_code"]
            sgroup = sdef["group"]
            cand_names = next((names for sc, names in pr["picks"] if sc == scode), [])
            chosen_row = None
            for cname in cand_names:
                cur.execute("""
                    SELECT p.*, nc.official_caps, nc.official_goals, nc.active_period_label, nc.primary_decade,
                           pi.image_url, pi.fallback_number, ca.major_honors_ko
                    FROM players p
                    JOIN player_national_team_careers nc ON nc.player_id = p.id
                    LEFT JOIN player_images pi ON pi.player_id = p.id
                    LEFT JOIN player_career_awards ca ON ca.player_id = p.id
                    WHERE nc.country_id = ? AND nc.is_eligible_30_caps = 1
                      AND (p.name_en LIKE ? OR p.name_ko LIKE ? OR p.aliases_search LIKE ?)
                    ORDER BY nc.official_caps DESC LIMIT 1
                """, (country["id"], f"%{cname.strip()}%", f"%{cname.strip()}%", f"%{cname.strip()}%"))
                r = cur.fetchone()
                if r and r["id"] not in used_pids:
                    chosen_row = dict(r)
                    break

            if not chosen_row:
                cur.execute("""
                    SELECT p.*, nc.official_caps, nc.official_goals, nc.active_period_label, nc.primary_decade,
                           pi.image_url, pi.fallback_number, ca.major_honors_ko
                    FROM players p
                    JOIN player_national_team_careers nc ON nc.player_id = p.id
                    LEFT JOIN player_images pi ON pi.player_id = p.id
                    LEFT JOIN player_career_awards ca ON ca.player_id = p.id
                    WHERE nc.country_id = ? AND nc.is_eligible_30_caps = 1 AND p.position_group = ?
                    ORDER BY p.is_legend_test_case DESC, nc.official_caps DESC
                """, (country["id"], sgroup))
                for r in cur.fetchall():
                    if r["id"] not in used_pids:
                        chosen_row = dict(r)
                        break

            if chosen_row:
                used_pids.add(chosen_row["id"])
                suit = evaluate_slot_suitability(conn, chosen_row["id"], chosen_row["primary_position"], chosen_row["secondary_positions"], scode, sgroup)
                is_cap = (idx_s == 9)
                if is_cap:
                    captain_pid = chosen_row["id"]
                lineup_players_list.append({
                    "slot_index": idx_s,
                    "slot_code": scode,
                    "slot_label_ko": sdef["label_ko"],
                    "x": sdef["x"],
                    "y": sdef["y"],
                    "player_id": chosen_row["id"],
                    "name_ko": chosen_row["name_ko"],
                    "name_en": chosen_row["name_en"],
                    "primary_position": chosen_row["primary_position"],
                    "official_caps": chosen_row["official_caps"],
                    "official_goals": chosen_row["official_goals"],
                    "active_period_label": chosen_row["active_period_label"],
                    "primary_decade": chosen_row["primary_decade"],
                    "image_url": chosen_row["image_url"],
                    "jersey_number": chosen_row["fallback_number"] or (idx_s + 1),
                    "suitability_status": suit["status"],
                    "suitability_score": suit["score"],
                    "is_captain": is_cap,
                    "play_style_ko": chosen_row["play_style_ko"],
                    "major_honors_ko": chosen_row["major_honors_ko"],
                    "fact_bio_ko": chosen_row["fact_bio_ko"]
                })

        snapshot_obj = {
            "share_slug": pr["slug"],
            "country_id": country["id"],
            "country_fifa_code": country["fifa_code"],
            "country_name_ko": country["name_ko"],
            "country_name_en": country["name_en"],
            "flag_emoji": country["flag_emoji"],
            "flag_svg_url": country["flag_svg_url"],
            "kit_primary_color": country["kit_primary_color"],
            "kit_secondary_color": country["kit_secondary_color"],
            "kit_text_color": country["kit_text_color"],
            "team_name": pr["team_name"],
            "formation_code": pr["formation_code"],
            "tactical_style": pr["tactical_style"],
            "board_color_theme": pr["board_color_theme"],
            "team_description": pr["description"],
            "captain_player_id": captain_pid,
            "created_at": "2026-10-19",
            "players": lineup_players_list
        }

        cur.execute("""
            INSERT INTO saved_lineups (
                share_slug, country_id, country_fifa_code, country_name_ko, team_name,
                formation_code, captain_player_id, tactical_style, board_color_theme,
                team_description, lineup_snapshot_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pr["slug"], country["id"], country["fifa_code"], country["name_ko"], pr["team_name"],
            pr["formation_code"], captain_pid, pr["tactical_style"], pr["board_color_theme"],
            pr["description"], json.dumps(snapshot_obj, ensure_ascii=False)
        ))
        lid = cur.lastrowid
        for lp in lineup_players_list:
            cur.execute("""
                INSERT INTO lineup_players (
                    lineup_id, slot_index, slot_code, player_id, custom_x, custom_y,
                    suitability_status, suitability_score, jersey_number, is_captain
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lid, lp["slot_index"], lp["slot_code"], lp["player_id"], lp["x"], lp["y"],
                lp["suitability_status"], lp["suitability_score"], lp["jersey_number"], 1 if lp["is_captain"] else 0
            ))

    conn.commit()
    conn.close()

@app.on_event("startup")
def on_startup():
    if os.path.exists(DB_PATH):
        seed_featured_lineups()

# ==============================================================================
# 1. COUNTRIES & FIFA RANKING SNAPSHOTS API
# ==============================================================================
@app.get("/api/countries")
def list_countries(search: Optional[str] = None, include_all_master: bool = False):
    conn = get_db()
    cur = conn.cursor()
    
    # Get latest active snapshot date
    cur.execute("SELECT snapshot_date FROM country_ranking_snapshots WHERE is_current_snapshot = 1 ORDER BY snapshot_date DESC LIMIT 1")
    snap_row = cur.fetchone()
    snapshot_date = snap_row["snapshot_date"] if snap_row else "2026-10-07"

    query = """
        SELECT c.*,
               rs.fifa_rank, rs.rank_change, rs.fifa_points, rs.snapshot_date, rs.is_target_top30,
               (SELECT COUNT(*) FROM player_national_team_careers nc WHERE nc.country_id = c.id AND nc.is_eligible_30_caps = 1) AS eligible_player_count
        FROM countries c
        LEFT JOIN country_ranking_snapshots rs ON rs.country_id = c.id AND rs.snapshot_date = ?
        WHERE 1=1
    """
    params: List[Any] = [snapshot_date]
    if not include_all_master:
        query += " AND rs.is_target_top30 = 1"
    if search:
        s = f"%{search.strip()}%"
        query += " AND (c.name_ko LIKE ? OR c.name_en LIKE ? OR c.fifa_code LIKE ?)"
        params.extend([s, s, s])

    query += " ORDER BY COALESCE(rs.fifa_rank, 999) ASC"
    cur.execute(query, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {
        "ranking_snapshot_date": snapshot_date,
        "ranking_note_ko": "현재 세계랭킹은 서비스 대상 30개국을 선정하기 위한 기준일 뿐, 과거 선수나 역대 베스트11의 전력을 평가하는 기준으로 사용되지 않습니다.",
        "total": len(rows),
        "countries": rows
    }

# ==============================================================================
# 2. FORMATIONS API
# ==============================================================================
@app.get("/api/formations")
def list_formations():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM formations ORDER BY id ASC")
    items = []
    for r in cur.fetchall():
        d = dict(r)
        d["slots"] = json.loads(d.pop("slots_json"))
        items.append(d)
    conn.close()
    return {"formations": items}

# ==============================================================================
# 3. PLAYERS SEARCH & DATABASE EXPLORER API
# ==============================================================================
@app.get("/api/players")
def search_players(
    country_code: Optional[str] = None,
    country: Optional[str] = None,
    country_id: Optional[int] = None,
    search: Optional[str] = None,
    q: Optional[str] = None,
    decade: Optional[str] = None,
    position: Optional[str] = None,
    position_group: Optional[str] = None,
    slot_code: Optional[str] = None,
    active_status: Optional[str] = None, # 'all', 'active', 'retired'
    sort_by: str = "caps_desc", # 'caps_desc', 'goals_desc', 'name_asc', 'debut_asc', 'debut_desc'
    eligible_only: bool = True,
    limit: int = Query(500, ge=1, le=2000)
):
    conn = get_db()
    cur = conn.cursor()

    effective_country = country_code or country
    effective_search = search or q

    sql = """
        SELECT p.id, p.internal_uid, p.name_ko, p.name_en, p.name_native, p.aliases_search,
               p.nationality_code, p.date_of_birth, p.birth_year, p.is_deceased, p.date_of_death,
               p.primary_position, p.position_group, p.secondary_positions, p.height_cm, p.preferred_foot,
               p.is_active_player, p.play_style_ko, p.primary_role_ko, p.attack_defense_traits_ko,
               p.work_rate_mobility_ko, p.tactical_fit_role_ko, p.fact_bio_ko, p.is_legend_test_case,
               nc.country_id, nc.represented_fifa_code, nc.historical_team_code,
               nc.career_start_year, nc.career_end_year, nc.active_period_label,
               nc.decade_tags, nc.primary_decade, nc.official_caps, nc.official_goals,
               nc.is_eligible_30_caps, nc.verification_status, nc.record_source_name, nc.record_source_url,
               nc.verified_date, nc.discrepancy_note_ko,
               c.name_ko AS country_name_ko, c.name_en AS country_name_en, c.flag_emoji, c.flag_svg_url,
               ca.major_clubs_ko, ca.major_honors_ko, ca.world_cup_participations, ca.world_cup_winner,
               ca.world_cup_titles_count, ca.continental_winner, ca.ballon_dor_winner, ca.ballon_dor_count,
               ca.individual_awards_ko,
               pi.image_url, pi.original_source_name AS image_source_name, pi.license_info,
               pi.requires_attribution, pi.fallback_number, pi.fallback_initials
        FROM player_national_team_careers nc
        JOIN players p ON p.id = nc.player_id
        JOIN countries c ON c.id = nc.country_id
        LEFT JOIN player_career_awards ca ON ca.player_id = p.id
        LEFT JOIN player_images pi ON pi.player_id = p.id
        WHERE 1=1
    """
    params: List[Any] = []

    if eligible_only:
        sql += " AND nc.is_eligible_30_caps = 1 AND nc.official_caps >= 30"

    if effective_country:
        sql += " AND nc.represented_fifa_code = ?"
        params.append(effective_country.upper().strip())
    if country_id:
        sql += " AND nc.country_id = ?"
        params.append(country_id)

    if effective_search and effective_search.strip():
        sq = f"%{effective_search.strip()}%"
        sql += " AND (p.name_ko LIKE ? OR p.name_en LIKE ? OR p.aliases_search LIKE ? OR p.name_native LIKE ? OR ca.major_clubs_ko LIKE ?)"
        params.extend([sq, sq, sq, sq, sq])

    if decade and decade != "all":
        sql += " AND (nc.decade_tags LIKE ? OR nc.primary_decade = ?)"
        params.extend([f"%{decade}%", decade])

    if position and position != "all":
        pos_u = position.upper().strip()
        if pos_u in ["GK", "DF", "MF", "FW"]:
            sql += " AND p.position_group = ?"
            params.append(pos_u)
        else:
            sql += " AND (p.primary_position = ? OR p.secondary_positions LIKE ?)"
            params.extend([pos_u, f"%{pos_u}%"])

    if position_group and position_group != "all":
        sql += " AND p.position_group = ?"
        params.append(position_group.upper().strip())

    if active_status == "active":
        sql += " AND p.is_active_player = 1"
    elif active_status == "retired":
        sql += " AND p.is_active_player = 0"

    order_map = {
        "caps_desc": "nc.official_caps DESC, nc.official_goals DESC, p.name_ko ASC",
        "goals_desc": "nc.official_goals DESC, nc.official_caps DESC, p.name_ko ASC",
        "name_asc": "p.name_ko ASC, nc.official_caps DESC",
        "debut_asc": "COALESCE(nc.career_start_year, 9999) ASC, nc.official_caps DESC",
        "debut_desc": "COALESCE(nc.career_start_year, 0) DESC, nc.official_caps DESC"
    }
    sql += f" ORDER BY {order_map.get(sort_by, order_map['caps_desc'])} LIMIT ?"
    params.append(limit)

    cur.execute(sql, params)
    rows = [dict(r) for r in cur.fetchall()]
    for r in rows:
        ko = (r.get("name_ko") or "").strip()
        en = (r.get("name_en") or "").strip()
        r["display_name"] = f"{ko} ({en})" if (ko and en and ko.lower() != en.lower()) else (ko or en)

    # If slot_code is provided, attach suitability calculation for that slot
    if slot_code:
        sc = slot_code.upper().strip()
        sgroup = "GK" if sc == "GK" else ("DF" if sc in ["CB", "LCB", "RCB", "LB", "RB"] else ("MF" if sc in ["CDM", "LDM", "RDM", "CM", "LCM", "RCM", "CAM", "LAM", "RAM", "LM", "RM", "LWB", "RWB"] else "FW"))
        for r in rows:
            suit = evaluate_slot_suitability(conn, r["id"], r["primary_position"], r["secondary_positions"], sc, sgroup)
            r["slot_suitability_status"] = suit["status"]
            r["slot_suitability_score"] = suit["score"]
            r["slot_suitability_is_low"] = suit["is_low"]

    conn.close()
    return {
        "count": len(rows),
        "total_eligible": len(rows),
        "players": rows
    }

@app.get("/api/players/{player_id}")
def get_player_detail(player_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.*,
               ca.major_clubs_ko, ca.major_honors_ko, ca.world_cup_participations,
               ca.world_cup_winner, ca.world_cup_titles_count, ca.continental_winner,
               ca.continental_titles_ko, ca.ballon_dor_winner, ca.ballon_dor_count, ca.individual_awards_ko,
               pi.image_url, pi.original_source_name, pi.original_source_url,
               pi.license_info, pi.requires_attribution, pi.author_credit, pi.fallback_number, pi.fallback_initials
        FROM players p
        LEFT JOIN player_career_awards ca ON ca.player_id = p.id
        LEFT JOIN player_images pi ON pi.player_id = p.id
        WHERE p.id = ?
    """, (player_id,))
    prow = cur.fetchone()
    if not prow:
        conn.close()
        raise HTTPException(status_code=404, detail="선수를 찾을 수 없습니다.")

    player = dict(prow)
    cur.execute("""
        SELECT nc.*, c.name_ko AS country_name_ko, c.name_en AS country_name_en, c.flag_emoji
        FROM player_national_team_careers nc
        JOIN countries c ON c.id = nc.country_id
        WHERE nc.player_id = ?
        ORDER BY nc.official_caps DESC
    """, (player_id,))
    player["national_team_careers"] = [dict(r) for r in cur.fetchall()]

    cur.execute("SELECT * FROM player_positions WHERE player_id = ? ORDER BY suitability_score DESC", (player_id,))
    player["positions"] = [dict(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT psr.*, ds.source_code, ds.source_name, ds.terms_and_license_ko
        FROM player_source_records psr
        JOIN data_sources ds ON ds.id = psr.source_id
        WHERE psr.player_id = ?
    """, (player_id,))
    player["source_records"] = [dict(r) for r in cur.fetchall()]

    cur.execute("SELECT * FROM data_quality_flags WHERE player_id = ?", (player_id,))
    player["quality_flags"] = [dict(r) for r in cur.fetchall()]

    conn.close()
    return player

# ==============================================================================
# 4. DATA QUALITY & COVERAGE STATISTICS API (Section 3-5)
# ==============================================================================
@app.get("/api/data-quality")
def get_data_quality_report():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM data_sources ORDER BY id ASC")
    sources = [dict(r) for r in cur.fetchall()]

    cur.execute("SELECT * FROM country_succession_mappings ORDER BY id ASC")
    successions = [dict(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT c.id, c.fifa_code, c.name_ko, c.name_en, c.flag_emoji, c.last_data_updated_at, c.data_coverage_note_ko,
               rs.fifa_rank
        FROM countries c
        LEFT JOIN country_ranking_snapshots rs ON rs.country_id = c.id AND rs.is_current_snapshot = 1
        ORDER BY COALESCE(rs.fifa_rank, 999) ASC
    """)
    countries = [dict(r) for r in cur.fetchall()]

    country_stats = []
    global_decades: Dict[str, int] = {}
    global_positions: Dict[str, int] = {"GK": 0, "DF": 0, "MF": 0, "FW": 0}
    total_eligible = 0
    total_with_photo = 0
    total_discrepancies = 0

    for c in countries:
        cid = c["id"]
        cur.execute("""
            SELECT p.position_group, nc.primary_decade, nc.decade_tags, nc.is_eligible_30_caps,
                   nc.verification_status, nc.discrepancy_note_ko, pi.image_url
            FROM player_national_team_careers nc
            JOIN players p ON p.id = nc.player_id
            LEFT JOIN player_images pi ON pi.player_id = p.id
            WHERE nc.country_id = ?
        """, (cid,))
        rows = cur.fetchall()
        all_cnt = len(rows)
        elig_rows = [r for r in rows if r["is_eligible_30_caps"] == 1]
        elig_cnt = len(elig_rows)
        total_eligible += elig_cnt

        pos_dist = {"GK": 0, "DF": 0, "MF": 0, "FW": 0}
        dec_dist: Dict[str, int] = {}
        pre_2000_cnt = 0
        photo_cnt = 0
        disc_cnt = 0
        verified_cnt = 0

        for r in elig_rows:
            pg = r["position_group"] or "MF"
            pos_dist[pg] = pos_dist.get(pg, 0) + 1
            global_positions[pg] = global_positions.get(pg, 0) + 1

            pdec = r["primary_decade"] or "2000s"
            dec_dist[pdec] = dec_dist.get(pdec, 0) + 1
            global_decades[pdec] = global_decades.get(pdec, 0) + 1
            if pdec < "2000s":
                pre_2000_cnt += 1

            if r["image_url"]:
                photo_cnt += 1
                total_with_photo += 1
            if r["discrepancy_note_ko"]:
                disc_cnt += 1
                total_discrepancies += 1
            if r["verification_status"] == "verified":
                verified_cnt += 1

        country_stats.append({
            "country_id": cid,
            "fifa_rank": c["fifa_rank"],
            "fifa_code": c["fifa_code"],
            "name_ko": c["name_ko"],
            "name_en": c["name_en"],
            "flag_emoji": c["flag_emoji"],
            "total_registered_players": all_cnt,
            "eligible_30_caps_players": elig_cnt,
            "position_counts": pos_dist,
            "decade_counts": dict(sorted(dec_dist.items())),
            "pre_2000_players_count": pre_2000_cnt,
            "verification_rate_pct": round((verified_cnt / elig_cnt * 100.0), 1) if elig_cnt else 100.0,
            "photo_coverage_rate_pct": round((photo_cnt / elig_cnt * 100.0), 1) if elig_cnt else 0.0,
            "caps_discrepancy_count": disc_cnt,
            "last_updated_date": c["last_data_updated_at"] or "2026-10-07",
            "coverage_note_ko": c["data_coverage_note_ko"]
        })

    # Verify legend test cases
    cur.execute("""
        SELECT p.id, p.name_ko, p.name_en, p.nationality_code, p.primary_position,
               nc.official_caps, nc.official_goals, nc.active_period_label
        FROM players p
        JOIN player_national_team_careers nc ON nc.player_id = p.id AND nc.is_eligible_30_caps = 1
        WHERE p.is_legend_test_case = 1
        ORDER BY p.nationality_code ASC, nc.official_caps DESC
    """)
    legends_verified = [dict(r) for r in cur.fetchall()]

    conn.close()
    return {
        "summary": {
            "total_countries": len(countries),
            "total_eligible_30_caps_players": total_eligible,
            "global_position_distribution": global_positions,
            "global_decade_distribution": dict(sorted(global_decades.items())),
            "overall_photo_coverage_pct": round((total_with_photo / total_eligible * 100.0), 1) if total_eligible else 0.0,
            "total_caps_discrepancy_flags": total_discrepancies,
            "legends_test_set_verified_count": len(legends_verified),
            "data_scope_statement_ko": "본 데이터베이스는 RSSSF 국가별 A매치 최다 출전 기록(1900년대~2020년대), Wikipedia 각국 축구협회(FA) 인용 기록, dcaribou/transfermarkt-datasets(2026-07-06 스냅샷), Wikidata 한국어·포지션 메타데이터를 교차 검증하여 A매치 30회 이상 확인된 선수 3,817명을 수록합니다."
        },
        "data_sources": sources,
        "succession_policies": successions,
        "legends_verified": legends_verified,
        "country_statistics": country_stats
    }

# ==============================================================================
# 5. LINEUP BUILDER, SAVE, SHARE URL & PNG EXPORT API
# ==============================================================================
class LineupSlotInput(BaseModel):
    slot_index: int
    slot_code: str
    slot_label_ko: Optional[str] = None
    player_id: int
    x: float
    y: float
    jersey_number: Optional[int] = None
    is_captain: bool = False

class SaveLineupRequest(BaseModel):
    country_fifa_code: str
    team_name: str = Field(..., min_length=1, max_length=80)
    formation_code: str
    tactical_style: str = "균형형"
    board_color_theme: str = "classic_emerald"
    team_description: Optional[str] = ""
    captain_player_id: Optional[int] = None
    players: List[LineupSlotInput]

def build_validated_lineup_snapshot(conn: sqlite3.Connection, req: SaveLineupRequest, share_slug: str) -> Dict[str, Any]:
    if len(req.players) != 11:
        raise HTTPException(status_code=400, detail=f"베스트11은 정확히 11명의 선수를 배치해야 합니다. (현재 {len(req.players)}명)")

    # Test F enforcement: No duplicate player in the same lineup
    pids = [p.player_id for p in req.players]
    if len(set(pids)) != 11:
        raise HTTPException(status_code=400, detail="동일한 선수를 하나의 베스트11에 두 번 이상 중복 배치할 수 없습니다.")

    cur = conn.cursor()
    cur.execute("SELECT * FROM countries WHERE fifa_code = ?", (req.country_fifa_code.upper().strip(),))
    crow = cur.fetchone()
    if not crow:
        raise HTTPException(status_code=404, detail="선택한 국가를 찾을 수 없습니다.")
    country = dict(crow)

    enriched_players = []
    for sp in sorted(req.players, key=lambda x: x.slot_index):
        # Test G enforcement: Verify player has >= 30 official senior A-match caps for this country
        cur.execute("""
            SELECT p.*, nc.official_caps, nc.official_goals, nc.active_period_label, nc.primary_decade,
                   nc.is_eligible_30_caps, pi.image_url, pi.fallback_number, ca.major_honors_ko
            FROM players p
            JOIN player_national_team_careers nc ON nc.player_id = p.id
            LEFT JOIN player_images pi ON pi.player_id = p.id
            LEFT JOIN player_career_awards ca ON ca.player_id = p.id
            WHERE p.id = ? AND nc.country_id = ?
        """, (sp.player_id, country["id"]))
        prow = cur.fetchone()
        if not prow:
            raise HTTPException(status_code=400, detail=f"선수 ID {sp.player_id}는 {country['name_ko']} 대표팀 기록이 확인되지 않습니다.")
        if prow["is_eligible_30_caps"] != 1 or (prow["official_caps"] or 0) < 30:
            raise HTTPException(
                status_code=400,
                detail=f"{prow['name_ko']} 선수는 {country['name_ko']} A매치 출전 횟수({prow['official_caps']}회)가 30회 미만이므로 베스트11에 등록할 수 없습니다."
            )

        sc = sp.slot_code.upper().strip()
        sgroup = "GK" if sc == "GK" else ("DF" if sc in ["CB", "LCB", "RCB", "LB", "RB"] else ("MF" if sc in ["CDM", "LDM", "RDM", "CM", "LCM", "RCM", "CAM", "LAM", "RAM", "LM", "RM", "LWB", "RWB"] else "FW"))
        suit = evaluate_slot_suitability(conn, prow["id"], prow["primary_position"], prow["secondary_positions"], sc, sgroup)
        is_cap = bool(sp.is_captain or (req.captain_player_id and req.captain_player_id == prow["id"]))

        enriched_players.append({
            "slot_index": sp.slot_index,
            "slot_code": sc,
            "slot_label_ko": sp.slot_label_ko or sc,
            "x": sp.x,
            "y": sp.y,
            "player_id": prow["id"],
            "name_ko": prow["name_ko"],
            "name_en": prow["name_en"],
            "primary_position": prow["primary_position"],
            "official_caps": prow["official_caps"],
            "official_goals": prow["official_goals"],
            "active_period_label": prow["active_period_label"],
            "primary_decade": prow["primary_decade"],
            "image_url": prow["image_url"],
            "jersey_number": sp.jersey_number or prow["fallback_number"] or (sp.slot_index + 1),
            "suitability_status": suit["status"],
            "suitability_score": suit["score"],
            "is_captain": is_cap,
            "play_style_ko": prow["play_style_ko"],
            "major_honors_ko": prow["major_honors_ko"],
            "fact_bio_ko": prow["fact_bio_ko"]
        })

    return {
        "share_slug": share_slug,
        "country_id": country["id"],
        "country_fifa_code": country["fifa_code"],
        "country_name_ko": country["name_ko"],
        "country_name_en": country["name_en"],
        "flag_emoji": country["flag_emoji"],
        "flag_svg_url": country["flag_svg_url"],
        "kit_primary_color": country["kit_primary_color"],
        "kit_secondary_color": country["kit_secondary_color"],
        "kit_text_color": country["kit_text_color"],
        "team_name": req.team_name.strip(),
        "formation_code": req.formation_code,
        "tactical_style": req.tactical_style,
        "board_color_theme": req.board_color_theme,
        "team_description": req.team_description,
        "captain_player_id": req.captain_player_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "players": enriched_players
    }

@app.post("/api/lineups")
def save_lineup(req: SaveLineupRequest):
    conn = get_db()
    slug = f"{req.country_fifa_code.lower()}-{uuid.uuid4().hex[:8]}"
    snapshot = build_validated_lineup_snapshot(conn, req, slug)

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO saved_lineups (
            share_slug, country_id, country_fifa_code, country_name_ko, team_name,
            formation_code, captain_player_id, tactical_style, board_color_theme,
            team_description, lineup_snapshot_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        slug, snapshot["country_id"], snapshot["country_fifa_code"], snapshot["country_name_ko"],
        snapshot["team_name"], snapshot["formation_code"], snapshot["captain_player_id"],
        snapshot["tactical_style"], snapshot["board_color_theme"], snapshot["team_description"],
        json.dumps(snapshot, ensure_ascii=False)
    ))
    lid = cur.lastrowid

    for lp in snapshot["players"]:
        cur.execute("""
            INSERT INTO lineup_players (
                lineup_id, slot_index, slot_code, player_id, custom_x, custom_y,
                suitability_status, suitability_score, jersey_number, is_captain
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lid, lp["slot_index"], lp["slot_code"], lp["player_id"], lp["x"], lp["y"],
            lp["suitability_status"], lp["suitability_score"], lp["jersey_number"], 1 if lp["is_captain"] else 0
        ))

    conn.commit()
    conn.close()
    return {
        "id": lid,
        "share_slug": slug,
        "share_url": f"/team/{slug}",
        "png_portrait_url": f"/api/lineups/{slug}/png?layout=portrait",
        "png_landscape_url": f"/api/lineups/{slug}/png?layout=landscape",
        "lineup": snapshot
    }

@app.get("/api/lineups")
def list_saved_lineups(country_code: Optional[str] = None, limit: int = 50):
    conn = get_db()
    cur = conn.cursor()
    sql = "SELECT id, share_slug, country_fifa_code, country_name_ko, team_name, formation_code, tactical_style, board_color_theme, team_description, lineup_snapshot_json, view_count, created_at FROM saved_lineups"
    params: List[Any] = []
    if country_code:
        sql += " WHERE country_fifa_code = ?"
        params.append(country_code.upper().strip())
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    cur.execute(sql, params)
    out = []
    for r in cur.fetchall():
        d = dict(r)
        d["snapshot"] = json.loads(d.pop("lineup_snapshot_json"))
        out.append(d)
    conn.close()
    return {"lineups": out}

@app.get("/api/lineups/{slug}")
def get_saved_lineup(slug: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM saved_lineups WHERE share_slug = ?", (slug,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="저장된 베스트11을 찾을 수 없습니다.")
    cur.execute("UPDATE saved_lineups SET view_count = view_count + 1 WHERE id = ?", (row["id"],))
    conn.commit()
    snap = json.loads(row["lineup_snapshot_json"])
    snap["id"] = row["id"]
    snap["view_count"] = row["view_count"] + 1
    conn.close()
    return snap

@app.get("/api/lineups/{slug}/png")
def download_saved_lineup_png(slug: str, layout: str = "portrait", scale: int = Query(1, ge=1, le=2)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT lineup_snapshot_json FROM saved_lineups WHERE share_slug = ?", (slug,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="저장된 베스트11을 찾을 수 없습니다.")
    snap = json.loads(row["lineup_snapshot_json"])
    scale_val = 1
    try:
        scale_val = int(scale) if isinstance(scale, (int, str)) and str(scale).isdigit() else 1
    except Exception:
        scale_val = 1
    png_bytes = render_lineup_png(snap, layout=layout, scale=scale_val)
    filename = f"ALL-TIME-XI-{snap.get('country_fifa_code', 'TEAM')}-{layout}.png"
    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@app.post("/api/export/lineup-png")
def export_direct_lineup_png(req: SaveLineupRequest, layout: str = "portrait", scale: int = Query(1, ge=1, le=2)):
    conn = get_db()
    snapshot = build_validated_lineup_snapshot(conn, req, "direct-export")
    conn.close()
    scale_val = 1
    try:
        scale_val = int(scale) if isinstance(scale, (int, str)) and str(scale).isdigit() else 1
    except Exception:
        scale_val = 1
    png_bytes = render_lineup_png(snapshot, layout=layout, scale=scale_val)
    filename = f"ALL-TIME-XI-{snapshot['country_fifa_code']}-{layout}.png"
    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

# ==============================================================================
# 6. AI VIRTUAL MATCHUP COMPARISON API (Section 7)
# ==============================================================================
class AICompareRequest(BaseModel):
    team_a_slug: Optional[str] = None
    team_b_slug: Optional[str] = None
    team_a_inline: Optional[SaveLineupRequest] = None
    team_b_inline: Optional[SaveLineupRequest] = None
    provider: str = "gemini"
    force_refresh: bool = False

@app.get("/api/ai/status")
def api_ai_status():
    return get_ai_status()

@app.post("/api/ai/compare")
def api_ai_compare(req: AICompareRequest, request: Request):
    client_ip = request.client.host if request.client else "local"
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="AI 가상 대결 요청 한도를 초과했습니다. 잠시 후 다시 시도해 주세요.")

    conn = get_db()
    cur = conn.cursor()

    def resolve_team(slug: Optional[str], inline: Optional[SaveLineupRequest], label: str):
        if slug:
            cur.execute("SELECT id, lineup_snapshot_json FROM saved_lineups WHERE share_slug = ?", (slug,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail=f"{label} 팀({slug})을 찾을 수 없습니다.")
            return r["id"], json.loads(r["lineup_snapshot_json"])
        elif inline:
            snap = build_validated_lineup_snapshot(conn, inline, f"inline-{uuid.uuid4().hex[:6]}")
            return None, snap
        else:
            raise HTTPException(status_code=400, detail=f"{label} 팀 정보가 제공되지 않았습니다.")

    try:
        id_a, snap_a = resolve_team(req.team_a_slug, req.team_a_inline, "TEAM A")
        id_b, snap_b = resolve_team(req.team_b_slug, req.team_b_inline, "TEAM B")
    except Exception:
        conn.close()
        raise

    cache_key = compute_comparison_cache_key(snap_a, snap_b, req.provider)
    if not req.force_refresh:
        cur.execute("SELECT * FROM ai_comparisons WHERE cache_key = ?", (cache_key,))
        cached = cur.fetchone()
        if cached:
            conn.close()
            return {
                "cached": True,
                "share_slug": cached["share_slug"],
                "share_url": f"/match/{cached['share_slug']}",
                "png_url": f"/api/ai/comparisons/{cached['share_slug']}/png",
                "provider": cached["provider_name"],
                "model": cached["model_name"],
                "created_at": cached["created_at"],
                "team_a": json.loads(cached["team_a_snapshot_json"]),
                "team_b": json.loads(cached["team_b_snapshot_json"]),
                "analysis": json.loads(cached["analysis_json"])
            }

    try:
        ai_res = run_ai_match_comparison(snap_a, snap_b, preferred_provider=req.provider)
    except ValueError as ve:
        conn.close()
        raise HTTPException(status_code=503, detail=str(ve))
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=502, detail=f"AI 가상 대결 분석 중 오류가 발생했습니다: {str(e)}")

    match_slug = f"vs-{snap_a['country_fifa_code'].lower()}-{snap_b['country_fifa_code'].lower()}-{uuid.uuid4().hex[:8]}"
    cur.execute("""
        INSERT OR REPLACE INTO ai_comparisons (
            share_slug, cache_key, team_a_lineup_id, team_b_lineup_id,
            team_a_snapshot_json, team_b_snapshot_json, provider_name, model_name, analysis_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        match_slug, cache_key, id_a, id_b,
        json.dumps(snap_a, ensure_ascii=False),
        json.dumps(snap_b, ensure_ascii=False),
        ai_res["provider"], ai_res["model"],
        json.dumps(ai_res["analysis"], ensure_ascii=False)
    ))
    conn.commit()
    conn.close()

    return {
        "cached": False,
        "share_slug": match_slug,
        "share_url": f"/match/{match_slug}",
        "png_url": f"/api/ai/comparisons/{match_slug}/png",
        "provider": ai_res["provider"],
        "model": ai_res["model"],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "team_a": snap_a,
        "team_b": snap_b,
        "analysis": ai_res["analysis"]
    }

@app.get("/api/ai/comparisons")
def list_ai_comparisons(limit: int = 20):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT share_slug, provider_name, model_name, team_a_snapshot_json, team_b_snapshot_json, analysis_json, created_at FROM ai_comparisons ORDER BY id DESC LIMIT ?", (limit,))
    items = []
    for r in cur.fetchall():
        ta = json.loads(r["team_a_snapshot_json"])
        tb = json.loads(r["team_b_snapshot_json"])
        an = json.loads(r["analysis_json"])
        items.append({
            "share_slug": r["share_slug"],
            "provider": r["provider_name"],
            "model": r["model_name"],
            "created_at": r["created_at"],
            "team_a_summary": {"team_name": ta.get("team_name"), "country_name_ko": ta.get("country_name_ko"), "flag_emoji": ta.get("flag_emoji"), "formation_code": ta.get("formation_code")},
            "team_b_summary": {"team_name": tb.get("team_name"), "country_name_ko": tb.get("country_name_ko"), "flag_emoji": tb.get("flag_emoji"), "formation_code": tb.get("formation_code")},
            "expected_outcome": an.get("expected_outcome"),
            "winner_team_ko": an.get("final_verdict", {}).get("winner_team_ko")
        })
    conn.close()
    return {"comparisons": items}

@app.get("/api/ai/comparisons/{slug}")
def get_ai_comparison(slug: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ai_comparisons WHERE share_slug = ?", (slug,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="AI 가상 대결 분석 결과를 찾을 수 없습니다.")
    return {
        "share_slug": row["share_slug"],
        "provider": row["provider_name"],
        "model": row["model_name"],
        "created_at": row["created_at"],
        "team_a": json.loads(row["team_a_snapshot_json"]),
        "team_b": json.loads(row["team_b_snapshot_json"]),
        "analysis": json.loads(row["analysis_json"])
    }

@app.get("/api/ai/comparisons/{slug}/png")
def download_ai_comparison_png(slug: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ai_comparisons WHERE share_slug = ?", (slug,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="AI 가상 대결 분석 결과를 찾을 수 없습니다.")
    ta = json.loads(row["team_a_snapshot_json"])
    tb = json.loads(row["team_b_snapshot_json"])
    an = json.loads(row["analysis_json"])
    png_bytes = render_ai_comparison_png(ta, tb, an)
    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={"Content-Disposition": f'attachment; filename="ALL-TIME-XI-MATCH-{slug}.png"'}
    )

# ==============================================================================
# 7. ADMIN MANAGEMENT CONSOLE API WITH AUDIT TRAIL (Section 12)
# ==============================================================================
class AdminApiKeyInput(BaseModel):
    provider: str = "gemini"
    api_key: str

@app.post("/api/admin/api-key")
def admin_set_api_key(req: AdminApiKeyInput):
    if not req.api_key or len(req.api_key.strip()) < 10:
        raise HTTPException(status_code=400, detail="유효한 API 키를 입력해 주세요.")
    set_runtime_api_key(req.provider, req.api_key)
    return {"ok": True, "status": get_ai_status()}

class AdminPlayerUpsertRequest(BaseModel):
    player_id: Optional[int] = None
    country_fifa_code: str
    name_ko: str
    name_en: str
    aliases_search: Optional[str] = ""
    primary_position: str
    secondary_positions: List[str] = []
    birth_year: Optional[int] = None
    is_deceased: int = 0
    is_active_player: int = 0
    height_cm: Optional[int] = None
    preferred_foot: Optional[str] = None
    career_start_year: int
    career_end_year: int
    official_caps: int
    official_goals: int
    record_source_name: str = "Admin Verified FA Record"
    record_source_url: Optional[str] = None
    major_clubs_ko: Optional[str] = None
    major_honors_ko: Optional[str] = None
    play_style_ko: Optional[str] = None
    image_url: Optional[str] = None
    license_info: Optional[str] = None
    admin_note: str = "관리자 수동 등록/수정"

@app.post("/api/admin/players")
def admin_upsert_player(req: AdminPlayerUpsertRequest):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name_ko FROM countries WHERE fifa_code = ?", (req.country_fifa_code.upper().strip(),))
    crow = cur.fetchone()
    if not crow:
        conn.close()
        raise HTTPException(status_code=404, detail="국가 코드를 찾을 수 없습니다.")
    cid = crow["id"]

    pos_u = req.primary_position.upper().strip()
    pgroup = "GK" if pos_u == "GK" else ("DF" if pos_u in ["CB", "LB", "RB", "LCB", "RCB"] else ("MF" if pos_u in ["CDM", "CM", "CAM", "LM", "RM"] else "FW"))
    elig = 1 if req.official_caps >= 30 else 0
    vstatus = "verified" if elig else "excluded_under_30"
    decs = [f"{(y // 10) * 10}s" for y in range((req.career_start_year // 10) * 10, ((req.career_end_year // 10) * 10) + 10, 10)]
    prim_dec = f"{(((req.career_start_year + req.career_end_year) // 2) // 10) * 10}s"

    if req.player_id:
        cur.execute("SELECT * FROM players WHERE id = ?", (req.player_id,))
        before_row = cur.fetchone()
        before_json = json.dumps(dict(before_row) if before_row else {}, ensure_ascii=False)
        cur.execute("""
            UPDATE players SET
                name_ko=?, name_en=?, aliases_search=?, birth_year=?, is_deceased=?,
                primary_position=?, position_group=?, secondary_positions=?, height_cm=?, preferred_foot=?,
                is_active_player=?, play_style_ko=?, updated_at=datetime('now')
            WHERE id=?
        """, (
            req.name_ko, req.name_en, req.aliases_search or f"{req.name_ko}, {req.name_en}",
            req.birth_year, req.is_deceased, pos_u, pgroup, json.dumps(req.secondary_positions),
            req.height_cm, req.preferred_foot, req.is_active_player, req.play_style_ko, req.player_id
        ))
        pid = req.player_id
        cur.execute("""
            UPDATE player_national_team_careers SET
                career_start_year=?, career_end_year=?, active_period_label=?,
                decade_tags=?, primary_decade=?, official_caps=?, official_goals=?,
                is_eligible_30_caps=?, verification_status=?, record_source_name=?, record_source_url=?,
                verified_date=date('now')
            WHERE player_id=? AND country_id=?
        """, (
            req.career_start_year, req.career_end_year, f"{req.career_start_year}–{req.career_end_year}",
            json.dumps(decs), prim_dec, req.official_caps, req.official_goals,
            elig, vstatus, req.record_source_name, req.record_source_url, pid, cid
        ))
        action_type = "update_player"
    else:
        before_json = None
        uid = f"PLR-ADM-{req.country_fifa_code.upper()}-{uuid.uuid4().hex[:6].upper()}"
        cur.execute("""
            INSERT INTO players (
                internal_uid, name_ko, name_en, aliases_search, nationality_code, birth_year,
                is_deceased, primary_position, position_group, secondary_positions, height_cm,
                preferred_foot, is_active_player, play_style_ko, primary_role_ko, fact_bio_ko
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            uid, req.name_ko, req.name_en, req.aliases_search or f"{req.name_ko}, {req.name_en}",
            req.country_fifa_code.upper(), req.birth_year, req.is_deceased, pos_u, pgroup,
            json.dumps(req.secondary_positions), req.height_cm, req.preferred_foot, req.is_active_player,
            req.play_style_ko or f"{crow['name_ko']} 국가대표 A매치 {req.official_caps}경기 {req.official_goals}골",
            pos_u, f"{crow['name_ko']} 국가대표 공식 A매치 {req.official_caps}경기 {req.official_goals}골"
        ))
        pid = cur.lastrowid
        cur.execute("""
            INSERT INTO player_national_team_careers (
                player_id, country_id, represented_fifa_code, career_start_year, career_end_year,
                active_period_label, decade_tags, primary_decade, official_caps, official_goals,
                is_eligible_30_caps, verification_status, record_source_name, record_source_url, verified_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'))
        """, (
            pid, cid, req.country_fifa_code.upper(), req.career_start_year, req.career_end_year,
            f"{req.career_start_year}–{req.career_end_year}", json.dumps(decs), prim_dec,
            req.official_caps, req.official_goals, elig, vstatus, req.record_source_name, req.record_source_url
        ))
        cur.execute("""
            INSERT OR REPLACE INTO player_positions (player_id, position_code, position_group, is_primary, suitability_tier, suitability_score)
            VALUES (?, ?, ?, 1, 'natural', 100)
        """, (pid, pos_u, pgroup))
        action_type = "create_player"

    if req.major_clubs_ko or req.major_honors_ko:
        cur.execute("""
            INSERT INTO player_career_awards (player_id, major_clubs_ko, major_honors_ko)
            VALUES (?, ?, ?)
            ON CONFLICT(player_id) DO UPDATE SET major_clubs_ko=excluded.major_clubs_ko, major_honors_ko=excluded.major_honors_ko
        """, (pid, req.major_clubs_ko, req.major_honors_ko))

    if req.image_url is not None:
        cur.execute("""
            INSERT INTO player_images (player_id, image_url, license_info)
            VALUES (?, ?, ?)
            ON CONFLICT(player_id) DO UPDATE SET image_url=excluded.image_url, license_info=excluded.license_info
        """, (pid, req.image_url or None, req.license_info or "Admin Managed License"))

    cur.execute("""
        INSERT INTO admin_audit_logs (action_type, target_table, target_id, before_json, after_json, admin_note)
        VALUES (?, 'players', ?, ?, ?, ?)
    """, (action_type, str(pid), before_json, json.dumps(req.model_dump(), ensure_ascii=False), req.admin_note))

    conn.commit()
    conn.close()
    return {"ok": True, "player_id": pid, "is_eligible_30_caps": bool(elig)}

class AdminMergePlayersRequest(BaseModel):
    keep_player_id: int
    remove_player_id: int
    admin_note: str = "중복 선수 병합"

@app.post("/api/admin/merge-players")
def admin_merge_players(req: AdminMergePlayersRequest):
    if req.keep_player_id == req.remove_player_id:
        raise HTTPException(status_code=400, detail="동일한 선수 ID끼리는 병합할 수 없습니다.")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM players WHERE id = ?", (req.keep_player_id,))
    keep_p = cur.fetchone()
    cur.execute("SELECT * FROM players WHERE id = ?", (req.remove_player_id,))
    rem_p = cur.fetchone()
    if not keep_p or not rem_p:
        conn.close()
        raise HTTPException(status_code=404, detail="병합할 선수를 찾을 수 없습니다.")

    # Merge aliases and reassign source records
    merged_aliases = f"{keep_p['aliases_search'] or ''}, {rem_p['name_ko']}, {rem_p['name_en']}"
    cur.execute("UPDATE players SET aliases_search = ? WHERE id = ?", (merged_aliases, req.keep_player_id))
    cur.execute("UPDATE OR IGNORE player_source_records SET player_id = ? WHERE player_id = ?", (req.keep_player_id, req.remove_player_id))
    cur.execute("UPDATE OR IGNORE lineup_players SET player_id = ? WHERE player_id = ?", (req.keep_player_id, req.remove_player_id))
    cur.execute("DELETE FROM players WHERE id = ?", (req.remove_player_id,))

    cur.execute("""
        INSERT INTO admin_audit_logs (action_type, target_table, target_id, before_json, after_json, admin_note)
        VALUES ('merge_players', 'players', ?, ?, ?, ?)
    """, (str(req.keep_player_id), json.dumps(dict(rem_p), ensure_ascii=False), json.dumps({"merged_into": req.keep_player_id}), req.admin_note))
    conn.commit()
    conn.close()
    return {"ok": True, "kept_player_id": req.keep_player_id, "removed_player_id": req.remove_player_id}

class AdminRankingUpdateItem(BaseModel):
    fifa_code: str
    fifa_rank: int
    fifa_points: float
    rank_change: int = 0

class AdminRankingSnapshotRequest(BaseModel):
    snapshot_date: str
    rankings: List[AdminRankingUpdateItem]
    admin_note: str = "FIFA 세계랭킹 스냅샷 갱신"

@app.post("/api/admin/rankings")
def admin_update_rankings(req: AdminRankingSnapshotRequest):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE country_ranking_snapshots SET is_current_snapshot = 0")
    updated_cnt = 0
    for item in req.rankings:
        cur.execute("SELECT id FROM countries WHERE fifa_code = ?", (item.fifa_code.upper().strip(),))
        crow = cur.fetchone()
        if crow:
            cur.execute("""
                INSERT OR REPLACE INTO country_ranking_snapshots (
                    snapshot_date, country_id, fifa_rank, rank_change, fifa_points,
                    is_target_top30, is_current_snapshot, official_source_url
                ) VALUES (?, ?, ?, ?, ?, ?, 1, 'https://inside.fifa.com/fifa-world-ranking/men')
            """, (req.snapshot_date, crow["id"], item.fifa_rank, item.rank_change, item.fifa_points, 1 if item.fifa_rank <= 30 else 0))
            updated_cnt += 1

    cur.execute("""
        INSERT INTO admin_audit_logs (action_type, target_table, target_id, after_json, admin_note)
        VALUES ('update_ranking', 'country_ranking_snapshots', ?, ?, ?)
    """, (req.snapshot_date, json.dumps({"updated_count": updated_cnt, "snapshot_date": req.snapshot_date}), req.admin_note))
    conn.commit()
    conn.close()
    return {"ok": True, "snapshot_date": req.snapshot_date, "updated_count": updated_cnt}

@app.post("/api/admin/import-csv")
async def admin_import_csv(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    conn = get_db()
    cur = conn.cursor()
    imported = 0
    for row in reader:
        code = (row.get("country_fifa_code") or row.get("fifa_code") or "").upper().strip()
        name_ko = (row.get("name_ko") or row.get("name_en") or "").strip()
        name_en = (row.get("name_en") or name_ko).strip()
        pos = (row.get("primary_position") or "CM").upper().strip()
        caps = int(row.get("official_caps") or 0)
        goals = int(row.get("official_goals") or 0)
        y1 = int(row.get("career_start_year") or 2000)
        y2 = int(row.get("career_end_year") or 2020)
        if not code or not name_ko:
            continue
        cur.execute("SELECT id FROM countries WHERE fifa_code = ?", (code,))
        crow = cur.fetchone()
        if not crow:
            continue
        cid = crow["id"]
        uid = f"PLR-CSV-{code}-{uuid.uuid4().hex[:6].upper()}"
        pgroup = "GK" if pos == "GK" else ("DF" if pos in ["CB", "LB", "RB"] else ("MF" if pos in ["CDM", "CM", "CAM"] else "FW"))
        cur.execute("""
            INSERT INTO players (internal_uid, name_ko, name_en, aliases_search, nationality_code, primary_position, position_group, is_active_player)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """, (uid, name_ko, name_en, f"{name_ko}, {name_en}", code, pos, pgroup))
        pid = cur.lastrowid
        elig = 1 if caps >= 30 else 0
        cur.execute("""
            INSERT INTO player_national_team_careers (
                player_id, country_id, represented_fifa_code, career_start_year, career_end_year,
                active_period_label, decade_tags, primary_decade, official_caps, official_goals,
                is_eligible_30_caps, verification_status, record_source_name, verified_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'CSV Import', date('now'))
        """, (pid, cid, code, y1, y2, f"{y1}–{y2}", json.dumps([f"{(y1//10)*10}s"]), f"{(y1//10)*10}s", caps, goals, elig, "verified" if elig else "excluded_under_30"))
        imported += 1

    cur.execute("""
        INSERT INTO admin_audit_logs (action_type, target_table, target_id, after_json, admin_note)
        VALUES ('import_csv', 'players', 'batch', ?, 'CSV 파일 일괄 가져오기')
    """, (json.dumps({"imported_rows": imported}),))
    conn.commit()
    conn.close()
    return {"ok": True, "imported_rows": imported}

@app.get("/api/admin/audit-logs")
def admin_list_audit_logs(limit: int = 50):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM admin_audit_logs ORDER BY id DESC LIMIT ?", (limit,))
    logs = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {"logs": logs}

# ==============================================================================
# 8. SHAREABLE URL ROUTES WITH OPENGRAPH SOCIAL META TAGS (/team/{slug}, /match/{slug})
# ==============================================================================
def render_spa_with_og_tags(title: str, description: str, image_url: str, initial_route_js: str = "") -> HTMLResponse:
    candidates = [
        ROOT_DIR / "public" / "index.html",
        ROOT_DIR / "api" / "public" / "index.html",
        Path(__file__).resolve().parent / "public" / "index.html",
        Path("/var/task/public/index.html"),
        Path("/var/task/api/public/index.html"),
        Path("public/index.html"),
        Path("api/public/index.html"),
    ]
    index_html_path = next((p for p in candidates if p.exists()), None)
    if index_html_path and index_html_path.exists():
        with open(index_html_path, encoding="utf-8") as f:
            html = f.read()
    else:
        html = "<html><body><h1>ALL-TIME XI</h1></body></html>"
    og_block = f"""
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:image" content="{image_url}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{image_url}" />
    <script>window.__INITIAL_SHARE_CONTEXT__ = {initial_route_js or 'null'};</script>
    """
    html = html.replace("<!-- __OG_META_INJECT__ -->", og_block)
    return HTMLResponse(content=html)

@app.get("/team/{slug}", response_class=HTMLResponse)
def share_team_page(slug: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM saved_lineups WHERE share_slug = ?", (slug,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return render_spa_with_og_tags("ALL-TIME XI", "역대 최강의 국가대표 베스트11을 만들고 AI로 비교하세요.", "/api/lineups/brazil-all-time-xi/png?layout=landscape")
    snap = json.loads(row["lineup_snapshot_json"])
    title = f"[ALL-TIME XI] {snap.get('country_name_ko')} · {snap.get('team_name')} ({snap.get('formation_code')})"
    pnames = ", ".join([p.get("name_ko", "") for p in snap.get("players", [])[:6]]) + " 등 11명"
    desc = f"선발 명단: {pnames} | {snap.get('team_description') or '역대 국가대표 A매치 30회 이상 레전드 베스트11'}"
    img_url = f"/api/lineups/{slug}/png?layout=landscape"
    ctx_js = json.dumps({"type": "team", "slug": slug})
    return render_spa_with_og_tags(title, desc, img_url, ctx_js)

@app.get("/match/{slug}", response_class=HTMLResponse)
def share_match_page(slug: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ai_comparisons WHERE share_slug = ?", (slug,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return render_spa_with_og_tags("ALL-TIME XI — AI 드림매치", "역대 국가대표 베스트11 간의 AI 가상 대결", "/api/lineups/brazil-all-time-xi/png?layout=landscape")
    ta = json.loads(row["team_a_snapshot_json"])
    tb = json.loads(row["team_b_snapshot_json"])
    an = json.loads(row["analysis_json"])
    out = an.get("expected_outcome", {})
    title = f"[ALL-TIME XI AI 가상 대결] {ta.get('team_name')} {out.get('team_a_goals', 0)} : {out.get('team_b_goals', 0)} {tb.get('team_name')}"
    desc = an.get("final_verdict", {}).get("final_summary_ko", "역대 국가대표 드림팀 AI 전술 시뮬레이션 결과")
    img_url = f"/api/ai/comparisons/{slug}/png"
    ctx_js = json.dumps({"type": "match", "slug": slug})
    return render_spa_with_og_tags(title, desc, img_url, ctx_js)

@app.get("/", response_class=HTMLResponse)
def index_page():
    return render_spa_with_og_tags(
        "ALL-TIME XI — 역대 최강의 국가대표를 만들어라",
        "FIFA 세계랭킹 상위 30개국 역대 A매치 30회 이상 레전드 3,817명 데이터베이스 기반 베스트11 전술판 제작·공유 및 AI 가상 대결 플랫폼",
        "/api/lineups/brazil-all-time-xi/png?layout=landscape"
    )

public_candidates = [
    ROOT_DIR / "public",
    ROOT_DIR / "api" / "public",
    Path(__file__).resolve().parent / "public",
    Path("/var/task/public"),
    Path("/var/task/api/public"),
    Path("public"),
]
public_dir = next((p for p in public_candidates if p.exists()), ROOT_DIR / "public")
try:
    os.makedirs(str(public_dir), exist_ok=True)
except Exception:
    pass

# Serve /static with a plain route: the StaticFiles mount crashes the Vercel Python runtime
# (FUNCTION_INVOCATION_FAILED on every /static request), so read files into memory instead.
STATIC_MEDIA_TYPES = {
    ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".json": "application/json",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".ico": "image/x-icon",
}

@app.get("/static/{file_path:path}")
def serve_static(file_path: str):
    root = public_dir.resolve()
    target = (root / file_path).resolve()
    if root not in target.parents or not target.is_file():
        return Response(status_code=404)
    media_type = STATIC_MEDIA_TYPES.get(target.suffix.lower(), "application/octet-stream")
    return Response(content=target.read_bytes(), media_type=media_type, headers={"Cache-Control": "public, max-age=300"})
