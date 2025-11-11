@echo off
title 🚀 Deploy Automatizado - PraxisPortal V9.9 (Verificação Total)
color 0A

setlocal enabledelayedexpansion
set LOGFILE=deploy_log_v9_9.txt
set REPO_DIR=C:\PraxisDemo\PraxisDemo_Local_Financeiro\PraxisDemo\PraxisPortal_Executivo_Blue

echo ====================================================== > "%LOGFILE%"
echo 🚀 Deploy Automatizado - PraxisPortal V9.9 iniciado em %date% %time% >> "%LOGFILE%"
echo ====================================================== >> "%LOGFILE%"

echo.
echo 🚀 Iniciando Deploy Automatizado - PraxisPortal V9.9
echo ------------------------------------------------------
cd /d "%REPO_DIR%"

:: 🔍 Verificar se diretório é válido
if not exist "%REPO_DIR%" (
    echo ❌ Diretório não encontrado: %REPO_DIR%
    echo ❌ Diretório não encontrado: %REPO_DIR% >> "%LOGFILE%"
    pause
    exit /b
)

:: 🧩 Verificar se Vercel CLI está instalado
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Vercel CLI não encontrado. Instale com: npm install -g vercel
    echo ❌ ERRO: Vercel CLI não encontrado. >> "%LOGFILE%"
    pause
    exit /b
)

:: 🧠 Verificar autenticação da Vercel
echo 🔐 Verificando autenticação com a Vercel...
vercel whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Nenhum usuário autenticado. Abrindo login...
    start cmd /k "vercel login"
    echo 🔒 Autenticação necessária. Execute o login e depois rode o script novamente. >> "%LOGFILE%"
    pause
    exit /b
)
echo ✅ Autenticação Vercel confirmada.
echo ✅ Autenticação Vercel confirmada. >> "%LOGFILE%"

:: 🔄 Atualizar repositório
echo 🔄 Atualizando repositório local...
git pull origin main >> "%LOGFILE%" 2>&1

:: 🧰 Detectar mudanças locais
git status > status_temp.txt
findstr /C:"nothing to commit" status_temp.txt >nul
if %errorlevel% neq 0 (
    echo 🧩 Alterações detectadas, realizando commit...
    git add . >> "%LOGFILE%"
    git commit -m "Deploy automatizado V9.9" >> "%LOGFILE%"
    git push origin main >> "%LOGFILE%"
) else (
    echo ✅ Nenhuma alteração local para enviar.
    echo ✅ Nenhuma alteração local para enviar. >> "%LOGFILE%"
)
del status_temp.txt

:: 🚀 Iniciar Deploy
echo 🚀 Executando deploy na Vercel...
vercel --prod --yes > "%LOGFILE%" 2>&1

:: ⏱️ Verificar resultado
findstr /C:"Ready!" "%LOGFILE%" >nul
if %errorlevel% equ 0 (
    echo ✅ Deploy concluído com sucesso! >> "%LOGFILE%"
    echo ✅ Deploy concluído com sucesso!
    powershell -c "(New-Object Media.SoundPlayer 'C:\Windows\Media\Windows Notify Calendar.wav').PlaySync();"
    powershell -Command "[System.Windows.MessageBox]::Show('Deploy finalizado com sucesso!','PraxisPortal - Sucesso')"
) else (
    echo ❌ Erro detectado durante o deploy! >> "%LOGFILE%"
    echo ❌ Erro detectado durante o deploy!
    powershell -c "(New-Object Media.SoundPlayer 'C:\Windows\Media\Windows Error.wav').PlaySync();"
    powershell -Command "[System.Windows.MessageBox]::Show('Erro detectado! Verifique o arquivo deploy_log_v9_9.txt.','PraxisPortal - Erro')"
)

echo ====================================================== >> "%LOGFILE%"
echo Fim do processo em %date% %time% >> "%LOGFILE%"
echo ====================================================== >> "%LOGFILE%"

pause
exit
