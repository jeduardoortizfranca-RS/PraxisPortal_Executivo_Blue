@echo off
title Publicar PraxisPortal no GitHub
echo ==========================================
echo    Publicador Automático - Praxis Portal
echo ==========================================
echo.

REM Verifica se o Git está instalado
git --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERRO] Git não encontrado! Instale o Git antes de continuar.
    pause
    exit /b
)

REM Vai para o diretório do projeto
cd /d C:\PraxisDemo\PraxisPortal

echo.
echo [1/5] Inicializando repositório Git local...
git init

echo.
echo [2/5] Adicionando arquivos...
git add .

echo.
echo [3/5] Criando commit inicial...
git commit -m "Versão inicial do PraxisPortal Executivo Blue"

echo.
echo [4/5] Configurando branch principal...
git branch -M main

echo.
echo [5/5] Conectando ao repositório remoto...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue.git

echo.
echo Enviando arquivos para o GitHub...
git push -u origin main

echo.
echo ==========================================
echo ✅ Publicação concluída!
echo Repositório: https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue
echo Download ZIP: https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue/archive/refs/heads/main.zip
echo ==========================================
pause