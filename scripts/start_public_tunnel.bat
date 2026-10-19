@echo off
chcp 65001 > nul
title ALL-TIME XI — 외부 공개 터널 (Cloudflare Quick Tunnel)

echo ========================================================
echo   ALL-TIME XI — 무료 외부 공개 웹사이트 터널 실행기
echo ========================================================
echo.
echo 로컬 서버(http://localhost:8000)를 외부 인터넷에서 누구나
echo 접속할 수 있도록 전세계 공개 HTTPS 주소를 발급합니다.
echo.

set CLOUDFLARED_EXE=%~dp0cloudflared.exe

if not exist "%CLOUDFLARED_EXE%" (
    echo [1/2] Cloudflare 터널 실행기(cloudflared) 다운로드 중...
    curl -L -o "%CLOUDFLARED_EXE%" https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe
    if errorlevel 1 (
        echo [오류] 다운로드에 실패했습니다. 인터넷 연결을 확인해 주세요.
        pause
        exit /b 1
    )
)

echo.
echo [2/2] 외부 공개 터널을 시작합니다!
echo 잠시 후 아래 로그에 생성되는 'https://....trycloudflare.com' 주소가
echo 외부 공개 웹사이트 주소입니다. 스마트폰이나 친구에게 공유해 보세요!
echo.
echo [주의] 이 창을 닫으면 외부 접속이 종료됩니다.
echo ========================================================
echo.

"%CLOUDFLARED_EXE%" tunnel --url http://localhost:8000
pause
