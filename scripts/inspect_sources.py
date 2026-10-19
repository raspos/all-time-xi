import os
import re
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup

with open(r'C:\Users\kimwo\.gemini\antigravity\brain\1b8e6734-c0a0-4112-a088-6d3f45b7107b\.system_generated\steps\12\content.md', encoding='utf-8', errors='replace') as f:
    rsssf_txt = f.read()

print("RSSSF length:", len(rsssf_txt))
lines = [line for line in rsssf_txt.splitlines() if line.strip()]
print("First 30 lines of RSSSF:")
for l in lines[:30]:
    print(" ", l[:120])

df_p = pd.read_csv('data/raw/players.csv.gz')
df_nt = pd.read_csv('data/raw/national_teams.csv.gz')
df_c = pd.read_csv('data/raw/countries.csv.gz')

print("\nCountries count:", len(df_c))
print("National teams count:", len(df_nt))
print(df_nt[['national_team_id', 'name', 'country_name', 'country_code', 'confederation']].head(35).to_string())
