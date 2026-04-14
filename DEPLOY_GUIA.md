# 🚀 Guia de Deploy - Sistema Lucenera PPT

## 📋 Pré-requisitos

- ✅ Windows 10/11
- ✅ Python 3.8+ com venv configurado
- ✅ Cloudflared instalado e configurado
- ✅ Domínio `apilucenera.site` apontando para o tunnel
- ✅ Credenciais SharePoint no arquivo `.env`

---

## 🔧 Passo 1: Verificar Cloudflared

Execute o script de verificação:

```powershell
.\verificar_cloudflared.ps1
```

**Verifique:**
- ✅ Cloudflared está instalado
- ✅ Cloudflared está rodando
- ✅ Porta configurada (deve ser `localhost:5001`)

### 🔍 Como descobrir a porta do Cloudflared

**Opção 1: Arquivo de configuração**
```powershell
cat $env:USERPROFILE\.cloudflared\config.yml
```

Procure por algo como:
```yaml
tunnel: <tunnel-id>
ingress:
  - hostname: apilucenera.site
    service: http://localhost:5001  # ← PORTA AQUI
  - service: http_status:404
```

**Opção 2: Dashboard Cloudflare**
1. Acesse: https://one.dash.cloudflare.com/
2. Access → Tunnels
3. Clique no seu tunnel
4. Verifique a configuração

### 📝 Configurar Cloudflared (se necessário)

Se o cloudflared ainda não estiver configurado para a porta 5001:

```powershell
cloudflared tunnel route dns <tunnel-name> apilucenera.site
cloudflared tunnel ingress validate
```

Edite `$env:USERPROFILE\.cloudflared\config.yml`:
```yaml
tunnel: <seu-tunnel-id>
credentials-file: C:\Users\<usuario>\.cloudflared\<tunnel-id>.json

ingress:
  - hostname: apilucenera.site
    service: http://localhost:5001
  - service: http_status:404
```

Reinicie o cloudflared:
```powershell
# Parar processo atual
Stop-Process -Name cloudflared -Force

# Iniciar novamente
cloudflared tunnel run <tunnel-name>
```

---

## 🎯 Passo 2: Configurar Startup Automático

### Opção A: Task Scheduler (Recomendado)

1. **Abrir Agendador de Tarefas:**
   - Pressione `Win + R`
   - Digite: `taskschd.msc`
   - Enter

2. **Criar Nova Tarefa:**
   - Clique em `Criar Tarefa...` (não "Criar Tarefa Básica")
   - Nome: `Lucenera PPT Server`
   - Descrição: `Sistema de geração automática de PowerPoint`
   - Marque: ✅ `Executar estando o usuário conectado ou não`
   - Marque: ✅ `Executar com privilégios mais altos`

3. **Configurar Gatilho:**
   - Aba `Gatilhos` → `Novo...`
   - Iniciar tarefa: `Ao fazer logon`
   - Usuário específico: `<seu-usuario>`
   - Marque: ✅ `Habilitado`

4. **Configurar Ação:**
   - Aba `Ações` → `Novo...`
   - Ação: `Iniciar um programa`
   - Programa/script: `C:\script python\script python power point\start_lucenera.bat`
   - Iniciar em: `C:\script python\script python power point`

5. **Configurações Adicionais:**
   - Aba `Condições`:
     - ❌ Desmarque: "Iniciar a tarefa apenas se o computador estiver conectado à energia CA"
   - Aba `Configurações`:
     - ✅ Marque: "Permitir que a tarefa seja executada sob demanda"
     - ✅ Marque: "Se a tarefa falhar, reiniciar a cada: 1 minuto"
     - Defina: "Tentar reiniciar até: 3 vezes"

6. **Salvar:**
   - Clique em `OK`
   - Digite sua senha do Windows se solicitado

### Opção B: Pasta de Inicialização (Mais simples, menos confiável)

1. Pressione `Win + R`
2. Digite: `shell:startup`
3. Enter
4. Criar atalho para `start_lucenera.bat` nesta pasta

---

## ⚙️ Passo 3: Verificar Variáveis de Ambiente

Verifique o arquivo `.env` na raiz do projeto:

```env
# SharePoint Microsoft Graph API
SHAREPOINT_CLIENT_ID=39ef469c-7496-40cb-ac08-ba01b514cf2d
SHAREPOINT_TENANT_ID=<seu-tenant-id>
SHAREPOINT_CLIENT_SECRET=<seu-secret>
SHAREPOINT_DRIVE_NAME=LUCENERA PROJETOS

# Configurações da Aplicação (Opcionais - usa padrões se não definido)
PORT=5001
UPLOAD_FOLDER=C:\Users\pedro\OneDrive\Desktop\lucenera
SCRIPT_DIR=C:\script python\script python power point
EXCEL_MASTER=C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx
```

