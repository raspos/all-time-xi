import os
import re
import html as html_lib
import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'AllTimeXI-DataEngine/1.0 (https://localhost; research@alltimexi.local)'}
r = requests.get("https://en.wikipedia.org/w/api.php", params={"action": "parse", "page": "List of Spain men's international footballers", "prop": "text", "format": "json", "redirects": 1}, headers=headers, timeout=30)
esp_html = r.json().get("parse", {}).get("text", {}).get("*", "")
if len(esp_html) > 10000:
    with open("data/raw/wikipedia/ESP.html", "w", encoding="utf-8") as f:
        f.write(esp_html)
    print("Updated ESP.html:", len(esp_html))

def parse_rsssf_file(code):
    path = f"data/raw/rsssf/{code}.html"
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("latin-1", errors="replace")
    # Remove HTML tags while keeping line breaks intact
    clean = html_lib.unescape(re.sub(r'<[^>]+>', '', text))
    
    # Cut at Goalscoring heading (skip table of contents at top)
    lines = clean.splitlines()
    players = []
    seen = set()
    in_goals = False
    for idx, line in enumerate(lines):
        line_s = line.strip()
        if idx > 25 and re.match(r'^(Goalscoring|Goalscorers|Goals\s+for)\b', line_s, re.IGNORECASE):
            break
        if not line_s or len(line_s) < 12:
            continue
        # Match: Name   1990-2006 [*]   142   [5]
        m = re.match(r'^(.+?)\s+(\d{4}(?:\s*-\s*(?:\d{2,4})?)?)\s*(\*)?\s+(\d+)(?:\s+(\d+|\-|\[\d+\]))?(?:\s+.*)?$', line_s)
        if m:
            raw_name = m.group(1).strip()
            raw_name = re.sub(r'^\d+[\.\)]?\s*', '', raw_name).strip()
            # Filter out headers or match score lines
            if any(w in raw_name.lower() for w in ['appearances', 'last match', 'name', 'total', 'note:', 'nb:']):
                continue
            years = m.group(2).replace(" ", "")
            # Normalize 1990-98 -> 1990-1998
            if re.match(r'^\d{4}-\d{2}$', years):
                y_start = years[:4]
                y_end_short = int(years[5:])
                century = y_start[:2] if y_end_short >= int(y_start[2:]) else str(int(y_start[:2]) + 1)
                years = f"{y_start}-{century}{years[5:]}"
            active = bool(m.group(3))
            caps = int(m.group(4))
            goals_str = m.group(5) or "0"
            goals_digits = re.sub(r'\D', '', goals_str)
            goals = int(goals_digits) if goals_digits else 0
            if 30 <= caps <= 250 and raw_name not in seen:
                seen.add(raw_name)
                players.append({
                    "raw_name": raw_name,
                    "years": years,
                    "active": active,
                    "caps": caps,
                    "goals": goals
                })
    return players

codes = ["ESP", "ARG", "FRA", "ENG", "POR", "BRA", "MAR", "BEL", "NED", "MEX",
         "COL", "SUI", "GER", "CRO", "ITA", "USA", "JPN", "SEN", "NOR", "URU",
         "DEN", "AUT", "IRN", "ECU", "EGY", "AUS", "CAN", "ALG", "CIV", "NGA"]

total_rsssf = 0
for c in codes:
    plist = parse_rsssf_file(c)
    total_rsssf += len(plist)
    eras = {}
    for p in plist:
        y1 = int(p["years"][:4])
        dec = f"{(y1 // 10) * 10}s"
        eras[dec] = eras.get(dec, 0) + 1
    print(f"{c}: {len(plist):3d} players (>=30 caps in RSSSF) | eras={dict(sorted(eras.items()))}")
print("Total RSSSF >=30 caps across 30 countries:", total_rsssf)
