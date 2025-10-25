@echo off
chcp 65001 >nul
title 🚀 Atualizador GitHub - PraxisPortal Executivo Blue (v2)

echo ======================================================
echo     🚀 Atualizando e Publicando PraxisPortal
echo ======================================================
echo.

:: === Diretórios principais ===
set BASEDIR=C:\PraxisDemo\PraxisPortal
cd /d %BASEDIR%

:: === Verifica se o Git está disponível ===
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Git nao encontrado! Instale o Git antes de continuar.
    pause
    exit /b
)

:: === Configura identidade Git global ===
echo 🔹 Configurando identidade Git...
git config --global user.name "Eduardo França"
git config --global user.email "jeduardo.ortiz.franca@gmail.com"

:: === Configura Credential Manager ===
echo 🔹 Configurando Credential Manager...
git config --global credential.helper manager
git-credential-manager configure >nul 2>nul

:: === Verifica repositório Git ===
if not exist "%BASEDIR%\.git" (
    echo 🔹 Inicializando repositório Git...
    git init
    git branch -M main
    git remote add origin https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue.git
)

:: === Sincroniza e envia para GitHub ===
echo 🔹 Adicionando arquivos modificados...
git add .

echo 🔹 Criando commit...
git commit -m "Atualização automática do PraxisPortal Executivo Blue (%date% %time%)"

echo 🔹 Enviando para GitHub...
git push -u origin main

if %errorlevel% neq 0 (
    echo ⚠️ Ocorreu um erro ao enviar para o GitHub.
    echo Tente rodar novamente apos verificar a autenticacao.
    pause
    exit /b
)

:: === Confirmação ===
echo.
echo ✅ Publicação concluída com sucesso!
echo Repositório: https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue
echo.
echo ======================================================
echo 🟢 Atualização do PraxisPortal finalizada!
echo ======================================================
pause
exit
