@echo off
title Publicador Automático - Praxis Portal (Correção Completa)
color 0B
echo ======================================================
echo     🚀 Publicador Automático - Praxis Portal
echo ======================================================
echo.

:: 1️⃣ Garante o diretório correto
cd /d "C:\PraxisDemo\PraxisPortal"
if not exist "C:\PraxisDemo\PraxisPortal" (
    echo [ERRO] O diretório C:\PraxisDemo\PraxisPortal nao foi encontrado!
    pause
    exit /b
)
echo Diretório atual: %cd%
echo.

:: 2️⃣ Verifica Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Git nao encontrado!
    echo Baixe e instale em: https://git-scm.com/download/win
    pause
    exit /b
)

:: 3️⃣ Garante segurança e permissões
git config --global --add safe.directory "C:/PraxisDemo/PraxisPortal"
git config --global --add safe.directory "C:/PraxisDemo"

:: 4️⃣ Configura identidade
echo Configurando usuario GitHub...
git config --global user.name "Eduardo Franca"
git config --global user.email "jeduardo.ortiz.franca@gmail.com"

:: 5️⃣ Configura credenciais e navegador
git config --global credential.helper manager
git config --global credential.useHttpPath true
git config --global credential.credentialStore cache
git config --global web.browser chrome

:: 6️⃣ Verifica o Git Credential Manager
where git-credential-manager >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando Git Credential Manager...
    winget install --id GitHub.GitCredentialManagerCore -e
)

:: 7️⃣ Inicializa repositório, se não existir
if not exist ".git" (
    echo Inicializando repositório local...
    git init
    git add .
    git commit -m "Versão inicial - Praxis Portal"
)

:: 8️⃣ Adiciona origem remota
git remote remove origin >nul 2>&1
git remote add origin https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue.git

:: 9️⃣ Login e envio
echo.
echo Abrindo navegador Chrome para login do GitHub...
git-credential-manager login

echo.
echo Enviando para o GitHub...
git branch -M main
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ⚠️ Erro ao enviar para o GitHub!
    echo Verifique a autenticação e tente novamente.
    pause
    exit /b
)

:: ✅ Finalização
echo.
echo ======================================================
echo ✅ Projeto publicado com sucesso no GitHub!
echo 🔗 https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue
echo ======================================================
pause
exit
