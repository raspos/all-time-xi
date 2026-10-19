# ALL-TIME XI — 데이터 출처, 라이선스 및 검증 보고서 (`DATA_SOURCES.md`)

본 문서는 **ALL-TIME XI** 서비스에 수록된 30개국 역대 남자 성인 A대표팀 선수 데이터베이스(`data/all_time_xi.db`)의 출처, 수록 범위, 라이선스 조건, 국가 승계 처리 원칙 및 한계점을 명시합니다.

---

## 1. 조사 및 결합한 데이터셋 목록

| 순번 | 출처 코드 | 데이터셋 / 기관명 | URL / 리포지토리 | 수록 범위 | 라이선스 및 이용 조건 | 활용 방식 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `rsssf` | **RSSSF** (Rec.Sport.Soccer Statistics Foundation) | `https://www.rsssf.org/miscellaneous/century.html` 및 국가별 `-intlp.html` | **1900년대 ~ 2026년** 국가별 A매치 최다 출전·득점 역사 기록 | 학술·비영리 통계 인용 허용 (출처 명시) | **1950~2000년대 이전 역사적 레전드 및 국가별 통산 A매치 출전/득점 1차 기준** (`data/raw/rsssf/<CODE>.html` 30개국 파싱) |
| 2 | `wikipedia_intl` | **Wikipedia** (`List of <Country> international footballers`) | `https://en.wikipedia.org/wiki/List_of_..._international_footballers` | **1900년대 ~ 2026년** 국가별 A대표팀 출전 선수 전체 테이블 | **CC BY-SA 4.0** (저작자 및 동일조건변경허락) | **포지션(`GK/DF/MF/FW`), 활동 연도, 통산 출전·득점 교차 검증 및 누락 보강** (`data/raw/wikipedia/<CODE>.html`) |
| 3 | `wikidata` / `wikimedia_commons` | **Wikidata SPARQL & MediaWiki API / Wikimedia Commons** | `https://www.wikidata.org/w/api.php` | 전 시대 축구선수 엔티티 (`Q5` 인간, `P106=Q937857` 축구선수) | **CC0 1.0 (Wikidata 데이터)** / **CC BY-SA 또는 Public Domain (Wikimedia Commons 이미지)** | **한국어 공식 표기(`labels.ko`), 생몰년(`P569`/`P570`), 신장(`P2048`), 포지션(`P413`), 위키미디어 커먼즈 초상화(`P18`) 매핑** (2,842명 엔티티 결합) |
| 4 | `transfermarkt_open` | **dcaribou/transfermarkt-datasets** (GitHub Open Dataset) | `https://github.com/dcaribou/transfermarkt-datasets` | 주로 **1990년대 후반 ~ 2020년대** 선수 50,149명 (`players.csv.gz`, `clubs.csv.gz`) | **CC0 1.0 Public Domain Dedication** | **현대 선수 상세 세부 포지션(`sub_position`), 주발(`foot`), 신장(`height_in_cm`), 소속 클럽 보강** (단독 사용 시 고전 레전드가 누락되므로 반드시 RSSSF/Wikipedia와 병합 사용) |
| 5 | `legends_curated` | **FIFA Century Club & 각국 축구협회 공인 레전드 검증 카탈로그** | 각국 축구협회(CBF, AFA, FFF, DFB, KFA, JFA 등) 및 FIFA 공식 기록 | 30개국 시대를 대표하는 핵심 레전드 및 전술 프로필 | 사실 기록(Fact) 인용 | **한국어 이름/별칭, 전성기 활동 기간, 주요 소속 클럽, 월드컵/대륙 대회 우승·발롱도르 수상 이력, 플레이 스타일·전술 역할 정밀 보강** |

---

## 2. 선수 등록 자격 및 판정 기준 (A매치 30회 이상)

1. **유일한 필수 자격**: 해당 국가의 **성인 남자 A대표팀 공식 경기 출전 횟수(`official_caps`) 30회 이상** (`is_eligible_30_caps = 1`).
2. **29회 이하 선수 제외**:
   - 공식 A매치 출전 29회 이하 선수는 후보 목록 API(`GET /api/players?country=...`)에서 기본 제외되며, 강제로 라인업 저장(`POST /api/lineups`)을 요청할 경우 서버에서 `HTTP 400`으로 차단합니다.
   - 검증 테스트를 위해 엔드릭(브라질 18경기), 발렌틴 바르코(아르헨티나 2경기), 파우 쿠바르시(스페인 10경기), 워렌 자이르에메리(프랑스 16경기) 등 `< 30`경기 레코드가 `is_eligible_30_caps = 0` 상태로 DB에 등록되어 있으며 후보 목록에서 제외됨을 자동 테스트(`Test G`)로 검증합니다.
