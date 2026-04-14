# ⚡ Comandos Rápidos - Sistema Lucenera PPT

## 🚀 STARTUP

### Iniciar Tudo
```powershell
.\deploy_rapido.ps1
```

### Iniciar Apenas Flask
```powershell
.\start_lucenera.bat
```

### Iniciar Apenas Cloudflared
```powershell
Start-Process cloudflared -ArgumentList "tunnel","run" -WindowStyle Hidden
```

---

## 🔍 VERIFICAÇÃO

### Status Rápido
```powershell
# Ver processos
Get-Process cloudflared,python | Format-Table ProcessName, Id, StartTime

# Health check
Invoke-RestMethod http://localhost:5001/health | Format-List
```

### Health Check Público
```powershell
Invoke-RestMethod https://sistema.apilucenera.site/health -UseBasicParsing | Format-List
```

### Ver Site no Navegador
```powershell
Start-Process https://sistema.apilucenera.site
```

---

## 📊 LOGS

### Logs da Aplicação (Tempo Real)
```powershell
Get-Content logs\app.log -Wait -Tail 30
```

### Últimos 50 Erros
```powershell
Select-String -Path logs\app.log -Pattern "ERROR" | Select-Object -Last 50
```

### Logs SharePoint
```powershell
Get-Content sharepoint_operations.log -Tail 50
```

### Limpar Logs Antigos (>7 dias)
```powershell
Get-ChildItem logs\*.log.* | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | Remove-Item
```

---

## 🔄 REINICIAR

### Reiniciar Flask
```powershell
Stop-Process -Name python -Force
.\start_lucenera.bat
```

### Reiniciar Cloudflared
```powershell
Stop-Process -Name cloudflared -Force
Start-Process cloudflared -ArgumentList "tunnel","run" -WindowStyle Hidden
```

### Reiniciar Tudo
```powershell
Stop-Process -Name python,cloudflared -Force
Start-Sleep -Seconds 2
.\deploy_rapido.ps1
```

---

## 🛑 PARAR

### Parar Flask
```powershell
Stop-Process -Name python -Force
```

### Parar Cloudflared
```powershell
Stop-Process -Name cloudflared -Force
```

### Parar Tudo
```powershell
Stop-Process -Name python,cloudflared -Force
```

---

## 🔧 MANUTENÇÃO

### Atualizar Dependências
```powershell
.\.venv\Scripts\Activate.ps1
pip install --upgrade -r requirements_sharepoint.txt
```

### Backup do .env
```powershell
Copy-Item .env .env.backup_$(Get-Date -Format 'yyyyMMdd')
```

### Verificar Espaço em Disco
```powershell
Get-PSDrive C | Select-Object Used, Free, @{Name='Free %';Expression={[math]::Round($_.Free/$_.Used*100,2)}}
```

### Limpar Arquivos Temporários
```powershell
# Limpar uploads antigos (>30 dias)
Get-ChildItem "C:\Users\pedro\OneDrive\Desktop\lucenera\orcamento_*" | 
  Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | 
  Remove-Item -Confirm
```

---

## 📈 MONITORAMENTO

### Status Completo
```powershell
Write-Host "=== CLOUDFLARED ===" -ForegroundColor Cyan
Get-Process cloudflared -ErrorAction SilentlyContinue | Format-Table

Write-Host "=== FLASK ===" -ForegroundColor Cyan  
Get-Process python -ErrorAction SilentlyContinue | Format-Table

Write-Host "=== HEALTH CHECK ===" -ForegroundColor Cyan
try {
    $h = Invoke-RestMethod http://localhost:5001/health -UseBasicParsing
    Write-Host "Status: $($h.status)" -ForegroundColor Green
    Write-Host "Versao: $($h.version)"
    Write-Host "Jobs: $($h.active_jobs)"
} catch {
    Write-Host "OFFLINE" -ForegroundColor Red
}
```

### Loop de Monitoramento (Ctrl+C para sair)
```powershell
while ($true) {
    Clear-Host
    $h = Invoke-RestMethod http://localhost:5001/health -UseBasicParsing -ErrorAction SilentlyContinue
    $timestamp = Get-Date -Format 'HH:mm:ss'
    if ($h) {
        Write-Host "[$timestamp] Status: $($h.status) | Jobs: $($h.active_jobs)" -ForegroundColor Green
    } else {
        Write-Host "[$timestamp] OFFLINE" -ForegroundColor Red
    }
    Start-Sleep -Seconds 10
}
```

