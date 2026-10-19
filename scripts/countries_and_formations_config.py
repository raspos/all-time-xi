# -*- coding: utf-8 -*-
"""
Master configuration for:
1. Official FIFA Men's World Ranking Top 30 (Snapshot Date: 2026-10-07) + Country Master Metadata
2. Historical Succession Mapping Rules (West Germany -> Germany, USSR/Yugoslavia/Czechoslovakia policy)
3. 7 Tactical Formations with exact coordinates (Attack on Top Y=14..24, GK on Bottom Y=88)
4. Data Sources Registry
"""

RANKING_SNAPSHOT_DATE = "2026-10-07"
NEXT_RANKING_DATE = "2026-11-18"

TOP_30_COUNTRIES = [
    {
        "fifa_rank": 1, "rank_change": 0, "fifa_points": 2011.57,
        "fifa_code": "ESP", "iso_alpha2": "es", "name_ko": "스페인", "name_en": "Spain",
        "confederation": "UEFA", "flag_emoji": "🇪🇸",
        "world_cup_titles": 1, "world_cup_winning_years": "2010",
        "major_honors_ko": "FIFA 월드컵 우승 1회(2010), UEFA 유로 우승 4회(1964, 2008, 2012, 2024), UEFA 네이션스리그 우승 1회(2023)",
        "kit_primary_color": "#C60B1E", "kit_secondary_color": "#FFC400", "kit_accent_color": "#1E3A8A", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3375, "rsssf_url": "https://www.rsssf.org/miscellaneous/span-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Spain_men%27s_international_footballers",
        "historical_note_ko": "1920년 첫 공식 A매치 이후 단일 국가대표팀 기록을 유지하고 있습니다."
    },
    {
        "fifa_rank": 2, "rank_change": 0, "fifa_points": 1972.80,
        "fifa_code": "ARG", "iso_alpha2": "ar", "name_ko": "아르헨티나", "name_en": "Argentina",
        "confederation": "CONMEBOL", "flag_emoji": "🇦🇷",
        "world_cup_titles": 3, "world_cup_winning_years": "1978, 1986, 2022",
        "major_honors_ko": "FIFA 월드컵 우승 3회(1978, 1986, 2022), 코파 아메리카 우승 16회(역대 최다)",
        "kit_primary_color": "#43A1D5", "kit_secondary_color": "#FFFFFF", "kit_accent_color": "#F59E0B", "kit_text_color": "#0F172A", "kit_pattern_type": "stripes",
        "tm_national_team_id": 3437, "rsssf_url": "https://www.rsssf.org/miscellaneous/arg-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Argentina_international_footballers",
        "historical_note_ko": "1902년 첫 A매치 이후 AFA 공식 기록 및 RSSSF 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 3, "rank_change": 0, "fifa_points": 1958.86,
        "fifa_code": "FRA", "iso_alpha2": "fr", "name_ko": "프랑스", "name_en": "France",
        "confederation": "UEFA", "flag_emoji": "🇫🇷",
        "world_cup_titles": 2, "world_cup_winning_years": "1998, 2018",
        "major_honors_ko": "FIFA 월드컵 우승 2회(1998, 2018), UEFA 유로 우승 2회(1984, 2000), 컨페더레이션스컵 우승 2회",
        "kit_primary_color": "#1E3A8A", "kit_secondary_color": "#FFFFFF", "kit_accent_color": "#EF4444", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3377, "rsssf_url": "https://www.rsssf.org/miscellaneous/fran-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_France_international_footballers",
        "historical_note_ko": "1904년 첫 공식 A매치 이후 FFF(프랑스축구협회) 공식 A매치 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 4, "rank_change": 0, "fifa_points": 1925.59,
        "fifa_code": "ENG", "iso_alpha2": "gb-eng", "name_ko": "잉글랜드", "name_en": "England",
        "confederation": "UEFA", "flag_emoji": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "world_cup_titles": 1, "world_cup_winning_years": "1966",
        "major_honors_ko": "FIFA 월드컵 우승 1회(1966), UEFA 유로 준우승 2회(2020, 2024)",
        "kit_primary_color": "#F8FAFC", "kit_secondary_color": "#1E3A8A", "kit_accent_color": "#DC2626", "kit_text_color": "#0F172A", "kit_pattern_type": "solid",
        "tm_national_team_id": 3299, "rsssf_url": "https://www.rsssf.org/miscellaneous/eng-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_England_international_footballers",
        "historical_note_ko": "1872년 세계 최초의 공식 A매치 이후 잉글랜드 축구협회(The FA) 기록을 따릅니다(영국 단일팀 올림픽 경기 제외)."
    },
    {
        "fifa_rank": 5, "rank_change": 2, "fifa_points": 1807.69,
        "fifa_code": "POR", "iso_alpha2": "pt", "name_ko": "포르투갈", "name_en": "Portugal",
        "confederation": "UEFA", "flag_emoji": "🇵🇹",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "UEFA 유로 우승 1회(2016), UEFA 네이션스리그 우승 1회(2019), FIFA 월드컵 3위(1966)",
        "kit_primary_color": "#991B1B", "kit_secondary_color": "#065F46", "kit_accent_color": "#FBBF24", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3300, "rsssf_url": "https://www.rsssf.org/miscellaneous/port-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Portugal_international_footballers",
        "historical_note_ko": "1921년 첫 공식 A매치 이후 포르투갈 축구연맹(FPF) 공식 기록을 따릅니다."
    },
    {
        "fifa_rank": 6, "rank_change": -1, "fifa_points": 1806.51,
        "fifa_code": "BRA", "iso_alpha2": "br", "name_ko": "브라질", "name_en": "Brazil",
        "confederation": "CONMEBOL", "flag_emoji": "🇧🇷",
        "world_cup_titles": 5, "world_cup_winning_years": "1958, 1962, 1970, 1994, 2002",
        "major_honors_ko": "FIFA 월드컵 우승 5회(역대 최다: 1958, 1962, 1970, 1994, 2002), 코파 아메리카 우승 9회, 컨페더레이션스컵 우승 4회",
        "kit_primary_color": "#FACC15", "kit_secondary_color": "#15803D", "kit_accent_color": "#1D4ED8", "kit_text_color": "#0F172A", "kit_pattern_type": "solid",
        "tm_national_team_id": 3439, "rsssf_url": "https://www.rsssf.org/miscellaneous/braz-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Brazil_international_footballers",
        "historical_note_ko": "비공식 클럽/선발팀 친선전을 제외한 FIFA/RSSSF 공인 성인 A매치 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 7, "rank_change": -1, "fifa_points": 1805.34,
        "fifa_code": "MAR", "iso_alpha2": "ma", "name_ko": "모로코", "name_en": "Morocco",
        "confederation": "CAF", "flag_emoji": "🇲🇦",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "아프리카 네이션스컵 우승 1회(1976), FIFA 월드컵 4위(2022 - 아프리카 최초)",
        "kit_primary_color": "#B91C1C", "kit_secondary_color": "#15803D", "kit_accent_color": "#FBBF24", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3575, "rsssf_url": "https://www.rsssf.org/miscellaneous/maro-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/Morocco_national_football_team",
        "historical_note_ko": "1957년 독립 이후 왕립 모로코 축구연맹(FRMF) 및 RSSSF 공인 A매치 기록을 수록합니다."
    },
    {
        "fifa_rank": 8, "rank_change": 0, "fifa_points": 1779.17,
        "fifa_code": "BEL", "iso_alpha2": "be", "name_ko": "벨기에", "name_en": "Belgium",
        "confederation": "UEFA", "flag_emoji": "🇧🇪",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "FIFA 월드컵 3위(2018), UEFA 유로 준우승(1980)",
        "kit_primary_color": "#991B1B", "kit_secondary_color": "#111827", "kit_accent_color": "#FACC15", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3382, "rsssf_url": "https://www.rsssf.org/miscellaneous/belg-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Belgium_international_footballers",
        "historical_note_ko": "1904년 첫 공식 A매치 이후 RBFA(벨기에 왕립축구협회) 공인 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 9, "rank_change": 0, "fifa_points": 1778.61,
        "fifa_code": "NED", "iso_alpha2": "nl", "name_ko": "네덜란드", "name_en": "Netherlands",
        "confederation": "UEFA", "flag_emoji": "🇳🇱",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "UEFA 유로 우승 1회(1988), FIFA 월드컵 준우승 3회(1974, 1978, 2010)",
        "kit_primary_color": "#EA580C", "kit_secondary_color": "#FFFFFF", "kit_accent_color": "#1E3A8A", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3379, "rsssf_url": "https://www.rsssf.org/miscellaneous/ned-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Netherlands_international_footballers",
        "historical_note_ko": "1905년 첫 공식 A매치 이후 KNVB(네덜란드 왕립축구협회) 공인 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 10, "rank_change": 0, "fifa_points": 1738.48,
        "fifa_code": "MEX", "iso_alpha2": "mx", "name_ko": "멕시코", "name_en": "Mexico",
        "confederation": "CONCACAF", "flag_emoji": "🇲🇽",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "FIFA 컨페더레이션스컵 우승 1회(1999), CONCACAF 골드컵/선수권 우승 12회",
        "kit_primary_color": "#065F46", "kit_secondary_color": "#FFFFFF", "kit_accent_color": "#DC2626", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 6303, "rsssf_url": "https://www.rsssf.org/miscellaneous/mex-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Mexico_international_footballers",
        "historical_note_ko": "CONCACAF 골드컵 중 비FIFA 회원국(과들루프·마르티니크) 상대 경기는 RSSSF/FMF 주석과 함께 표기합니다."
    },
    {
        "fifa_rank": 11, "rank_change": 0, "fifa_points": 1735.80,
        "fifa_code": "COL", "iso_alpha2": "co", "name_ko": "콜롬비아", "name_en": "Colombia",
        "confederation": "CONMEBOL", "flag_emoji": "🇨🇴",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "코파 아메리카 우승 1회(2001), 코파 아메리카 준우승 2회(1975, 2024)",
        "kit_primary_color": "#FACC15", "kit_secondary_color": "#1E3A8A", "kit_accent_color": "#DC2626", "kit_text_color": "#0F172A", "kit_pattern_type": "solid",
        "tm_national_team_id": 3816, "rsssf_url": "https://www.rsssf.org/miscellaneous/col-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/Colombia_national_football_team",
        "historical_note_ko": "1938년 첫 A매치 이후 FCF 및 RSSSF 공인 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 12, "rank_change": 2, "fifa_points": 1725.39,
        "fifa_code": "SUI", "iso_alpha2": "ch", "name_ko": "스위스", "name_en": "Switzerland",
        "confederation": "UEFA", "flag_emoji": "🇨🇭",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "FIFA 월드컵 8강 3회(1934, 1938, 1954), UEFA 유로 8강 3회(2020, 2024)",
        "kit_primary_color": "#DC2626", "kit_secondary_color": "#FFFFFF", "kit_accent_color": "#FFFFFF", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3384, "rsssf_url": "https://www.rsssf.org/miscellaneous/zwit-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Switzerland_international_footballers",
        "historical_note_ko": "1905년 첫 공식 A매치 이후 SFV(스위스 축구협회) 공인 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 13, "rank_change": -1, "fifa_points": 1717.52,
        "fifa_code": "GER", "iso_alpha2": "de", "name_ko": "독일", "name_en": "Germany",
        "confederation": "UEFA", "flag_emoji": "🇩🇪",
        "world_cup_titles": 4, "world_cup_winning_years": "1954, 1974, 1990, 2014",
        "major_honors_ko": "FIFA 월드컵 우승 4회(1954, 1974, 1990, 2014), UEFA 유로 우승 3회(1972, 1980, 1996), 컨페더레이션스컵 우승 1회",
        "kit_primary_color": "#F8FAFC", "kit_secondary_color": "#111827", "kit_accent_color": "#EAB308", "kit_text_color": "#0F172A", "kit_pattern_type": "solid",
        "tm_national_team_id": 3262, "rsssf_url": "https://www.rsssf.org/miscellaneous/duit-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Germany_international_footballers",
        "historical_note_ko": "FIFA 및 독일축구협회(DFB) 공식 승계 기준에 따라 서독(FRG, 1950–1990) 기록을 공식 승계하며, 동독(GDR) 단독 출전 기록은 합산하지 않고 구분합니다."
    },
    {
        "fifa_rank": 14, "rank_change": -1, "fifa_points": 1714.74,
        "fifa_code": "CRO", "iso_alpha2": "hr", "name_ko": "크로아티아", "name_en": "Croatia",
        "confederation": "UEFA", "flag_emoji": "🇭🇷",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "FIFA 월드컵 준우승(2018), FIFA 월드컵 3위 2회(1998, 2022), UEFA 네이션스리그 준우승(2023)",
        "kit_primary_color": "#DC2626", "kit_secondary_color": "#FFFFFF", "kit_accent_color": "#1D4ED8", "kit_text_color": "#FFFFFF", "kit_pattern_type": "checkered",
        "tm_national_team_id": 3556, "rsssf_url": "https://www.rsssf.org/miscellaneous/kroa-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Croatia_international_footballers",
        "historical_note_ko": "구 유고슬라비아(YUG) 대표팀 출전 기록을 합산하지 않으며, 크로아티아 독립 이후 HNS 공식 A매치(1990~현재) 출전 30회 이상 선수만 등록합니다."
    },
    {
        "fifa_rank": 15, "rank_change": 0, "fifa_points": 1713.04,
        "fifa_code": "ITA", "iso_alpha2": "it", "name_ko": "이탈리아", "name_en": "Italy",
        "confederation": "UEFA", "flag_emoji": "🇮🇹",
        "world_cup_titles": 4, "world_cup_winning_years": "1934, 1938, 1982, 2006",
        "major_honors_ko": "FIFA 월드컵 우승 4회(1934, 1938, 1982, 2006), UEFA 유로 우승 2회(1968, 2020)",
        "kit_primary_color": "#1D4ED8", "kit_secondary_color": "#FFFFFF", "kit_accent_color": "#15803D", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3376, "rsssf_url": "https://www.rsssf.org/miscellaneous/ital-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Italy_international_footballers",
        "historical_note_ko": "1910년 첫 공식 A매치 이후 이탈리아 축구연맹(FIGC) 공인 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 16, "rank_change": 0, "fifa_points": 1705.47,
        "fifa_code": "USA", "iso_alpha2": "us", "name_ko": "미국", "name_en": "United States",
        "confederation": "CONCACAF", "flag_emoji": "🇺🇸",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "FIFA 월드컵 3위(1930), CONCACAF 골드컵 우승 7회, CONCACAF 네이션스리그 우승 3회, 컨페더레이션스컵 준우승(2009)",
        "kit_primary_color": "#1E293B", "kit_secondary_color": "#DC2626", "kit_accent_color": "#FFFFFF", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3505, "rsssf_url": "https://www.rsssf.org/miscellaneous/usa-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_United_States_men%27s_international_soccer_players",
        "historical_note_ko": "미국축구연맹(USSF) 및 RSSSF 공인 성인 남자 A매치 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 17, "rank_change": 0, "fifa_points": 1684.75,
        "fifa_code": "JPN", "iso_alpha2": "jp", "name_ko": "일본", "name_en": "Japan",
        "confederation": "AFC", "flag_emoji": "🇯🇵",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "AFC 아시안컵 우승 4회(1992, 2000, 2004, 2011 - 역대 최다), FIFA 컨페더레이션스컵 준우승(2001)",
        "kit_primary_color": "#1E40AF", "kit_secondary_color": "#FFFFFF", "kit_accent_color": "#EF4444", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3435, "rsssf_url": "https://www.rsssf.org/miscellaneous/jap-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Japan_international_footballers",
        "historical_note_ko": "일본축구협회(JFA) 및 RSSSF 공인 A매치 기록을 기준으로 합니다(올림픽 예선 중 비공인 경기 주석 표기)."
    },
    {
        "fifa_rank": 18, "rank_change": 0, "fifa_points": 1648.84,
        "fifa_code": "SEN", "iso_alpha2": "sn", "name_ko": "세네갈", "name_en": "Senegal",
        "confederation": "CAF", "flag_emoji": "🇸🇳",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "아프리카 네이션스컵 우승 1회(2021), FIFA 월드컵 8강(2002)",
        "kit_primary_color": "#15803D", "kit_secondary_color": "#FACC15", "kit_accent_color": "#DC2626", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3499, "rsssf_url": "https://www.rsssf.org/miscellaneous/sene-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/Senegal_national_football_team",
        "historical_note_ko": "1960년 독립 이후 세네갈 축구연맹(FSF) 및 RSSSF 공인 A매치 기록을 수록합니다."
    },
    {
        "fifa_rank": 19, "rank_change": 0, "fifa_points": 1637.89,
        "fifa_code": "NOR", "iso_alpha2": "no", "name_ko": "노르웨이", "name_en": "Norway",
        "confederation": "UEFA", "flag_emoji": "🇳🇴",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "FIFA 월드컵 16강(1938, 1998), 올림픽 동메달(1936)",
        "kit_primary_color": "#DC2626", "kit_secondary_color": "#1E3A8A", "kit_accent_color": "#FFFFFF", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3440, "rsssf_url": "https://www.rsssf.org/miscellaneous/noo-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Norway_international_footballers",
        "historical_note_ko": "1908년 첫 공식 A매치 이후 노르웨이 축구협회(NFF) 공식 기록을 따릅니다."
    },
    {
        "fifa_rank": 20, "rank_change": 0, "fifa_points": 1635.54,
        "fifa_code": "URU", "iso_alpha2": "uy", "name_ko": "우루과이", "name_en": "Uruguay",
        "confederation": "CONMEBOL", "flag_emoji": "🇺🇾",
        "world_cup_titles": 2, "world_cup_winning_years": "1930, 1950",
        "major_honors_ko": "FIFA 월드컵 우승 2회(1930, 1950), 코파 아메리카 우승 15회, 올림픽 금메달 2회(1924, 1928 - FIFA 주관 세계선수권 인정)",
        "kit_primary_color": "#38BDF8", "kit_secondary_color": "#111827", "kit_accent_color": "#FBBF24", "kit_text_color": "#0F172A", "kit_pattern_type": "solid",
        "tm_national_team_id": 3449, "rsssf_url": "https://www.rsssf.org/miscellaneous/uru-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Uruguay_international_footballers",
        "historical_note_ko": "1902년 첫 A매치 이후 우루과이 축구협회(AUF) 및 RSSSF 공인 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 21, "rank_change": 0, "fifa_points": 1619.62,
        "fifa_code": "DEN", "iso_alpha2": "dk", "name_ko": "덴마크", "name_en": "Denmark",
        "confederation": "UEFA", "flag_emoji": "🇩🇰",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "UEFA 유로 우승 1회(1992), FIFA 컨페더레이션스컵 우승 1회(1995), FIFA 월드컵 8강(1998)",
        "kit_primary_color": "#B91C1C", "kit_secondary_color": "#FFFFFF", "kit_accent_color": "#FFFFFF", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3436, "rsssf_url": "https://www.rsssf.org/miscellaneous/den-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Denmark_international_footballers",
        "historical_note_ko": "1908년 첫 공식 A매치 이후 덴마크 축구연합(DBU) 공식 기록을 따릅니다."
    },
    {
        "fifa_rank": 22, "rank_change": 1, "fifa_points": 1600.66,
        "fifa_code": "AUT", "iso_alpha2": "at", "name_ko": "오스트리아", "name_en": "Austria",
        "confederation": "UEFA", "flag_emoji": "🇦🇹",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "FIFA 월드컵 3위(1954), FIFA 월드컵 4위(1934)",
        "kit_primary_color": "#DC2626", "kit_secondary_color": "#FFFFFF", "kit_accent_color": "#111827", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3383, "rsssf_url": "https://www.rsssf.org/miscellaneous/oost-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Austria_international_footballers",
        "historical_note_ko": "1902년 첫 공식 A매치 이후 오스트리아 축구협회(ÖFB) 공인 기록을 따릅니다(1938–1945 독일 병합기 기록 분리)."
    },
    {
        "fifa_rank": 23, "rank_change": -1, "fifa_points": 1597.31,
        "fifa_code": "IRN", "iso_alpha2": "ir", "name_ko": "이란", "name_en": "IR Iran",
        "confederation": "AFC", "flag_emoji": "🇮🇷",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "AFC 아시안컵 우승 3회(1968, 1972, 1976)",
        "kit_primary_color": "#F8FAFC", "kit_secondary_color": "#15803D", "kit_accent_color": "#DC2626", "kit_text_color": "#0F172A", "kit_pattern_type": "solid",
        "tm_national_team_id": 3582, "rsssf_url": "https://www.rsssf.org/miscellaneous/iran-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Iran_international_footballers",
        "historical_note_ko": "1941년 첫 공식 A매치 이후 이란 축구연맹(FFIRI) 및 RSSSF 공인 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 24, "rank_change": 1, "fifa_points": 1587.07,
        "fifa_code": "ECU", "iso_alpha2": "ec", "name_ko": "에콰도르", "name_en": "Ecuador",
        "confederation": "CONMEBOL", "flag_emoji": "🇪🇨",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "FIFA 월드컵 16강(2006), 코파 아메리카 4위 2회(1959, 1993)",
        "kit_primary_color": "#FACC15", "kit_secondary_color": "#1E3A8A", "kit_accent_color": "#DC2626", "kit_text_color": "#0F172A", "kit_pattern_type": "solid",
        "tm_national_team_id": 5750, "rsssf_url": "https://www.rsssf.org/miscellaneous/ecua-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Ecuador_international_footballers",
        "historical_note_ko": "1938년 첫 공식 A매치 이후 에콰도르 축구연맹(FEF) 및 RSSSF 공인 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 25, "rank_change": -1, "fifa_points": 1585.86,
        "fifa_code": "EGY", "iso_alpha2": "eg", "name_ko": "이집트", "name_en": "Egypt",
        "confederation": "CAF", "flag_emoji": "🇪🇬",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "아프리카 네이션스컵 우승 7회(역대 최다: 1957, 1959, 1986, 1998, 2006, 2008, 2010)",
        "kit_primary_color": "#991B1B", "kit_secondary_color": "#111827", "kit_accent_color": "#FFFFFF", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3672, "rsssf_url": "https://www.rsssf.org/miscellaneous/egy-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/Egypt_national_football_team",
        "historical_note_ko": "1920년 첫 공식 A매치 이후 이집트 축구협회(EFA, 구 아랍공화국 시기 포함) 공식 연속 기록을 따릅니다."
    },
    {
        "fifa_rank": 26, "rank_change": 2, "fifa_points": 1585.52,
        "fifa_code": "AUS", "iso_alpha2": "au", "name_ko": "호주", "name_en": "Australia",
        "confederation": "AFC", "flag_emoji": "🇦🇺",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "AFC 아시안컵 우승 1회(2015), OFC 네이션스컵 우승 4회, FIFA 월드컵 16강 2회(2006, 2022)",
        "kit_primary_color": "#EAB308", "kit_secondary_color": "#065F46", "kit_accent_color": "#065F46", "kit_text_color": "#0F172A", "kit_pattern_type": "solid",
        "tm_national_team_id": 3433, "rsssf_url": "https://www.rsssf.org/miscellaneous/aus-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Australia_men%27s_international_soccer_players",
        "historical_note_ko": "OFC 소속 시기(~2005)와 AFC 편입 이후(2006~) 호주축구연맹(FA) 공식 A매치 기록을 통합 수록합니다."
    },
    {
        "fifa_rank": 27, "rank_change": 3, "fifa_points": 1575.31,
        "fifa_code": "CAN", "iso_alpha2": "ca", "name_ko": "캐나다", "name_en": "Canada",
        "confederation": "CONCACAF", "flag_emoji": "🇨🇦",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "CONCACAF 골드컵/선수권 우승 2회(1985, 2000), 코파 아메리카 4위(2024)",
        "kit_primary_color": "#DC2626", "kit_secondary_color": "#111827", "kit_accent_color": "#FFFFFF", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3510, "rsssf_url": "https://www.rsssf.org/miscellaneous/can-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Canada_men%27s_international_soccer_players",
        "historical_note_ko": "캐나다 축구협회(Canada Soccer) 및 RSSSF 공인 A매치 기록을 기준으로 합니다."
    },
    {
        "fifa_rank": 28, "rank_change": 1, "fifa_points": 1574.77,
        "fifa_code": "ALG", "iso_alpha2": "dz", "name_ko": "알제리", "name_en": "Algeria",
        "confederation": "CAF", "flag_emoji": "🇩🇿",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "아프리카 네이션스컵 우승 2회(1990, 2019), FIFA 아랍컵 우승 1회(2021), FIFA 월드컵 16강(2014)",
        "kit_primary_color": "#F8FAFC", "kit_secondary_color": "#15803D", "kit_accent_color": "#DC2626", "kit_text_color": "#0F172A", "kit_pattern_type": "solid",
        "tm_national_team_id": 3614, "rsssf_url": "https://www.rsssf.org/miscellaneous/alg-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/List_of_Algeria_international_footballers",
        "historical_note_ko": "1962년 독립 이후 알제리 축구연맹(FAF) 공식 A매치 기록을 따릅니다(독립 이전 FLN 비공인 경기 제외)."
    },
    {
        "fifa_rank": 29, "rank_change": 2, "fifa_points": 1569.32,
        "fifa_code": "CIV", "iso_alpha2": "ci", "name_ko": "코트디부아르", "name_en": "Côte d'Ivoire",
        "confederation": "CAF", "flag_emoji": "🇨🇮",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "아프리카 네이션스컵 우승 3회(1992, 2015, 2023)",
        "kit_primary_color": "#EA580C", "kit_secondary_color": "#15803D", "kit_accent_color": "#FFFFFF", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3591, "rsssf_url": "https://www.rsssf.org/miscellaneous/ivo-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/Ivory_Coast_national_football_team",
        "historical_note_ko": "1960년 독립 이후 코트디부아르 축구연맹(FIF) 및 RSSSF 공인 A매치 기록을 수록합니다."
    },
    {
        "fifa_rank": 30, "rank_change": -4, "fifa_points": 1567.97,
        "fifa_code": "NGA", "iso_alpha2": "ng", "name_ko": "나이지리아", "name_en": "Nigeria",
        "confederation": "CAF", "flag_emoji": "🇳🇬",
        "world_cup_titles": 0, "world_cup_winning_years": None,
        "major_honors_ko": "아프리카 네이션스컵 우승 3회(1980, 1994, 2013), FIFA 월드컵 16강 3회(1994, 1998, 2014)",
        "kit_primary_color": "#16A34A", "kit_secondary_color": "#FFFFFF", "kit_accent_color": "#064E3B", "kit_text_color": "#FFFFFF", "kit_pattern_type": "solid",
        "tm_national_team_id": 3444, "rsssf_url": "https://www.rsssf.org/miscellaneous/nig-recintlp.html",
        "wiki_list_url": "https://en.wikipedia.org/wiki/Nigeria_national_football_team",
        "historical_note_ko": "1949년/1960년 이후 나이지리아 축구연맹(NFF) 및 RSSSF 공인 A매치 기록을 수록합니다."
    },
]

