# ✅ SISTEMA PRONTO PARA DEPLOY!

## 🎯 Configuração Concluída

### ✅ Arquivos Criados
1. **app_production.py** - Servidor Flask para produção
   - Logging com rotação (10MB, 5 backups)
   - Health check em `/health`
   - Modo produção (sem debug)
   - Porta 5001

2. **start_lucenera.bat** - Script de startup automático
   - Ativa venv
   - Inicia servidor
   - Mostra logs de erro

3. **verificar_cloudflared.ps1** - Diagnóstico cloudflared
   - Verifica instalação
   - Processos ativos
   - Configuração
   - Conectividade

4. **DEPLOY_GUIA.md** - Guia completo de deploy
   - Pré-requisitos
   - Configuração passo a passo
   - Troubleshooting
   - Monitoramento

5. **.env_example** - Template de configuração

---

## 🔧 CONFIGURAÇÃO DESCOBERTA

### Cloudflared
- ✅ Instalado em: `C:\Users\pedro\AppData\Local\cloudflared\cloudflared.exe`
- ⚠️ **NÃO está rodando** (precisa iniciar)
- 📁 Config: `C:\Users\pedro\.cloudflared\config.yml`

### Portas Configuradas
```yaml
# apilucenera.site → localhost:5000 (não usar)
# sistema.apilucenera.site → localhost:5001 ← USAR ESTA!
```

### URL Pública
**https://sistema.apilucenera.site** ← Domínio correto para acessar o sistema!

---

## 🚀 PRÓXIMOS PASSOS

### 1. Iniciar Cloudflared

**Opção A: Iniciar manualmente (testar primeiro)**
```powershell
cd "C:\Users\pedro\.cloudflared"
cloudflared tunnel run
```

**Opção B: Instalar como serviço (produção)**
```powershell
cloudflared service install
cloudflared service start
```

Verifique se está rodando:
```powershell
Get-Process cloudflared
Get-Service cloudflared
```

---

### 2. Iniciar Flask (Teste Manual)

```powershell
cd "C:\script python\script python power point"
.\start_lucenera.bat
```

Você verá:
```
========================================
LUCENERA - Sistema de Geracao de PPT
========================================

[1/3] Ativando ambiente virtual...
[2/3] Ambiente virtual ativado
[3/3] Iniciando servidor Flask...
============================================================
SERVIDOR LUCENERA - PRODUÇÃO
============================================================
Porta: 5001
Acesse: http://localhost:5001
Público: https://sistema.apilucenera.site
============================================================
```

---

### 3. Testar Sistema

**Teste local:**
```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:5001/health"

# Interface web
Start-Process "http://localhost:5001"
```

**Teste público:**
```powershell
# Health check
Invoke-WebRequest -Uri "https://sistema.apilucenera.site/health"

# Interface web
Start-Process "https://sistema.apilucenera.site"
```

---

### 4. Configurar Startup Automático

**Windows Task Scheduler:**

1. Win + R → `taskschd.msc`
2. Criar Tarefa
   - Nome: `Lucenera PPT Server`
   - Gatilho: `Ao fazer logon`
   - Ação: `C:\script python\script python power point\start_lucenera.bat`
   - Configurações:
     - ✅ Executar com privilégios elevados
     - ✅ Reiniciar se falhar (3 tentativas)

**Cloudflared como serviço:**
```powershell
cloudflared service install
Set-Service cloudflared -StartupType Automatic
Start-Service cloudflared
```

---

### 5. Compartilhar com Equipe

Envie esta mensagem:

```
🎉 Sistema de Geração de PowerPoint está no ar!

📍 URL: https://sistema.apilucenera.site

📋 Como usar:
1. Acesse o link
2. Faça upload do arquivo XML do orçamento
3. Aguarde 1-2 minutos
4. Baixe o PowerPoint pronto!

⚠️ Use APENAS arquivos XML (não PDF)

🔄 Sistema disponível 24/7
```

---

