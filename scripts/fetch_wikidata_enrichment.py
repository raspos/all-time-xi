import os
import re
import json
import html as html_lib
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from scripts.test_all_30_parsers import parse_rsssf_universal

codes = ["ESP", "ARG", "FRA", "ENG", "POR", "BRA", "MAR", "BEL", "NED", "MEX",
         "COL", "SUI", "GER", "CRO", "ITA", "USA", "JPN", "SEN", "NOR", "URU",
         "DEN", "AUT", "IRN", "ECU", "EGY", "AUS", "CAN", "ALG", "CIV", "NGA"]

def clean_rsssf_display_name(raw_name):
    # If quoted nickname exists like 'Edson Arantes do Nascimento "PELÉ"', extract nickname or clean name
    q = re.search(r'"([^"]+)"', raw_name)
    if q:
        nick = q.group(1).strip()
        if len(nick) >= 3 and nick.isupper():
            return nick.title()
        elif len(nick) >= 3:
            return nick
    # Check if LASTNAME Firstname format (like 'BUFFON Gianluigi' or 'ZIDANE Zinedine')
    parts = raw_name.split()
    if len(parts) == 2 and parts[0].isupper() and len(parts[0]) > 2 and not parts[1].isupper():
        return f"{parts[1]} {parts[0].title()}"
    if len(parts) == 3 and parts[0].isupper() and parts[1].isupper() and not parts[2].isupper():
        # e.g. DE ROSSI Daniele
        return f"{parts[2]} {parts[0].title()} {parts[1].title()}"
    # Convert ALLCAPS words to Title Case
    out = []
    for p in parts:
        if p.isupper() and len(p) > 2:
            out.append(p.title())
        else:
            out.append(p)
    return " ".join(out)

def parse_wiki_all(code):
    files = [f"data/raw/wikipedia/{code}.html"]
    if code == "ESP" and os.path.exists("data/raw/wikipedia/ESP_TEAM.html"):
        files.append("data/raw/wikipedia/ESP_TEAM.html")
    results = []
    seen = set()
    for path in files:
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        for table in soup.find_all("table", class_="wikitable"):
            rows = table.find_all("tr")
            if len(rows) < 4:
                continue
            headers = [th.get_text(" ", strip=True).lower() for th in rows[0].find_all(["th", "td"])]
            data_start = 1
            # Check if 2-row header
            if len(rows) > 2 and any("national team" in h or "appearances" in h or "career" in h for h in headers):
                sub_h = [th.get_text(" ", strip=True).lower() for th in rows[1].find_all(["th", "td"])]
                if any(h in ["caps", "goals", "apps"] for h in sub_h):
                    # Combine headers if needed
                    pass
            name_idx = next((i for i, h in enumerate(headers) if h in ["player", "players", "name", "footballer"]), None)
            if name_idx is None:
                name_idx = next((i for i, h in enumerate(headers) if "player" in h or "name" in h), None)
            caps_idx = next((i for i, h in enumerate(headers) if h in ["caps", "number of caps", "appearances", "apps", "matches", "gp"]), None)
            if caps_idx is None:
                caps_idx = next((i for i, h in enumerate(headers) if ("cap" in h or "app" in h) and "first" not in h and "last" not in h and "most" not in h and "per" not in h), None)
            if name_idx is None or caps_idx is None:
                continue
            pos_idx = next((i for i, h in enumerate(headers) if "pos" in h or "role" in h), None)
            goals_idx = next((i for i, h in enumerate(headers) if h in ["goals", "number of goals", "gls"] or ("goal" in h and "per" not in h and "ratio" not in h)), None)
            birth_idx = next((i for i, h in enumerate(headers) if "birth" in h or "born" in h), None)
            first_idx = next((i for i, h in enumerate(headers) if "first" in h or "debut" in h or "career" in h or "years" in h or "span" in h or "period" in h), None)
            last_idx = next((i for i, h in enumerate(headers) if "last" in h), None)

            for row in rows[data_start:]:
                cells = row.find_all(["th", "td"])
                if len(cells) <= max(name_idx, caps_idx):
                    continue
                name_cell = cells[name_idx]
                raw_name = re.sub(r'\[[^\]]+\]', '', name_cell.get_text(" ", strip=True)).replace('*', '').replace('†', '').replace('§', '').strip()
                raw_name = re.sub(r'#\d+', '', raw_name).strip()
                if not raw_name or len(raw_name) < 2 or raw_name.lower() in ["player", "name", "total", "players"]:
                    continue
                link = name_cell.find("a", href=re.compile(r'^/wiki/'))
                wiki_title = link.get("title") if link else None
                wiki_url = f"https://en.wikipedia.org{link['href']}" if link else None

                caps_txt = re.sub(r'\[[^\]]+\]', '', cells[caps_idx].get_text(" ", strip=True))
                caps_m = re.search(r'(\d+)', caps_txt.replace(',', ''))
                if not caps_m:
                    continue
                caps = int(caps_m.group(1))
                if caps < 30 or caps > 250:
                    continue
                goals = 0
                if goals_idx is not None and goals_idx < len(cells):
                    gm = re.search(r'(\d+)', re.sub(r'\[[^\]]+\]', '', cells[goals_idx].get_text(" ", strip=True)))
                    if gm:
                        goals = int(gm.group(1))
                pos_raw = cells[pos_idx].get_text(" ", strip=True) if (pos_idx is not None and pos_idx < len(cells)) else None
                birth_year = None
                if birth_idx is not None and birth_idx < len(cells):
                    bm = re.search(r'(18\d\d|19\d\d|20\d\d)', cells[birth_idx].get_text(" ", strip=True))
                    if bm:
                        birth_year = int(bm.group(1))
                y1, y2 = None, None
                if first_idx is not None and first_idx < len(cells):
                    ys = [int(y) for y in re.findall(r'(18\d\d|19\d\d|20\d\d)', cells[first_idx].get_text(" ", strip=True))]
                    if ys:
                        y1 = ys[0]
                        if len(ys) > 1:
                            y2 = ys[-1]
                if last_idx is not None and last_idx < len(cells):
                    ys = [int(y) for y in re.findall(r'(18\d\d|19\d\d|20\d\d)', cells[last_idx].get_text(" ", strip=True))]
                    if ys:
                        y2 = ys[-1]
                key = raw_name.lower()
                if key not in seen:
                    seen.add(key)
                    results.append({
                        "name": raw_name, "wiki_title": wiki_title, "wiki_url": wiki_url,
                        "pos_raw": pos_raw, "caps": caps, "goals": goals,
                        "birth_year": birth_year, "y1": y1, "y2": y2
                    })
    return results