---

## 🧪 Passo 4: Testar Manualmente

Antes de habilitar o startup automático, teste manualmente:

```powershell
# Navegar para pasta do projeto
cd "C:\script python\script python power point"

# Executar script
.\start_lucenera.bat
```

Você deve ver:
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
Pasta de upload: C:\Users\pedro\OneDrive\Desktop\lucenera
Python venv: C:\script python\script python power point\.venv\Scripts\python.exe
Excel master: C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx
Porta: 5001
Acesse: http://localhost:5001
Público: https://apilucenera.site
============================================================
```

### Testar Health Check

Em outro terminal PowerShell:

```powershell
# Teste local
Invoke-WebRequest -Uri "http://localhost:5001/health"

# Teste público (após cloudflared configurado)
Invoke-WebRequest -Uri "https://apilucenera.site/health"
```

Resposta esperada:
```json
{
  "status": "healthy",
  "timestamp": "2026-04-14T12:00:00",
  "checks": {
    "upload_folder": true,
    "excel_master": true,
    "python_venv": true,
    "script_dir": true
  },
  "active_jobs": 0,
  "version": "2.0-production"
}
```

---

## 📱 Passo 5: Compartilhar com a Equipe

Envie para sua equipe:

```
🎉 Sistema de Geração de PowerPoint está no ar!

📍 Acesse: https://apilucenera.site

📋 Como usar:
1. Acesse o link acima
2. Faça upload do arquivo XML do orçamento
3. Aguarde o processamento (1-2 minutos)
4. Baixe o PowerPoint gerado automaticamente

⚠️ Importante:
- Use APENAS arquivos XML (não PDF)
- Tamanho máximo: 10MB
- Se ocorrer erro, contate o suporte

✅ O sistema está disponível 24/7
```

---

## 🔐 Passo 6: Segurança (Opcional mas Recomendado)

### Adicionar Autenticação Cloudflare Access

1. Acesse: https://one.dash.cloudflare.com/
2. Access → Applications
3. Add an Application → Self-hosted
4. Configure:
   - Name: `Lucenera PPT System`
   - Subdomain: `apilucenera`
   - Domain: `site`
5. Adicionar políticas de acesso:
   - Emails permitidos: lista de emails da equipe
   - Ou: Domínio corporativo

---

## 🐛 Troubleshooting

### Problema: Site não acessível

```powershell
# 1. Verificar se Flask está rodando
Get-Process python | Where-Object {$_.MainWindowTitle -like "*Flask*"}

# 2. Verificar se cloudflared está rodando
Get-Process cloudflared

# 3. Testar porta local
Test-NetConnection -ComputerName localhost -Port 5001

# 4. Ver logs da aplicação
cat "C:\script python\script python power point\logs\app.log" | Select-Object -Last 50
```

### Problema: Erro ao processar XML

```powershell
# Ver logs detalhados
cat "C:\script python\script python power point\logs\app.log" | Select-String -Pattern "ERRO"
cat "C:\script python\script python power point\sharepoint_operations.log" | Select-Object -Last 100
```

### Problema: SharePoint 403 Error

- Verifique credenciais no `.env`
- Confirme permissões Azure AD (Files.Read.All, Sites.Read.All)
- Teste com `python teste_final_corrigido.py`

---

## 📊 Monitoramento

### Health Check Automático

Crie um monitor no UptimeRobot ou similar:
- URL: `https://apilucenera.site/health`
- Intervalo: 5 minutos
- Esperado: Status 200 + JSON com `"status": "healthy"`

### Ver Logs em Tempo Real

```powershell
# Windows PowerShell
Get-Content "C:\script python\script python power point\logs\app.log" -Wait -Tail 50
```

---

## 🔄 Atualizações Futuras

Para atualizar o sistema:

1. Fazer backup do `.env`
2. Parar o servidor (matar processo ou desabilitar Task)
3. Atualizar arquivos
4. Testar manualmente
5. Re-habilitar Task/Startup

---

## 📞 Suporte

Em caso de problemas:

1. Verificar logs: `logs\app.log`
2. Executar: `verificar_cloudflared.ps1`
3. Testar health check: `https://apilucenera.site/health`
4. Contatar administrador do sistema

---

## ✅ Checklist Final

Antes de considerar o deploy completo:

- [ ] Cloudflared configurado e rodando
- [ ] Porta 5001 acessível localmente
- [ ] Flask rodando e respondendo
- [ ] Health check retorna "healthy"
- [ ] Site público acessível via `apilucenera.site`
- [ ] Teste de upload + geração de PPT funcionando
- [ ] Task Scheduler configurado
- [ ] Equipe notificada e treinada
- [ ] Logs sendo gerados corretamente
- [ ] Backup do `.env` feito

---

**Sistema pronto para produção! 🚀**
