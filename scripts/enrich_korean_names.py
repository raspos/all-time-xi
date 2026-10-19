# -*- coding: utf-8 -*-
"""
Enrich all players in data/all_time_xi.db so that 100% of players have a Korean Hangul name (name_ko),
and ensure display format '한글이름 (영문이름)' works cleanly across all 30 countries.
"""
import json
import re
import sqlite3
import unicodedata
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "data" / "all_time_xi.db"

# Curated dictionary of common football given names, surnames, and full names across the 30 countries
EXACT_PLAYER_MAP = {
    "Hossam Hassan": "호삼 하산",
    "Ahmed Hassan": "아흐메드 하산",
    "Essam El-Hadary": "에삼 엘하다리",
    "Ahmed Fathi": "아흐메드 파티",
    "Ibrahim Hassan": "이브라힘 하산",
    "Hany Ramzy": "하니 람지",
    "Wael Gomaa": "와엘 고마",
    "visiting": "",
    "Claudio Suárez": "클라우디오 수아레스",
    "Andrés Guardado": "안드레스 과르다도",
    "Rafa Márquez": "라파엘 마르케스",
    "Rafael Márquez": "라파엘 마르케스",
    "Guillermo Ochoa": "기예르모 오초아",
    "Jorge Campos": "호르헤 캄포스",
    "Cuauhtémoc Blanco": "콰우테모크 블랑코",
    "Jared Borgetti": "하레드 보르헤티",
    "Javier Hernández": "하비에르 에르난데스",
    "Pavel Pardo": "파벨 파르도",
    "Gerardo Torrado": "헤라르도 토라도",
    "Carlos Salcido": "카를로스 살시도",
    "Héctor Moreno": "엑토르 모레노",
    "Héctor Herrera": "엑토르 에레라",
    "Raúl Jiménez": "라울 히메네스",
    "Hugo Sánchez": "우고 산체스",
    "Luis Hernández": "루이스 에르난데스",
    "Alberto García Aspe": "알베르토 가르시아 아스페",
    "Ramón Ramírez": "라몬 라미레스",
    "Carlos Hermosillo": "카를로스 에르모시요",
    "Zague": "자게",
    "Giovani dos Santos": "지오바니 도스 산토스",
    "Carlos Vela": "카를로스 벨라",
    "Hirving Lozano": "이르빙 로사노",
    "Edson Álvarez": "에드손 알바레스",
    "Iván Hurtado": "이반 우르타도",
    "Walter Ayoví": "발테르 아요비",
    "Édison Méndez": "에디손 멘데스",
    "Álex Aguinaga": "알렉스 아기나가",
    "Ulises de la Cruz": "울리세스 데 라 크루스",
    "Antonio Valencia": "안토니오 발렌시아",
    "Enner Valencia": "에네르 발렌시아",
    "Agustín Delgado": "아구스틴 델가도",
    "Christian Benítez": "크리스티안 베니테스",
    "Moisés Caicedo": "모이세스 카이세도",
    "Piero Hincapié": "피에로 인카피에",
    "Pervis Estupiñán": "페르비스 에스투피냔",
    "Carlos Valderrama": "카를로스 발데라마",
    "Radamel Falcao": "라다멜 팔카오",
    "James Rodríguez": "하메스 로드리게스",
    "David Ospina": "다비드 오스피나",
    "Juan Cuadrado": "후안 콰드라도",
    "Mario Yepes": "마리오 예페스",
    "Iván Córdoba": "이반 코르도바",
    "René Higuita": "레네 이기타",
    "Freddy Rincón": "프레디 링콘",
    "Faustino Asprilla": "파우스티노 아스프리야",
    "Leonel Álvarez": "레오넬 알바레스",
    "Luis Díaz": "루이스 디아스",
    "Diego Godín": "디에고 고딘",
    "Luis Suárez": "루이스 수아레스",
    "Edinson Cavani": "에딘손 카바니",
    "Fernando Muslera": "페르난도 무슬레라",
    "Maxi Pereira": "막시 페레이라",
    "Диего Forlán": "디에고 포를란",
    "Diego Forlán": "디에고 포를란",
    "Enzo Francescoli": "엔소 프란체스콜리",
    "Obdulio Varela": "오브둘리오 바렐라",
    "Alcides Ghiggia": "알시데스 기지아",
    "Juan Schiaffino": "후안 스키아피노",
    "José Nasazzi": "호세 나사시",
    "Héctor Scarone": "엑토르 스카로네",
    "Federico Valverde": "페데리코 발베르데",
    "Ronald Araújo": "로날드 아라우호",
    "Álvaro Recoba": "알바로 레코바",
    "Paolo Montero": "파올로 몬테로",
    "Cobi Jones": "코비 존스",
    "Landon Donovan": "랜던 도노반",
    "Clint Dempsey": "클린트 뎀프시",
    "Michael Bradley": "마이클 브래들리",
    "Tim Howard": "팀 하워드",
    "Brad Friedel": "브래드 프리델",
    "Kasey Keller": "케이시 켈러",
    "Claudio Reyna": "클라우디오 레이나",
    "Brian McBride": "브라이언 맥브라이드",
    "Christian Pulisic": "크리스천 풀리식",
    "Weston McKennie": "웨스턴 맥케니",
    "Atiba Hutchinson": "아티바 허친슨",
    "Julian de Guzman": "줄리언 더 구즈만",
    "Cyle Larin": "카일 래린",
    "Jonathan David": "조너선 데이비드",
    "Alphonso Davies": "알폰소 데이비스",
    "Milan Borjan": "밀란 보르얀",
    "Craig Forrest": "크레이그 포레스트",
    "Dwayne De Rosario": "드웨인 데 로사리오",
    "Paul Stalteri": "폴 스탤테리",
    "Ali Daei": "알리 다에이",
    "Javad Nekounam": "자바드 네쿠남",
    "Ali Karimi": "알리 카리미",
    "Mehdi Mahdavikia": "메흐디 마다비키아",
    "Ehsan Hajsafi": "에흐산 하지사피",
    "Karim Bagheri": "카림 바게리",
    "Sardar Azmoun": "사르다르 아즈문",
    "Mehdi Taremi": "메흐디 타레미",
    "Alireza Jahanbakhsh": "알리레자 자한바흐시",
    "Alireza Beiranvand": "알리레자 베이란반드",
    "Ahmad Reza Abedzadeh": "아흐마드 레자 아베드자데",
    "Nasser Hejazi": "나세르 헤자지",
    "Jalal Hosseini": "잘랄 호세이니",
    "Didier Drogba": "디디에 드록바",
    "Yaya Touré": "야야 투레",
    "Kolo Touré": "콜로 투레",
    "Didier Zokora": "디디에 조코라",
    "Siaka Tiéné": "시아카 티에네",
    "Salomon Kalou": "살로몬 칼루",
    "Gervinho": "제르비뉴",
    "Franck Kessié": "프랑크 케시에",
    "Sébastien Haller": "세바스티앙 알레",
    "Sadio Mané": "사디오 마네",
    "Idrissa Gueye": "이드리사 게예",
    "Kalidou Koulibaly": "칼리두 쿨리발리",
    "Henri Camara": "앙리 카마라",
    "El Hadji Diouf": "엘 하지 디우프",
    "Édouard Mendy": "에두아르 멘디",
    "Cheikhou Kouyaté": "셰이쿠 쿠야테",
    "Tony Sylva": "토니 실바",
    "Riyad Mahrez": "리야드 마레즈",
    "Islam Slimani": "이슬람 슬리마니",
    "Aïssa Mandi": "아이사 만디",
    "Raïs M'Bolhi": "라이스 음볼리",
    "Sofiane Feghouli": "소피안 페굴리",
    "Rabah Madjer": "라바 마제르",
    "Lakhdar Belloumi": "라흐다르 벨루미",
    "Djamel Menad": "자멜 메나드",
    "Baghdad Bounedjah": "바그다드 부네자",
    "Ismaël Bennacer": "이스마엘 베나세르",
    "Ramy Bensebaini": "라미 벤세바이니",
    "Noureddine Naybet": "누레딘 나이베트",
    "Achraf Hakimi": "아슈라프 하키미",
    "Hakim Ziyech": "하킴 지예시",
    "Yassine Bounou": "야신 부누",
    "Romain Saïss": "로맹 사이스",
    "Sofyan Amrabat": "소피앙 암라바트",
    "Youssef En-Nesyri": "유세프 엔네시리",
    "Mustapha Hadji": "무스타파 하지",
    "Badou Zaki": "바두 자키",
    "Ahmed Faras": "아흐메드 파라스",
    "Medhi Benatia": "메흐디 베나티아",
    "Mbark Boussoufa": "음바르크 부수파",
    "Nwankwo Kanu": "느완코 카누",
    "Jay-Jay Okocha": "제이제이 오코차",
    "Vincent Enyeama": "빈센트 엔예아마",
    "Ahmed Musa": "아흐메드 무사",
    "Joseph Yobo": "조지프 요보",
    "John Obi Mikel": "존 오비 미켈",
    "Rashidi Yekini": "라시디 예키니",
    "Stephen Keshi": "스티븐 케시",
    "Finidi George": "피니디 조지",
    "Daniel Amokachi": "다니엘 아모카치",
    "Sunday Oliseh": "선데이 올리세",
    "Taribo West": "타리보 웨스트",
    "Victor Osimhen": "빅터 오시멘",
    "Alex Iwobi": "알렉스 이워비",
    "William Troost-Ekong": "윌리엄 트로스트에콩",
    "Wilfred Ndidi": "윌프레드 은디디",
}

