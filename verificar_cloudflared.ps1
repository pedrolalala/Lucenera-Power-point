# Script para verificar configuracao do Cloudflared

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VERIFICACAO CLOUDFLARED" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar se cloudflared esta instalado
Write-Host "[1/4] Verificando instalacao do Cloudflared..." -ForegroundColor Yellow

$cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue

if ($cloudflared) {
    Write-Host "OK Cloudflared encontrado: $($cloudflared.Source)" -ForegroundColor Green
    $version = & cloudflared --version
    Write-Host "  Versao: $version" -ForegroundColor Gray
} else {
    Write-Host "ERRO Cloudflared NAO encontrado" -ForegroundColor Red
    Write-Host "  Instale em: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# 2. Verificar processos ativos
Write-Host "[2/4] Verificando processos ativos..." -ForegroundColor Yellow

$processes = Get-Process cloudflared -ErrorAction SilentlyContinue

if ($processes) {
    Write-Host "OK Cloudflared esta RODANDO" -ForegroundColor Green
    foreach ($proc in $processes) {
        Write-Host "  PID: $($proc.Id)" -ForegroundColor Gray
        Write-Host "  Memoria: $([math]::Round($proc.WorkingSet64 / 1MB, 2)) MB" -ForegroundColor Gray
    }
} else {
    Write-Host "ERRO Cloudflared NAO esta rodando" -ForegroundColor Red
}

Write-Host ""

# 3. Verificar arquivo de configuracao
Write-Host "[3/4] Verificando configuracao..." -ForegroundColor Yellow

$configPath = "$env:USERPROFILE\.cloudflared\config.yml"

if (Test-Path $configPath) {
    Write-Host "OK Arquivo de configuracao encontrado" -ForegroundColor Green
    Write-Host "  Localizacao: $configPath" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Conteudo:" -ForegroundColor Gray
    Get-Content $configPath | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
} else {
    Write-Host "AVISO Arquivo de configuracao NAO encontrado" -ForegroundColor Yellow
    Write-Host "  Localizacao esperada: $configPath" -ForegroundColor Gray
}

Write-Host ""

# 4. Verificar conectividade com apilucenera.site
Write-Host "[4/4] Testando conexao com apilucenera.site..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "https://apilucenera.site/health" -TimeoutSec 10 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "OK Site esta ACESSIVEL" -ForegroundColor Green
        Write-Host "  Status: $($response.StatusCode)" -ForegroundColor Gray
        try {
            $healthData = $response.Content | ConvertFrom-Json
            Write-Host "  Status da API: $($healthData.status)" -ForegroundColor Gray
            Write-Host "  Versao: $($healthData.version)" -ForegroundColor Gray
        } catch {
            Write-Host "  (Health endpoint nao disponivel)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "ERRO Site NAO esta acessivel" -ForegroundColor Red
    Write-Host "  Erro: $($_.Exception.Message)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Possiveis causas:" -ForegroundColor Yellow
    Write-Host "    1. Cloudflared nao esta rodando" -ForegroundColor Gray
    Write-Host "    2. Aplicacao Flask nao esta rodando na porta configurada" -ForegroundColor Gray
    Write-Host "    3. Configuracao do tunnel incorreta" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VERIFICACAO CONCLUIDA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "PORTA ESPERADA PELO FLASK: 5001" -ForegroundColor Yellow
Write-Host "Verifique se o cloudflared aponta para: localhost:5001" -ForegroundColor Yellow
Write-Host ""

Read-Host "Pressione ENTER para sair"
