@echo off
setlocal enabledelayedexpansion

:: ✅ Caminho do PROJETO
SET PROJ=C:\PraxisDemo\PraxisDemo_Local_Financeiro\PraxisDemo\PraxisPortal_Executivo_Blue

echo =====================================
echo  FASTAPI DEPLOY — EXECUTANDO CORRETAMENTE
echo =====================================

:: ✅ Força mudança para o diretório do projeto
echo -> Entrando no diretório do projeto:
echo     %PROJ%
cd /d "%PROJ%"

IF NOT "%CD%"=="%PROJ%" (
    echo ❌ FALHA AO ACESSAR O DIRETÓRIO DO PROJETO!
    pause
    exit /b
)

echo ✅ Diretório OK: %CD%
echo.

echo [1/5] Criando requirements.txt...
(
echo fastapi
echo uvicorn
echo python-multipart
echo python-dotenv
echo sqlalchemy
echo python-jose
echo passlib[bcrypt]
) > requirements.txt
echo ✅ OK
echo.


echo [2/5] Criando main.py...
(
echo from fastapi import FastAPI
echo app = FastAPI()
echo ^@app.get("/")
echo async def root():
echo^    return {"status": "✅ OK", "mensagem": "API ativa"}
) > main.py
echo ✅ OK
echo.


echo [3/5] Criando vercel.json...
(
echo {
echo   "version": 2,
echo   "builds": [
echo     { "src": "main.py", "use": "@vercel/python" }
echo   ],
echo   "routes": [
echo     { "src": "/(.*)", "dest": "main.py" }
echo   ]
echo }
) > vercel.json
echo ✅ OK
echo.


echo [4/5] Git push...
git add .
git commit -m "deploy fix"
git push
echo ✅ OK
echo.


echo [5/5] Vercel deploy...
vercel --prod --force
echo ✅ DEPLOY CONCLUÍDO
echo.

pause
exit
