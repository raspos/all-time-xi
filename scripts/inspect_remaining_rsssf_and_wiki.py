import re
import html as html_lib
from bs4 import BeautifulSoup

zero_codes = ["ESP", "FRA", "ENG", "POR", "BEL", "NED", "COL", "GER", "ITA", "NOR", "URU", "AUT"]
for c in zero_codes:
    with open(f"data/raw/rsssf/{c}.html", "rb") as f:
        text = html_lib.unescape(re.sub(r'<[^>]+>', '', f.read().decode("latin-1", errors="replace")))
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    print(f"=== RSSSF {c} ===")
    for l in lines[10:28]:
        print("  ", l[:110])
