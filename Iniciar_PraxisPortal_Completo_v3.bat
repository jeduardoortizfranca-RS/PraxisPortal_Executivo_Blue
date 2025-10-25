@echo off
chcp 65001 >nul
title 🚀 Inicializador Completo - PraxisPortal Executivo Blue (v3)

echo ======================================================
echo     🚀 Iniciando PraxisPortal - Backend + Frontend
echo ======================================================
echo.

:: --- Define os diretórios principais ---
set BASEDIR=C:\PraxisDemo
set BACKEND=%BASEDIR%\PraxisDemo_Local_Financeiro\PraxisDemo\backend
set VENV=%BASEDIR%\PraxisDemo_Local_Financeiro\PraxisDemo\venv\Scripts\activate
set FRONTEND=http://127.0.0.1:8000

:: --- Verifica se o backend existe ---
if not exist "%BACKEND%\app.py" (
    echo [ERRO] O backend não foi encontrado em %BACKEND%
    echo Verifique se o projeto está corretamente extraído.
    pause
    exit /b
)

:: --- Ativa o ambiente virtual ---
echo 🔹 Ativando ambiente virtual...
call "%VENV%"
if errorlevel 1 (
    echo [ERRO] Falha ao ativar o ambiente virtual.
    pause
    exit /b
)

:: --- Inicia o servidor FastAPI ---
echo 🔹 Iniciando servidor FastAPI (backend)...
start "Praxis Backend" cmd /k "cd /d %BACKEND% && uvicorn app:app --reload --host 127.0.0.1 --port 8000"

:: --- Aguarda o servidor iniciar ---
echo Aguardando inicialização do servidor...
timeout /t 6 >nul

:: --- Abre o navegador Chrome ---
echo 🔹 Abrindo navegador Chrome no painel do PraxisPortal...
start chrome "%FRONTEND%"
echo.

echo ✅ PraxisPortal iniciado com sucesso!
echo Backend ativo em: %FRONTEND%
echo.
echo ======================================================
echo 🟢  Portal Executivo Blue em execução
echo ======================================================
pause
exit
