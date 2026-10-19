import re
import pandas as pd
import requests

with open(r'C:\Users\kimwo\.gemini\antigravity\brain\1b8e6734-c0a0-4112-a088-6d3f45b7107b\.system_generated\steps\12\content.md', encoding='utf-8', errors='replace') as f:
    rsssf_txt = f.read()

country_links = {}
for m in re.finditer(r'\[([^\[\]]+)\]\((https://www\.rsssf\.org/miscellaneous/[a-z0-9_-]+-recintlp\.html)\)', rsssf_txt):
    cname, url = m.group(1).strip(), m.group(2).strip()
    country_links[cname] = url

print("Clean RSSSF country links:", len(country_links))
for cname in ["Spain", "Argentina", "France", "England", "Portugal", "Brazil", "Morocco",
              "Belgium", "Netherlands", "Mexico", "Colombia", "Switzerland", "Germany",
              "Croatia", "Italy", "USA", "Japan", "Senegal", "Norway", "Uruguay",
              "Denmark", "Austria", "Iran", "Ecuador", "Egypt", "Australia", "Canada",
              "Algeria", "Ivory Coast", "Nigeria", "South Korea"]:
    print(f"  {cname:15s} -> {country_links.get(cname)}")

df_p = pd.read_csv('data/raw/players.csv.gz')
civ = df_p[df_p['country_of_citizenship'].str.contains('Ivoire|Ivory', case=False, na=False)]
print("\nIvory Coast players in TM:", len(civ), "national_team_ids:", civ['current_national_team_id'].value_counts().to_dict())

# Test fetching one RSSSF recintlp page (e.g. Brazil) and one Wikipedia page
headers = {'User-Agent': 'AllTimeXI-ResearchBot/1.0 (https://localhost; contact@example.com)'}
r_braz = requests.get("https://www.rsssf.org/miscellaneous/braz-recintlp.html", headers=headers, timeout=20)
print("RSSSF Brazil status:", r_braz.status_code, "len:", len(r_braz.text))
print(r_braz.text[:1500])
