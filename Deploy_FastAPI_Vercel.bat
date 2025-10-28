@echo off
SETLOCAL

REM ================================================
REM   FastAPI Deploy — Praxis Portal Executivo Blue
REM ================================================

echo.
echo ✅ Iniciando deploy FastAPI na Vercel...
echo.

REM 🔥 Forçar execução no caminho onde o BAT está
cd /d "%~dp0"
echo 📁 Diretório atual:
cd
echo.

REM 1) Validar Python
echo [1/10] — Validando Python...
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python não encontrado!
    pause
    exit /b
)

REM 2) Criar main.py
echo.
echo [2/10] — Criando main.py...
(
echo from fastapi import FastAPI
echo.
echo app = FastAPI()
echo.
echo @app.get("/")
echo async def root():
echo^    return {"status": "✅ API FastAPI ativa na Vercel"}
) > main.py
echo ✅ main.py criado/atualizado

REM 3) Criar requirements.txt
echo.
echo [3/10] — Criando requirements.txt...
(
echo fastapi
echo uvicorn
) > requirements.txt
echo ✅ requirements.txt criado/atualizado

REM 4) Criar api/index.py
echo.
echo [4/10] — Criando api/index.py...
IF NOT EXIST api mkdir api

(
echo from main import app
) > api\index.py
echo ✅ api/index.py criado/atualizado

REM 5) Criar vercel.json
echo.
echo [5/10] — Criando vercel.json...
(
echo {
echo   "version": 2,
echo   "routes": [
echo     { "src": "/(.*)", "dest": "/api/index.py" }
echo   ]
echo }
) > vercel.json
echo ✅ vercel.json criado/atualizado

REM 6) Git add
echo.
echo [6/10] — Git add...
git add .

REM 7) Git commit
echo.
echo [7/10] — Git commit...
git commit -m "auto: fastapi minimal structure for vercel"

REM 8) Git push
echo.
echo [8/10] — Git push...
git push

REM 9) Deploy
echo.
echo [9/10] — Deploy Vercel...
vercel --prod --force

echo.
echo ✅ Deploy finalizado!
echo Teste em: https://praxis-portal-executivo-blue.vercel.app/
echo.
pause
