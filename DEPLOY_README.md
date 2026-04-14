# 🚀 Deploy em Produção - Sistema Completo

## ⚡ INÍCIO RÁPIDO (3 minutos)

Execute este comando no PowerShell:

```powershell
.\deploy_rapido.ps1
```

Este script irá:
- ✅ Verificar cloudflared
- ✅ Verificar porta 5001
- ✅ Verificar arquivos necessários
- ✅ Iniciar servidor Flask
- ✅ Testar health check

---

## 📚 DOCUMENTAÇÃO COMPLETA

### Arquivos de Deploy

| Arquivo | Descrição |
|---------|-----------|
| **[DEPLOY_RESUMO.md](DEPLOY_RESUMO.md)** | 📋 RESUMO EXECUTIVO - Configuração descoberta, próximos passos, checklist |
| **[DEPLOY_GUIA.md](DEPLOY_GUIA.md)** | 📖 GUIA COMPLETO - Passo a passo detalhado, troubleshooting, monitoramento |
| **deploy_rapido.ps1** | ⚡ Script automático de deploy (executa tudo de uma vez) |
| **verificar_cloudflared.ps1** | 🔍 Diagnóstico completo do cloudflared |
| **start_lucenera.bat** | 🎯 Startup do Flask (usado pelo Task Scheduler) |

### Arquivos de Produção

| Arquivo | Descrição |
|---------|-----------|
| **app_production.py** | Servidor Flask para produçãocom logging e health check |
| **.env** | Credenciais SharePoint e configurações |
| **.env_example** | Template de configuração |

---

## 🎯 CONFIGURAÇÃO ATUAL

### URLs Configuradas
- **URL Pública**: `https://sistema.apilucenera.site` ← USAR ESTA
- **URL Local**: `http://localhost:5001`
- **Health Check**: `https://sistema.apilucenera.site/health`

### Cloudflared
- **Instalado**: ✅ C:\Users\pedro\AppData\Local\cloudflared\
- **Status**: ⚠️ Precisa iniciar (ver comandos abaixo)
- **Config**: C:\Users\pedro\.cloudflared\config.yml

### Portas
- **5000**: apilucenera.site (não usar)
- **5001**: sistema.apilucenera.site ← Flask rodará aqui

---

## 🚀 COMANDOS ESSENCIAIS

### Deploy Completo (Primeira Vez)
```powershell
# 1. Iniciar cloudflared como serviço (permanente)
cloudflared service install
Start-Service cloudflared

# 2. Executar deploy automático
.\deploy_rapido.ps1

# 3. Configurar startup automático (Task Scheduler)
# Ver instruções em DEPLOY_GUIA.md seção "Passo 3"
```

### Uso Diário
```powershell
# Ver se está tudo rodando
Get-Process cloudflared,python | Format-Table ProcessName, Id, StartTime

# Health check rápido
Invoke-WebRequest http://localhost:5001/health

# Ver logs em tempo real
Get-Content logs\app.log -Wait -Tail 30
```

### Troubleshooting
```powershell
# Diagnóstico completo
.\verificar_cloudflared.ps1

# Reiniciar tudo
Stop-Process -Name python -Force
Restart-Service cloudflared
.\start_lucenera.bat

# Ver últimos erros
Select-String -Path logs\app.log -Pattern "ERROR" | Select-Object -Last 10
```

---

## 📋 CHECKLIST DE DEPLOY

### Antes de Iniciar
- [ ] Python 3.8+ instalado
- [ ] Ambiente virtual criado (.venv)
- [ ] Dependências instaladas (`pip install -r requirements_sharepoint.txt`)
- [ ] Arquivo .env configurado com credenciais SharePoint
- [ ] Cloudflared instalado

### Deploy
- [ ] Cloudflared rodando (`Get-Process cloudflared`)
- [ ] Flask iniciado (`.\start_lucenera.bat`)
- [ ] Porta 5001 respondendo (`Test-NetConnection localhost -Port 5001`)
- [ ] Health check OK (`http://localhost:5001/health`)
- [ ] Site público acessível (`https://sistema.apilucenera.site`)

