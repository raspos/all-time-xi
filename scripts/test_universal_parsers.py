import re
import html as html_lib
from bs4 import BeautifulSoup

for c in ["ESP", "FRA", "ENG", "POR", "BEL", "NED"]:
    with open(f"data/raw/rsssf/{c}.html", "rb") as f:
        text = html_lib.unescape(re.sub(r'<[^>]+>', '', f.read().decode("latin-1", errors="replace")))
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    print(f"=== RSSSF {c} ===")
    for l in lines[12:28]:
        print("  ", l[:110])
