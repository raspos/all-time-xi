import json
import requests
from collections import Counter

with open("data/raw/wikidata_enrichment.json", encoding="utf-8") as f:
    wd = json.load(f)

qids = Counter()
for k, v in wd.items():
    for q in v.get("pos_qids", []):
        qids[q] += 1

print("Unique position QIDs:", len(qids))
top_qids = [q for q, _ in qids.most_common(100)]

headers = {'User-Agent': 'AllTimeXI-DataEngine/1.0 (https://localhost; research@alltimexi.local)'}
pos_map = {}
for i in range(0, len(top_qids), 50):
    batch = top_qids[i:i+50]
    r = requests.get("https://www.wikidata.org/w/api.php", params={
        "action": "wbgetentities",
        "ids": "|".join(batch),
        "props": "labels",
        "languages": "en|ko",
        "format": "json"
    }, headers=headers, timeout=20).json()
    for q, ent in r.get("entities", {}).items():
        en = ent.get("labels", {}).get("en", {}).get("value", "")
        ko = ent.get("labels", {}).get("ko", {}).get("value", "")
        pos_map[q] = {"en": en, "ko": ko, "count": qids[q]}

for q, info in sorted(pos_map.items(), key=lambda x: -x[1]["count"])[:35]:
    print(f"  {q:10s} ({info['count']:4d}): en='{info['en']}' | ko='{info['ko']}'")

with open("data/raw/wikidata_position_qids.json", "w", encoding="utf-8") as f:
    json.dump(pos_map, f, ensure_ascii=False, indent=2)
