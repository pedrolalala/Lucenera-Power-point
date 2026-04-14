# Script de Deploy Completo - Lucenera PPT System
# Executa todos os passos necessários para colocar o sistema no ar

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DEPLOY LUCENERA PPT SYSTEM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0

# 0. Verificar/corrigir config.yml do cloudflared
$configPath = "$env:USERPROFILE\.cloudflared\config.yml"
if (Test-Path $configPath) {
    try {
        cloudflared tunnel list *>$null
    } catch {
        Write-Host "[0/5] Corrigindo config.yml corrompido..." -ForegroundColor Yellow
        $configContent = @"
tunnel: 25ea7377-a23d-4f4f-a350-621b5bc90cfb
credentials-file: C:\Users\pedro\.cloudflared\25ea7377-a23d-4f4f-a350-621b5bc90cfb.json
ingress:
  - hostname: apilucenera.site
    service: http://localhost:5000
  - hostname: sistema.apilucenera.site
    service: http://localhost:5001
  - service: http_status:404
"@
        $configContent | Set-Content -Path $configPath -Encoding UTF8
        Write-Host "  OK Config corrigido" -ForegroundColor Green
        Write-Host ""
    }
}

# 1. Verificar Cloudflared
Write-Host "[1/5] Verificando Cloudflared..." -ForegroundColor Yellow

$cloudflaredProcess = Get-Process cloudflared -ErrorAction SilentlyContinue

if ($cloudflaredProcess) {
    Write-Host "  OK Cloudflared ja esta rodando (PID: $($cloudflaredProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "  AVISO Cloudflared nao esta rodando" -ForegroundColor Yellow
    Write-Host "  Iniciando cloudflared..." -ForegroundColor Gray
    
    try {
        $cloudflaredService = Get-Service cloudflared -ErrorAction SilentlyContinue
        
        if ($cloudflaredService) {
            Start-Service cloudflared
            Write-Host "  OK Servico cloudflared iniciado" -ForegroundColor Green
        } else {
            Write-Host "  AVISO Servico nao instalado. Iniciando manualmente..." -ForegroundColor Yellow
            
            $configPath = "$env:USERPROFILE\.cloudflared\config.yml"
            if (Test-Path $configPath) {
                Start-Process -FilePath "cloudflared" -ArgumentList "tunnel", "run" -WindowStyle Minimized
                Start-Sleep -Seconds 3
                Write-Host "  OK Cloudflared iniciado em background" -ForegroundColor Green
            } else {
                Write-Host "  ERRO Config nao encontrado: $configPath" -ForegroundColor Red
                Write-Host "  Execute: cloudflared tunnel login" -ForegroundColor Yellow
                $ErrorCount++
            }
        }
    } catch {
        Write-Host "  ERRO Falha ao iniciar: $($_.Exception.Message)" -ForegroundColor Red
        $ErrorCount++
    }
}

Write-Host ""

# 2. Verificar porta 5001
Write-Host "[2/5] Verificando porta 5001..." -ForegroundColor Yellow

$portTest = Test-NetConnection -ComputerName localhost -Port 5001 -InformationLevel Quiet -WarningAction SilentlyContinue

if ($portTest) {
    Write-Host "  OK Porta 5001 em uso (Flask ja rodando?)" -ForegroundColor Green
} else {
    Write-Host "  OK Porta 5001 disponivel" -ForegroundColor Green
}

Write-Host ""

# 3. Verificar arquivos necessarios
Write-Host "[3/5] Verificando arquivos..." -ForegroundColor Yellow

$projectPath = "C:\script python\script python power point"
$filesToCheck = @(
    "app_production.py",
    "start_lucenera.bat",
    ".venv\Scripts\python.exe",
    ".env"
)

foreach ($file in $filesToCheck) {
    $fullPath = Join-Path $projectPath $file
    if (Test-Path $fullPath) {
        Write-Host "  OK $file" -ForegroundColor Green
    } else {
        Write-Host "  ERRO $file NAO encontrado" -ForegroundColor Red
        $ErrorCount++
    }
}

Write-Host ""

# 4. Verificar Excel master
Write-Host "[4/5] Verificando Excel master..." -ForegroundColor Yellow

$excelPath = "C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx"
if (Test-Path $excelPath) {
    Write-Host "  OK Excel master encontrado" -ForegroundColor Green
} else {
    Write-Host "  AVISO Excel master nao encontrado" -ForegroundColor Yellow
    Write-Host "  Caminho: $excelPath" -ForegroundColor Gray
}

Write-Host ""

# 5. Iniciar Flask (se nao estiver rodando)
Write-Host "[5/5] Iniciando servidor Flask..." -ForegroundColor Yellow

if ($portTest) {
    Write-Host "  OK Flask ja esta rodando na porta 5001" -ForegroundColor Green
} else {
    Write-Host "  Iniciando start_lucenera.bat..." -ForegroundColor Gray
    
    $batPath = Join-Path $projectPath "start_lucenera.bat"
    
    if (Test-Path $batPath) {
        # Iniciar em nova janela
        Start-Process -FilePath $batPath -WorkingDirectory $projectPath
        
        Write-Host "  Aguardando servidor iniciar..." -ForegroundColor Gray
        Start-Sleep -Seconds 5
        
        # Verificar se iniciou
        $portTestAfter = Test-NetConnection -ComputerName localhost -Port 5001 -InformationLevel Quiet -WarningAction SilentlyContinue
        
        if ($portTestAfter) {
            Write-Host "  OK Flask iniciado com sucesso!" -ForegroundColor Green
        } else {
            Write-Host "  AVISO Flask pode estar iniciando... aguarde mais alguns segundos" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ERRO start_lucenera.bat nao encontrado" -ForegroundColor Red
        $ErrorCount++
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RESULTADO DO DEPLOY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($ErrorCount -eq 0) {
    Write-Host "OK Deploy concluido com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "URLs disponiveis:" -ForegroundColor Cyan
    Write-Host "  Local:   http://localhost:5001" -ForegroundColor Gray
    Write-Host "  Publico: https://sistema.apilucenera.site" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Testando health check em 3 segundos..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    
    try {
        $health = Invoke-RestMethod -Uri "http://localhost:5001/health" -UseBasicParsing -ErrorAction Stop
        Write-Host "Health Check: $($health.status)" -ForegroundColor Green
        Write-Host "Versao: $($health.version)" -ForegroundColor Gray
        Write-Host "Jobs ativos: $($health.active_jobs)" -ForegroundColor Gray
    } catch {
        Write-Host "AVISO Health check falhou (sistema ainda pode estar iniciando)" -ForegroundColor Yellow
        Write-Host "Aguarde 10-20 segundos e teste: http://localhost:5001/health" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "SISTEMA PRONTO PARA USO!" -ForegroundColor Green
    
} else {
    Write-Host "AVISO Deploy concluido com $ErrorCount erro(s)" -ForegroundColor Yellow
    Write-Host "Verifique os erros acima e corrija antes de usar" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Para diagnostico completo, execute:" -ForegroundColor Cyan
    Write-Host "  .\verificar_cloudflared.ps1" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

Write-Host ""
Read-Host "Pressione ENTER para sair"
