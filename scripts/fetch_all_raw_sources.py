import os
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

os.makedirs("data/raw/rsssf", exist_ok=True)
os.makedirs("data/raw/wikipedia", exist_ok=True)

headers = {'User-Agent': 'AllTimeXI-DataEngine/1.0 (https://localhost; research@alltimexi.local)'}

RSSSF_MAP = {
    "ESP": "https://www.rsssf.org/miscellaneous/span-recintlp.html",
    "ARG": "https://www.rsssf.org/miscellaneous/arg-recintlp.html",
    "FRA": "https://www.rsssf.org/miscellaneous/fran-recintlp.html",
    "ENG": "https://www.rsssf.org/miscellaneous/eng-recintlp.html",
    "POR": "https://www.rsssf.org/miscellaneous/port-recintlp.html",
    "BRA": "https://www.rsssf.org/miscellaneous/braz-recintlp.html",
    "MAR": "https://www.rsssf.org/miscellaneous/maro-recintlp.html",
    "BEL": "https://www.rsssf.org/miscellaneous/belg-recintlp.html",
    "NED": "https://www.rsssf.org/miscellaneous/ned-recintlp.html",
    "MEX": "https://www.rsssf.org/miscellaneous/mex-recintlp.html",
    "COL": "https://www.rsssf.org/miscellaneous/col-recintlp.html",
    "SUI": "https://www.rsssf.org/miscellaneous/zwit-recintlp.html",
    "GER": "https://www.rsssf.org/miscellaneous/duit-recintlp.html",
    "CRO": "https://www.rsssf.org/miscellaneous/kroa-recintlp.html",
    "ITA": "https://www.rsssf.org/miscellaneous/ital-recintlp.html",
    "USA": "https://www.rsssf.org/miscellaneous/usa-recintlp.html",
    "JPN": "https://www.rsssf.org/miscellaneous/jap-recintlp.html",
    "SEN": "https://www.rsssf.org/miscellaneous/sene-recintlp.html",
    "NOR": "https://www.rsssf.org/miscellaneous/noo-recintlp.html",
    "URU": "https://www.rsssf.org/miscellaneous/uru-recintlp.html",
    "DEN": "https://www.rsssf.org/miscellaneous/den-recintlp.html",
    "AUT": "https://www.rsssf.org/miscellaneous/oost-recintlp.html",
    "IRN": "https://www.rsssf.org/miscellaneous/iran-recintlp.html",
    "ECU": "https://www.rsssf.org/miscellaneous/ecua-recintlp.html",
    "EGY": "https://www.rsssf.org/miscellaneous/egy-recintlp.html",
    "AUS": "https://www.rsssf.org/miscellaneous/aus-recintlp.html",
    "CAN": "https://www.rsssf.org/miscellaneous/can-recintlp.html",
    "ALG": "https://www.rsssf.org/miscellaneous/alg-recintlp.html",
    "CIV": "https://www.rsssf.org/miscellaneous/ivo-recintlp.html",
    "NGA": "https://www.rsssf.org/miscellaneous/nig-recintlp.html",
    "KOR": "https://www.rsssf.org/miscellaneous/skor-recintlp.html",
}

WIKI_MAP = {
    "ESP": "List of Spain international footballers",
    "ARG": "List of Argentina international footballers",
    "FRA": "List of France international footballers",
    "ENG": "List of England international footballers",
    "POR": "List of Portugal international footballers",
    "BRA": "List of Brazil international footballers",
    "MAR": "Morocco national football team",
    "BEL": "List of Belgium international footballers",
    "NED": "List of Netherlands international footballers",
    "MEX": "List of Mexico international footballers",
    "COL": "Colombia national football team",
    "SUI": "List of Switzerland international footballers",
    "GER": "List of Germany international footballers",
    "CRO": "List of Croatia international footballers",
    "ITA": "List of Italy international footballers",
    "USA": "List of United States men's international soccer players",
    "JPN": "List of Japan international footballers",
    "SEN": "Senegal national football team",
    "NOR": "List of Norway international footballers",
    "URU": "List of Uruguay international footballers",
    "DEN": "List of Denmark international footballers",
    "AUT": "List of Austria international footballers",
    "IRN": "List of Iran international footballers",
    "ECU": "List of Ecuador international footballers",
    "EGY": "Egypt national football team",
    "AUS": "List of Australia men's international soccer players",
    "CAN": "List of Canada men's international soccer players",
    "ALG": "List of Algeria international footballers",
    "CIV": "Ivory Coast national football team",
    "NGA": "Nigeria national football team",
    "KOR": "List of South Korea international footballers",
}

def fetch_rsssf(item):
    code, url = item
    path = f"data/raw/rsssf/{code}.html"
    if os.path.exists(path) and os.path.getsize(path) > 500:
        return code, True, os.path.getsize(path)
    r = requests.get(url, headers=headers, timeout=25)
    if r.status_code == 200:
        with open(path, "wb") as f:
            f.write(r.content)
        return code, True, len(r.content)
    return code, False, r.status_code

def fetch_wiki(item):
    code, title = item
    path = f"data/raw/wikipedia/{code}.html"
    if os.path.exists(path) and os.path.getsize(path) > 500:
        return code, True, os.path.getsize(path)
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "format": "json",
        "redirects": 1
    }
    r = requests.get(url, params=params, headers=headers, timeout=30)
    if r.status_code == 200:
        data = r.json()
        html = data.get("parse", {}).get("text", {}).get("*", "")
        if html:
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            return code, True, len(html)
    return code, False, r.status_code

print("Fetching RSSSF pages...")
with ThreadPoolExecutor(max_workers=6) as ex:
    for code, ok, info in ex.map(fetch_rsssf, RSSSF_MAP.items()):
        print(f"  RSSSF {code}: ok={ok}, info={info}")

print("\nFetching Wikipedia pages...")
with ThreadPoolExecutor(max_workers=6) as ex:
    for code, ok, info in ex.map(fetch_wiki, WIKI_MAP.items()):
        print(f"  Wiki {code}: ok={ok}, info={info}")
