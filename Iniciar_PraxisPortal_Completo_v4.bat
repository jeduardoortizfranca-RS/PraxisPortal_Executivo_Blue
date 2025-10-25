@echo off
chcp 65001 >nul
title 🚀 Inicializador Completo - PraxisPortal Executivo Blue (v4)

echo ======================================================
echo     🚀 Iniciando PraxisPortal - Backend + Frontend
echo ======================================================
echo.

:: --- Define diretórios principais ---
set BASEDIR=C:\PraxisDemo
set BACKEND=%BASEDIR%\PraxisDemo_Local_Financeiro\PraxisDemo\backend
set VENV=%BASEDIR%\PraxisDemo_Local_Financeiro\PraxisDemo\venv\Scripts\activate
set FRONTEND=http://127.0.0.1:8000

:: --- Verifica se o backend existe ---
if not exist "%BACKEND%\app.py" (
    echo [ERRO] O backend nao foi encontrado em:
    echo %BACKEND%
    echo Verifique se o projeto esta corretamente extraido.
    pause
    exit /b
)

:: --- Ativa o ambiente virtual ---
echo 🔹 Ativando ambiente virtual do projeto...
call "%VENV%"
if errorlevel 1 (
    echo [ERRO] Falha ao ativar o ambiente virtual.
    pause
    exit /b
)

:: --- Inicia o servidor FastAPI (com caminho absoluto de pacote corrigido) ---
echo 🔹 Iniciando servidor FastAPI (backend)...
start "Praxis Backend" cmd /k "cd /d %BASEDIR%\PraxisDemo_Local_Financeiro\PraxisDemo && uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000"

:: --- Aguarda alguns segundos para inicializacao ---
echo Aguardando inicializacao do servidor...
timeout /t 6 >nul

:: --- Abre o navegador Chrome ---
echo 🔹 Abrindo navegador Chrome no painel do PraxisPortal...
start chrome "%FRONTEND%"
echo.

echo ✅ PraxisPortal iniciado com sucesso!
echo Backend ativo em: %FRONTEND%
echo.
echo ======================================================
echo 🟢  Portal Executivo Blue em execucao (modo local)
echo ======================================================
pause
exit