### Teste Completo
- [ ] Upload de arquivo XML
- [ ] Geração de PowerPoint
- [ ] Download do arquivo gerado
- [ ] Verificar imagens no PPT

### Startup Automático
- [ ] Task Scheduler configurado (Flask)
- [ ] Cloudflared como serviço (`Get-Service cloudflared`)
- [ ] Testar reiniciar computador

### Equipe
- [ ] URL compartilhada (sistema.apilucenera.site)
- [ ] Instruções de uso enviadas
- [ ] Teste com usuário final

---

## 🎓 COMO USAR O SISTEMA

### Para Administrador (Você)

1. **Iniciar sistema** (primeira vez ou após reiniciar PC):
   ```powershell
   .\deploy_rapido.ps1
   ```

2. **Monitorar sistema**:
   ```powershell
   Get-Content logs\app.log -Wait -Tail 50
   ```

3. **Ver status**:
   ```powershell
   Invoke-RestMethod http://localhost:5001/health | Format-List
   ```

### Para Usuários Finais (Sua Equipe)

1. Acessar: **https://sistema.apilucenera.site**
2. Fazer upload do arquivo **XML** do orçamento
3. Aguardar 1-2 minutos
4. Baixar PowerPoint gerado

⚠️ **Importante**: Use APENAS arquivos XML (não PDF)

---

## 📊 MONITORAMENTO

### Health Check Automático
```powershell
# Script para monitorar continuamente
while ($true) {
    $health = Invoke-RestMethod http://localhost:5001/health -ErrorAction SilentlyContinue
    $status = if ($health.status -eq 'healthy') { 'OK' } else { 'ERRO' }
    $timestamp = Get-Date -Format 'HH:mm:ss'
    Write-Host "[$timestamp] Status: $status | Jobs: $($health.active_jobs)" -ForegroundColor $(if($status -eq 'OK'){'Green'}else{'Red'})
    Start-Sleep -Seconds 30
}
```

### Logs Importantes
- **App**: `logs\app.log` - Log principal da aplicação
- **SharePoint**: `sharepoint_operations.log` - Operações SharePoint

---

## 🐛 ERROS COMUNS

### "Site não acessível"
```powershell
# Verificar cloudflared
Get-Process cloudflared
# Se não estiver rodando:
Start-Service cloudflared

# Verificar Flask
Test-NetConnection localhost -Port 5001
# Se não responder:
.\start_lucenera.bat
```

### "Erro 403 SharePoint"
```powershell
# Testar credenciais
python teste_final_corrigido.py
# Se falhar, verificar .env
notepad .env
```

### "PowerPoint sem imagens"
```powershell
# Ver logs SharePoint
Get-Content sharepoint_operations.log -Tail 50
# Verificar mapeamento
Test-Path "C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx"
```

---

## 📞 SUPORTE

### Ordem de Diagnóstico
1. Executar: `.\verificar_cloudflared.ps1`
2. Verificar: `logs\app.log`
3. Testar: `http://localhost:5001/health`
4. Consultar: [DEPLOY_GUIA.md](DEPLOY_GUIA.md)

### Comandos de Emergência
```powershell
# Parar tudo
Stop-Process -Name python,cloudflared -Force

# Limpar porta 5001
Get-Process -Id (Get-NetTCPConnection -LocalPort 5001).OwningProcess | Stop-Process -Force

# Reiniciar do zero
.\deploy_rapido.ps1
```

---

## 🎉 SUCESSO!

Quando tudo estiver funcionando, você verá:

- ✅ Cloudflared rodando como serviço
- ✅ Flask respondendo na porta 5001
- ✅ Health check retornando `"status": "healthy"`
- ✅ Site público acessível em https://sistema.apilucenera.site
- ✅ Equipe conseguindo usar o sistema

**Sistema pronto para produção! 🚀**

---

## 📎 LINKS ÚTEIS

- [Cloudflare Tunnel Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [Flask Production Best Practices](https://flask.palletsprojects.com/en/latest/deploying/)
- [Microsoft Graph API](https://docs.microsoft.com/en-us/graph/)

---

**Criado por: Deploy Automation**  
**Data: Abril 2026**  
**Versão: 2.0-production**
