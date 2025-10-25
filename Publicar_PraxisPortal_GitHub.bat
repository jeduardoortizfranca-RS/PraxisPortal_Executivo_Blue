@echo off
chcp 65001 >nul
title Publicador Automático - Praxis Portal

echo ======================================================
echo     🚀 Configuração Completa Git + GitHub
echo ======================================================
echo.

:: --- Verifica se o Git está instalado ---
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Git não encontrado! Instale o Git antes de continuar.
    pause
    exit /b
)

:: --- Verifica se o Git Credential Manager está instalado ---
where git-credential-manager >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Git Credential Manager não encontrado.
    echo Baixe e instale manualmente em:
    echo https://github.com/git-ecosystem/git-credential-manager/releases/latest
    pause
    exit /b
)

echo ✅ Git e Credential Manager detectados.
echo.

:: --- Configura identidade do Git ---
echo Configurando identidade global do Git...
git config --global user.name "Eduardo França"
git config --global user.email "jeduardo.ortiz.franca@gmail.com"
git config --global credential.helper manager
git config --global credential.credentialStore wincred
echo.

:: --- Define o diretório do projeto ---
set PROJETO=C:\PraxisDemo\PraxisPortal
if not exist "%PROJETO%" (
    echo [ERRO] Diretório do projeto não encontrado: %PROJETO%
    pause
    exit /b
)

cd /d "%PROJETO%"
echo Diretório do projeto: %PROJETO%
echo.

:: --- Inicializa e prepara o repositório Git ---
echo Inicializando repositório Git...
git init
git add .
git commit -m "Versão inicial do PraxisPortal Executivo Blue"
git branch -M main
git remote remove origin 2>nul
git remote add origin https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue.git
echo.

:: --- Login GitHub via navegador ---
echo Abrindo navegador Chrome para autenticação GitHub...
start chrome "https://github.com/login"
echo Aguarde a autenticação e mantenha o Chrome aberto até finalizar o login.
pause

:: --- Push inicial ---
echo Enviando para o GitHub...
git push -u origin main

if errorlevel 1 (
    echo ⚠️  Ocorreu um erro ao enviar para o GitHub.
    echo Verifique se o login foi autorizado no navegador.
    pause
) else (
    echo ✅ Publicação concluída com sucesso!
)

echo.
echo ======================================================
echo 🟢  Processo Finalizado - Praxis Portal Publicado
echo ======================================================
pause
exit