SUCCESSION_MAPPINGS = [
    {
        "historical_team_code": "FRG",
        "historical_team_name_ko": "서독 (독일연방공화국, 1950–1990)",
        "historical_team_name_en": "West Germany (1950–1990)",
        "modern_fifa_code": "GER",
        "is_auto_merged": 1,
        "policy_rule_ko": "공식 기록 승계 인정 (독일 대표팀에 통합)",
        "fifa_recognition_note_ko": "FIFA와 독일축구협회(DFB)는 1908년~현재 독일 대표팀과 1950~1990년 서독 대표팀을 동일한 법적·역사적 주체로 공식 인정합니다."
    },
    {
        "historical_team_code": "GDR",
        "historical_team_name_ko": "동독 (독일민주공화국, 1952–1990)",
        "historical_team_name_en": "East Germany (1952–1990)",
        "modern_fifa_code": "GER",
        "is_auto_merged": 0,
        "policy_rule_ko": "별도 역사적 기록으로 분리 (서독/통일독일 출전 횟수와 단순 합산 금지)",
        "fifa_recognition_note_ko": "마티아스 자머, 울프 키르스텐 등 동독과 통일독일 양쪽에서 뛴 선수는 각 대표팀 출전 횟수를 분리해 30회 자격을 판정합니다."
    },
    {
        "historical_team_code": "YUG",
        "historical_team_name_ko": "유고슬라비아 (1920–1992)",
        "historical_team_name_en": "Yugoslavia (1920–1992)",
        "modern_fifa_code": "CRO",
        "is_auto_merged": 0,
        "policy_rule_ko": "크로아티아(CRO)에 무단 귀속·합산 금지",
        "fifa_recognition_note_ko": "로베르트 프로시네치키, 다보르 슈케르, 즈보니미르 보반 등 유고슬라비아 대표팀 경력이 있는 크로아티아 선수는 유고슬라비아 출전분을 제외한 순수 크로아티아 A대표팀 출전 횟수만으로 30회 이상 여부를 판정합니다."
    },
    {
        "historical_team_code": "URS",
        "historical_team_name_ko": "소련 (소비에트 연방, 1924–1991)",
        "historical_team_name_en": "Soviet Union (1924–1991)",
        "modern_fifa_code": None,
        "is_auto_merged": 0,
        "policy_rule_ko": "현대 개별 국가에 무조건 귀속·합산 금지",
        "fifa_recognition_note_ko": "소련/CIS 대표팀 기록은 우크라이나·러시아·조지아 등 신생 독립국 A매치 출전 기록과 합산하지 않고 별도 역사 코드로 분리합니다."
    },
    {
        "historical_team_code": "TCH",
        "historical_team_name_ko": "체코슬로바키아 (1920–1993)",
        "historical_team_name_en": "Czechoslovakia (1920–1993)",
        "modern_fifa_code": None,
        "is_auto_merged": 0,
        "policy_rule_ko": "현대 체코/슬로바키아 단독 기록과 합산 금지",
        "fifa_recognition_note_ko": "체코슬로바키아 해체(1993) 이전 기록은 현대 국가 단독 출전 횟수와 분리하여 관리합니다."
    }
]

