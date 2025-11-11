@echo off
setlocal
title Configurador e Publicador Git - Praxis Portal
color 0A

echo ==========================================
echo   CONFIGURADOR AUTOMATICO DO GIT
echo ==========================================
echo.

REM 1) Configura identidade global do Git
echo [1/6] Configurando nome e e-mail globais do Git...
git config --global user.name "Eduardo França"
git config --global user.email "jeduardo.ortiz.franca@gmail.com"

echo Nome  : %USERNAME%
echo E-mail: jeduardo.ortiz.franca@gmail.com
echo.

REM 2) Confirma se o Git foi configurado corretamente
echo [2/6] Verificando configuracao atual...
git config --global --list
echo.
pause

REM 3) Vai para o diretorio do projeto
echo [3/6] Acessando o diretorio do projeto PraxisPortal...
cd /d C:\PraxisDemo\PraxisPortal
if errorlevel 1 (
    echo [ERRO] Diretorio C:\PraxisDemo\PraxisPortal nao encontrado.
    pause
    exit /b 1
)
echo OK - Diretorio localizado.
echo.

REM 4) Inicializa repositório se ainda não existir
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo [4/6] Inicializando repositório Git local...
    git init
) else (
    echo [4/6] Repositorio Git ja inicializado.
)

REM 5) Adiciona e cria commit inicial se necessario
echo [5/6] Preparando commit inicial...
git add .
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "Versao inicial do PraxisPortal Executivo Blue"
) else (
    echo Nenhuma alteracao detectada, pulando commit.
)

REM 6) Define branch principal e remoto
echo [6/6] Configurando branch e remoto...
git branch -M main
git remote remove origin >nul 2>&1
git remote add origin https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue.git

echo.
echo Enviando para o GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao enviar os arquivos.
    echo Possiveis causas:
    echo  - Nao autenticou no GitHub (abrira navegador pedindo login)
    echo  - Branch 'main' nao existe no remoto (sera criado automaticamente apos login)
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ✅ Configuracao e Publicacao Concluidas!
echo Repo: https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue
echo ZIP : https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue/archive/refs/heads/main.zip
echo ==========================================
pause
exit
