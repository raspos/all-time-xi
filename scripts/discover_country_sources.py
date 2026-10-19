import re
import json
import pandas as pd

with open(r'C:\Users\kimwo\.gemini\antigravity\brain\1b8e6734-c0a0-4112-a088-6d3f45b7107b\.system_generated\steps\12\content.md', encoding='utf-8', errors='replace') as f:
    rsssf_txt = f.read()

country_links = {}
for m in re.finditer(r'\[([^\]]+)\]\((https://www\.rsssf\.org/miscellaneous/[a-z0-9_-]+-recintlp\.html)\)', rsssf_txt):
    cname, url = m.group(1).strip(), m.group(2).strip()
    if cname not in country_links:
        country_links[cname] = url

print("Found RSSSF country recintlp links:", len(country_links))
for k, v in sorted(country_links.items()):
    print(f"  {k}: {v}")

df_nt = pd.read_csv('data/raw/national_teams.csv.gz')
df_p = pd.read_csv('data/raw/players.csv.gz')

top30_names = [
    "Spain", "Argentina", "France", "England", "Portugal", "Brazil", "Morocco",
    "Belgium", "Netherlands", "Mexico", "Colombia", "Switzerland", "Germany",
    "Croatia", "Italy", "United States", "Japan", "Senegal", "Norway", "Uruguay",
    "Denmark", "Austria", "Iran", "Ecuador", "Egypt", "Australia", "Canada",
    "Algeria", "Ivory Coast", "Nigeria"
]

print("\nMatching Top 30 in Transfermarkt national_teams:")
for name in top30_names:
    matches = df_nt[df_nt['name'].str.contains(name, case=False, na=False) | df_nt['country_name'].str.contains(name, case=False, na=False)]
    if len(matches) == 0 and name == "Ivory Coast":
        matches = df_nt[df_nt['name'].str.contains("Ivoire", case=False, na=False)]
    if len(matches) == 0 and name == "United States":
        matches = df_nt[df_nt['name'].str.contains("United States|USA", case=False, na=False)]
    print(f"  {name}: {matches[['national_team_id', 'name', 'country_name']].to_dict(orient='records')}")
