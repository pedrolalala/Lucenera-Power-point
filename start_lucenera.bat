@echo off
REM Script de Startup do Sistema Lucenera PPT
REM Executa automaticamente na inicialização do Windows

echo ========================================
echo LUCENERA - Sistema de Geracao de PPT
echo ========================================
echo.

REM Navegar para diretório do projeto
cd /d "C:\script python\script python power point"

REM Ativar ambiente virtual
echo [1/3] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Verificar se venv foi ativado
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual
    pause
    exit /b 1
)

echo [2/3] Ambiente virtual ativado

REM Iniciar aplicação Flask em modo produção
echo [3/3] Iniciando servidor Flask...
python app_production.py

REM Se o Python terminar, mostrar erro
if errorlevel 1 (
    echo.
    echo ERRO: Servidor encerrou com erro
    echo Verifique os logs em: logs\app.log
)

pause
