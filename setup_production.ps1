# ============================================================
# Script de Setup Inicial - Lucenera PowerPoint System
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " LUCENERA - Setup Inicial" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Este script irá configurar o ambiente de produção." -ForegroundColor White
Write-Host ""

# 1. Verificar se .env já existe
Write-Host "[1/5] Verificando arquivo de configuração..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "AVISO: Arquivo .env já existe!" -ForegroundColor Yellow
    $resposta = Read-Host "Deseja sobrescrever? (s/N)"
    if ($resposta -ne "s") {
        Write-Host "Mantendo .env existente." -ForegroundColor Green
    } else {
        Remove-Item ".env"
        Copy-Item ".env_example" ".env"
        Write-Host "[OK] Novo .env criado a partir do template" -ForegroundColor Green
        Write-Host "IMPORTANTE: Edite o .env e configure as credenciais!" -ForegroundColor Red
    }
} else {
    Copy-Item ".env_example" ".env"
    Write-Host "[OK] Arquivo .env criado a partir do template" -ForegroundColor Green
}
Write-Host ""

# 2. Verificar ambiente virtual
Write-Host "[2/5] Verificando ambiente virtual..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    Write-Host "ERRO: Ambiente virtual não encontrado!" -ForegroundColor Red
    Write-Host "Criando ambiente virtual..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "[OK] Ambiente virtual criado" -ForegroundColor Green
} else {
    Write-Host "[OK] Ambiente virtual encontrado" -ForegroundColor Green
}
Write-Host ""

# 3. Ativar ambiente virtual e instalar dependências
Write-Host "[3/5] Instalando dependências..." -ForegroundColor Yellow
try {
    & ".\.venv\Scripts\Activate.ps1"
    
    # Atualizar pip
    Write-Host "Atualizando pip..." -ForegroundColor Cyan
    python -m pip install --upgrade pip --quiet
    
    # Instalar dependências
    Write-Host "Instalando pacotes do requirements_sharepoint.txt..." -ForegroundColor Cyan
    pip install -r requirements_sharepoint.txt --quiet
    
    Write-Host "[OK] Dependências instaladas com sucesso" -ForegroundColor Green
} catch {
    Write-Host "ERRO ao instalar dependências!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
Write-Host ""

# 4. Criar pastas necessárias
Write-Host "[4/5] Criando estrutura de pastas..." -ForegroundColor Yellow

# Ler pasta de upload do .env
$uploadFolder = ""
Get-Content ".env" | ForEach-Object {
    if ($_ -match "^UPLOAD_FOLDER=(.+)$") {
        $uploadFolder = $matches[1]
    }
}

if ($uploadFolder -and -not (Test-Path $uploadFolder)) {
    Write-Host "Criando pasta de upload: $uploadFolder" -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $uploadFolder -Force | Out-Null
}

# Criar pasta de logs
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" -Force | Out-Null
}

Write-Host "[OK] Estrutura de pastas criada" -ForegroundColor Green
Write-Host ""

# 5. Verificar configuração
Write-Host "[5/5] Verificando configuração final..." -ForegroundColor Yellow

# Verificar credenciais no .env
$temClientId = $false
$temClientSecret = $false
$temTenantId = $false

Get-Content ".env" | ForEach-Object {
    if ($_ -match "^SHAREPOINT_CLIENT_ID=.+$" -and $_ -notmatch "seu-client-id") {
        $temClientId = $true
    }
    if ($_ -match "^SHAREPOINT_CLIENT_SECRET=.+$" -and $_ -notmatch "seu-client-secret") {
        $temClientSecret = $true
    }
    if ($_ -match "^SHAREPOINT_TENANT_ID=.+$" -and $_ -notmatch "seu-tenant-id") {
        $temTenantId = $true
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " RESULTADO DO SETUP" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if ($temClientId -and $temClientSecret -and $temTenantId) {
    Write-Host "CREDENCIAIS SHAREPOINT: Configuradas" -ForegroundColor Green
    Write-Host ""
    Write-Host "PRÓXIMO PASSO:" -ForegroundColor Yellow
    Write-Host "  1. Iniciar servidor de produção:" -ForegroundColor White
    Write-Host "     .\start_production.ps1" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "CREDENCIAIS SHAREPOINT: NAO CONFIGURADAS!" -ForegroundColor Red
    Write-Host ""
    Write-Host "ACAO NECESSARIA:" -ForegroundColor Yellow
    Write-Host "  1. Editar arquivo .env:" -ForegroundColor White
    Write-Host "     notepad .env" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  2. Preencher as credenciais do Azure:" -ForegroundColor White
    Write-Host "     - SHAREPOINT_CLIENT_ID" -ForegroundColor Cyan
    Write-Host "     - SHAREPOINT_CLIENT_SECRET (GERAR NOVO - revogado!)" -ForegroundColor Red
    Write-Host "     - SHAREPOINT_TENANT_ID" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  3. Iniciar servidor:" -ForegroundColor White
    Write-Host "     .\start_production.ps1" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Pressione Enter para sair"
