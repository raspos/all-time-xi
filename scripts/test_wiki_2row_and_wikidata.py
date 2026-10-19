import os
import re
from bs4 import BeautifulSoup
import requests

def inspect_wiki_headers(code):
    path = f"data/raw/wikipedia/{code}.html"
    with open(path, encoding="utf-8", errors="replace") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for idx, t in enumerate(soup.find_all("table", class_="wikitable")):
        rows = t.find_all("tr")[:3]
        h_texts = [[c.get_text(" ", strip=True) for c in r.find_all(["th", "td"])] for r in rows]
        print(f"{code} Table {idx} (rows={len(t.find_all('tr'))}): {h_texts[:2]}")

for c in ["ESP", "ARG", "BEL", "NED", "DEN", "URU", "USA", "JPN"]:
    inspect_wiki_headers(c)

# Test Wikidata wbgetentities batch for 5 legends
headers = {'User-Agent': 'AllTimeXI-DataEngine/1.0 (https://localhost; research@alltimexi.local)'}
params = {
    "action": "wbgetentities",
    "sites": "enwiki",
    "titles": "Pelé|Diego Maradona|Johan Cruyff|Franz Beckenbauer|Zinedine Zidane",
    "props": "labels|claims",
    "languages": "ko|en",
    "format": "json"
}
r = requests.get("https://www.wikidata.org/w/api.php", params=params, headers=headers, timeout=20).json()
for qid, ent in r.get("entities", {}).items():
    ko = ent.get("labels", {}).get("ko", {}).get("value")
    en = ent.get("labels", {}).get("en", {}).get("value")
    claims = ent.get("claims", {})
    p413 = [c["mainsnak"]["datavalue"]["value"]["id"] for c in claims.get("P413", []) if "datavalue" in c.get("mainsnak", {})]
    p18 = [c["mainsnak"]["datavalue"]["value"] for c in claims.get("P18", []) if "datavalue" in c.get("mainsnak", {})]
    p570 = [c["mainsnak"]["datavalue"]["value"]["time"] for c in claims.get("P570", []) if "datavalue" in c.get("mainsnak", {})]
    print(f"Wikidata {qid}: en={en}, ko={ko}, pos={p413}, img={p18[:1]}, death={p570}")
