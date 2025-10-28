@echo off
setlocal
title Praxis AI Core - Etapa 2 (Bot Jurídico)

echo ======================================================
echo        Praxis AI Core - Etapa 2 (FastAPI)
echo ======================================================

REM Caminho do projeto
set PROJECT_DIR=C:\PraxisDemo\PraxisDemo_Local_Financeiro\PraxisDemo\PraxisPortal_Executivo_Blue

pushd "%PROJECT_DIR%"
echo Diretório atual:
cd

echo ======================================================
echo Criando main.py na RAIZ
echo ======================================================
(
echo from fastapi import FastAPI
echo from backend.api.index import router as api_router
echo.
echo app = FastAPI(
echo ^    title="Praxis AI Core API",
echo ^    version="0.1.0"
echo )
echo.
echo app.include_router(api_router)
echo.
echo @app.get("/")
echo async def root():
echo ^    return {
echo ^        "status": "online",
echo ^        "message": "Praxis AI Core API ativa e funcionando 🚀"
echo ^    }
) > main.py

echo ======================================================
echo Garantindo backend/api/index.py
echo ======================================================
if not exist backend\api mkdir backend\api
(
echo from fastapi import APIRouter
echo.
echo router = APIRouter()
echo.
echo @router.get("/health")
echo def health_check():
echo ^    return {"status": "ok", "service": "juridico"}
) > backend\api\index.py

echo ======================================================
echo Criando vercel.json
echo ======================================================
(
echo {
echo   "version": 3,
echo   "builds": [
echo     {
echo       "src": "main.py",
echo       "use": "@vercel/python"
echo     }
echo   ],
echo   "routes": [
echo     {
echo       "src": "/(.*)",
echo       "dest": "main.py"
echo     }
echo   ]
echo }
) > vercel.json

echo ======================================================
echo Ativando VENV
echo ======================================================
if exist .venv\Scripts\activate call .venv\Scripts\activate

echo ======================================================
echo Instalando dependencias
echo ======================================================
pip install -r backend\requirements.txt

echo ======================================================
echo Commit + Push
echo ======================================================
git add .
git commit -m "Etapa 2: main.py + index.py + vercel.json"
git push origin main

echo ======================================================
echo Deploy Vercel
echo ======================================================
npx vercel --prod --yes

echo ======================================================
echo  FIM DO PROCESSO
echo ======================================================
pause
popd
endlocal
pause
