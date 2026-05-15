# 🚀 GUIA DE DEPLOY - LUCENERA POWERPOINT SYSTEM

## 📋 CHECKLIST PRÉ-DEPLOY

### 🔴 CRÍTICO - SEGURANÇA

- [ ] **REVOGAR client secret exposto no GitHub**
  - Acessar Azure Portal: https://portal.azure.com
  - App Registrations → Lucenera App → Certificates & secrets
  - Deletar secret antigo
  - Gerar novo secret
  - Atualizar `.env` com novo secret

- [ ] **Verificar .gitignore**
  - Confirmar que `.env` está listado
  - NUNCA commitar arquivo `.env`

### ⚙️ CONFIGURAÇÃO

- [ ] **Criar arquivo `.env`**
  ```bash
  # Copiar template
  copy .env_example .env
  
  # Editar com credenciais reais
  notepad .env
  ```

- [ ] **Configurar variáveis no `.env`**
  - `SHAREPOINT_CLIENT_ID` - ID da aplicação Azure
  - `SHAREPOINT_CLIENT_SECRET` - Novo secret (revogado o antigo!)
  - `SHAREPOINT_TENANT_ID` - ID do tenant
  - `UPLOAD_FOLDER` - Pasta para uploads/outputs
  - `EXCEL_MASTER` - Caminho do Excel master
  - `SITE_URL` - https://sistema.apilucenera.site
  - `PORT` - 5001 (ou porta configurada)

### 📦 DEPENDÊNCIAS

- [ ] **Instalar dependências**
  ```bash
  # Ativar ambiente virtual
  .venv\Scripts\activate
  
  # Instalar todas as dependências (incluindo waitress)
  pip install -r requirements_sharepoint.txt
  ```

## 🌐 DEPLOY PARA SERVIDOR LOCAL

### Opção 1: Script Automático (Recomendado)

**Windows Batch:**
```bash
start_production.bat
```

**PowerShell:**
```powershell
.\start_production.ps1
```

**Python Direto:**
```bash
python start_production.py
```

### Opção 2: Manual

```bash
# 1. Ativar ambiente virtual
.venv\Scripts\activate

# 2. Iniciar servidor de produção
python start_production.py
```

## 🔧 CONFIGURAÇÃO DO DOMÍNIO

### https://sistema.apilucenera.site

Você precisa de um **reverse proxy** ou **túnel** para expor o servidor local:

#### Opção A: Cloudflare Tunnel (Recomendado)

1. **Instalar Cloudflared**
   ```bash
   # Download: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
   ```

2. **Autenticar**
   ```bash
   cloudflared tunnel login
   ```

3. **Criar túnel**
   ```bash
   cloudflared tunnel create lucenera-ppt
   ```

4. **Configurar túnel** (criar `config.yml`):
   ```yaml
   tunnel: lucenera-ppt
   credentials-file: C:\Users\pedro\.cloudflared\<tunnel-id>.json
   
   ingress:
     - hostname: sistema.apilucenera.site
       service: http://localhost:5001
     - service: http_status:404
   ```

5. **Criar rota DNS**
   ```bash
   cloudflared tunnel route dns lucenera-ppt sistema.apilucenera.site
   ```

6. **Iniciar túnel**
   ```bash
   cloudflared tunnel run lucenera-ppt
   ```

#### Opção B: ngrok (Desenvolvimento/Teste)

```bash
# Instalar ngrok: https://ngrok.com/download

# Expor porta 5001
ngrok http 5001 --domain=sistema.apilucenera.site
```

## 🔒 SEGURANÇA

### Configurações HTTPS

O servidor `waitress` está configurado com `url_scheme='https'` para funcionar corretamente atrás de um proxy HTTPS (Cloudflare/nginx).

### Firewall

Se estiver em rede local:
```powershell
# Permitir porta 5001 no Windows Firewall
New-NetFirewallRule -DisplayName "Lucenera PowerPoint" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow
```

## 📊 MONITORAMENTO

### Health Check

```bash
curl http://localhost:5001/health
```

Retorna:
```json
{
  "status": "healthy",
  "upload_folder": true,
  "excel_master": true,
  "python_venv": true,
  "timestamp": "2026-05-15T..."
}
```

### Logs

Logs salvos em: `logs/app.log`

```bash
# Seguir logs em tempo real
tail -f logs/app.log   # Linux/Mac
Get-Content logs/app.log -Wait   # PowerShell
```

## 🐛 TROUBLESHOOTING

### Erro: "Credenciais SharePoint não configuradas"
- Verificar se `.env` existe
- Verificar se variáveis estão preenchidas (sem aspas)

### Erro: "Excel master não encontrado"
- Verificar caminho em `EXCEL_MASTER` no `.env`
- Verificar se arquivo existe

### Erro: "Módulo waitress não encontrado"
```bash
pip install waitress
```

### Erro 403 SharePoint
- **CLIENT SECRET REVOGADO!** Gere novo no Azure Portal
- Verificar permissões da aplicação Azure

### Porta já em uso
```powershell
# Ver o que está usando a porta 5001
netstat -ano | findstr :5001

# Matar processo (substituir PID)
taskkill /PID <PID> /F

# Ou mudar porta no .env
# PORT=5002
```

## 🔄 ATUALIZAÇÃO

```bash
# 1. Parar servidor (Ctrl+C)

# 2. Fazer backup do .env
copy .env .env.backup

# 3. Atualizar código
git pull origin main

# 4. Atualizar dependências
pip install -r requirements_sharepoint.txt --upgrade

# 5. Restaurar .env (se sobrescrito)
copy .env.backup .env

# 6. Reiniciar servidor
python start_production.py
```

## 📁 ESTRUTURA DE ARQUIVOS

```
C:\script python\script python power point\
├── .env                    # ⚠️ CREDENCIAIS (não commitar!)
├── .env_example           # Template de configuração
├── start_production.py    # Script de início (produção)
├── start_production.bat   # Atalho Windows (batch)
├── start_production.ps1   # Atalho Windows (PowerShell)
├── app_production.py      # App Flask (produção)
├── app.py                 # App Flask (desenvolvimento)
├── ppt.py                 # Geração PowerPoint
├── sharepoint_client.py   # Cliente SharePoint
├── data_manager.py        # Parser XML/Excel
├── pdf_parser.py          # Parser PDF
├── logs/                  # Logs do sistema
│   └── app.log
├── web/                   # Interface web
│   ├── index.html
│   ├── script.js
│   └── styles.css
└── .venv/                 # Ambiente virtual Python
```

## 🆘 SUPORTE

- **GitHub Issues**: https://github.com/pedrolalala/Lucenera-Power-point/issues
- **Email**: [seu-email-aqui]

## ✅ VERIFICAÇÃO FINAL

Antes de colocar em produção:

```bash
# 1. Testar localmente
python start_production.py

# 2. Acessar health check
curl http://localhost:5001/health

# 3. Testar upload de XML
# (usar interface web)

# 4. Verificar logs
Get-Content logs/app.log -Tail 50

# 5. Testar domínio público
curl https://sistema.apilucenera.site/health
```

---

**Data de criação**: Maio 2026  
**Versão**: 2.0 (Upload Múltiplo + SharePoint)