## 📊 MONITORAMENTO

### Logs da Aplicação
```powershell
# Ver logs em tempo real
Get-Content "C:\script python\script python power point\logs\app.log" -Wait -Tail 50

# Ver últimos erros
Select-String -Path "logs\app.log" -Pattern "ERROR" | Select-Object -Last 20
```

### Verificar Processos
```powershell
# Flask
Get-Process python | Where-Object {$_.CommandLine -like "*app_production*"}

# Cloudflared
Get-Process cloudflared

# Ambos
Get-Process python,cloudflared | Format-Table ProcessName, Id, StartTime, CPU
```

### Health Check Manual
```powershell
# Script rápido
$health = Invoke-RestMethod -Uri "http://localhost:5001/health"
Write-Host "Status: $($health.status)" -ForegroundColor $(if($health.status -eq 'healthy'){'Green'}else{'Red'})
Write-Host "Jobs ativos: $($health.active_jobs)"
Write-Host "Versão: $($health.version)"
```

---

## 🐛 TROUBLESHOOTING RÁPIDO

### Site não acessível externamente
```powershell
# 1. Verificar cloudflared
Get-Process cloudflared
# Se não estiver rodando: Start-Service cloudflared

# 2. Verificar Flask
Test-NetConnection localhost -Port 5001
# Se não responder: execute start_lucenera.bat
```

### Erro 403 SharePoint
```powershell
# Testar credenciais
cd "C:\script python\script python power point"
python teste_final_corrigido.py
```

### PowerPoint não gera imagens
```powershell
# Ver logs SharePoint
Get-Content "sharepoint_operations.log" -Tail 50

# Verificar arquivo Excel master
Test-Path "C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx"
```

---

## 📞 COMANDOS ÚTEIS

### Parar tudo
```powershell
Stop-Process -Name python -Force
Stop-Service cloudflared
```

### Reiniciar tudo
```powershell
Restart-Service cloudflared
cd "C:\script python\script python power point"
.\start_lucenera.bat
```

### Status completo
```powershell
Write-Host "=== CLOUDFLARED ===" -ForegroundColor Cyan
Get-Process cloudflared -ErrorAction SilentlyContinue | Format-Table

Write-Host "=== FLASK ===" -ForegroundColor Cyan
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*script python*"} | Format-Table

Write-Host "=== HEALTH CHECK ===" -ForegroundColor Cyan
try {
    $h = Invoke-RestMethod "http://localhost:5001/health"
    Write-Host "Status: $($h.status)" -ForegroundColor Green
} catch {
    Write-Host "OFFLINE" -ForegroundColor Red
}
```

---

## ✅ CHECKLIST FINAL

Antes de considerar o deploy completo:

- [ ] Cloudflared rodando (`Get-Process cloudflared`)
- [ ] Cloudflared como serviço (`Get-Service cloudflared`)
- [ ] Flask rodando (`Test-NetConnection localhost -Port 5001`)
- [ ] Health check OK (`http://localhost:5001/health`)
- [ ] Site público acessível (`https://sistema.apilucenera.site`)
- [ ] Teste completo: upload XML → geração PPT → download
- [ ] Task Scheduler configurado
- [ ] Equipe notificada
- [ ] Logs sendo gerados (`logs\app.log` existe)

---

## 🎯 RESULTADO ESPERADO

Quando tudo estiver funcionando:

1. **Cloudflared**: Rodando como serviço do Windows
2. **Flask**: Iniciado automaticamente ao fazer login
3. **URL pública**: https://sistema.apilucenera.site
4. **Equipe**: 3 pessoas acessando simultaneamente
5. **Uptime**: 24/7 (enquanto computador ligado)
6. **Logs**: Rotacionando automaticamente em `logs\`
7. **Monitoramento**: `/health` retornando status

---

**Sistema 100% configurado e pronto para uso! 🎉**

Basta executar os comandos da seção "PRÓXIMOS PASSOS" e está tudo pronto!
