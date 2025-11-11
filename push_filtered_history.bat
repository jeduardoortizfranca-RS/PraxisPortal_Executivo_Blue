@echo off
SETLOCAL

REM Define a URL do seu repositório remoto (SSH ou HTTPS, use a que voce usa para push)
SET REMOTE_URL="git@github.com:jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue.git"
REM Se voce usa HTTPS, use: SET REMOTE_URL="https://github.com/jeduardoortizfranca-RS/PraxisPortal_Executivo_Blue.git"

echo.
echo =================================================================
echo INICIANDO PROCESSO DE PUSH DO HISTORICO CORRIGIDO PARA GITHUB
echo =================================================================
echo.

REM 1. Verifica se estamos na branch 'main'
echo Verificando a branch atual...
for /f "delims=" %%i in ('git rev-parse --abbrev-ref HEAD') do set CURRENT_BRANCH=%%i
if "%CURRENT_BRANCH%" NEQ "main" (
    echo ERRO: Voce nao esta na branch 'main'. Por favor, mude para a branch 'main' e execute este script novamente.
    echo Exemplo: git checkout main
    GOTO :EOF
)
echo OK: Voce esta na branch 'main'.
echo.

REM 2. Garante que o remote 'origin' esteja configurado corretamente
echo Verificando e configurando o remote 'origin'...
git remote remove origin 2>NUL

REM 3. Forca o push para o GitHub
echo Forcando o push para o GitHub...
echo ATENCAO: Esta operacao sobrescreve o historico no repositorio remoto.
echo Pressione qualquer tecla para continuar ou Ctrl+C para cancelar.
pause

git push origin main --force
IF %ERRORLEVEL% NEQ 0 (
    echo ERRO: git push --force falhou. Verifique a mensagem acima.
    GOTO :EOF
)
echo OK: Push forcado para o GitHub concluido com sucesso!
echo.

echo =================================================================
echo PROCESSO CONCLUIDO. SEU REPOSITORIO NO GITHUB DEVE ESTAR ATUALIZADO E SEGURO.
echo =================================================================
echo.

ENDLOCAL
pause
