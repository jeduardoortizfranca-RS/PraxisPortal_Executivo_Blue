@echo off
setlocal ENABLEDELAYEDEXPANSION

echo =====================================
echo  FASTAPI DEPLOY — EXECUTANDO
echo =====================================

REM ✅ ALTERE SE NECESSARIO
SET "PROJ=C:\PraxisDemo\PraxisDemo_Local_Financeiro\PraxisDemo\PraxisPortal_Executivo_Blue"

echo Target: %PROJ%

IF NOT EXIST "%PROJ%" (
    echo ❌ ERRO: Diretorio nao encontrado!
    pause
    exit /b
)

echo ✓ Diretorio confirmado


echo.
echo [1/5] Criando requirements.txt...
(
    echo fastapi
    echo uvicorn
) > "%PROJ%\requirements.txt"
echo ✓ OK


echo.
echo [2/5] Criando main.py...
(
    echo from fastapi import FastAPI
    echo app = FastAPI()
    echo @app.get("/")
    echo async def root():
    echo ^    return {"status": "OK", "mensagem": "API ativa"}
) > "%PROJ%\main.py"
echo ✓ OK


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
) > "%PROJ%\vercel.json"
echo ✓ OK


echo.
echo [4/5] Git push...
pushd "%PROJ%"
git add .
git commit -m "deploy fix" 2>nul
git push
popd
echo ✓ OK


echo.
echo =======================
echo [5/5] DEPLOY — EXECUTANDO...
echo =======================

cmd /k "vercel --cwd "%PROJ%" --prod --force & echo. & echo FINALIZADO & pause"
exit /b
