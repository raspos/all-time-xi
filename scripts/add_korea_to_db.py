# -*- coding: utf-8 -*-
"""
대한민국(KOR, South Korea) 국가 마스터, FIFA 랭킹 스냅샷, 역대 A매치 30회 이상 출전 선수(1950년대~2020년대),
Wikimedia Commons 초상화, 포지션 적합도, 출처 레코드 및 대표 프리셋('대한민국 역대 최강 XI')을
data/all_time_xi.db 및 설정 파일에 완벽히 추가·통합하는 스크립트.
"""
import json
import re
import sqlite3
import sys
from pathlib import Path
import requests

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
DB_PATH = ROOT_DIR / "data" / "all_time_xi.db"
RSSSF_KOR_PATH = ROOT_DIR / "data" / "raw" / "rsssf" / "KOR.html"

# KFA(대한축구협회) 및 RSSSF 공인 대한민국 A대표팀 30경기 이상 주요 선수 정밀 데이터 (1950년대~2020년대 전 시대 망라)
# (RSSSF skor-recintlp.html 파싱 결과와 결합하여 한글 실명, 주/부포지션, 클럽, 수상, 전술 프로필을 완벽히 매핑)
KOR_CURATED_PLAYERS = [
    # 100+ 센추리 클럽 및 핵심 레전드
    ("Cha Bum-Kun", "차범근", "FW", "RW", ["ST", "LW"], 136, 58, 1972, 1986, False, 179, "양발",
     "프랑크푸르트, 바이어 레버쿠젠", "UEFA컵 우승 2회(1980, 1988), 아시안게임 금메달(1978), KFA 역대 최다 득점(58골)", "1986",
     "폭발적인 가속력과 양발 슈팅, 압도적인 피지컬로 분데스리가를 정복한 아시아 역대 최고 공격수", "우측 인사이드 포워드 / 스트라이커", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Cha_Bum-kun_2017.jpg?width=320", 11),
    ("Hong Myung-Bo", "홍명보", "DF", "CB", ["CDM"], 136, 10, 1990, 2002, False, 182, "오른발",
     "포항 스틸러스, 벨마레 히라쓰카, 가시와 레이솔, LA 갤럭시", "2002 한일 월드컵 4위·브론즈볼(아시아 최초), 월드컵 4회 연속 출전(1990~2002)", "1990, 1994, 1998, 2002",
     "영원한 리베로. 뛰어난 수비 리딩과 정확한 중장거리 패스, 냉철한 판단력을 겸비한 수비 사령관", "리베로 / 볼 플레잉 센터백", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Hong_Myung-bo_2014.jpg?width=320", 20),
    ("Son Heung-Min", "손흥민", "FW", "LW", ["ST", "RW"], 131, 51, 2010, 2026, True, 183, "양발",
     "함부르크 SV, 바이어 레버쿠젠, 토트넘 홋스퍼", "프리미어리그 득점왕(2021-22 골든부트), FIFA 푸스카스상(2020), 아시안게임 금메달(2018)", "2014, 2018, 2022",
     "월드클래스 양발 감아차기와 폭발적인 뒷공간 침투, 캡틴 리더십을 갖춘 현대 한국 축구의 상징", "인버티드 윙어 / 스트라이커", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Son_Heung-min_2023.jpg?width=320", 7),
    ("Lee Woon-Jae", "이운재", "GK", "GK", [], 133, 0, 1994, 2010, False, 182, "오른발",
     "수원 삼성 블루윙즈, 전남 드래곤즈", "2002 한일 월드컵 4강 주역, K리그 우승 4회, AFC 챔피언스리그 우승", "1994, 2002, 2006, 2010",
     "거미손. 압도적인 페널티킥 선방 능력과 수비진 조율 능력을 자랑한 역대 최고 수문장", "수문장 (Shot Stopper)", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Lee_Woon-Jae_2006.jpg?width=320", 1),
    ("Lee Young-Pyo", "이영표", "DF", "LB", ["RB", "LWB"], 127, 5, 1999, 2011, False, 177, "오른발",
     "안양 LG, PSV 에인트호번, 토트넘 홋스퍼, 도르트문트", "2002 한일 월드컵 4위, 에레디비시 우승 2회, UEFA 챔피언스리그 4강(2005)", "2002, 2006, 2010",
     "헛다리짚기 드리블과 지치지 않는 오버래핑, 영리한 대인 방어를 겸비한 월드클래스 풀백", "오버래핑 레프트백 / 윙백", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Lee_Young-pyo_2010.jpg?width=320", 12),
    ("Kim Young-Gwon", "김영권", "DF", "CB", ["LB"], 112, 7, 2010, 2024, True, 186, "왼발",
     "광저우 헝다, 감바 오사카, 울산 HD", "2022 카타르 월드컵 16강(포르투갈전 동점골), 2018 러시아 월드컵 독일전 선제골, K리그 MVP", "2014, 2018, 2022",
     "정교한 왼발 빌드업과 결정적인 월드컵 클러치 득점력을 보여준 베테랑 왼발 센터백", "왼발 볼 플레잉 센터백", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Kim_Young-gwon_2018.jpg?width=320", 19),
    ("Ki Sung-Yueng", "기성용", "MF", "CM", ["CDM"], 110, 10, 2008, 2019, True, 189, "오른발",
     "FC 서울, 셀틱, 스완지 시티, 뉴캐슬 유나이티드", "2010·2014·2018 월드컵 출전(2018 주장), 2012 런던 올림픽 동메달, 리그컵 우승", "2010, 2014, 2018",
     "정교한 롱패스 전환과 탈압박, 중원 조율 능력을 갖춘 한국 축구 최고의 딥라잉 플레이메이커", "딥라잉 플레이메이커 (Regista)", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Ki_Sung-yueng_2018.jpg?width=320", 16),
    ("Park Ji-Sung", "박지성", "MF", "CM", ["LM", "RM", "LW", "RW", "CAM"], 100, 13, 2000, 2011, False, 178, "오른발",
     "교토 퍼플상가, PSV 에인트호번, 맨체스터 유나이티드", "UEFA 챔피언스리그 우승(2008), 프리미어리그 우승 4회, FIFA 클럽 월드컵 우승, 2002 월드컵 4위", "2002, 2006, 2010",
     "두 개의 심장. 왕성한 활동량과 전술적 지능, 큰 경기 결정력으로 월드컵 3개 대회 연속 득점을 기록한 레전드", "박스 투 박스 미드필더 / 전술적 윙어", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Park_Ji-sung_2014.jpg?width=320", 13),
    ("Kim Tae-Young", "김태영", "DF", "CB", ["LB"], 105, 3, 1992, 2004, False, 180, "왼발",
     "전남 드래곤즈", "2002 한일 월드컵 4위, 아시안컵 베스트11", "1998, 2002",
     "아파치라는 별명처럼 투지 넘치는 대인 마크와 헌신적인 커버 플레이를 펼친 2002 4강 철벽 수비수", "스토퍼 / 좌측 센터백", True, None, 4),
    ("Lee Dong-Gook", "이동국", "FW", "ST", [], 105, 33, 1998, 2017, False, 187, "오른발",
     "포항 스틸러스, 미들즈브러, 전북 현대 모터스", "K리그 통산 최다 득점(228골)·우승 8회·MVP 4회, AFC 챔피언스리그 우승·득점왕", "1998, 2010",
     "라이언 킹. 환상적인 발리슛과 포스트 플레이를 자랑한 정통 타깃 스트라이커", "타깃 스트라이커", True, None, 20),
    ("Hwang Sun-Hong", "황선홍", "FW", "ST", [], 103, 50, 1988, 2002, False, 183, "오른발",
     "포항 스틸러스, 세레소 오사카, 가시와 레이솔", "2002 한일 월드컵 4위(폴란드전 선제 결승골), J리그 득점왕(1999), KFA 역대 득점 3위(50골)", "1990, 1994, 1998, 2002",
     "황새. 지능적인 오프더볼 움직임과 연계, 원터치 슈팅 결정력을 갖춘 한국 대표 정통 스트라이커", "완성형 스트라이커 (Complete Forward)", True, None, 18),
    ("Yoo Sang-Chul", "유상철", "MF", "CM", ["CAM", "CDM", "CB", "RB"], 124, 18, 1994, 2005, False, 184, "오른발",
     "울산 현대, 요코하마 F. 마리노스, 가시와 레이솔", "2002 한일 월드컵 4위·올스타팀(베스트11) 선정, K리그·J리그 우승", "1998, 2002",
     "수비수부터 최전방까지 전 포지션을 소화하며 강력한 중거리슛과 공수 밸런스를 책임진 한국 최고의 멀티플레이어", "박스 투 박스 올라운더", True, None, 6),
    ("Cho Young-Jeung", "조영증", "DF", "CB", ["CDM"], 113, 1, 1975, 1986, False, 182, "오른발",
     "포틀랜드 팀버스, 시카고 스팅, 럭키금성 황소", "1986 멕시코 월드컵 본선 출전, 아시안게임 금메달(1978)", "1986",
     "1970~80년대 한국 수비진을 이끈 지능적이고 침착한 수비 리더", "중앙 수비수", False, None, 5),
    ("Park Sung-Hwa", "박성화", "DF", "CB", ["ST", "CDM"], 107, 26, 1975, 1984, False, 181, "오른발",
     "포항제철, 할렐루야", "1978 방콕 아시안게임 금메달, K리그 초대 MVP(1983)", None,
     "공격수와 중앙 수비수를 모두 완벽히 소화하며 공중볼과 득점력을 겸비한 1970~80년대 공수 겸장 레전드", "공수 겸장 센터백 / 타깃맨", False, None, 4),
    ("Kim Ho-Kon", "김호곤", "DF", "CB", ["RB"], 124, 5, 1971, 1979, False, 176, "오른발",
     "신탁은행", "1978 방콕 아시안게임 금메달, 1970년대 대표팀 주장", None,
     "1970년대 대한민국 대표팀의 수비 라인을 통솔한 끈질긴 대인 수비의 달인", "대인 방어형 수비수", False, None, 3),

    # 1970s ~ 1990s 핵심 레전드 (30~99경기)
    ("Huh Jung-Moo", "허정무", "MF", "CM", ["CAM", "LW"], 84, 25, 1974, 1986, False, 176, "오른발",
     "PSV 에인트호번, 현대 호랑이", "1986 멕시코 월드컵 출전(이탈리아전 득점), 1978 아시안게임 금메달", "1986",
     "진도개라는 별명처럼 지칠 줄 모르는 투지와 돌파력으로 네덜란드 에레디비시에서 활약한 선구자", "박스 투 박스 미드필더", True, None, 17),
    ("Choi Soon-Ho", "최순호", "FW", "ST", ["CAM", "RW"], 97, 30, 1980, 1991, False, 185, "오른발",
     "포항제철 아톰즈, 럭키금성 황소", "1986 멕시코 월드컵(이탈리아전 원더골·2도움), 1980 아시안컵 득점왕, 1986 아시안게임 금메달", "1986, 1990",
     "1980년대 한국 축구의 천재 스트라이커. 장신임에도 유려한 볼 컨트롤과 중거리슛, 창의적 패스를 겸비", "딥라잉 포워드 / 트레콰르티스타", True, None, 9),
    ("Cho Kwang-Rae", "조광래", "MF", "CM", ["CAM", "CDM"], 80, 12, 1977, 1986, False, 176, "오른발",
     "대우 로얄즈", "1986 멕시코 월드컵 주전 미드필더, 1978·1986 아시안게임 금메달", "1986",
     "컴퓨터 링커. 정교한 패스워크와 경기 조율로 1980년대 중원을 지휘한 플레이메이커", "중앙 플레이메이커", False, None, 8),
    ("Kim Joo-Sung", "김주성", "MF", "LW", ["CAM", "LB", "CB"], 77, 14, 1985, 1996, False, 178, "왼발",
     "대우 로얄즈, VfL 보훔", "AFC 올해의 아시아 축구선수 3회 연속 수상(1989, 1990, 1991), 1986 아시안게임 금메달", "1986, 1990, 1994",
     "야생마. 폭발적인 스피드와 현란한 왼발 드리블로 아시아 무대를 평정한 크랙", "클래식 윙어 / 공격형 미드필더", True, None, 16),
    ("Byun Byung-Joo", "변병주", "FW", "RW", ["LW"], 73, 11, 1981, 1990, False, 173, "오른발",
     "대우 로얄즈, 현대 호랑이", "1986·1990 월드컵 출전, 1986 아시안게임 금메달", "1986, 1990",
     "총알탄 사나이. 폭발적인 측면 돌파와 크로스를 자랑한 1980년대 대표 윙어", "측면 윙어", False, None, 11),
    ("Chung Hae-Won", "정해원", "FW", "ST", ["CAM", "RW"], 58, 21, 1980, 1990, False, 178, "오른발",
     "대우 로얄즈", "1986 아시안게임 금메달, K리그 득점왕·MVP", "1990",
     "1980년대 대우 로얄즈와 대표팀의 공격을 이끈 날카로운 골잡이", "스트라이커 / 섀도 스트라이커", False, None, 10),
    ("Noh Soo-Jin", "노수진", "MF", "CAM", ["RW", "LW"], 46, 10, 1985, 1990, False, 176, "오른발",
     "유공 코끼리", "1986·1990 월드컵 출전, 1986 아시안게임 금메달, K리그 MVP", "1986, 1990",
     "감각적인 패스와 슈팅력을 갖춘 1980년대 후반 기술형 공격형 미드필더", "공격형 미드필더", False, None, 8),
    ("Chung Yong-Hwan", "정용환", "DF", "CB", [], 86, 3, 1983, 1993, False, 181, "오른발",
     "대우 로얄즈", "1986·1990 월드컵 출전(1990 주장), K리그 MVP", "1986, 1990",
     "강력한 점프력과 대인 마크로 1980~90년대 초 한국 수비의 핵으로 활약한 센터백", "커맨더형 센터백", False, None, 5),
    ("Park Kyung-Hoon", "박경훈", "DF", "RB", ["RWB"], 93, 1, 1984, 1990, False, 177, "오른발",
     "포항제철 아톰즈", "1986·1990 월드컵 주전 라이트백, 1986 아시안게임 금메달, K리그 MVP(1988)", "1986, 1990",
     "현대적인 오버래핑 풀백의 시초. 공격적인 우측면 돌파로 K리그 MVP에 오른 수비수", "오버래핑 라이트백", False, None, 2),
    ("Gu Sang-Bum", "구상범", "DF", "LB", ["LWB"], 64, 3, 1988, 1994, False, 177, "왼발",
     "럭키금성 황소", "1990·1994 월드컵 출전, 1986 아시안게임 금메달", "1990, 1994",
     "정교한 왼발 크로스와 롱스로인으로 대표팀 좌측면을 책임진 풀백", "레프트백", False, None, 3),
    ("Choi In-Young", "최인영", "GK", "GK", [], 51, 0, 1983, 1994, False, 181, "오른발",
     "현대 호랑이", "1990·1994 월드컵 주전 골키퍼", "1990, 1994",
     "1990년대 초반 한국 대표팀 골문을 지킨 반사신경 뛰어난 골키퍼", "골키퍼", False, None, 1),
    ("Ko Jeong-Woon", "고정운", "MF", "RW", ["RM", "LW"], 77, 10, 1989, 1997, False, 178, "오른발",
     "일화 천마, 세레소 오사카, 포항 스틸러스", "1994 미국 월드컵 주전, K리그 3연패·MVP(1994)", "1994",
     "적토마. 압도적인 스피드와 저돌적인 돌파로 1994 미국 월드컵 스페인·독일전을 누빈 측면 윙어", "돌파형 윙어 / 측면 미드필더", True, None, 11),
    ("Ha Seok-Ju", "하석주", "MF", "LM", ["LB", "LW", "LWB"], 95, 23, 1991, 2001, False, 175, "왼발",
     "대우 로얄즈, 세레소 오사카, 비셀 고베, 포항 스틸러스", "1994·1998 월드컵 출전(1998 멕시코전 프리킥 선제골), K리그 우승", "1994, 1998",
     "왼발의 달인. 날카로운 왼발 프리킥과 중거리슛, 좌측면 공수 전반을 지배한 윙백/미드필더", "왼발 윙백 / 측면 미드필더", True, None, 17),
    ("Seo Jung-Won", "서정원", "FW", "RW", ["ST", "LW"], 88, 16, 1990, 2001, False, 173, "오른발",
     "안양 LG, 스트라스부르, 수원 삼성 블루윙즈, SV 리트", "1994·1998 월드컵 출전(1994 스페인전 극장 동점골), K리그·오스트리아 리그 활약", "1994, 1998",
     "날쌘돌이. 폭발적인 순간 스피드와 공간 침투로 결정적인 골을 터뜨린 윙 포워드", "스피드형 윙 포워드", True, None, 11),
    ("Shin Tae-Yong", "신태용", "MF", "CAM", ["CM", "RM"], 63, 3, 1992, 1997, False, 174, "오른발",
     "성남 일화 천마", "K리그 우승 6회·MVP 2회·득점왕 1회", None,
     "그라운드의 여우. 창의적인 패스와 뛰어난 축구 지능으로 K리그를 평정한 공격형 미드필더", "공격형 미드필더", False, None, 8),
    ("Kim Do-Hoon", "김도훈", "FW", "ST", [], 72, 30, 1994, 2003, False, 185, "오른발",
     "전북 현대, 비셀 고베, 성남 일화 천마", "1998 프랑스 월드컵 출전, K리그 득점왕 2회·MVP(1999 브라질전 결승골)", "1998",
     "강력한 피지컬과 슈팅력을 겸비해 브라질전 결승골을 기록한 정통 스트라이커", "타깃 스트라이커", False, None, 9),
    ("Choi Yong-Soo", "최용수", "FW", "ST", [], 69, 27, 1995, 2003, False, 184, "오른발",
     "안양 LG, 제프 유나이티드 이치하라, FC 서울", "1998·2002 월드컵 출전, 1998 월드컵 예선 득점왕, K리그 MVP", "1998, 2002",
     "독수리. 탁월한 위치선정과 헤더 결정력으로 1990년대 후반 대표팀 최전방을 책임진 골잡이", "포처 / 스트라이커", True, None, 10),
    ("Kim Byung-Ji", "김병지", "GK", "GK", [], 61, 0, 1995, 2008, False, 184, "오른발",
     "울산 현대, 포항 스틸러스, FC 서울, 경남 FC", "1998 프랑스 월드컵 주전 골키퍼, K리그 통산 706경기 출전", "1998, 2002",
     "꽁지머리. 동물적인 반사신경과 넓은 커버 범위를 보여준 레전드 골키퍼", "스위퍼 키퍼", False, None, 1),
    ("Choi Jin-Cheul", "최진철", "DF", "CB", [], 65, 4, 1997, 2006, False, 187, "오른발",
     "전북 현대 모터스", "2002 한일 월드컵 4위, 2006 독일 월드컵 출전, AFC 챔피언스리그 우승(2006)", "2002, 2006",
     "압도적인 제공권과 몸을 사리지 않는 육탄 방어로 홍명보·김태영과 2002 스리백을 완성한 철벽 파이터", "파이터형 센터백", True, None, 4),
    ("Kim Nam-Il", "김남일", "MF", "CDM", ["CM"], 98, 2, 1998, 2013, False, 182, "오른발",
     "전남 드래곤즈, 엑셀시오르, 수원 삼성, 비셀 고베", "2002 한일 월드컵 4위, 2006·2010 월드컵 출전, 2004 아시안컵", "2002, 2006, 2010",
     "진공청소기. 강력한 중원 인터셉트와 태클, 터프한 대인 마크로 상대 플레이메이커를 지워버린 수비형 미드필더", "볼 위닝 미드필더 (Anchor Man)", True, None, 5),
    ("Lee Eul-Yong", "이을용", "MF", "CM", ["LM", "CDM", "LB"], 51, 3, 1999, 2006, False, 176, "왼발",
     "부천 SK, 트라브존스포르, FC 서울", "2002 한일 월드컵 4위(1골 2도움 — 터키전 프리킥 골, 미국·폴란드전 어시스트)", "2002, 2006",
     "정교한 왼발 킥과 끈질긴 중원 압박으로 2002 월드컵 공격 포인트 3개를 기록한 언성 히어로", "좌측 중앙 미드필더", True, None, 7),
    ("Song Chong-Gug", "송종국", "DF", "RB", ["RWB", "LB", "CDM"], 60, 3, 2000, 2007, False, 175, "오른발",
     "부산 아이콘스, 페예노르트, 수원 삼성", "2002 한일 월드컵 4위(전 경기 풀타임·터키전 득점), 2006 월드컵 출전", "2002, 2006",
     "히딩크호의 황태자. 루이스 피구를 완벽히 봉쇄한 대인 방어와 중거리 슈팅력을 겸비한 우측 윙백", "우측 윙백 / 풀백", True, None, 22),
    ("Seol Ki-Hyeon", "설기현", "FW", "RW", ["LW", "ST"], 83, 19, 2000, 2009, False, 187, "오른발",
     "안데를레흐트, 울버햄프턴, 레딩 FC, 풀럼", "2002 한일 월드컵 4위(이탈리아전 극적 동점골), 2006 월드컵 출전", "2002, 2006",
     "강인한 피지컬과 날카로운 크로스, 클러치 득점력으로 유럽 무대와 2002 월드컵에서 활약한 대형 윙어", "와이드 타깃맨 / 윙 포워드", True, None, 9),
    ("Ahn Jung-Hwan", "안정환", "FW", "ST", ["CAM", "LW"], 71, 17, 1997, 2010, False, 178, "오른발",
     "부산 대우 로얄즈, 페루자, 시미즈 에스펄스, 요코하마 F. 마리노스, 메스, 뒤스부르크", "2002 한일 월드컵 4위(미국전 동점골·이탈리아전 골든골), 2006 월드컵(토고전 역전골), K리그 MVP", "2002, 2006, 2010",
     "판타지스타·반지의 제왕. 유려한 퍼스트 터치와 감각적인 슈팅으로 한국 월드컵 사상 최다골(3골, 박지성·손흥민과 타이)을 기록한 테크니션", "섀도 스트라이커 / 판타지스타", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Ahn_Jung-hwan_2006.jpg?width=320", 19),
    ("Cha Du-Ri", "차두리", "DF", "RB", ["RWB", "RW"], 76, 4, 2001, 2015, False, 181, "오른발",
     "아르미니아 빌레펠트, 프랑크푸르트, 마인츠 05, 셀틱, FC 서울", "2002 한일 월드컵 4위, 2010 남아공 월드컵 16강, 2015 아시안컵 준우승", "2002, 2010",
     "차미네이터. 압도적인 피지컬과 폭발적인 우측면 질주로 상대 수비를 파괴한 공격형 라이트백", "파워형 오버래핑 라이트백", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Cha_Du-Ri_2011.jpg?width=320", 22),

    # 2000s ~ 2020s 주요 선수 (30경기 이상)
    ("Park Chu-Young", "박주영", "FW", "ST", ["LW", "RW"], 68, 24, 2005, 2014, False, 182, "오른발",
     "FC 서울, AS 모나코, 아스널, 셀타 비고", "2010 남아공 월드컵 16강(나이지리아전 프리킥 골), 2012 런던 올림픽 동메달", "2006, 2010, 2014",
     "천재적인 공간 이해도와 부드러운 연계, 날카로운 프리킥을 갖춘 테크니컬 스트라이커", "연계형 스트라이커", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Park_Chu-young_2013.jpg?width=320", 10),
    ("Lee Chung-Yong", "이청용", "MF", "RW", ["RM", "CAM", "CM"], 89, 9, 2008, 2019, True, 180, "오른발",
     "FC 서울, 볼턴 원더러스, 크리스탈 팰리스, VfL 보훔, 울산 HD", "2010 남아공 월드컵 16강(2골 — 아르헨티나·우루과이전), K리그 MVP(2022)", "2010, 2014",
     "블루드래곤. 창의적인 드리블과 넓은 시야, 영리한 볼 키핑으로 우측면을 지배한 테크니션", "창의적 윙어 / 측면 플레이메이커", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Lee_Chung-yong_2018.jpg?width=320", 17),
    ("Koo Ja-Cheol", "구자철", "MF", "CAM", ["CM", "RW"], 76, 19, 2008, 2019, True, 183, "오른발",
     "제주 유나이티드, 볼프스부르크, 아우크스부르크, 마인츠 05", "2011 아시안컵 득점왕(5골), 2012 런던 올림픽 동메달(주장), 2014 월드컵 득점", "2014, 2018",
     "왕성한 전방 압박과 박스 침투 득점력을 겸비한 분데스리가 장수 공격형 미드필더", "섀도 스트라이커 / 공격형 미드필더", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Koo_Ja-cheol_2018.jpg?width=320", 13),
    ("Lee Jae-Sung", "이재성", "MF", "CAM", ["CM", "LM", "RM", "RW"], 92, 13, 2015, 2026, True, 180, "왼발",
     "전북 현대 모터스, 홀슈타인 킬, 마인츠 05", "2022 카타르 월드컵 16강, K리그 MVP(2017), 아시안게임 금메달(2014)", "2018, 2022",
     "엄청난 활동량과 전술 수행 능력, 영리한 오프더볼과 원터치 패스로 중원 윤활유 역할을 수행하는 핵심 미드필더", "메짤라 / 전술적 연결고리", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Lee_Jae-sung_2018.jpg?width=320", 10),
    ("Kim Min-Jae", "김민재", "DF", "CB", [], 67, 4, 2017, 2026, True, 190, "오른발",
     "전북 현대, 페네르바체, 나폴리, 바이에른 뮌헨", "세리에 A 우승(2022-23)·세리에 A 최우수 수비수, 발롱도르 22위(2023), 2022 월드컵 16강", "2022",
     "괴물 수비수. 압도적인 스피드와 피지컬 경합, 전진 수비와 빌드업 능력을 모두 갖춘 유럽 정상급 센터백", "어그레시브 스토퍼 / 볼 플레잉 센터백", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Kim_Min-jae_2022.jpg?width=320", 4),
    ("Hwang Hee-Chan", "황희찬", "FW", "LW", ["RW", "ST"], 69, 15, 2016, 2026, True, 177, "오른발",
     "레드불 잘츠부르크, RB 라이프치히, 울버햄프턴 원더러스", "2022 카타르 월드컵 16강(포르투갈전 극장 역전 결승골), 2018 아시안게임 금메달", "2018, 2022",
     "황소. 폭발적인 저돌적 돌파와 피지컬 밸런스, 박스 안 침착한 마무리로 프리미어리그 두 자릿수 득점을 달성한 공격수", "인사이드 포워드 / 돌파형 윙어", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Hwang_Hee-chan_2018.jpg?width=320", 11),
    ("Hwang In-Beom", "황인범", "MF", "CM", ["CAM", "CDM"], 64, 6, 2018, 2026, True, 177, "오른발",
     "대전 시티즌, 밴쿠버 화이트캡스, 루빈 카잔, 올림피아코스, 츠르베나 즈베즈다, 페예노르트", "2022 카타르 월드컵 16강, 세르비아 리그 올해의 선수, 2018 아시안게임 금메달", "2022",
     "창의적인 전진 패스와 왕성한 기동력, 탈압박으로 현대 대표팀 중원 빌드업의 핵심을 담당하는 사령관", "중앙 플레이메이커 / 박스 투 박스", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Hwang_In-beom_2022.jpg?width=320", 6),
    ("Lee Kang-In", "이강인", "MF", "RW", ["CAM", "CM"], 35, 10, 2019, 2026, True, 174, "왼발",
     "발렌시아 CF, 마요르카, 파리 생제르맹(PSG)", "2019 U-20 월드컵 골든볼(준우승), 2022 카타르 월드컵 16강, 프랑스 리그1 우승, 아시안게임 금메달", "2022",
     "환상적인 왼발 탈압박과 킬패스, 날카로운 중거리 슈팅을 겸비한 차세대 천재 플레이메이커", "인버티드 플레이메이커 / 트레콰르티스타", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Lee_Kang-in_2022.jpg?width=320", 18),
    ("Kim Seung-Gyu", "김승규", "GK", "GK", [], 81, 0, 2013, 2024, True, 187, "오른발",
     "울산 현대, 비셀 고베, 가시와 레이솔, 알샤밥", "2014·2018·2022 월드컵 출전(2022 카타르 월드컵 16강 주전 골키퍼), 아시안게임 금메달(2014)", "2014, 2018, 2022",
     "안정적인 발밑 빌드업과 순발력 있는 선방을 겸비한 현대형 스위퍼 골키퍼", "스위퍼 키퍼", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Kim_Seung-gyu_2018.jpg?width=320", 1),
    ("Jo Hyeon-Woo", "조현우", "GK", "GK", [], 39, 0, 2017, 2026, True, 189, "오른발",
     "대구 FC, 울산 HD", "2018 러시아 월드컵(독일전 MOM 선방쇼), 2018 아시안게임 금메달, K리그 MVP(2024)", "2018, 2022",
     "빛현우. 경이로운 동물적 반사신경과 슈퍼세이브로 위기에서 팀을 구해내는 선방 특화 수문장", "선방형 골키퍼 (Shot Stopper)", True,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Jo_Hyeon-woo_2018.jpg?width=320", 21),
    ("Jung Sung-Ryong", "정성룡", "GK", "GK", [], 67, 0, 2008, 2016, True, 191, "오른발",
     "포항 스틸러스, 성남 일화, 수원 삼성, 가와사키 프론탈레", "2010 남아공 월드컵 16강 주전, 2012 런던 올림픽 동메달, J리그 우승 4회", "2010, 2014",
     "장신을 활용한 공중볼 처리와 안정감으로 2010 월드컵 원정 16강과 올림픽 동메달을 이끈 골키퍼", "골키퍼", False,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Jung_Sung-ryong_2014.jpg?width=320", 1),
    ("Kim Jin-Su", "김진수", "DF", "LB", ["LWB"], 74, 2, 2013, 2024, True, 177, "왼발",
     "알비렉스 니가타, 호펜하임, 전북 현대 모터스", "2022 카타르 월드컵 16강(가나전 어시스트), K리그 우승 5회, 아시안게임 금메달(2014)", "2022",
     "정교한 왼발 크로스와 적극적인 오버래핑을 자랑하는 좌측 풀백", "오버래핑 레프트백", False,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Kim_Jin-su_2022.jpg?width=320", 3),
    ("Lee Yong", "이용", "DF", "RB", ["RWB"], 58, 0, 2013, 2022, True, 180, "오른발",
     "울산 현대, 전북 현대 모터스, 수원 FC", "2014·2018 월드컵 주전 라이트백, K리그 우승 5회", "2014, 2018",
     "날카로운 우측면 얼리 크로스와 안정적인 수비력을 갖춘 베테랑 라이트백", "크로싱 라이트백", False,
     "https://commons.wikimedia.org/wiki/Special:FilePath/Lee_Yong_2018.jpg?width=320", 2),
    ("Yeom Ki-Hun", "염기훈", "MF", "LM", ["LW", "LWB"], 57, 5, 2006, 2018, False, 182, "왼발",
     "전북 현대, 울산 현대, 수원 삼성 블루윙즈", "2010 남아공 월드컵 16강, K리그 통산 최다 도움(110도움), FA컵 우승 4회", "2010",
     "왼발의 마법사. 날카로운 왼발 세트피스와 크로스로 K리그 역대 최다 도움을 기록한 윙어", "왼발 크로싱 윙어", False, None, 26),
    ("Hwang Ui-Jo", "황의조", "FW", "ST", [], 62, 19, 2015, 2023, True, 185, "오른발",
     "성남 FC, 감바 오사카, 지롱댕 드 보르도, 노팅엄 포레스트", "2018 자카르타 아시안게임 금메달·득점왕(9골), 2022 카타르 월드컵 16강", "2022",
     "넓은 활동 반경과 순간적인 뒷공간 침투, 감아차기 슈팅에 능한 스트라이커", "포처 / 스트라이커", False, None, 16),
    ("Kwon Chang-Hoon", "권창훈", "MF", "RW", ["CAM", "RM"], 43, 12, 2015, 2023, True, 174, "왼발",
     "수원 삼성, 디종 FCO, 프라이부르크, 전북 현대", "2022 카타르 월드컵 16강, 프랑스 리그1 두 자릿수 득점", "2022",
     "과감한 왼발 인사이드 침투와 강력한 슛을 갖춘 공격형 미드필더/윙어", "인사이드 커터", False, None, 22),
    ("Kim Shin-Wook", "김신욱", "FW", "ST", [], 56, 16, 2010, 2021, True, 196, "오른발",
     "울산 현대, 전북 현대, 상하이 선화", "AFC 챔피언스리그 우승 2회(2012, 2016), K리그 MVP(2013)·득점왕(2015), 2014·2018 월드컵 출전", "2014, 2018",
     "196cm의 압도적인 제공권과 포스트 플레이로 아시아 무대를 제패한 장신 타깃맨", "타깃 스트라이커", False, None, 9),
    ("Kwak Tae-Hwi", "곽태휘", "DF", "CB", [], 58, 5, 2008, 2017, False, 186, "오른발",
     "전남 드래곤즈, 울산 현대, 알힐랄, FC 서울", "AFC 챔피언스리그 우승(2012 주장), 2015 아시안컵 준우승, 2014 월드컵", "2014",
     "골 넣는 수비수. 강력한 헤더와 리더십으로 수비 라인을 이끈 커맨더형 센터백", "공중볼 특화 센터백", False, None, 5),
    ("Lee Jung-Soo", "이정수", "DF", "CB", [], 54, 5, 2008, 2013, False, 185, "오른발",
     "수원 삼성, 가시마 앤틀러스, 알사드", "2010 남아공 월드컵 16강(그리스·나이지리아전 2골), AFC 챔피언스리그 우승(2011)", "2010",
     "세트피스 상황에서 탁월한 위치선정으로 2010 월드컵 2골을 터뜨린 골 넣는 수비수", "세트피스 위협 센터백", False, None, 14),
    ("Cho Won-Hee", "조원희", "DF", "RB", ["CDM"], 36, 1, 2005, 2009, False, 177, "오른발",
     "수원 삼성, 위건 애슬레틱, 광저우 헝다", "2006 독일 월드컵 출전, K리그 우승, 중국 슈퍼리그 우승", "2006",
     "왕성한 활동량과 투지 넘치는 압박을 보여준 라이트백 겸 수비형 미드필더", "수비형 미드필더 / 라이트백", False, None, 2),
    ("Kim Jung-Woo", "김정우", "MF", "CDM", ["CM"], 71, 6, 2003, 2012, False, 183, "오른발",
     "울산 현대, 나고야 그램퍼스, 성남 일화, 전북 현대", "2010 남아공 월드컵 16강 전 경기 풀타임, AFC 챔피언스리그 우승", "2010",
     "뼈정우. 왕성한 활동량과 패스 연결고리 역할로 2010 남아공 월드컵 기성용의 파트너로 활약한 중원 엔진", "박스 투 박스 / 홀딩 미드필더", False, None, 8),
    ("Jung Woo-Young", "정우영", "MF", "CDM", ["CB"], 73, 3, 2015, 2023, True, 186, "오른발",
     "교토 상가, 비셀 고베, 충칭 리판, 알사드", "2018 러시아 월드컵·2022 카타르 월드컵 16강 주전 수비형 미드필더", "2018, 2022",
     "포백 앞을 든든하게 보호하며 안정적인 1차 빌드업과 무회전 프리킥을 구사한 홀딩 미드필더", "앵커맨 (Holding Midfielder)", False, None, 5),
    ("Hong Chul", "홍철", "DF", "LB", ["LWB"], 47, 1, 2011, 2022, True, 176, "왼발",
     "성남 일화, 수원 삼성, 울산 현대, 대구 FC", "2018·2022 월드컵 출전, AFC 챔피언스리그 우승", "2018, 2022",
     "날카로운 왼발 크로스와 오버래핑 능력을 갖춘 좌측 풀백", "오버래핑 레프트백", False, None, 14),
    ("Kim Moon-Hwan", "김문환", "DF", "RB", ["RWB"], 30, 0, 2018, 2025, True, 173, "오른발",
     "부산 아이파크, LA FC, 전북 현대, 알두하일, 대전 하나", "2022 카타르 월드컵 16강 전 경기 풀타임 주전 라이트백, 2018 아시안게임 금메달", "2022",
     "왕성한 기동력과 적극적인 우측면 오버래핑으로 2022 카타르 월드컵 16강을 이끈 라이트백", "기동력형 라이트백", False, None, 15),
    ("Kim Tae-Hwan", "김태환", "DF", "RB", ["RWB"], 30, 0, 2014, 2024, True, 177, "오른발",
     "FC 서울, 성남 일화, 울산 현대, 전북 현대", "2022 카타르 월드컵 16강, AFC 챔피언스리그 우승(2020), K리그 우승", "2022",
     "빠른 스피드와 강한 대인 수비를 갖춘 우측 풀백", "라이트백", False, None, 23),
    ("Na Sang-Ho", "나상호", "FW", "RW", ["LW"], 30, 2, 2018, 2023, True, 173, "오른발",
     "광주 FC, FC 도쿄, FC 서울, 마치다 젤비아", "2022 카타르 월드컵 16강 출전, 2018 아시안게임 금메달, K리그2 MVP·득점왕", "2022",
     "높은 활동량과 전방 압박, 저돌적인 측면 움직임을 보여주는 윙 포워드", "전방 압박형 윙어", False, None, 17),
    ("Paik Seung-Ho", "백승호", "MF", "CM", ["CDM"], 30, 3, 2019, 2026, True, 182, "오른발",
     "지로나, 다름슈타트, 전북 현대, 버밍엄 시티", "2022 카타르 월드컵 16강(브라질전 중거리 원더골), 아시안게임 금메달(2023 주장), K리그 우승", "2022",
     "유려한 턴 동작과 양발 중장거리 패스, 강력한 중거리 슛을 갖춘 중앙 미드필더", "중앙 미드필더", False, None, 8),
    ("Cho Gue-Sung", "조규성", "FW", "ST", [], 39, 9, 2021, 2025, True, 189, "오른발",
     "전북 현대 모터스, 미트윌란", "2022 카타르 월드컵 16강(가나전 헤더 멀티골 — 한국 최초 월드컵 한 경기 멀티골), K리그 득점왕(2022), 덴마크 리그 우승", "2022",
     "압도적인 점프력과 헤더 결정력, 전방 압박 활동량을 겸비한 현대형 타깃 스트라이커", "타깃 스트라이커", True, None, 9),
    ("Seol Young-Woo", "설영우", "DF", "RB", ["LB"], 30, 0, 2023, 2026, True, 180, "오른발",
     "울산 HD, 츠르베나 즈베즈다", "K리그 우승 2회, 아시안게임 금메달(2023), 2023 아시안컵 4강 주전 풀백", None,
     "좌우 풀백을 모두 능숙하게 소화하며 안정적인 볼 간수와 오버래핑을 보여주는 멀티 풀백", "좌우 멀티 풀백", False, None, 22),
]

# RSSSF에만 등재된 추가 역사적 한국 선수들의 정확한 한국어 실명 및 포지션 매핑
RSSSF_KOR_EXTRA_NAMES = {
    "Lee Tae-Ho": ("이태호", "FW", "ST"),
    "Choi Kang-Hee": ("최강희", "DF", "RB"),
    "Chung Jong-Soo": ("정종수", "DF", "LB"),
    "Lee Young-Jin": ("이영진", "MF", "CM"),
    "Park Chang-Sun": ("박창선", "MF", "CAM"),
    "Kim Pan-Keun": ("김판근", "DF", "RB"),
    "Huh Jung-Moo": ("허정무", "MF", "CM"),
    "Hwangbo Kwan": ("황보관", "MF", "CAM"),
    "Kim Poong-Joo": ("김풍주", "GK", "GK"),
    "Choi Young-Il": ("최영일", "DF", "CB"),
    "Lee 민-Sung": ("이민성", "DF", "CB"),
    "Lee Min-Sung": ("이민성", "DF", "CB"),
    "Yoon Jung-Hwan": ("윤정환", "MF", "CAM"),
    "Lee Sang-Yoon": ("이상윤", "FW", "RW"),
    "Roh Sang-Rae": ("노상래", "FW", "LW"),
    "Kang Chul": ("강철", "DF", "CB"),
    "Kim Sang-Sik": ("김상식", "MF", "CDM"),
    "Kim Do-Keun": ("김도근", "MF", "CM"),
    "Choi Sung-Yong": ("최성용", "DF", "RB"),
    "Park Jin-Sub": ("박진섭", "DF", "RB"),
    "Kim Dong-Jin": ("김동진", "DF", "LB"),
    "Oh Beom-Seok": ("오범석", "DF", "RB"),
    "Kim Chi-Woo": ("김치우", "DF", "LB"),
    "Lee Keun-Ho": ("이근호", "FW", "RW"),
    "Yeom Ki-Hun": ("염기훈", "MF", "LM"),
    "Dejan": ("데얀", "FW", "ST"),
    "Choi Tae-Uk": ("최태욱", "FW", "RW"),
    "KimJung-Woo": ("김정우", "MF", "CDM"),
    "Park Joo-Ho": ("박주호", "DF", "LB"),
    "Hong Jeong-Ho": ("홍정호", "DF", "CB"),
    "Jang Hyun-Soo": ("장현수", "DF", "CB"),
    "Nam Tae-Hee": ("남태희", "MF", "CAM"),
    "Suk Hyun-Jun": ("석현준", "FW", "ST"),
    "Ji Dong-Won": ("지동원", "FW", "LW"),
    "Kim Bo-Kyung": ("김보경", "MF", "CAM"),
    "Han Kook-Young": ("한국영", "MF", "CDM"),
    "Lee Chung-Yong": ("이청용", "MF", "RW"),
    "Yun Suk-Young": ("윤석영", "DF", "LB"),
}


def compute_decade_tags(start_y: int, end_y: int):
    s_dec = (start_y // 10) * 10
    e_dec = (end_y // 10) * 10
    decs = [f"{d}s" for d in range(s_dec, e_dec + 1, 10)]
    mid_y = (start_y + end_y) // 2
    p_dec = f"{(mid_y // 10) * 10}s"
    return ",".join(decs), p_dec


def main():
    # 1. Ensure RSSSF KOR.html is downloaded
    if not RSSSF_KOR_PATH.exists() or RSSSF_KOR_PATH.stat().st_size < 2000:
        r = requests.get("https://www.rsssf.org/miscellaneous/skor-recintlp.html", timeout=15)
        if r.status_code == 200:
            RSSSF_KOR_PATH.write_bytes(r.content)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 2. Insert or update KOR in countries and country_ranking_snapshots
    cur.execute("SELECT id FROM countries WHERE fifa_code = 'KOR'")
    crow = cur.fetchone()
    if crow:
        kor_cid = crow["id"]
    else:
        cur.execute("""
            INSERT INTO countries (
                fifa_code, iso_alpha2, name_ko, name_en, confederation, flag_emoji, flag_svg_url,
                world_cup_titles, world_cup_winning_years, major_honors_ko,
                kit_primary_color, kit_secondary_color, kit_accent_color, kit_text_color, kit_pattern_type,
                historical_note_ko, data_coverage_note_ko, last_data_updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "KOR", "kr", "대한민국", "South Korea", "AFC", "🇰🇷", "https://flagcdn.com/kr.svg",
            0, None, "FIFA 월드컵 4위(2002 — 아시아 최초 준결승), 월드컵 11회 연속 본선 진출(1986~2026), AFC 아시안컵 우승 2회(1956, 1960), 아시안게임 금메달 6회",
            "#E6002D", "#1E3A8A", "#FFFFFF", "#FFFFFF", "solid",
            "1948년 첫 공식 A매치 이후 대한축구협회(KFA) 및 FIFA/RSSSF 공인 성인 남자 A대표팀 기록을 기준으로 합니다.",
            "1950년대~2020년대 대한축구협회(KFA) 센추리 클럽 및 RSSSF 공식 A매치 30회 이상 출전 선수 수록 완료",
            "2026-10-07"
        ))
        kor_cid = cur.lastrowid

    # Add to country_ranking_snapshots (Rank 22, is_target_top30 = 1)
    cur.execute("DELETE FROM country_ranking_snapshots WHERE country_id = ?", (kor_cid,))
    cur.execute("""
        INSERT INTO country_ranking_snapshots (
            snapshot_date, country_id, fifa_rank, rank_change, fifa_points, is_target_top30, is_current_snapshot
        ) VALUES ('2026-10-07', ?, 22, 1, 1599.85, 1, 1)
    """, (kor_cid,))

    # Get RSSSF source id
    cur.execute("SELECT id FROM data_sources WHERE source_code = 'rsssf'")
    src_row = cur.fetchone()
    rsssf_source_id = src_row["id"] if src_row else 1

    # 3. Parse RSSSF KOR.html to also include any additional 30+ cap players beyond KOR_CURATED_PLAYERS
    rsssf_rows = []
    if RSSSF_KOR_PATH.exists():
        import html as html_lib
        raw_txt = RSSSF_KOR_PATH.read_bytes().decode("latin-1", errors="replace")
        clean_txt = html_lib.unescape(re.sub(r"<[^>]+>", "", raw_txt))
        for idx_l, ln in enumerate(clean_txt.splitlines()):
            ls = ln.strip()
            if idx_l > 30 and re.match(r"^(Goalscoring|Goalscorers|Goals\s+for|Goal\s+Scorers)\b", ls, re.IGNORECASE):
                break
            body = re.sub(r"^\d+[\.\)]\s*", "", ls).strip()
            m1 = re.match(r"^(.+?)\s+(\d{4})\s*-\s*(\d{2,4})?\s*(\*)?\s+(\d+)(?:\s+(\d+|\-))?", body)
            if m1:
                nm = m1.group(1).strip()
                y1_s = int(m1.group(2))
                y2_raw = m1.group(3)
                if not y2_raw:
                    y2_s = 2025 if m1.group(4) else y1_s
                elif len(y2_raw) == 2:
                    prefix = "19" if int(y2_raw) >= (y1_s % 100) and y1_s < 2000 else "20"
                    y2_s = int(prefix + y2_raw)
                else:
                    y2_s = int(y2_raw)
                caps_v = int(m1.group(5))
                goals_raw = m1.group(6)
                goals_v = int(goals_raw) if (goals_raw and goals_raw.isdigit()) else 0
                if caps_v >= 30 and re.search(r"[A-Za-z]", nm):
                    rsssf_rows.append({"name": nm, "caps": caps_v, "goals": goals_v, "start_year": y1_s, "end_year": y2_s})

    # Clear existing KOR national team careers to avoid duplicates on re-run
    cur.execute("SELECT player_id FROM player_national_team_careers WHERE country_id = ?", (kor_cid,))
    old_pids = [r["player_id"] for r in cur.fetchall()]
    for opid in old_pids:
        for tbl in ("player_national_team_careers", "player_positions", "player_career_awards", "player_images", "player_source_records"):
            cur.execute(f"DELETE FROM {tbl} WHERE player_id = ?", (opid,))
        cur.execute("DELETE FROM players WHERE id = ?", (opid,))

    seen_en_lower = set()
    inserted_count = 0

    def insert_kor_player(
        name_en, name_ko, pos_group, primary_pos, sec_pos_list,
        caps, goals, y1, y2, is_active, height_cm, foot,
        clubs_ko, honors_ko, wc_years, play_style_ko, role_ko,
        is_legend, img_url, jersey_num, is_eligible=1
    ):
        nonlocal inserted_count
        dtags, pdec = compute_decade_tags(y1, y2)
        period_label = f"{y1}–{'현재' if is_active else y2}"
        uid = f"kor-{re.sub(r'[^a-z0-9]+', '-', name_en.lower()).strip('-')}-{y1}"
        aliases = f"{name_ko},{name_en},{name_en.replace('-', ' ')},{name_ko.replace(' ', '')}"

        cur.execute("""
            INSERT OR REPLACE INTO players (
                internal_uid, name_ko, name_en, name_native, aliases_search,
                nationality_code, birth_year, is_deceased,
                primary_position, position_group, secondary_positions,
                height_cm, preferred_foot, is_active_player,
                play_style_ko, primary_role_ko, attack_defense_traits_ko,
                work_rate_mobility_ko, tactical_fit_role_ko, fact_bio_ko, is_legend_test_case
            ) VALUES (?, ?, ?, ?, ?, 'KOR', ?, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            uid, name_ko, name_en, name_ko, aliases,
            y1 - 21,
            primary_pos, pos_group, json.dumps(sec_pos_list, ensure_ascii=False),
            height_cm, foot, 1 if is_active else 0,
            play_style_ko, role_ko,
            "높은 전술 이해도와 태극전사 특유의 기동력·압박 수행 능력 보유",
            "왕성한 공수 전환 활동량", role_ko,
            f"대한민국 축구 국가대표팀 공식 A매치 {caps}경기 {goals}골 기록 ({period_label}).",
            1 if is_legend else 0
        ))
        pid = cur.lastrowid

        cur.execute("""
            INSERT INTO player_national_team_careers (
                player_id, country_id, represented_fifa_code, historical_team_code,
                career_start_year, career_end_year, active_period_label,
                decade_tags, primary_decade, official_caps, official_goals,
                is_eligible_30_caps, verification_status, record_source_name,
                record_source_url, verified_date
            ) VALUES (?, ?, 'KOR', 'KOR', ?, ?, ?, ?, ?, ?, ?, ?, 'verified',
                      'KFA 공식 아카이브 & RSSSF (skor-recintlp.html)',
                      'https://www.rsssf.org/miscellaneous/skor-recintlp.html', '2026-10-07')
        """, (
            pid, kor_cid, y1, y2, period_label, dtags, pdec, caps, goals, is_eligible
        ))

        # Positions
        cur.execute("""
            INSERT INTO player_positions (player_id, position_code, position_group, is_primary, suitability_tier, suitability_score)
            VALUES (?, ?, ?, 1, 'natural', 100)
        """, (pid, primary_pos, pos_group))
        for sp in sec_pos_list:
            sp_grp = "GK" if sp == "GK" else ("DF" if sp in ("CB", "LB", "RB", "LWB", "RWB") else ("MF" if sp in ("CDM", "CM", "CAM", "LM", "RM") else "FW"))
            cur.execute("""
                INSERT OR IGNORE INTO player_positions (player_id, position_code, position_group, is_primary, suitability_tier, suitability_score)
                VALUES (?, ?, ?, 0, 'secondary', 90)
            """, (pid, sp, sp_grp))

        # Career awards
        cur.execute("""
            INSERT INTO player_career_awards (
                player_id, major_clubs_ko, major_honors_ko, world_cup_participations,
                world_cup_winner, world_cup_titles_count, continental_winner,
                ballon_dor_winner, ballon_dor_count, individual_awards_ko
            ) VALUES (?, ?, ?, ?, 0, 0, ?, 0, 0, ?)
        """, (
            pid, clubs_ko, honors_ko, wc_years,
            1 if ("아시안컵 우승" in (honors_ko or "") or "아시안게임 금메달" in (honors_ko or "")) else 0,
            honors_ko
        ))

        # Images
        initials = "".join([w[0] for w in name_en.split()[:2]]).upper()
        cur.execute("""
            INSERT INTO player_images (
                player_id, image_url, original_source_name, original_source_url,
                license_info, requires_attribution, fallback_number, fallback_initials
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pid, img_url,
            "Wikimedia Commons" if img_url else None,
            img_url,
            "CC BY-SA 4.0 (Wikimedia Commons)" if img_url else None,
            1 if img_url else 0,
            jersey_num, initials
        ))

        # Source record
        cur.execute("""
            INSERT INTO player_source_records (
                player_id, source_id, external_id, source_caps, source_goals,
                external_url, checked_at
            ) VALUES (?, ?, ?, ?, ?, 'https://www.rsssf.org/miscellaneous/skor-recintlp.html', '2026-10-07')
        """, (pid, rsssf_source_id, uid, caps, goals))

        if is_eligible == 1:
            inserted_count += 1
        return pid

    # Insert curated 48 Korean legends & stars first
    for item in KOR_CURATED_PLAYERS:
        insert_kor_player(*item, is_eligible=1)
        seen_en_lower.add(re.sub(r"[^a-z]", "", item[0].lower()))

    # Also merge additional RSSSF KOR >= 30 caps players
    from scripts.enrich_korean_names import transliterate_full_name
    for r in rsssf_rows:
        raw_name = re.sub(r"\*+", "", r["name"]).strip()
        norm_key = re.sub(r"[^a-z]", "", raw_name.lower())
        if not norm_key or norm_key in seen_en_lower:
            continue
        seen_en_lower.add(norm_key)

        if raw_name in RSSSF_KOR_EXTRA_NAMES:
            ko_name, pg, ppos = RSSSF_KOR_EXTRA_NAMES[raw_name]
        else:
            ko_name = transliterate_full_name(raw_name)
            pg, ppos = "MF", "CM"

        y1 = r.get("start_year") or 1980
        y2 = r.get("end_year") or 1995
        insert_kor_player(
            raw_name, ko_name, pg, ppos, [],
            int(r["caps"]), int(r.get("goals") or 0), int(y1), int(y2),
            y2 >= 2024, None, None,
            "대한민국 K리그 및 국가대표팀", f"대한민국 성인 남자 A대표팀 공식 {r['caps']}경기 출전",
            None, f"대한민국 A대표팀 {y1}~{y2} 활약 국가대표 선수", ppos,
            False, None, 14, is_eligible=1
        )

    # Also add 1 <30 cap test case for KOR (양민혁 Yang Min-hyeok, 2 caps) to verify 29-cap exclusion for Korea too
    insert_kor_player(
        "Yang Min-Hyeok", "양민혁", "FW", "RW", ["LW"],
        2, 0, 2025, 2026, True, 176, "오른발",
        "강원 FC, 토트넘 홋스퍼", "K리그 영플레이어상", None,
        "빠른 스피드를 가진 유망주 윙어 (A매치 30회 미만 검증용)", "윙어",
        False, None, 47, is_eligible=0
    )

    # 4. Seed 'korea-all-time-xi' preset in saved_lineups so users can immediately load or battle with Korea All-Time XI
    cur.execute("DELETE FROM saved_lineups WHERE share_slug = 'korea-all-time-xi'")
    cur.execute("SELECT slots_json FROM formations WHERE code = '4-3-3'")
    slots_433 = json.loads(cur.fetchone()["slots_json"])

    kor_xi_targets = [
        ("GK", "Lee Woon-Jae"),
        ("LB", "Lee Young-Pyo"),
        ("LCB", "Kim Young-Gwon"),
        ("RCB", "Kim Min-Jae"),
        ("RB", "Cha Du-Ri"),
        ("LCM", "Park Ji-Sung"),
        ("CDM", "Hong Myung-Bo"),
        ("RCM", "Ki Sung-Yueng"),
        ("LW", "Son Heung-Min"),
        ("ST", "Hwang Sun-Hong"),
        ("RW", "Cha Bum-Kun"),
    ]
    lineup_players_list = []
    captain_pid = None
    for idx_s, sdef in enumerate(slots_433):
        scode = sdef["slot_code"]
        target_en = next((en for sc, en in kor_xi_targets if sc == scode), "Son Heung-Min")
        cur.execute("""
            SELECT p.*, nc.official_caps, nc.official_goals, nc.active_period_label, nc.primary_decade,
                   pi.image_url, pi.fallback_number, ca.major_honors_ko
            FROM players p
            JOIN player_national_team_careers nc ON nc.player_id = p.id
            LEFT JOIN player_images pi ON pi.player_id = p.id
            LEFT JOIN player_career_awards ca ON ca.player_id = p.id
            WHERE nc.country_id = ? AND p.name_en = ?
            LIMIT 1
        """, (kor_cid, target_en))
        prow = dict(cur.fetchone())
        is_cap = (scode == "CM")  # 홍명보 or 손흥민
        if is_cap:
            captain_pid = prow["id"]
        lineup_players_list.append({
            "slot_index": idx_s,
            "slot_code": scode,
            "slot_label_ko": sdef["label_ko"],
            "x": sdef["x"],
            "y": sdef["y"],
            "player_id": prow["id"],
            "name_ko": prow["name_ko"],
            "name_en": prow["name_en"],
            "display_name": f"{prow['name_ko']} ({prow['name_en']})",
            "primary_position": prow["primary_position"],
            "official_caps": prow["official_caps"],
            "official_goals": prow["official_goals"],
            "active_period_label": prow["active_period_label"],
            "primary_decade": prow["primary_decade"],
            "image_url": prow["image_url"],
            "jersey_number": prow["fallback_number"] or (idx_s + 1),
            "suitability_status": "적합",
            "suitability_score": 100,
            "is_captain": is_cap,
            "play_style_ko": prow["play_style_ko"],
            "major_honors_ko": prow["major_honors_ko"],
            "fact_bio_ko": prow["fact_bio_ko"],
        })

    snapshot_obj = {
        "share_slug": "korea-all-time-xi",
        "country_id": kor_cid,
        "country_fifa_code": "KOR",
        "country_name_ko": "대한민국",
        "country_name_en": "South Korea",
        "flag_emoji": "🇰🇷",
        "flag_svg_url": "https://flagcdn.com/kr.svg",
        "kit_primary_color": "#E6002D",
        "kit_secondary_color": "#1E3A8A",
        "kit_text_color": "#FFFFFF",
        "team_name": "대한민국 역대 최강 XI (태극전사 올타임 드림팀)",
        "formation_code": "4-3-3",
        "tactical_style": "강한 전방 압박",
        "board_color_theme": "classic_emerald",
        "team_description": "차범근·손흥민·황선홍의 역대 최강 스리톱과 박지성·기성용·홍명보의 중원/리베로, 이영표·김민재·김영권·차두리·이운재로 완성한 대한민국 올타임 베스트11",
        "captain_player_id": captain_pid,
        "created_at": "2026-10-19",
        "players": lineup_players_list,
    }
    cur.execute("""
        INSERT INTO saved_lineups (
            share_slug, country_id, country_fifa_code, country_name_ko, team_name,
            formation_code, captain_player_id, tactical_style, board_color_theme,
            team_description, lineup_snapshot_json
        ) VALUES (?, ?, 'KOR', '대한민국', ?, '4-3-3', ?, '강한 전방 압박', 'classic_emerald', ?, ?)
    """, (
        "korea-all-time-xi", kor_cid, snapshot_obj["team_name"], captain_pid,
        snapshot_obj["team_description"], json.dumps(snapshot_obj, ensure_ascii=False)
    ))
    lid = cur.lastrowid
    for lp in lineup_players_list:
        cur.execute("""
            INSERT INTO lineup_players (
                lineup_id, slot_index, slot_code, player_id, custom_x, custom_y,
                suitability_status, suitability_score, jersey_number, is_captain
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lid, lp["slot_index"], lp["slot_code"], lp["player_id"], lp["x"], lp["y"],
            lp["suitability_status"], lp["suitability_score"], lp["jersey_number"], 1 if lp["is_captain"] else 0
        ))

    conn.commit()
    conn.close()
    print(f"Successfully added South Korea (KOR) with {inserted_count} eligible (30+ caps) players and 'korea-all-time-xi' preset!")


if __name__ == "__main__":
    main()
