import os
import re
import json
from bs4 import BeautifulSoup

codes = ["ESP", "ARG", "FRA", "ENG", "POR", "BRA", "MAR", "BEL", "NED", "MEX",
         "COL", "SUI", "GER", "CRO", "ITA", "USA", "JPN", "SEN", "NOR", "URU",
         "DEN", "AUT", "IRN", "ECU", "EGY", "AUS", "CAN", "ALG", "CIV", "NGA"]

def normalize_pos(pos_raw):
    if not pos_raw:
        return None
    p = pos_raw.upper().strip()
    if any(k in p for k in ["GK", "GOALKEEPER"]):
        return "GK"
    if any(k in p for k in ["CB", "DF", "DEF", "FB", "LB", "RB", "SW", "WB", "BACK"]):
        if "LB" in p or "LWB" in p:
            return "LB"
        if "RB" in p or "RWB" in p:
            return "RB"
        return "CB"
    if any(k in p for k in ["MF", "MID", "CM", "DM", "AM", "HB", "WH", "LH", "RH", "CH"]):
        if "DM" in p or "CH" in p or "HB" in p:
            return "CDM"
        if "AM" in p:
            return "CAM"
        return "CM"
    if any(k in p for k in ["FW", "FWD", "ST", "CF", "WG", "LW", "RW", "IF", "OR", "OL", "ATT", "STRIKER", "FORWARD"]):
        if "LW" in p or "OL" in p:
            return "LW"
        if "RW" in p or "OR" in p:
            return "RW"
        return "ST"
    return None

def parse_wiki_country(code):
    path = f"data/raw/wikipedia/{code}.html"
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", errors="replace") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    results = []
    seen = set()
    for table in soup.find_all("table", class_="wikitable"):
        headers = [th.get_text(" ", strip=True).lower() for th in table.find_all("tr")[0].find_all(["th", "td"])] if table.find_all("tr") else []
        header_str = " | ".join(headers)
        if not any(k in header_str for k in ["cap", "app", "match"]):
            continue
        if not any(k in header_str for k in ["player", "name"]):
            continue
            
        # Identify column indices
        name_idx = next((i for i, h in enumerate(headers) if "player" in h or "name" in h), None)
        pos_idx = next((i for i, h in enumerate(headers) if "pos" in h), None)
        caps_idx = next((i for i, h in enumerate(headers) if "cap" in h or "app" in h or "match" in h), None)
        goals_idx = next((i for i, h in enumerate(headers) if "goal" in h), None)
        birth_idx = next((i for i, h in enumerate(headers) if "birth" in h or "born" in h), None)
        first_idx = next((i for i, h in enumerate(headers) if "first" in h or "debut" in h or "career" in h or "years" in h or "period" in h), None)
        last_idx = next((i for i, h in enumerate(headers) if "last" in h), None)
        
        if name_idx is None or caps_idx is None:
            continue
            
        for row in table.find_all("tr")[1:]:
            cells = row.find_all(["th", "td"])
            if len(cells) <= max(name_idx, caps_idx):
                continue
            name_cell = cells[name_idx]
            raw_name = name_cell.get_text(" ", strip=True)
            raw_name = re.sub(r'\[[^\]]+\]', '', raw_name).replace('*', '').replace('†', '').strip()
            if not raw_name or len(raw_name) < 2 or raw_name.lower() in ["player", "name", "total"]:
                continue
            link = name_cell.find("a", href=re.compile(r'^/wiki/'))
            wiki_url = f"https://en.wikipedia.org{link['href']}" if link else None
            wiki_title = link.get("title") if link else None
            
            caps_txt = re.sub(r'\[[^\]]+\]', '', cells[caps_idx].get_text(" ", strip=True))
            caps_m = re.search(r'(\d+)', caps_txt.replace(',', ''))
            if not caps_m:
                continue
            caps = int(caps_m.group(1))
            if caps < 20 or caps > 250:
                continue
                
            goals = 0
            if goals_idx is not None and goals_idx < len(cells):
                g_txt = re.sub(r'\[[^\]]+\]', '', cells[goals_idx].get_text(" ", strip=True))
                gm = re.search(r'(\d+)', g_txt)
                if gm:
                    goals = int(gm.group(1))
                    
            pos = None
            if pos_idx is not None and pos_idx < len(cells):
                pos = normalize_pos(cells[pos_idx].get_text(" ", strip=True))
                
            birth_year = None
            if birth_idx is not None and birth_idx < len(cells):
                bm = re.search(r'(18\d\d|19\d\d|20\d\d)', cells[birth_idx].get_text(" ", strip=True))
                if bm:
                    birth_year = int(bm.group(1))
                    
            y1, y2 = None, None
            if first_idx is not None and first_idx < len(cells):
                ftxt = cells[first_idx].get_text(" ", strip=True)
                ys = [int(y) for y in re.findall(r'(18\d\d|19\d\d|20\d\d)', ftxt)]
                if ys:
                    y1 = ys[0]
                    if len(ys) > 1:
                        y2 = ys[-1]
            if last_idx is not None and last_idx < len(cells):
                ltxt = cells[last_idx].get_text(" ", strip=True)
                ys = [int(y) for y in re.findall(r'(18\d\d|19\d\d|20\d\d)', ltxt)]
                if ys:
                    y2 = ys[-1]
            if y1 and not y2:
                y2 = 2026 if "–" in (cells[first_idx].get_text() if first_idx is not None else "") else y1
                
            key = (raw_name.lower(), caps)
            if key not in seen:
                seen.add(key)
                results.append({
                    "name": raw_name,
                    "wiki_title": wiki_title,
                    "wiki_url": wiki_url,
                    "pos": pos,
                    "caps": caps,
                    "goals": goals,
                    "birth_year": birth_year,
                    "y1": y1,
                    "y2": y2
                })
    return results

if __name__ == "__main__":
    for c in codes:
        res = parse_wiki_country(c)
        res30 = [r for r in res if r["caps"] >= 30]
        pos_cnt = sum(1 for r in res30 if r["pos"])
        print(f"Wiki {c}: total_parsed={len(res):4d}, >=30_caps={len(res30):3d}, with_pos={pos_cnt:3d}")