# 7 Required Formations: Attack on TOP (y=16..26), Midfield (y=40..58), Defense (y=72..75), GK on BOTTOM (y=88)
FORMATIONS = [
    {
        "code": "4-3-3",
        "name_ko": "4-3-3 (클래식 윙 포워드 & 역삼각형 중원)",
        "description_ko": "측면 공격수(LW·RW)의 파괴력과 원 볼란치(CDM)·인사이드 하프(LCM·RCM)의 균형을 극대화하는 현대 축구의 표준 전술입니다.",
        "tactical_characteristics_ko": "측면 수적 우위, 전방 압박 용이, 하프스페이스 침투",
        "slots": [
            {"slot_index": 0, "slot_code": "GK",  "label_ko": "골키퍼",       "group": "GK", "x": 50, "y": 88, "compatible": ["GK"]},
            {"slot_index": 1, "slot_code": "LB",  "label_ko": "좌측 풀백",     "group": "DF", "x": 15, "y": 73, "compatible": ["LB", "LWB", "CB"]},
            {"slot_index": 2, "slot_code": "LCB", "label_ko": "좌측 센터백",   "group": "DF", "x": 37, "y": 75, "compatible": ["CB", "LCB", "RCB", "CDM"]},
            {"slot_index": 3, "slot_code": "RCB", "label_ko": "우측 센터백",   "group": "DF", "x": 63, "y": 75, "compatible": ["CB", "RCB", "LCB", "CDM"]},
            {"slot_index": 4, "slot_code": "RB",  "label_ko": "우측 풀백",     "group": "DF", "x": 85, "y": 73, "compatible": ["RB", "RWB", "CB"]},
            {"slot_index": 5, "slot_code": "LCM", "label_ko": "좌측 중앙 미드필더", "group": "MF", "x": 28, "y": 48, "compatible": ["CM", "CAM", "CDM", "LM"]},
            {"slot_index": 6, "slot_code": "CDM", "label_ko": "수비형 미드필더",   "group": "MF", "x": 50, "y": 56, "compatible": ["CDM", "CM", "CB"]},
            {"slot_index": 7, "slot_code": "RCM", "label_ko": "우측 중앙 미드필더", "group": "MF", "x": 72, "y": 48, "compatible": ["CM", "CAM", "CDM", "RM"]},
            {"slot_index": 8, "slot_code": "LW",  "label_ko": "좌측 윙어",     "group": "FW", "x": 18, "y": 23, "compatible": ["LW", "LM", "ST", "CAM"]},
            {"slot_index": 9, "slot_code": "ST",  "label_ko": "스트라이커",     "group": "FW", "x": 50, "y": 17, "compatible": ["ST", "CF", "LW", "RW", "CAM"]},
            {"slot_index": 10, "slot_code": "RW", "label_ko": "우측 윙어",     "group": "FW", "x": 82, "y": 23, "compatible": ["RW", "RM", "ST", "CAM"]}
        ]
    },
    {
        "code": "4-2-3-1",
        "name_ko": "4-2-3-1 (더블 볼란치 & 플레이메이커)",
        "description_ko": "2명의 수비형 미드필더(LDM·RDM)가 포백을 보호하고, 중앙 공격형 미드필더(CAM, 10번 롤)에게 창조적 자유를 부여하는 포메이션입니다.",
        "tactical_characteristics_ko": "10번 플레이메이커 극대화, 공수 전환 안정성, 더블 피벗 빌드업",
        "slots": [
            {"slot_index": 0, "slot_code": "GK",  "label_ko": "골키퍼",       "group": "GK", "x": 50, "y": 88, "compatible": ["GK"]},
            {"slot_index": 1, "slot_code": "LB",  "label_ko": "좌측 풀백",     "group": "DF", "x": 15, "y": 73, "compatible": ["LB", "LWB", "CB"]},
            {"slot_index": 2, "slot_code": "LCB", "label_ko": "좌측 센터백",   "group": "DF", "x": 37, "y": 75, "compatible": ["CB", "LCB", "RCB", "CDM"]},
            {"slot_index": 3, "slot_code": "RCB", "label_ko": "우측 센터백",   "group": "DF", "x": 63, "y": 75, "compatible": ["CB", "RCB", "LCB", "CDM"]},
            {"slot_index": 4, "slot_code": "RB",  "label_ko": "우측 풀백",     "group": "DF", "x": 85, "y": 73, "compatible": ["RB", "RWB", "CB"]},
            {"slot_index": 5, "slot_code": "LDM", "label_ko": "좌측 수비형 미드필더", "group": "MF", "x": 35, "y": 56, "compatible": ["CDM", "CM"]},
            {"slot_index": 6, "slot_code": "RDM", "label_ko": "우측 수비형 미드필더", "group": "MF", "x": 65, "y": 56, "compatible": ["CDM", "CM"]},
            {"slot_index": 7, "slot_code": "LAM", "label_ko": "좌측 공격형 미드필더", "group": "MF", "x": 20, "y": 35, "compatible": ["LW", "CAM", "LM", "ST"]},
            {"slot_index": 8, "slot_code": "CAM", "label_ko": "중앙 공격형 미드필더", "group": "MF", "x": 50, "y": 35, "compatible": ["CAM", "CM", "ST", "LW", "RW"]},
            {"slot_index": 9, "slot_code": "RAM", "label_ko": "우측 공격형 미드필더", "group": "MF", "x": 80, "y": 35, "compatible": ["RW", "CAM", "RM", "ST"]},
            {"slot_index": 10, "slot_code": "ST", "label_ko": "스트라이커",     "group": "FW", "x": 50, "y": 17, "compatible": ["ST", "CF", "LW", "RW"]}
        ]
    },
    {
        "code": "4-4-2",
        "name_ko": "4-4-2 (클래식 투톱 & 두 줄 수비)",
        "description_ko": "전통적인 2명의 스트라이커(LS·RS) 파트너십과 견고한 4-4 두 줄 블록을 바탕으로 직선적인 공격과 측면 크로스를 전개합니다.",
        "tactical_characteristics_ko": "투톱 콤비 플레이, 4-4 두 줄 수비 조직력, 빠른 측면 전개",
        "slots": [
            {"slot_index": 0, "slot_code": "GK",  "label_ko": "골키퍼",       "group": "GK", "x": 50, "y": 88, "compatible": ["GK"]},
            {"slot_index": 1, "slot_code": "LB",  "label_ko": "좌측 풀백",     "group": "DF", "x": 15, "y": 73, "compatible": ["LB", "LWB", "CB"]},
            {"slot_index": 2, "slot_code": "LCB", "label_ko": "좌측 센터백",   "group": "DF", "x": 37, "y": 75, "compatible": ["CB", "LCB", "RCB", "CDM"]},
            {"slot_index": 3, "slot_code": "RCB", "label_ko": "우측 센터백",   "group": "DF", "x": 63, "y": 75, "compatible": ["CB", "RCB", "LCB", "CDM"]},
            {"slot_index": 4, "slot_code": "RB",  "label_ko": "우측 풀백",     "group": "DF", "x": 85, "y": 73, "compatible": ["RB", "RWB", "CB"]},
            {"slot_index": 5, "slot_code": "LM",  "label_ko": "좌측 미드필더",   "group": "MF", "x": 16, "y": 47, "compatible": ["LW", "LM", "CM", "CAM"]},
            {"slot_index": 6, "slot_code": "LCM", "label_ko": "좌측 중앙 미드필더", "group": "MF", "x": 39, "y": 50, "compatible": ["CM", "CDM", "CAM"]},
            {"slot_index": 7, "slot_code": "RCM", "label_ko": "우측 중앙 미드필더", "group": "MF", "x": 61, "y": 50, "compatible": ["CM", "CDM", "CAM"]},
            {"slot_index": 8, "slot_code": "RM",  "label_ko": "우측 미드필더",   "group": "MF", "x": 84, "y": 47, "compatible": ["RW", "RM", "CM", "CAM"]},
            {"slot_index": 9, "slot_code": "LS",  "label_ko": "좌측 스트라이커",  "group": "FW", "x": 36, "y": 19, "compatible": ["ST", "CF", "LW", "CAM"]},
            {"slot_index": 10, "slot_code": "RS", "label_ko": "우측 스트라이커",  "group": "FW", "x": 64, "y": 19, "compatible": ["ST", "CF", "RW", "CAM"]}
        ]
    },
    {
        "code": "4-1-4-1",
        "name_ko": "4-1-4-1 (원 볼란치 & 2선 압박 블록)",
        "description_ko": "포백 앞의 단독 홀딩 미드필더(CDM)가 수비 라인을 보호하고, 4명의 2선 미드필더가 촘촘한 간격으로 중원을 장악합니다.",
        "tactical_characteristics_ko": "포백 보호 극대화, 2선 4인방의 유기적 압박과 공격 가담",
        "slots": [
            {"slot_index": 0, "slot_code": "GK",  "label_ko": "골키퍼",       "group": "GK", "x": 50, "y": 88, "compatible": ["GK"]},
            {"slot_index": 1, "slot_code": "LB",  "label_ko": "좌측 풀백",     "group": "DF", "x": 15, "y": 73, "compatible": ["LB", "LWB", "CB"]},
            {"slot_index": 2, "slot_code": "LCB", "label_ko": "좌측 센터백",   "group": "DF", "x": 37, "y": 75, "compatible": ["CB", "LCB", "RCB"]},
            {"slot_index": 3, "slot_code": "RCB", "label_ko": "우측 센터백",   "group": "DF", "x": 63, "y": 75, "compatible": ["CB", "RCB", "LCB"]},
            {"slot_index": 4, "slot_code": "RB",  "label_ko": "우측 풀백",     "group": "DF", "x": 85, "y": 73, "compatible": ["RB", "RWB", "CB"]},
            {"slot_index": 5, "slot_code": "CDM", "label_ko": "수비형 미드필더",   "group": "MF", "x": 50, "y": 60, "compatible": ["CDM", "CM", "CB"]},
            {"slot_index": 6, "slot_code": "LM",  "label_ko": "좌측 미드필더",   "group": "MF", "x": 16, "y": 41, "compatible": ["LW", "LM", "CAM"]},
            {"slot_index": 7, "slot_code": "LCM", "label_ko": "좌측 공격형/중앙 MF", "group": "MF", "x": 38, "y": 43, "compatible": ["CM", "CAM", "CDM"]},
            {"slot_index": 8, "slot_code": "RCM", "label_ko": "우측 공격형/중앙 MF", "group": "MF", "x": 62, "y": 43, "compatible": ["CM", "CAM", "CDM"]},
            {"slot_index": 9, "slot_code": "RM",  "label_ko": "우측 미드필더",   "group": "MF", "x": 84, "y": 41, "compatible": ["RW", "RM", "CAM"]},
            {"slot_index": 10, "slot_code": "ST", "label_ko": "스트라이커",     "group": "FW", "x": 50, "y": 17, "compatible": ["ST", "CF"]}
        ]
    },
    {
        "code": "3-5-2",
        "name_ko": "3-5-2 (스리백 & 윙백 지배형 투톱)",
        "description_ko": "3명의 센터백(리베로 포함)으로 후방 수적 우위를 확보하고, 양 윙백(LWB·RWB)이 측면 전체를 지배하며 투톱을 지원합니다.",
        "tactical_characteristics_ko": "리베로/스리백 빌드업, 중원 3미드필더 수적 우위, 투톱 파괴력",
        "slots": [
            {"slot_index": 0, "slot_code": "GK",  "label_ko": "골키퍼",       "group": "GK", "x": 50, "y": 88, "compatible": ["GK"]},
            {"slot_index": 1, "slot_code": "LCB", "label_ko": "좌측 스토퍼/센터백", "group": "DF", "x": 26, "y": 74, "compatible": ["CB", "LB"]},
            {"slot_index": 2, "slot_code": "CB",  "label_ko": "중앙 센터백/리베로", "group": "DF", "x": 50, "y": 76, "compatible": ["CB", "CDM"]},
            {"slot_index": 3, "slot_code": "RCB", "label_ko": "우측 스토퍼/센터백", "group": "DF", "x": 74, "y": 74, "compatible": ["CB", "RB"]},
            {"slot_index": 4, "slot_code": "LWB", "label_ko": "좌측 윙백",     "group": "MF", "x": 13, "y": 50, "compatible": ["LB", "LWB", "LW", "LM"]},
            {"slot_index": 5, "slot_code": "LCM", "label_ko": "좌측 중앙 미드필더", "group": "MF", "x": 34, "y": 48, "compatible": ["CM", "CAM", "CDM"]},
            {"slot_index": 6, "slot_code": "CDM", "label_ko": "수비형 미드필더",   "group": "MF", "x": 50, "y": 56, "compatible": ["CDM", "CM"]},
            {"slot_index": 7, "slot_code": "RCM", "label_ko": "우측 중앙 미드필더", "group": "MF", "x": 66, "y": 48, "compatible": ["CM", "CAM", "CDM"]},
            {"slot_index": 8, "slot_code": "RWB", "label_ko": "우측 윙백",     "group": "MF", "x": 87, "y": 50, "compatible": ["RB", "RWB", "RW", "RM"]},
            {"slot_index": 9, "slot_code": "LS",  "label_ko": "좌측 스트라이커",  "group": "FW", "x": 36, "y": 19, "compatible": ["ST", "CF", "LW", "CAM"]},
            {"slot_index": 10, "slot_code": "RS", "label_ko": "우측 스트라이커",  "group": "FW", "x": 64, "y": 19, "compatible": ["ST", "CF", "RW", "CAM"]}
        ]
    },
    {
        "code": "3-4-3",
        "name_ko": "3-4-3 (토탈 풋볼 & 스리톱 하이프레싱)",
        "description_ko": "스리백과 4명의 미드필더 위에 3명의 공격수(LW·ST·RW)를 배치해 경기장 전역에서 공격적인 압박과 패스 워크를 구사합니다.",
        "tactical_characteristics_ko": "전방 스리톱 압박, 측면 윙백-윙어 오버래핑, 공격적 패스 네트워크",
        "slots": [
            {"slot_index": 0, "slot_code": "GK",  "label_ko": "골키퍼",       "group": "GK", "x": 50, "y": 88, "compatible": ["GK"]},
            {"slot_index": 1, "slot_code": "LCB", "label_ko": "좌측 센터백",   "group": "DF", "x": 26, "y": 74, "compatible": ["CB", "LB"]},
            {"slot_index": 2, "slot_code": "CB",  "label_ko": "중앙 센터백",   "group": "DF", "x": 50, "y": 76, "compatible": ["CB", "CDM"]},
            {"slot_index": 3, "slot_code": "RCB", "label_ko": "우측 센터백",   "group": "DF", "x": 74, "y": 74, "compatible": ["CB", "RB"]},
            {"slot_index": 4, "slot_code": "LM",  "label_ko": "좌측 윙백/미드필더", "group": "MF", "x": 14, "y": 50, "compatible": ["LB", "LWB", "LM", "LW"]},
            {"slot_index": 5, "slot_code": "LCM", "label_ko": "좌측 중앙 미드필더", "group": "MF", "x": 38, "y": 52, "compatible": ["CM", "CDM", "CAM"]},
            {"slot_index": 6, "slot_code": "RCM", "label_ko": "우측 중앙 미드필더", "group": "MF", "x": 62, "y": 52, "compatible": ["CM", "CDM", "CAM"]},
            {"slot_index": 7, "slot_code": "RM",  "label_ko": "우측 윙백/미드필더", "group": "MF", "x": 86, "y": 50, "compatible": ["RB", "RWB", "RM", "RW"]},
            {"slot_index": 8, "slot_code": "LW",  "label_ko": "좌측 윙포워드",  "group": "FW", "x": 20, "y": 23, "compatible": ["LW", "ST", "CAM"]},
            {"slot_index": 9, "slot_code": "ST",  "label_ko": "스트라이커",     "group": "FW", "x": 50, "y": 17, "compatible": ["ST", "CF", "CAM"]},
            {"slot_index": 10, "slot_code": "RW", "label_ko": "우측 윙포워드",  "group": "FW", "x": 80, "y": 23, "compatible": ["RW", "ST", "CAM"]}
        ]
    },
    {
        "code": "4-2-2-2",
        "name_ko": "4-2-2-2 (매직 스퀘어 & 듀얼 플레이메이커)",
        "description_ko": "1982 브라질 황금중원·프랑스 매직 스퀘어로 상징되는 전술로, 2명의 수비형 MF와 2명의 공격형 MF(LAM·RAM)가 사각형 중원을 형성합니다.",
        "tactical_characteristics_ko": "중앙 매직 스퀘어 점유, 2명의 플레이메이커 공존, 풀백의 넓은 오버래핑",
        "slots": [
            {"slot_index": 0, "slot_code": "GK",  "label_ko": "골키퍼",       "group": "GK", "x": 50, "y": 88, "compatible": ["GK"]},
            {"slot_index": 1, "slot_code": "LB",  "label_ko": "좌측 풀백",     "group": "DF", "x": 15, "y": 73, "compatible": ["LB", "LWB", "CB"]},
            {"slot_index": 2, "slot_code": "LCB", "label_ko": "좌측 센터백",   "group": "DF", "x": 37, "y": 75, "compatible": ["CB", "LCB", "RCB"]},
            {"slot_index": 3, "slot_code": "RCB", "label_ko": "우측 센터백",   "group": "DF", "x": 63, "y": 75, "compatible": ["CB", "RCB", "LCB"]},
            {"slot_index": 4, "slot_code": "RB",  "label_ko": "우측 풀백",     "group": "DF", "x": 85, "y": 73, "compatible": ["RB", "RWB", "CB"]},
            {"slot_index": 5, "slot_code": "LDM", "label_ko": "좌측 수비형 미드필더", "group": "MF", "x": 36, "y": 56, "compatible": ["CDM", "CM"]},
            {"slot_index": 6, "slot_code": "RDM", "label_ko": "우측 수비형 미드필더", "group": "MF", "x": 64, "y": 56, "compatible": ["CDM", "CM"]},
            {"slot_index": 7, "slot_code": "LAM", "label_ko": "좌측 공격형 미드필더", "group": "MF", "x": 26, "y": 36, "compatible": ["CAM", "LW", "CM", "LM"]},
            {"slot_index": 8, "slot_code": "RAM", "label_ko": "우측 공격형 미드필더", "group": "MF", "x": 74, "y": 36, "compatible": ["CAM", "RW", "CM", "RM"]},
            {"slot_index": 9, "slot_code": "LS",  "label_ko": "좌측 스트라이커",  "group": "FW", "x": 36, "y": 18, "compatible": ["ST", "CF", "LW", "CAM"]},
            {"slot_index": 10, "slot_code": "RS", "label_ko": "우측 스트라이커",  "group": "FW", "x": 64, "y": 18, "compatible": ["ST", "CF", "RW", "CAM"]}
        ]
    }
]

