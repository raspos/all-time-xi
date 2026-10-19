import re
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'AllTimeXI-ResearchBot/1.0 (https://localhost; contact@example.com)'}
r_braz = requests.get("https://www.rsssf.org/miscellaneous/braz-recintlp.html", headers=headers, timeout=20)
print(r_braz.text[:6000])

wiki_titles = [
    "List of Spain international footballers",
    "List of Argentina international footballers",
    "List of France international footballers",
    "List of England international footballers",
    "List of Portugal international footballers",
    "List of Brazil international footballers",
    "List of Morocco international footballers",
    "List of Belgium international footballers",
    "List of Netherlands international footballers",
    "List of Mexico international footballers",
    "List of Colombia international footballers",
    "List of Switzerland international footballers",
    "List of Germany international footballers",
    "List of Croatia international footballers",
    "List of Italy international footballers",
    "List of United States men's international soccer players",
    "List of Japan international footballers",
    "List of Senegal international footballers",
    "List of Norway international footballers",
    "List of Uruguay international footballers",
    "List of Denmark international footballers",
    "List of Austria international footballers",
    "List of Iran international footballers",
    "List of Ecuador international footballers",
    "List of Egypt international footballers",
    "List of Australia international soccer players",
    "List of Canada men's international soccer players",
    "List of Algeria international footballers",
    "List of Ivory Coast international footballers",
    "List of Nigeria international footballers",
]

api_url = "https://en.wikipedia.org/w/api.php"
params = {
    "action": "query",
    "titles": "|".join(wiki_titles),
    "redirects": 1,
    "format": "json"
}
resp = requests.get(api_url, params=params, headers=headers, timeout=20).json()
pages = resp.get("query", {}).get("pages", {})
for pid, pdata in pages.items():
    print(f"Wiki Page [{pid}]: {pdata.get('title')} (missing={ 'missing' in pdata })")
