@echo off
SETLOCAL

echo ================================================
echo   FastAPI Deploy — Praxis Portal Executivo Blue
echo ================================================

REM 🔥 Fix path (remove trailing quotes)
for %%I in ("%~dp0.") do set PROJECT_DIR=%%~fI
echo ✅ Diretório alvo: "%PROJECT_DIR%"
cd /d "%PROJECT_DIR%"

echo.

echo [1/8] Verificando Python
python --version || (echo ❌ Python não encontrado! & pause & exit /b)

echo.
echo [2/8] Criando main.py...
(
echo from fastapi import FastAPI
echo.
echo app = FastAPI()
echo.
echo @app.get("/")
echo async def root():
echo^    return {"status": "✅ API FastAPI ativa na Vercel"}
) > main.py

echo.
echo [3/8] Criando requirements.txt...
(
echo fastapi
echo uvicorn
) > requirements.txt

echo.
echo [4/8] Criando api/index.py...
if not exist api mkdir api
(
echo from main import app
) > api\index.py

echo.
echo [5/8] Criando vercel.json...
(
echo {
echo   "version": 2,
echo   "routes": [
echo     { "src": "/(.*)", "dest": "/api/index.py" }
echo   ]
echo }
) > vercel.json

echo.
echo [6/8] Git add...
git add .

echo.
echo [7/8] Git commit...
git commit -m "auto: safe deploy structure" || echo (nada para commitar)

echo.
echo [8/8] Git push...
git push

echo.
echo 🚀 Deploy Vercel...
vercel deploy --prod --force --cwd "%PROJECT_DIR%"

echo.
echo ✅ FINALIZADO
pause
