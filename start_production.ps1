# ============================================================
# Script de inicialização PRODUÇÃO - Lucenera PowerPoint
# PowerShell Version
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " LUCENERA - Sistema PowerPoint - PRODUCAO" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está no diretório correto
if (-not (Test-Path ".venv")) {
    Write-Host "ERRO: Pasta .venv não encontrada!" -ForegroundColor Red
    Write-Host "Execute este script da raiz do projeto." -ForegroundColor Red
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Ativar ambiente virtual
Write-Host "[1/3] Ativando ambiente virtual..." -ForegroundColor Yellow
try {
    & ".\.venv\Scripts\Activate.ps1"
    Write-Host "[OK] Ambiente virtual ativado" -ForegroundColor Green
} catch {
    Write-Host "ERRO: Não foi possível ativar o ambiente virtual!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# Verificar se .env existe
Write-Host "[2/3] Verificando configurações..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "ERRO: Arquivo .env não encontrado!" -ForegroundColor Red
    Write-Host "Copie .env_example para .env e configure as credenciais:" -ForegroundColor Yellow
    Write-Host "  Copy-Item .env_example .env" -ForegroundColor Cyan
    Write-Host "  notepad .env" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "[OK] Arquivo .env encontrado" -ForegroundColor Green
Write-Host ""

# Verificar se waitress está instalado
Write-Host "[3/3] Verificando dependências..." -ForegroundColor Yellow
try {
    python -c "import waitress" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "AVISO: Waitress não instalado. Instalando..." -ForegroundColor Yellow
        pip install waitress
    }
    Write-Host "[OK] Dependências verificadas" -ForegroundColor Green
} catch {
    Write-Host "AVISO: Erro ao verificar dependências" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Iniciar servidor de produção
Write-Host "Iniciando servidor de producao..." -ForegroundColor Green
Write-Host ""

try {
    python start_production.py
} catch {
    Write-Host ""
    Write-Host "ERRO ao iniciar servidor!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Se o script terminar normalmente
Write-Host ""
Write-Host "Servidor parado." -ForegroundColor Yellow
Read-Host "Pressione Enter para sair"
