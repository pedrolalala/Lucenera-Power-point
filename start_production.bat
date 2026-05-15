@echo off
REM ============================================================
REM Script de inicialização PRODUÇÃO - Lucenera PowerPoint
REM ============================================================

echo.
echo ============================================================
echo  LUCENERA - Sistema PowerPoint - PRODUCAO
echo ============================================================
echo.

REM Ativar ambiente virtual
echo [1/3] Ativando ambiente virtual...
call .venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Nao foi possivel ativar o ambiente virtual!
    echo Certifique-se de que a pasta .venv existe.
    pause
    exit /b 1
)

echo [OK] Ambiente virtual ativado
echo.

REM Verificar se .env existe
echo [2/3] Verificando configuracoes...
if not exist .env (
    echo ERRO: Arquivo .env nao encontrado!
    echo Copie .env_example para .env e configure as credenciais.
    pause
    exit /b 1
)

echo [OK] Arquivo .env encontrado
echo.

REM Iniciar servidor de produção
echo [3/3] Iniciando servidor de producao...
echo.
python start_production.py

REM Se o script terminar, pausar para ver mensagens
pause
