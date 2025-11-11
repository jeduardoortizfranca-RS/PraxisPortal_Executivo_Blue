@echo off
SETLOCAL

REM Define o caminho do arquivo com o segredo. ATENÇÃO: Verifique se este caminho está correto!
REM Agora apontando para o arquivo .env na raiz do projeto
SET SECRET_FILE_PATH=".env"

echo.
echo =================================================================
echo INICIANDO PROCESSO DE CORRECAO DO HISTORICO DO GIT E PUSH PARA GITHUB
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

REM 2. Remove o arquivo com o segredo do historico do Git usando git-filter-repo
echo Removendo o arquivo com o segredo do historico do Git...
echo ATENCAO: Esta operacao reescreve o historico do Git.
echo Pressione qualquer tecla para continuar ou Ctrl+C para cancelar.
pause

REM O comando --invert-paths significa "manter tudo, exceto este caminho"
git filter-repo --path %SECRET_FILE_PATH% --invert-paths --force

IF %ERRORLEVEL% NEQ 0 (
    echo ERRO: git filter-repo falhou. Verifique a mensagem acima.
    GOTO :EOF
)
echo OK: Arquivo com segredo removido do historico.
echo.

REM 3. Adiciona o .gitignore (se ainda nao foi commitado) e os novos arquivos
echo Adicionando todas as mudancas (incluindo .gitignore) ao staging area...
git add .
IF %ERRORLEVEL% NEQ 0 (
    echo ERRO: git add falhou.
    GOTO :EOF
)
echo OK: Mudancas adicionadas.
echo.

REM 4. Cria um commit com as mudancas
echo Criando um novo commit...
git commit -m "feat: Adiciona tabela leads_marketing e endpoint FastAPI correspondente, corrige scripts SQL e configura Supabase. Remove .env do historico e adiciona venv/ e .env ao .gitignore."
IF %ERRORLEVEL% NEQ 0 (
    echo ERRO: git commit falhou.
    GOTO :EOF
)
echo OK: Novo commit criado.
echo.

REM 5. Forca o push para o GitHub
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