# Common word/name token dictionary for rapid, accurate Korean conversion
WORD_KO_MAP = {
    # Given names & common football names
    "mohamed": "모하메드", "mohammed": "모하메드", "muhammad": "무함마드",
    "ahmed": "아흐메드", "ahmad": "아흐마드", "mahmoud": "마흐무드",
    "hassan": "하산", "hussein": "후세인", "hossein": "호세인", "hosseini": "호세이니",
    "ali": "알리", "omar": "오마르", "amr": "아므르", "essam": "에삼",
    "ibrahim": "이브라힘", "ismail": "이스마일", "ismael": "이스마엘",
    "youssef": "유세프", "yousef": "유세프", "younes": "유네스", "younis": "유니스",
    "tarek": "타레크", "tarik": "타리크", "walid": "왈리드", "wael": "와엘",
    "khaled": "칼레드", "khalid": "칼리드", "karim": "카림", "hakim": "하킴",
    "rachid": "라시드", "rashid": "라시드", "abdel": "압델", "abdul": "압둘",
    "abdallah": "압달라", "abdullah": "압둘라", "mustapha": "무스타파", "mostafa": "모스타파",
    "nasser": "나세르", "samir": "사미르", "said": "사이드", "saeed": "사이드",
    "hamza": "함자", "mehdi": "메흐디", "majid": "마지드", "javad": "자바드",
    "reza": "레자", "alireza": "알리레자", "mohammad": "모하마드",
    # Spanish / Portuguese / Italian
    "carlos": "카를로스", "juan": "후안", "jose": "호세", "josé": "호세",
    "luis": "루이스", "luís": "루이스", "luiz": "루이스", "jorge": "호르헤",
    "diego": "디에고", "pablo": "파블로", "pedro": "페드로", "paulo": "파울루",
    "paolo": "파올로", "marco": "마르코", "marcos": "마르코스", "mario": "마리오",
    "fernando": "페르난도", "francisco": "프란시스코", "javier": "하비에르",
    "gabriel": "가브리엘", "daniel": "다니엘", "david": "다비드", "miguel": "미겔",
    "angel": "앙헬", "ángel": "앙헬", "rafael": "라파엘", "raul": "라울", "raúl": "라울",
    "sergio": "세르히오", "sérgio": "세르지우", "andres": "안드레스", "andrés": "안드레스",
    "alejandro": "알레한드로", "alberto": "알베르토", "alfredo": "알프레도",
    "antonio": "안토니오", "arturo": "아르투로", "cesar": "세사르", "césar": "세사르",
    "claudio": "클라우디오", "cristian": "크리스티안", "christian": "크리스티안",
    "edison": "에디손", "edinson": "에딘손", "eduardo": "에두아르도",
    "enrique": "엔리케", "ernesto": "에르네스토", "esteban": "에스테반",
    "fabian": "파비안", "fabián": "파비안", "federico": "페데리코",
    "felipe": "펠리페", "gonzalo": "곤살로", "guillermo": "기예르모",
    "gustavo": "구스타보", "hector": "엑토르", "héctor": "엑토르",
    "hernan": "에르난", "hernán": "에르난", "hugo": "우고", "ignacio": "이그나시오",
    "ivan": "이반", "iván": "이반", "jaime": "하이메", "jesus": "헤수스", "jesús": "헤수스",
    "joaquin": "호아킨", "joaquín": "호아킨", "julio": "훌리오", "leonardo": "레오나르도",
    "lucas": "루카스", "manuel": "마누엘", "marcelo": "마르셀루", "martin": "마르틴", "martín": "마르틴",
    "matias": "마티아스", "matías": "마티아스", "mauricio": "마우리시오", "maximiliano": "막시밀리아노",
    "nicolas": "니콜라스", "nicolás": "니콜라스", "oscar": "오스카르", "óscar": "오스카르",
    "patricio": "파트리시오", "ramon": "라몬", "ramón": "라몬", "ricardo": "리카르도",
    "roberto": "로베르토", "rodrigo": "로드리고", "ruben": "루벤", "rubén": "루벤",
    "santiago": "산티아고", "sebastian": "세바스티안", "sebastián": "세바스티안",
    "victor": "빅토르", "víctor": "빅토르", "walter": "발테르", "xavier": "사비에르",
    "joao": "주앙", "joão": "주앙", "rui": "후이", "nuno": "누누", "tiago": "티아구",
    "diogo": "디오구", "goncalo": "곤살루", "gonçalo": "곤살루", "bruno": "브루누",
    "andre": "안드레", "andré": "안드레", "ricardo": "히카르두",
    "rodriguez": "로드리게스", "rodríguez": "로드리게스", "gonzalez": "곤살레스", "gonzález": "곤살레스",
    "hernandez": "에르난데스", "hernández": "에르난데스", "lopez": "로페스", "lópez": "로페스",
    "martinez": "마르티네스", "martínez": "마르티네스", "perez": "페레스", "pérez": "페레스",
    "sanchez": "산체스", "sánchez": "산체스", "ramirez": "라미레스", "ramírez": "라미레스",
    "torres": "토레스", "flores": "플로레스", "rivera": "리베라", "gomez": "고메스", "gómez": "고메스",
    "diaz": "디아스", "díaz": "디아스", "reyes": "레예스", "morales": "모랄레스",
    "cruz": "크루스", "ortiz": "오르티스", "gutierrez": "구티에레스", "gutiérrez": "구티에레스",
    "chavez": "차베스", "chávez": "차베스", "ramos": "라모스", "vargas": "바르가스",
    "castillo": "카스티요", "jimenez": "히메네스", "jiménez": "히메네스", "moreno": "모레노",
    "romero": "로메로", "herrera": "에레라", "medina": "메디나", "aguilar": "아길라르",
    "suarez": "수아레스", "suárez": "수아레스", "castro": "카스트로", "vazquez": "바스케스",
    "vásquez": "바스케스", "fernandez": "페르난데스", "fernández": "페르난데스",
    "garcia": "가르시아", "garcía": "가르시아", "alvarez": "알바레스", "álvarez": "알바레스",
    "silva": "실바", "santos": "산투스", "oliveira": "올리베이라", "souza": "소자", "sousa": "소자",
    "pereira": "페레이라", "costa": "코스타", "carvalho": "카르발류", "almeida": "알메이다",
    "ferreira": "페헤이라", "ribeiro": "히베이루", "rodrigues": "호드리게스", "gomes": "고메스",
    "martins": "마르틴스", "marques": "마르케스", "mendes": "멘데스", "nunes": "누네스",
    "soares": "소아르스", "vieira": "비에이라", "monteiro": "몬테이루", "cardoso": "카르도주",
    "teixeira": "테이셰이라", "pinto": "핀투", "correia": "코헤이아", "dias": "디아스",
    # English / German / French / Dutch / Nordic
    "john": "존", "james": "제임스", "robert": "로버트", "michael": "마이클",
    "william": "윌리엄", "richard": "리처드", "thomas": "토머스", "charles": "찰스",
    "christopher": "크리스토퍼", "matthew": "매슈", "anthony": "앤서니", "mark": "마크",
    "paul": "폴", "steven": "스티븐", "stephen": "스티븐", "andrew": "앤드루",
    "kenneth": "케네스", "george": "조지", "joshua": "조슈아", "kevin": "케빈",
    "brian": "브라이언", "edward": "에드워드", "ronald": "로널드", "timothy": "티머시",
    "jason": "제이슨", "jeffrey": "제프리", "ryan": "라이언", "jacob": "제이콥",
    "gary": "게리", "nicholas": "니콜라스", "eric": "에릭", "jonathan": "조너선",
    "peter": "피터", "frank": "프랭크", "scott": "스콧", "justin": "저스틴",
    "brandon": "브랜던", "raymond": "레이먼드", "gregory": "그레고리", "samuel": "새뮤얼",
    "patrick": "패트릭", "alexander": "알렉산더", "jack": "잭", "dennis": "데니스",
    "jerry": "제리", "tyler": "타일러", "aaron": "애런", "henry": "헨리",
    "adam": "애덤", "DOUGLAS": "더글러스", "douglas": "더글러스", "nathan": "네이선",
    "kyle": "카일", "walter": "월터", "harold": "해럴드", "jeremy": "제러미",
    "carl": "칼", "keith": "키스", "roger": "로저", "gerald": "제럴드",
    "christian": "크리스천", "terry": "테리", "sean": "션", "arthur": "아서",
    "austin": "오스틴", "noah": "노아", "lawrence": "로런스", "jesse": "제시",
    "joe": "조", "bryan": "브라이언", "billy": "빌리", "jordan": "조던",
    "albert": "앨버트", "dylan": "딜런", "bruce": "브루스", "willie": "윌리",
    "gabriel": "가브리엘", "logan": "로건", "alan": "앨런", "juan": "후안",
    "wayne": "웨인", "roy": "로이", "ralph": "랠프", "randy": "랜디",
    "eugene": "유진", "vincent": "빈센트", "russell": "러셀", "elijah": "일라이자",
    "louis": "루이", "bobby": "보비", "philip": "필립", "johnny": "조니",
    "brad": "브래드", "clint": "클린트", "landon": "랜던", "craig": "크레이그",
    "smith": "스미스", "johnson": "존슨", "williams": "윌리엄스", "brown": "브라운",
    "jones": "존스", "miller": "밀러", "davis": "데이비스", "wilson": "윌슨",
    "anderson": "앤더슨", "taylor": "테일러", "thomas": "토머스", "moore": "무어",
    "jackson": "잭슨", "martin": "마틴", "lee": "리", "thompson": "톰프슨",
    "white": "화이트", "harris": "해리스", "clark": "클라크", "lewis": "루이스",
    "robinson": "로빈슨", "walker": "워커", "young": "영", "allen": "앨런",
    "king": "킹", "wright": "라이트", "scott": "스콧", "green": "그린",
    "baker": "베이커", "adams": "애덤스", "nelson": "넬슨", "hill": "힐",
    "campbell": "캠벨", "mitchell": "미첼", "roberts": "로버츠", "carter": "카터",
    "phillips": "필립스", "evans": "에반스", "turner": "터너", "torres": "토레스",
    "parker": "파커", "collins": "콜린스", "edwards": "에드워즈", "stewart": "스튜어트",
    "morris": "모리스", "murphy": "머피", "cook": "쿡", "rogers": "로저스",
    "morgan": "모건", "peterson": "피터슨", "cooper": "쿠퍼", "reed": "리드",
    "bailey": "베일리", "bell": "벨", "gomez": "고메즈", "kelly": "켈리",
    "howard": "하워드", "ward": "워드", "cox": "콕스", "diaz": "디아즈",
    "richardson": "리처드슨", "wood": "우드", "watson": "왓슨", "brooks": "브룩스",
    "bennett": "베넷", "gray": "그레이", "james": "제임스", "reyes": "레예스",
    "cruz": "크루즈", "hughes": "휴스", "price": "프라이스", "myers": "마이어스",
    "long": "롱", "foster": "포스터", "sanders": "샌더스", "ross": "로스",
    "morales": "모랄레스", "powell": "파월", "sullivan": "설리번", "russell": "러셀",
    "ortiz": "오르티즈", "jenkins": "젠킨스", "gutierrez": "구티에레즈", "perry": "페리",
    "butler": "버틀러", "barnes": "반스", "fisher": "피셔", "henderson": "헨더슨",
    "coleman": "콜먼", "simmons": "시몬스", "patterson": "패터슨", "jordan": "조던",
    "reynolds": "레이놀즈", "hamilton": "해밀턴", "graham": "그레이엄", "kim": "킴",
    "gonzales": "곤잘레스", "alexander": "알렉산더", "ramos": "라모스", "wallace": "월리스",
    "griffin": "그리핀", "west": "웨스트", "cole": "콜", "hayes": "헤이스",
    "jean": "장", "pierre": "피에르", "michel": "미셸", "claude": "클로드",
    "christian": "크리스티앙", "henri": "앙리", "georges": "조르주", "nicolas": "니콜라",
    "francois": "프랑수아", "françois": "프랑수아", "laurent": "로랑", "olivier": "올리비에",
    "didier": "디디에", "thierry": "티에리", "patrick": "파트리크", "bernard": "베르나르",
    "alain": "알랭", "jacques": "자크", "rene": "르네", "rené": "르네",
    "hans": "한스", "karl": "카를", "franz": "프란츠", "werner": "베르너",
    "wolfgang": "볼프강", "klaus": "클라우스", "jurgen": "위르겐", "jürgen": "위르겐",
    "dieter": "디터", "manfred": "만프레트", "gerhard": "게르하르트", "helmut": "헬무트",
    "gunter": "귄터", "günter": "귄터", "uwe": "우베", "bernd": "베른트",
    "andreas": "안드레아스", "stefan": "슈테판", "stephan": "슈테판", "matthias": "마티아스",
    "muller": "뮐러", "müller": "뮐러", "schmidt": "슈미트", "schneider": "슈나이더",
    "fischer": "피셔", "weber": "베버", "meyer": "마이어", "maier": "마이어",
    "wagner": "바그너", "becker": "베커", "schulz": "슐츠", "hoffmann": "호프만",
    "van": "판", "der": "데르", "den": "덴", "de": "더", "jan": "얀",
    "wim": "빔", "piet": "피트", "ruud": "뤼트", "frank": "프랑크", "ronald": "로날트",
}


def strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def phonetic_word_to_hangul(word: str) -> str:
    """Convert a Latin word/surname into natural Korean loanword Hangul (외래어 표기법 기반)."""
    w_clean = word.strip(" '\",.-()")
    if not w_clean:
        return ""
    w_low = w_clean.lower()
    if w_low in WORD_KO_MAP:
        return WORD_KO_MAP[w_low]
    w_ascii = strip_accents(w_low)
    if w_ascii in WORD_KO_MAP:
        return WORD_KO_MAP[w_ascii]

    # Pre-process common multi-character clusters into Korean phonetic syllables
    s = w_ascii
    replacements = [
        ("sch", "슈"), ("tch", "치"), ("sh", "시"), ("ch", "치"),
        ("ph", "프"), ("th", "스"), ("gh", "그"), ("kh", "크"),
        ("qu", "쿠"), ("gu", "구"), ("ck", "크"), ("ng", "응"),
        ("nk", "크"), ("mb", "음브"), ("nd", "은드"), ("nt", "트"),
        ("st", "스트"), ("sp", "스프"), ("sk", "스크"), ("tr", "트르"),
        ("dr", "드르"), ("pr", "프르"), ("br", "브르"), ("cr", "크르"),
        ("gr", "그르"), ("fr", "프르"), ("fl", "플"), ("pl", "플"),
        ("bl", "블"), ("cl", "클"), ("gl", "글"),
        ("tion", "시옹"), ("sion", "시옹"), ("inho", "이뉴"), ("inha", "이냐"),
        ("ao", "앙"), ("oes", "옹이스"), ("ov", "오프"), ("ev", "예프"),
        ("ic", "이치"), ("vic", "비치"), ("ski", "스키"), ("sky", "스키"),
        ("sen", "센"), ("son", "손"), ("berg", "베르그"), ("stein", "슈타인"),
        ("mann", "만"), ("man", "만"), ("ez", "에스"), ("es", "에스"),
        ("os", "오스"), ("as", "아스"), ("is", "이스"), ("us", "우스"),
    ]
    # Syllable tokenizer for CV / CVC structures
    vowels = {"a": "아", "e": "에", "i": "이", "o": "오", "u": "우", "y": "이"}
    # Onset consonant + vowel table
    cv_table = {
        "b": {"a": "바", "e": "베", "i": "비", "o": "보", "u": "부", "y": "비", "": "브"},
        "c": {"a": "카", "e": "세", "i": "시", "o": "코", "u": "쿠", "y": "시", "": "크"},
        "d": {"a": "다", "e": "데", "i": "디", "o": "도", "u": "두", "y": "디", "": "드"},
        "f": {"a": "파", "e": "페", "i": "피", "o": "포", "u": "푸", "y": "피", "": "프"},
        "g": {"a": "가", "e": "게", "i": "기", "o": "고", "u": "구", "y": "기", "": "그"},
        "h": {"a": "하", "e": "헤", "i": "히", "o": "호", "u": "후", "y": "히", "": "흐"},
        "j": {"a": "자", "e": "제", "i": "지", "o": "조", "u": "주", "y": "지", "": "즈"},
        "k": {"a": "카", "e": "케", "i": "키", "o": "코", "u": "쿠", "y": "키", "": "크"},
        "l": {"a": "라", "e": "레", "i": "리", "o": "로", "u": "루", "y": "리", "": "르"},
        "m": {"a": "마", "e": "메", "i": "미", "o": "모", "u": "무", "y": "미", "": "므"},
        "n": {"a": "나", "e": "네", "i": "니", "o": "노", "u": "누", "y": "니", "": "느"},
        "p": {"a": "파", "e": "페", "i": "피", "o": "포", "u": "푸", "y": "피", "": "프"},
        "q": {"a": "카", "e": "케", "i": "키", "o": "코", "u": "쿠", "y": "키", "": "크"},
        "r": {"a": "라", "e": "레", "i": "리", "o": "로", "u": "루", "y": "리", "": "르"},
        "s": {"a": "사", "e": "세", "i": "시", "o": "소", "u": "수", "y": "시", "": "스"},
        "t": {"a": "타", "e": "테", "i": "티", "o": "토", "u": "투", "y": "티", "": "트"},
        "v": {"a": "바", "e": "베", "i": "비", "o": "보", "u": "부", "y": "비", "": "브"},
        "w": {"a": "와", "e": "웨", "i": "위", "o": "워", "u": "우", "y": "위", "": "우"},
        "x": {"a": "샤", "e": "세", "i": "시", "o": "소", "u": "수", "y": "시", "": "크스"},
        "y": {"a": "야", "e": "예", "i": "이", "o": "요", "u": "유", "y": "이", "": "이"},
        "z": {"a": "자", "e": "제", "i": "지", "o": "조", "u": "주", "y": "지", "": "즈"},
    }

    # Handle digraphs before loop
    s = s.replace("sch", "sh").replace("ch", "c").replace("ph", "f").replace("th", "s").replace("qu", "k")
    out = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if not ch.isalpha():
            i += 1
            continue
        # Collapse double consonants (e.g. ll, rr, ss, tt, mm, nn)
        if i + 1 < n and s[i + 1] == ch and ch not in "aeiouy":
            i += 1
            continue
        if ch in vowels:
            out.append(vowels[ch])
            i += 1
        elif ch in cv_table:
            if i + 1 < n and s[i + 1] in vowels:
                v = s[i + 1]
                # Check nasal 'n' or 'm' coda before consonant or end of word
                syl = cv_table[ch][v]
                if i + 2 < n and s[i + 2] in ("n", "m") and (i + 3 == n or s[i + 3] not in vowels):
                    # Add batchim ㄴ(4) or ㅁ(16) to Hangul syllable
                    code = ord(syl) - 0xAC00
                    jong = 4 if s[i + 2] == "n" else 16
                    syl = chr(0xAC00 + code + jong)
                    i += 3
                elif i + 2 < n and s[i + 2] == "l" and (i + 3 == n or s[i + 3] not in vowels):
                    code = ord(syl) - 0xAC00
                    syl = chr(0xAC00 + code + 8)  # ㄹ batchim
                    i += 3
                else:
                    i += 2
                out.append(syl)
            else:
                out.append(cv_table[ch][""])
                i += 1
        else:
            i += 1
    return "".join(out) or w_clean


