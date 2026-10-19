# ALL-TIME XI — 외부 공개 웹사이트 배포 가이드

본 프로젝트는 **외부 공개 웹사이트(Public Web Application)**로 즉시 운영될 수 있도록 모든 배포 설정이 완료되었습니다.  
방문자에게 어떠한 API 키 등록도 요구하지 않으며, 자체 탑재된 **전술 시뮬레이션 AI 엔진**이 기본 작동하여 24시간 안정적으로 전술판 제작, 팀 공유, 고해상도 PNG 다운로드, 가상 대결을 제공합니다.

---

## ⚡ 방법 1. GitHub + Vercel 조합 배포 (가장 빠르고 강력한 추천)

본 프로젝트는 Vercel Serverless Function(`api/index.py`, `vercel.json`)과 완전히 호환되도록 구성되어 있습니다.  
GitHub에 저장소를 푸시하고 Vercel에서 가져오기만 하면 **무료 글로벌 CDN HTTPS 사이트**가 1분 만에 완성됩니다.

### 1단계: GitHub에 새 저장소 생성 및 푸시
1. [GitHub.com](https://github.com)에서 **New repository**를 클릭합니다. (예: `all-time-xi`)
2. 터미널(PowerShell)에서 아래 명령어를 순서대로 실행합니다:
   ```bash
   git remote add origin https://github.com/<내-GitHub-아이디>/<저장소이름>.git
   git branch -M main
   git push -u origin main
   ```

### 2단계: Vercel에서 원클릭 배포
1. [Vercel.com](https://vercel.com)에 로그인 후 **[Add New...] → [Project]**를 클릭합니다.
2. 방금 올린 GitHub 저장소(`all-time-xi`)에서 **[Import]**를 클릭합니다.
3. 기본 설정 그대로 둔 채 **[Deploy]** 버튼을 누릅니다!
   - `vercel.json`과 `api/index.py`, `requirements.txt`가 이미 완벽히 세팅되어 있어 추가 설정이 필요 없습니다.
4. 약 1분 후 배포가 완료되면 `https://all-time-xi-xxx.vercel.app` 형태의 고유 공개 주소가 즉시 생성됩니다.
5. 방문자는 로그인이나 API 키 등록 없이 전술판을 만들고, 고해상도 PNG를 다운로드하고, AI 맞대결을 즐길 수 있습니다.

---

## 🚀 방법 2. 내 컴퓨터에서 즉시 외부 공개 (무료 1클릭 터널)

복잡한 클라우드 가입 없이 **지금 바로 스마트폰이나 친구들에게 사이트를 공개**하고 싶을 때 사용합니다.

1. 서버가 실행 중인 상태(`python -X utf8 -m uvicorn server.app:app --host 0.0.0.0 --port 8000`)를 유지합니다.
2. `scripts/start_public_tunnel.bat` 파일을 더블 클릭하여 실행합니다.
3. 콘솔 창에 출력되는 **`https://xxxxx.trycloudflare.com`** 형식의 공개 주소를 복사하여 공유하면, 전세계 어디서든 내 사이트에 접속할 수 있습니다!

---

## ☁️ 방법 3. Render.com 무료 클라우드 배포 (대안: 상시 운영)

GitHub 저장소와 연동하여 24시간 꺼지지 않는 무료 웹사이트를 생성할 수 있습니다.

1. [Render.com](https://render.com)에 로그인 후 **[New +] → [Web Service]**를 클릭합니다.
2. 본 프로젝트 GitHub 저장소를 선택합니다.
3. 설정값:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -X utf8 -m uvicorn server.app:app --host 0.0.0.0 --port $PORT`
4. 저장소 루트에 `render.yaml`이 포함되어 있어 **Blueprint**로 자동 설정도 가능합니다.
5. 배포 완료 시 `https://all-time-xi.onrender.com` 과 같은 고유 도메인이 생성됩니다.

---

## 🚆 방법 3. Railway / Fly.io 배포

- **Railway.app**: 저장소를 연결하면 `Procfile`과 `requirements.txt`를 감지하여 원클릭으로 배포됩니다.
- **Fly.io**: 
  ```bash
  fly launch
  fly deploy
  ```
  저장소의 `fly.toml`과 `Dockerfile`을 통해 도쿄(NRT) 리전에 초고속으로 배포됩니다.

---

## 🐳 방법 4. Docker / VPS (Ubuntu, AWS, GCP, Lightsail)

서버 인스턴스에서 직접 도커 컨테이너로 운영할 경우:

```bash
# 컨테이너 빌드 및 백그라운드 실행
docker compose up -d

# 상태 및 로그 확인
docker compose logs -f
```

- `data/` 디렉터리가 볼륨으로 마운트되어 저장된 라인업과 SQLite 데이터가 영구 보존됩니다.
- 리눅스 환경에서도 한글(Nanum, Noto CJK) 폰트가 탑재되어 고해상도 PNG 이미지가 한글 깨짐 없이 완벽하게 렌더링됩니다.

---

## ⚙️ 환경변수 설정 (선택 사항)

`.env.example` 파일을 복사하여 `.env`를 생성할 수 있습니다.
- `PORT`: 서비스 포트 (기본값: `8000`)
- `AI_PROVIDER`: 기본 `engine` (내장 전술 시뮬레이션 AI 사용)
- `GEMINI_API_KEY`: (선택) 외부 Gemini LLM 모델로 대결 분석을 한층 더 고도화하고 싶을 경우 서버 관리자만 등록 (일반 방문자에게는 절대 노출되지 않음)