---

## 🐛 DIAGNÓSTICO

### Verificar Cloudflared
```powershell
.\verificar_cloudflared.ps1
```

### Testar Conectividade SharePoint
```powershell
python teste_final_corrigido.py
```

### Verificar Porta 5001
```powershell
Test-NetConnection localhost -Port 5001 -InformationLevel Detailed
```

### Ver Todas as Portas Usadas
```powershell
Get-NetTCPConnection | Where-Object {$_.State -eq 'Listen'} | 
  Select-Object LocalPort, OwningProcess, @{Name='Process';Expression={(Get-Process -Id $_.OwningProcess).ProcessName}} | 
  Sort-Object LocalPort
```

### Verificar Uso de Memória
```powershell
Get-Process python,cloudflared -ErrorAction SilentlyContinue | 
  Select-Object ProcessName, Id, @{Name='Memoria (MB)';Expression={[math]::Round($_.WorkingSet64/1MB,1)}} | 
  Format-Table
```

---

## 🔐 SEGURANÇA

### Ver Credenciais SharePoint (cuidado!)
```powershell
# Mostrar apenas Client ID
Select-String -Path .env -Pattern "CLIENT_ID"

# NUNCA executar Get-Content .env em tela compartilhada!
```

### Testar Permissões SharePoint
```powershell
python -c "from sharepoint_client import SharePointClient; sp = SharePointClient(); print(sp.get_token())"
```

---

## 📦 BACKUP

### Backup Completo
```powershell
$backupDate = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupPath = "C:\Backups\lucenera_$backupDate"

# Criar pasta de backup
New-Item -ItemType Directory -Path $backupPath

# Copiar arquivos críticos
Copy-Item .env $backupPath
Copy-Item app_production.py $backupPath
Copy-Item sharepoint_client.py $backupPath
Copy-Item ppt.py $backupPath
Copy-Item data_manager.py $backupPath
Copy-Item -Recurse web $backupPath

# Compactar
Compress-Archive -Path $backupPath -DestinationPath "$backupPath.zip"

Write-Host "Backup criado: $backupPath.zip"
```

---

## 🎯 ATALHOS ÚTEIS

### Abrir Logs
```powershell
notepad logs\app.log
```

### Abrir Pasta de Upload
```powershell
explorer "C:\Users\pedro\OneDrive\Desktop\lucenera"
```

### Editar .env
```powershell
notepad .env
```

### Ver Variáveis de Ambiente
```powershell
Get-Content .env
```

---

## 📞 COMANDOS DE EMERGÊNCIA

### Sistema Travado?
```powershell
# Matar todos os processos Python e Cloudflared
Get-Process python,cloudflared | Stop-Process -Force

# Limpar porta 5001 se estiver travada
$proc = Get-NetTCPConnection -LocalPort 5001 -ErrorAction SilentlyContinue
if ($proc) {
    Stop-Process -Id $proc.OwningProcess -Force
}

# Reiniciar
.\deploy_rapido.ps1
```

### Erro Crítico?
```powershell
# 1. Parar tudo
Stop-Process -Name python,cloudflared -Force

# 2. Ver últimos erros
Select-String -Path logs\app.log -Pattern "ERROR|CRITICAL" | Select-Object -Last 20

# 3. Backup de emergência
Copy-Item .env .env.EMERGENCY

# 4. Reiniciar limpo
Remove-Item logs\*.log -Confirm
.\deploy_rapido.ps1
```

---

## 💡 DICAS

### Criar Alias PowerShell
Adicione ao seu `$PROFILE`:
```powershell
# Abrir profile
notepad $PROFILE

# Adicionar estas linhas:
function Start-Lucenera { Set-Location "C:\script python\script python power point"; .\deploy_rapido.ps1 }
function Stop-Lucenera { Stop-Process -Name python,cloudflared -Force }
function Status-Lucenera { Invoke-RestMethod http://localhost:5001/health -UseBasicParsing | Format-List }
function Logs-Lucenera { Get-Content "C:\script python\script python power point\logs\app.log" -Wait -Tail 30 }

# Salvar e recarregar
. $PROFILE
```

Agora você pode usar:
- `Start-Lucenera` - Iniciar sistema
- `Stop-Lucenera` - Parar sistema  
- `Status-Lucenera` - Ver status
- `Logs-Lucenera` - Ver logs em tempo real

---

**Mantenha este arquivo como referência rápida! ⚡**