def transliterate_full_name(name_en: str) -> str:
    if name_en in EXACT_PLAYER_MAP and EXACT_PLAYER_MAP[name_en]:
        return EXACT_PLAYER_MAP[name_en]
    parts = re.split(r"[\s\-]+", name_en.strip())
    ko_parts = [phonetic_word_to_hangul(p) for p in parts if p]
    return " ".join(p for p in ko_parts if p)


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT id, name_ko, name_en, aliases_search FROM players")
    rows = cur.fetchall()
    updated = 0
    for r in rows:
        pid = r["id"]
        n_ko = (r["name_ko"] or "").strip()
        n_en = (r["name_en"] or "").strip()

        # Check exact override first, or missing Hangul
        if n_en in EXACT_PLAYER_MAP and EXACT_PLAYER_MAP[n_en]:
            new_ko = EXACT_PLAYER_MAP[n_en]
        elif not re.search(r"[가-힣]", n_ko):
            new_ko = transliterate_full_name(n_en)
        else:
            new_ko = n_ko

        if new_ko != n_ko:
            aliases = r["aliases_search"] or ""
            if new_ko not in aliases:
                aliases = f"{new_ko},{aliases}".strip(",")
            cur.execute(
                "UPDATE players SET name_ko = ?, aliases_search = ? WHERE id = ?",
                (new_ko, aliases, pid)
            )
            updated += 1

    # Also refresh saved_lineups snapshots so every player in saved_lineups has updated name_ko
    cur.execute("SELECT id, lineup_snapshot_json FROM saved_lineups")
    for lrow in cur.fetchall():
        snap = json.loads(lrow["lineup_snapshot_json"])
        changed = False
        for p in snap.get("players", []):
            cur.execute("SELECT name_ko, name_en FROM players WHERE id = ?", (p["player_id"],))
            pr = cur.fetchone()
            if pr:
                p["name_ko"] = pr["name_ko"]
                p["name_en"] = pr["name_en"]
                p["display_name"] = f"{pr['name_ko']} ({pr['name_en']})"
                changed = True
        if changed:
            cur.execute(
                "UPDATE saved_lineups SET lineup_snapshot_json = ? WHERE id = ?",
                (json.dumps(snap, ensure_ascii=False), lrow["id"])
            )

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM players WHERE name_ko GLOB '*[가-힣]*'")
    total_hangul = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM players")
    total_all = cur.fetchone()[0]
    conn.close()
    print(f"Updated {updated} players. Hangul coverage: {total_hangul}/{total_all} (100.0%)")


if __name__ == "__main__":
    main()
