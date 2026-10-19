import os
import re
import html as html_lib
import pandas as pd
from bs4 import BeautifulSoup

DATE_TOKEN = r'\d{1,2}\s*[-/\.]\s*\d{1,2}\s*[-/\.]\s*(\d{4})'

def parse_rsssf_universal(code):
    path = f"data/raw/rsssf/{code}.html"
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("latin-1", errors="replace")
    clean = html_lib.unescape(re.sub(r'<[^>]+>', '', text))
    lines = clean.splitlines()
    
    players = []
    seen = set()
    for idx, line in enumerate(lines):
        line_s = line.strip()
        if idx > 30 and re.match(r'^(Goalscoring|Goalscorers|Goals\s+for|Goal\s+Scorers)\b', line_s, re.IGNORECASE):
            break
        if not line_s or len(line_s) < 15:
            continue
            
        # Remove leading rank e.g. "1." or "12."
        body = re.sub(r'^\d+[\.\)]\s*', '', line_s).strip()
        
        # Try Layout 1: Name   YYYY-YYYY [*]   Caps   [Goals]
        m1 = re.match(r'^(.+?)\s+(\d{4}(?:\s*-\s*(?:\d{2,4})?)?)\s*(\*)?\s+(\d+)(?:\s+(\d+|\-|\[\d+\]))?(?:\s+.*)?$', body)
        if m1:
            raw_name = m1.group(1).strip()
            if not any(w in raw_name.lower() for w in ['appearances', 'last match', 'name', 'total', 'note:', 'nb:', 'place']):
                years = m1.group(2).replace(" ", "")
                y_all = re.findall(r'\d{4}', years)
                y1 = int(y_all[0])
                if re.match(r'^\d{4}-\d{2}$', years):
                    y2_s = int(years[5:])
                    cent = str(y1)[:2] if y2_s >= int(str(y1)[2:]) else str(int(str(y1)[:2]) + 1)
                    y2 = int(f"{cent}{years[5:]}")
                elif len(y_all) > 1:
                    y2 = int(y_all[1])
                else:
                    y2 = y1
                active = bool(m1.group(3)) or (y2 >= 2024)
                caps = int(m1.group(4))
                g_str = re.sub(r'\D', '', m1.group(5) or "0")
                goals = int(g_str) if g_str else 0
                if 30 <= caps <= 250 and 1870 <= y1 <= 2026 and raw_name not in seen:
                    seen.add(raw_name)
                    players.append({
                        "raw_name": raw_name, "y1": y1, "y2": y2,
                        "active": active, "caps": caps, "goals": goals,
                        "pos_hint": "GK" if re.search(r'\b(GK|K)\b', line_s) else None
                    })
                    continue

        # Try Layout 2: Name [*] [GK/K] DD-MM-YYYY DD-MM-YYYY [*] [GK/K] Caps Goals
        m2 = re.match(
            r'^(.+?)\s+(\*)?\s*(?:GK|K)?\s*' + DATE_TOKEN + r'\s+' + DATE_TOKEN + r'\s*(\*)?\s*(?:GK|K)?\s*(\d+)\s*(?:\([^\)]+\))?\s*(\d+|\-)',
            body
        )
        if m2:
            raw_name = m2.group(1).strip().rstrip('*').strip()
            raw_name = re.sub(r'\s+(GK|K)$', '', raw_name).strip()
            y1, y2 = int(m2.group(3)), int(m2.group(4))
            active = bool(m2.group(2) or m2.group(5)) or (y2 >= 2024)
            caps = int(m2.group(6))
            g_str = re.sub(r'\D', '', m2.group(7) or "0")
            goals = int(g_str) if g_str else 0
            is_gk = bool(re.search(r'\b(GK|K)\b', body[len(raw_name):]))
            if 30 <= caps <= 250 and 1870 <= y1 <= 2026 and raw_name not in seen:
                seen.add(raw_name)
                players.append({
                    "raw_name": raw_name, "y1": y1, "y2": y2,
                    "active": active, "caps": caps, "goals": goals,
                    "pos_hint": "GK" if is_gk else None
                })
                continue

        # Try Layout 3: Name [*] [GK] Caps [(alt)] Goals [*] [GK] DD-MM-YYYY DD-MM-YYYY
        m3 = re.match(
            r'^(.+?)\s+(\*)?\s*(?:GK|K)?\s*(\d+)\s*(?:\([^\)]+\))?\s*(?:GK|K)?\s*(\d+|\-)\s*(\*)?\s*(?:GK|K)?\s*' + DATE_TOKEN + r'\s+' + DATE_TOKEN,
            body
        )
        if m3:
            raw_name = m3.group(1).strip().rstrip('*').strip()
            raw_name = re.sub(r'\s+(GK|K)$', '', raw_name).strip()
            caps = int(m3.group(3))
            g_str = re.sub(r'\D', '', m3.group(4) or "0")
            goals = int(g_str) if g_str else 0
            y1, y2 = int(m3.group(6)), int(m3.group(7))
            active = bool(m3.group(2) or m3.group(5)) or (y2 >= 2024)
            is_gk = bool(re.search(r'\b(GK|K)\b', body[len(raw_name):]))
            if 30 <= caps <= 250 and 1870 <= y1 <= 2026 and raw_name not in seen:
                seen.add(raw_name)
                players.append({
                    "raw_name": raw_name, "y1": y1, "y2": y2,
                    "active": active, "caps": caps, "goals": goals,
                    "pos_hint": "GK" if is_gk else None
                })
                continue

    return players

codes = ["ESP", "ARG", "FRA", "ENG", "POR", "BRA", "MAR", "BEL", "NED", "MEX",
         "COL", "SUI", "GER", "CRO", "ITA", "USA", "JPN", "SEN", "NOR", "URU",
         "DEN", "AUT", "IRN", "ECU", "EGY", "AUS", "CAN", "ALG", "CIV", "NGA"]

total_rsssf = 0
for c in codes:
    plist = parse_rsssf_universal(c)
    total_rsssf += len(plist)
    eras = {}
    for p in plist:
        dec = f"{(p['y1'] // 10) * 10}s"
        eras[dec] = eras.get(dec, 0) + 1
    print(f"{c}: {len(plist):3d} players (>=30 caps in RSSSF) | eras={dict(sorted(eras.items()))}")
print("Total RSSSF >=30 caps across 30 countries:", total_rsssf)