3. **복수 국가 A대표팀 출전 선수 분리 원칙**:
   - 특정 선수가 복수 국가의 성인 A대표팀에서 활약한 경우, **두 국가의 출전 횟수를 합산하여 30회 자격을 부여하지 않습니다.**
   - 대표 사례: **알프레도 디 스테파노(Alfredo Di Stéfano)**
     - 아르헨티나(`ARG`) 대표팀: **6경기 6골** (`1947`) → `is_eligible_30_caps = 0` (**아르헨티나 후보에서 제외**)
     - 스페인(`ESP`) 대표팀: **31경기 23골** (`1957–1961`) → `is_eligible_30_caps = 1` (**스페인 후보에서 선택 가능**)
   - 대표 사례: **페렌츠 푸스카스(Ferenc Puskás)** — 스페인(`ESP`) 대표팀에서는 4경기 출전으로 제외.

---

## 3. 역사적 국가대표팀 승계(Succession) 처리 원칙

`country_succession_mappings` 테이블을 통해 FIFA 및 각국 축구협회가 공식 인정하는 역사적 승계 관계를 관리합니다.

| 현대 국가 코드 | 선행(과거) 대표팀 코드 및 명칭 | 출전 기록 합산 여부 | 처리 근거 및 주의사항 |
| :--- | :--- | :--- | :--- |
| **GER (독일)** | `FRG` (서독, 1950–1990) | **포함 (`include_in_caps = 1`)** | DFB 및 FIFA 공식 기록상 서독(FRG)과 통일 독일(GER)은 동일 연맹으로 승계됨 (프란츠 베켄바워, 게르트 뮐러, 로타어 마테우스 등 포함) |
| **GER (독일)** | `GDR` (동독, 1952–1990) | **조건부 분리** | 동독(DFV) 단독 A매치 기록은 서독/독일 A매치 출전 횟수와 무단 합산하지 않으며, 통일 이후 독일 대표팀 출전분과 구분 관리 |
| **CRO (크로아티아)** / **SRB (세르비아)** | `YUG` (유고슬라비아) | **자동 귀속 금지 (`include_in_caps = 0`)** | 구 유고슬라비아 대표팀 출전 기록을 현대 크로아티아 대표팀에 무분별하게 합산하지 않음 (크로아티아 독립 이후 HNS 공식 A매치 30회 이상 기준 적용) |
| **UKR (우크라이나)** | `URS` (소련) | **자동 귀속 금지 (`include_in_caps = 0`)** | 구 소련(URS) 대표팀 기록을 현대 우크라이나(UAF) 대표팀 30경기 자격에 무조건 합산하지 않음 (독립 이후 우크라이나 대표팀 30경기 이상 선수 수록) |

---

## 4. 선수 초상화 라이선스 및 폴백(대체 이미지) 정책

- **위키미디어 커먼즈(`Wikimedia Commons`) 사진**: Wikidata `P18` 속성으로 확인된 위키미디어 커먼즈 파일명만 `Special:FilePath/<filename>?width=320` 경로로 연결하며, `player_images` 테이블에 `license_name = 'CC BY-SA / Public Domain (Wikimedia Commons)'`, `requires_attribution = 1`을 명시합니다.
- **저작권 미확인 외부 사진 무단 복제 금지**: 저작권이 불분명한 상업 사이트 사진을 무단 크롤링하지 않습니다.
- **국가별 유니폼 엠블럼 폴백**: 사진이 존재하지 않는 고전 시대 선수(`image_url = null`)는 전술판 UI 및 고해상도 PNG 내보내기 시 **해당 국가의 고유 유니폼 컬러 배지 + 포지션/이름 이니셜 엠블럼**으로 자동 대체되어 깨진 이미지가 발생하지 않습니다.

---

## 5. 데이터 수록 한계 및 품질 보증

- 본 데이터베이스는 **30개국 총 3,817명의 A매치 30회 이상 검증 선수**(`1920s`~`2020s`)를 수록하고 있습니다.
- 단, RSSSF와 Wikipedia에서 동명이인 구분이나 세부 전술 역할(`세부 포지션`, `주발`, `신장`)이 역사적 사료에 남아 있지 않은 1930~1970년대 일부 선수의 경우, 확인되지 않은 정보를 AI로 임의 생성하지 않고 `null`로 유지합니다.
- 각 국가 선택 시 화면 상단 배너 및 **「데이터 품질·관리」** 탭에서 해당 국가의 **데이터 수록 시대 범위, 출전 기록 검증 완료율, 사진 확보율, 출전 횟수 출처 간 차이(Discrepancy) 건수**를 투명하게 공개합니다.