DATA_SOURCES_CONFIG = [
    {
        "source_code": "RSSSF",
        "source_name": "Rec.Sport.Soccer Statistics Foundation (RSSSF) Countrywise International Records",
        "base_url": "https://www.rsssf.org/miscellaneous/century.html",
        "coverage_scope_ko": "1872년~2026년 7월 전 세계 국가별 역대 성인 남자 A매치 최다 출전·득점 기록 아카이브 (1900년대~2020년대 전 시대 포괄)",
        "last_updated_date": "2026-07-06",
        "terms_and_license_ko": "학술·통계 연구 아카이브 인용 허용(출처 및 저자 명시). 비공식 클럽전 및 올림픽 경기 구분 주석 포함",
        "collection_method_ko": "국가별 *-recintlp.html 정적 아카이브 파싱 및 A매치 30회 이상 검증"
    },
    {
        "source_code": "TM_DATASETS",
        "source_name": "dcaribou/transfermarkt-datasets (Open Football Dataset on GitHub/Cloudflare R2)",
        "base_url": "https://github.com/dcaribou/transfermarkt-datasets",
        "coverage_scope_ko": "선수 50,149명의 세부 포지션(주/부포지션), 신체 조건(키·주발), 생년월일, 소속 클럽, A매치 출전·득점, 프로필 이미지 URL (2026-07-06 스냅샷)",
        "last_updated_date": "2026-07-06",
        "terms_and_license_ko": "CC0 1.0 Universal Public Domain Dedication (공개 데이터셋)",
        "collection_method_ko": "공식 R2 패키지(players.csv.gz, national_teams.csv.gz, countries.csv.gz) 다운로드 및 교차 매칭"
    },
    {
        "source_code": "WIKIPEDIA_INTL",
        "source_name": "Wikipedia 'List of [Country] international footballers' & National Team Records",
        "base_url": "https://en.wikipedia.org/wiki/List_of_men%27s_footballers_with_100_or_more_international_caps",
        "coverage_scope_ko": "30개국 역대 국가대표 선수별 포지션(GK/DF/MF/FW), 생몰년, 활동 연도, 각국 축구협회(FA) 인용 A매치 출전·득점 표",
        "last_updated_date": "2026-10-15",
        "terms_and_license_ko": "CC BY-SA 4.0 (크리에이티브 커먼즈 저작자표시-동일조건변경허락 4.0)",
        "collection_method_ko": "MediaWiki Action API (action=parse) 정식 호출을 통한 HTML 위키테이블 구조화"
    },
    {
        "source_code": "WIKIDATA_COMMONS",
        "source_name": "Wikidata & Wikimedia Commons",
        "base_url": "https://www.wikidata.org",
        "coverage_scope_ko": "한국어 선수명(ko label), 생년월일·사망 여부, 수상 경력(월드컵·발롱도르), 자유 라이선스(CC BY-SA / Public Domain) 선수 초상 사진",
        "last_updated_date": "2026-10-15",
        "terms_and_license_ko": "Wikidata CC0 1.0 / Wikimedia Commons 개별 파일 CC BY-SA·Public Domain 라이선스 및 저작자 표기 준수",
        "collection_method_ko": "MediaWiki/Wikidata API 및 검증된 레전드 메타데이터 매핑"
    },
    {
        "source_code": "FIFA_RANKING",
        "source_name": "FIFA/Coca-Cola Men's World Ranking Official Release",
        "base_url": "https://inside.fifa.com/fifa-world-ranking/men",
        "coverage_scope_ko": "2026년 10월 7일 발표 공식 FIFA 남자 세계랭킹 상위 30개국 순위 및 포인트",
        "last_updated_date": "2026-10-07",
        "terms_and_license_ko": "공식 발표 통계 인용 (국가 마스터 테이블과 랭킹 스냅샷 분리 저장)",
        "collection_method_ko": "2026-10-07 기준 스냅샷 적재 및 관리자 수동/CSV 갱신 지원"
    }
]
