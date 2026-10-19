# ALL-TIME XI — 역대 최강의 국가대표를 만들어라

FIFA 세계랭킹 상위 30개국(기준일: **2026-10-07**)을 대상으로, **성인 남자 A대표팀 공식 경기 30회 이상 출전**이 검증된 **3,766명(1920년대~2020년대)**의 실제 축구 데이터베이스를 기반으로 나만의 역대 베스트11 전술판을 제작·공유하고, **Gemini / OpenAI AI 가상 대결**을 수행하는 풀스택 웹서비스입니다.

---

## 1. 주요 기능 요약

1. **FIFA 세계랭킹 TOP 30 국가 선택 (`2026-10-07` 스냅샷)**
   - 국가 마스터 테이블(`countries`)과 랭킹 스냅샷(`country_ranking_snapshots`) 분리 설계로 향후 FIFA 랭킹 갱신 시에도 기존 저장된 베스트11 영구 보존
   - 대륙 연맹별 필터(`UEFA`, `CONMEBOL`, `CONCACAF`, `CAF`, `AFC`) 및 국가명(한국어/영문/FIFA 코드) 실시간 검색
2. **시대를 초월한 역대 베스트11 전술판 빌더**
   - **선수 이름 `한글(영문)` 기본 표기**: 모든 선수를 `펠레 (Pelé)`, `호나우두 (Ronaldo)`, `리오넬 메시 (Lionel Messi)` 형태의 **한글(영문)** 기본 포맷으로 표시
   - **포지션 슬롯 클릭 시 A매치 출전 경기 순 추천**: 전술판에서 포지션 슬롯(`GK`, `LB`, `CB`, `CM`, `ST` 등)을 클릭하면 해당 포지션 적합 선수들을 **A매치 공식 출전 경기 많은 순(`official_caps DESC`)**으로 즉시 추천
   - **직접 선수 검색**: 추천 목록 상단 검색창에서 한글·영문·별칭으로 전체 선수를 직접 검색하여 즉시 배치 가능
   - **7종 전술 포메이션 지원**: `4-3-3`, `4-4-2`, `4-2-3-1`, `3-5-2`, `3-4-3`, `4-1-4-1`, `5-3-2` (포메이션 변경 시 기존 배치 선수 유지 및 포지션 적합도 자동 재계산)
   - **드래그 앤 드롭 & 터치/클릭 스왑**: 전술판 위에서 선수 위치를 자유롭게 교체하고 주장(`C`) 지정 가능
3. **고해상도 PNG 전술판 이미지 내보내기 & 고유 공유 URL**
   - **세로형(`1080×1350`)**, **가로형(`1200×675`)**, **2배율 초고해상도(`2x`)** PNG 즉시 렌더링 및 다운로드
   - 사진이 없는 고전 시대 선수는 **국가별 대표 컬러 유니폼 배지**로 자동 폴백 렌더링
   - `/team/{slug}` 고유 공유 URL 생성, 타 브라우저/세션 열람, 원클릭 복제 수정 지원
4. **AI 베스트11 가상 대결 (`Gemini API` 기본 / `OpenAI API` 지원)**
   - 양 팀 22명 전원의 실제 전성기 기록·수상 이력·포지션 적합도·전술 스타일을 서버에서 프롬프트로 구성하여 구조화된 전술 분석 리포트 생성
   - API 키 미설정 시 가짜 고정 응답을 생성하지 않으며, 상단 **「🔑 AI API 키 설정」** 모달 또는 `.env`를 통해 즉시 등록 가능

---

## 2. 로컬 서버 실행 방법

### 사전 요구사항
- Python 3.10 이상 (현재 환경: **Python 3.12.10**)
- 필수 패키지 설치:
  ```powershell
  pip install fastapi uvicorn pydantic pillow requests beautifulsoup4 pandas openai
  ```

### 데이터베이스 재구축 (선택 — 이미 `data/all_time_xi.db`가 구축되어 있습니다)
```powershell
python -X utf8 scripts/build_database.py
python -X utf8 scripts/enrich_korean_names.py
```

### 개발/서비스 서버 실행
```powershell
uvicorn server.app:app --host 0.0.0.0 --port 8000
```
- 브라우저에서 접속: **http://localhost:8000**

### 자동 검증 테스트 스위트(Tests A ~ J) 실행
```powershell
python -X utf8 scripts/run_all_tests.py
```

---

## 3. AI API 키(`GEMINI_API_KEY`) 설정 방법

1. **방법 A — 환경변수 또는 `.env` 파일 설정**:
   프로젝트 루트(`all-time-xi/.env`)에 아래 내용을 작성합니다 (`.env.example` 참고):
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   # 선택: OpenAI 사용 시
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   ```
2. **방법 B — 웹 UI에서 런타임 즉시 등록**:
   웹 화면 우측 상단 **`🔑 AI API 키 설정`** 버튼을 클릭하여 `GEMINI_API_KEY` 또는 `OPENAI_API_KEY`를 입력하면 서버 메모리에 즉시 반영됩니다.

---

## 4. 배포 방법 (Render / Railway / Docker / Cloud Run)

- **단일 컨테이너/프로세스 배포**: FastAPI가 정적 프론트엔드(`public/`)와 REST API(`/api/...`), 서버사이드 PNG 렌더러, SQLite DB(`data/all_time_xi.db`)를 모두 서빙합니다.
- **시작 커맨드(Start Command)**:
  ```bash
  uvicorn server.app:app --host 0.0.0.0 --port ${PORT:-8000}
  ```
- **환경변수 등록**: 배포 플랫폼의 Environment Variables 설정에 `GEMINI_API_KEY`를 등록합니다.