all_titles = set()
wiki_by_country = {}
for c in codes:
    wlist = parse_wiki_all(c)
    wiki_by_country[c] = wlist
    for w in wlist:
        if w["wiki_title"] and "redlink=1" not in (w["wiki_url"] or ""):
            all_titles.add(w["wiki_title"])
    rlist = parse_rsssf_universal(c)
    for r in rlist:
        cname = clean_rsssf_display_name(r["raw_name"])
        all_titles.add(cname)

print("Total unique candidate titles for Wikidata batch lookup:", len(all_titles))
with open("data/raw/wiki_parsed_30.json", "w", encoding="utf-8") as f:
    json.dump(wiki_by_country, f, ensure_ascii=False, indent=2)

# Batch query Wikidata wbgetentities (50 titles per batch)
titles_list = sorted(list(all_titles))
batches = [titles_list[i:i+50] for i in range(0, len(titles_list), 50)]
print(f"Fetching {len(batches)} batches from Wikidata...")

headers = {'User-Agent': 'AllTimeXI-DataEngine/1.0 (https://localhost; research@alltimexi.local)'}
enrichment = {}

def fetch_batch(batch_idx_and_titles):
    b_idx, b_titles = batch_idx_and_titles
    params = {
        "action": "wbgetentities",
        "sites": "enwiki",
        "titles": "|".join(b_titles),
        "props": "labels|claims|sitelinks",
        "languages": "ko|en",
        "sitefilter": "enwiki|kowiki",
        "format": "json"
    }
    try:
        resp = requests.get("https://www.wikidata.org/w/api.php", params=params, headers=headers, timeout=25)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        out = {}
        for qid, ent in data.get("entities", {}).items():
            if qid.startswith("-"):
                continue
            en_title = ent.get("sitelinks", {}).get("enwiki", {}).get("title")
            ko_title = ent.get("sitelinks", {}).get("kowiki", {}).get("title")
            ko_label = ent.get("labels", {}).get("ko", {}).get("value")
            en_label = ent.get("labels", {}).get("en", {}).get("value")
            if ko_title:
                ko_title = re.sub(r'\s*\([^\)]+\)\s*$', '', ko_title).strip()
            name_ko = ko_label or ko_title
            claims = ent.get("claims", {})
            # P413 position
            pos_qids = []
            for c in claims.get("P413", []):
                dv = c.get("mainsnak", {}).get("datavalue", {}).get("value", {})
                if isinstance(dv, dict) and "id" in dv:
                    pos_qids.append(dv["id"])
            # P569 birth date
            dob = None
            for c in claims.get("P569", []):
                t = c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("time")
                if t:
                    m = re.search(r'(\d{4}-\d{2}-\d{2})', t)
                    if m:
                        dob = m.group(1)
                        break
            # P570 death date
            dod = None
            for c in claims.get("P570", []):
                t = c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("time")
                if t:
                    m = re.search(r'(\d{4}-\d{2}-\d{2})', t)
                    if m:
                        dod = m.group(1)
                        break
            # P2048 height
            height_cm = None
            for c in claims.get("P2048", []):
                amt = c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("amount")
                unit = c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("unit", "")
                if amt:
                    try:
                        val = float(amt.lstrip('+'))
                        if val < 3.0:
                            height_cm = int(round(val * 100))
                        elif 140 <= val <= 220:
                            height_cm = int(round(val))
                    except Exception:
                        pass
            # P18 image
            commons_img = None
            for c in claims.get("P18", []):
                v = c.get("mainsnak", {}).get("datavalue", {}).get("value")
                if isinstance(v, str) and v:
                    commons_img = v
                    break
            key = en_title or en_label
            if key:
                out[key] = {
                    "qid": qid,
                    "name_ko": name_ko,
                    "name_en": en_label or en_title,
                    "pos_qids": pos_qids,
                    "dob": dob,
                    "dod": dod,
                    "height_cm": height_cm,
                    "commons_img": commons_img
                }
        return out
    except Exception as e:
        return {}

with ThreadPoolExecutor(max_workers=6) as ex:
    for res in ex.map(fetch_batch, enumerate(batches)):
        enrichment.update(res)

print("Wikidata enriched records count:", len(enrichment))
with open("data/raw/wikidata_enrichment.json", "w", encoding="utf-8") as f:
    json.dump(enrichment, f, ensure_ascii=False, indent=2)
