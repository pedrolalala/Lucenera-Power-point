# 🚀 Sistema Lucenera - Gerador de Fichas Técnicas PowerPoint

Sistema automatizado para geração de apresentações PowerPoint com fichas técnicas integrado ao Microsoft SharePoint via Graph API.

## ⭐ Características

- 🌐 **Integração SharePoint**: Busca automática de fichas técnicas e bulas
- 📄 **Dual Input**: Suporte a arquivos XML e PDF
- 🤖 **100% Automático**: Geração de PPT sem intervenção manual
- 💻 **Interface Web**: Upload via browser com tabs para XML/PDF
- 🏷️ **Multi-formatos**: Suporta `.docx`, `.jpg`, `.png`, `.pdf` do SharePoint
- 📋 **Bulas Separadas**: Detecta e cria slides dedicados para manuais/bulas
- ⚡ **Background Processing**: Status em tempo real
- 🔒 **HTTPS Público**: Deploy com Cloudflared

## 📋 Requisitos

- Python 3.8+
- Microsoft Graph API (credenciais configuradas)
- SharePoint Lucenera (acesso configurado)
- Excel master: `C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx`

## 🚀 Instalação

### 1. Instalar Dependências
```powershell
.\install_sharepoint_deps.ps1
```

### 2. Configurar Variáveis de Ambiente
Editar `.env` (já configurado):
```env
TENANT_ID=seu_tenant_id
CLIENT_ID=39ef469c-7496-40cb-ac08-ba01b514cf2d
CLIENT_SECRET=seu_client_secret
```

### 3. Iniciar Servidor

**Desenvolvimento (local):**
```bash
python app.py
```
Acesse: http://localhost:5001

**Produção (HTTPS público):**
```powershell
.\deploy_rapido.ps1
```
Acesse: https://sistema.apilucenera.site

**Atalho Windows:**
```
start_lucenera.bat
```

## 📁 Estrutura do Projeto

```
├── app.py                    # Servidor Flask (desenvolvimento)
├── app_production.py         # Servidor Flask (produção)
├── ppt.py                    # Geração de PowerPoint
├── sharepoint_client.py      # Cliente Microsoft Graph API
├── data_manager.py           # Processamento XML/Excel
├── pdf_parser.py             # Parser PDF (modo legado)
├── reference_extractor.py    # Extração de referências
├── web/                      # Interface web
│   ├── index.html           # UI principal (tabs XML/PDF)
│   ├── script.js            # Lógica frontend
│   └── styles.css           # Estilos
├── requirements_sharepoint.txt
├── requirements_web.txt
├── deploy_rapido.ps1         # Script de deploy
├── start_lucenera.bat        # Atalho de inicialização
└── README.md                 # Este arquivo
```

## 🎯 Como Usar

### 1. XML (Recomendado)
1. Acesse o sistema (local ou HTTPS)
2. Clique na aba **"XML (Novo - SharePoint)"**
3. Arraste ou selecione arquivo XML do orçamento
4. Clique em **"Processar XML"**
5. Aguarde processamento (barra de progresso)
6. Download automático do PPT gerado

### 2. PDF (Modo Legado)
1. Clique na aba **"PDF (SharePoint)"**
2. Arraste ou selecione arquivo PDF do orçamento
3. Clique em **"Processar PDF"**
4. Aguarde processamento
5. Download automático do PPT gerado

## 📊 Estrutura SharePoint

**Pasta fixa:**
```
LUCENERA PROJETOS/Fichas Técnicas/Ficha técnica processada/Ficha Técnica Renomeado/
```

**Nomenclatura de arquivos:**
- Fichas: `13133.docx` (código interno)
- Bulas: `13133_BULA.jpg` ou `13133_MANUAL.pdf`
- Imagens: `13133.png` ou `13133_FOTO.jpg`

**Formatos suportados:**
- `.docx` - Fichas técnicas
- `.jpg`, `.png` - Imagens de produto
- `.pdf` - Manuais técnicos

## 🔍 Sistema de Bulas

O sistema detecta automaticamente bulas/manuais por keywords:
- `bula`, `manual`, `instruction`, `guide`, `info`

**Comportamento:**
- Bulas são criadas em **slides separados** (não misturam com ficha técnica)
- Cada bula ocupa um slide completo
- Mantém número LXX no canto superior direito

## 🏢 Excel Master

**Localização:** `C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx`

**Colunas obrigatórias:**
- `codigo` - Código interno do produto
- `ref` - Referência do fabricante
- `marca` - Nome da marca
- `nome` - Nome do produto
- `categoria` - Categoria
- `potencia` - Potência (ex: "12W")

## 🌐 Deploy HTTPS

Sistema configurado com Cloudflared para acesso público:

**URL Pública:** https://sistema.apilucenera.site

**Deploy automático:**
```powershell
.\deploy_rapido.ps1
```

O script verifica:
- ✅ Cloudflared ativo
- ✅ Porta 5001 disponível
- ✅ Arquivos essenciais
- ✅ Excel master
- ✅ Servidor Flask


## 🐛 Troubleshooting

**Erro de autenticação SharePoint:**
- Verifique variáveis `.env`
- Teste credenciais com Microsoft Graph Explorer

**Arquivos não encontrados no SharePoint:**
- Verifique nomenclatura (código interno exato)
- Confirme pasta configurada em `sharepoint_client.py`

**PowerPoint vazio ou incompleto:**
- Verifique Excel master preenchido
- Confirme códigos no XML correspondem ao Excel

**Site HTTPS não acessível:**
- Execute `deploy_rapido.ps1`
- Verifique Cloudflared: `Get-Process cloudflared`
- Reinicie: `cloudflared service uninstall` + `cloudflared service install`

## 📝 Notas Técnicas

- **Encoding:** Sistema usa UTF-8, logs sem emojis (compatibilidade Windows cp1252)
- **Cache:** Interface pode precisar Ctrl+Shift+R após atualizações
- **Performance:** ~1-2s por produto (busca SharePoint + download)
- **Logs:** Pasta `logs/` com rotação automática (10MB, 5 backups)

## 📄 Licença

Sistema proprietário - Lucenera Ltda.

---

**Versão:** 2.0-production  
**Última atualização:** Abril 2026  
**Desenvolvido para:** Lucenera - Atelier da Luz

## 🌐 SharePoint - Estrutura Necessária

```
LUCENERA PROJETOS/
└── Fichas Técnicas/
    ├── Interlight/           # Pasta por marca
    │   ├── 10289_ficha_tecnica.docx
    │   ├── 10289_BULA_INSTALACAO.pdf
    │   └── 3649-AB-S-PX_especificacao.docx
    ├── Bella Luce/
    ├── Direct Light/
    └── Jean Lux/
```

## 💾 Excel Master - Formato

| codigo | ref | marca | nome | categoria | potencia |
|--------|-----|--------|------|-----------|----------|
| 10289 | 3649-AB-S-PX | Interlight | Luminária LED 30W | Embutir | 30W |
| 10539 | 3649-FE-S-PX | Interlight | Luminária LED 45W | Sobrepor | 45W |

**Colunas obrigatórias:** `codigo`, `ref`, `marca`, `nome`

## 📄 XML - Formato de Entrada

```xml
<orcamento id="OR_006020" data="2026-04-10">
    <itens>
        <item 
            linha="43" 
            codigo="10289" 
            ref="3649-AB-S-PX" 
            preco="655.39" 
            quantidade="57"
            marca="Interlight"
            descricao="Luminária de embutir LED 30W"
        />
    </itens>
</orcamento>
```

## 🚀 Como Usar

### 1. 📤 Upload via Web
- Abra `http://localhost:5001`
- Escolha aba **XML (SharePoint)** 
- Selecione arquivo XML de orçamento
- Clique **"Processar XML"**

### 2. ⏳ Acompanhar Progresso
- Sistema processa em background
- Status atualizado em tempo real
- Download automático quando pronto

### 3. 📊 Resultado
- PowerPoint profissional gerado
- Slides com imagens dos produtos
- Informações técnicas e comerciais
- Layout padronizado Lucenera

## 🛠️ Configuração Avançada

### 🔐 Variáveis de Ambiente (.env)

O sistema utiliza um arquivo `.env` para armazenar credenciais e configurações sensíveis:

```bash
# Credenciais SharePoint (JÁ CONFIGURADAS ✅)
SHAREPOINT_CLIENT_ID=39ef469c-7496-40cb-ac08-ba01b514cf2d
SHAREPOINT_TENANT_ID=b68c427b-b3f8-4bba-9252-66b24ce29c9d
SHAREPOINT_CLIENT_SECRET=your_client_secret_here

# Configurações SharePoint
SHAREPOINT_SITE_ID=luceneraprojetos.sharepoint.com
SHAREPOINT_DRIVE_NAME=LUCENERA PROJETOS
SHAREPOINT_FICHAS_PATH=Fichas Técnicas

# Caminho Excel Master
EXCEL_MASTER_PATH=C:/Users/pedro/OneDrive/Desktop/lucenera/master_produtos.xlsx
```

**⚠️ Segurança:** O arquivo `.env` nunca é commitado no Git (protegido pelo `.gitignore`)

### Credenciais SharePoint
Configure em `sharepoint_client.py`:
```python
CLIENT_ID = "39ef469c-7496-40cb-ac08-ba01b514cf2d"
CLIENT_SECRET = "sua_chave_secreta"  
TENANT_ID = "seu_tenant_id"
```

### Caminhos Personalizados
Ajuste em `data_manager.py`:
```python
EXCEL_MASTER_PATH = "C:/seu/caminho/master_produtos.xlsx"
SHAREPOINT_BASE_PATH = "LUCENERA PROJETOS/Fichas Técnicas"
```

## 🔍 Troubleshooting

### ❌ Produto não encontrado
1. Verifique se `codigo` existe no Excel master
2. Confirme nome da `marca` 
3. Verifique pasta da marca no SharePoint

### ❌ Falha autenticação
1. Confirme credenciais SharePoint
2. Verifique permissões da aplicação
3. Teste conectividade: `python test_system.py`

### ❌ Imagens não aparecem  
1. Verifique arquivos .docx no SharePoint
2. Confirme nomes incluem código do produto
3. Teste manualmente: `python sharepoint_client.py`

## 📞 Comandos Úteis

```bash
# Setup completo automático (RECOMENDADO)
python setup_completo.py

# Testar credenciais e configurações
python test_env.py

# Validação completa do sistema
python validacao_sistema.py

# Teste específico conectividade SharePoint
python test_system.py

# Criar novo Excel master
python criar_excel_template.py

# Debug modo verbose
python app.py --debug

# Instalar dependências manualmente
pip install -r requirements_sharepoint.txt
```

## 🔄 Compatibilidade

✅ **Suporte completo:**
- Windows 10/11
- Python 3.8+
- Microsoft Graph API v1.0
- SharePoint Online

⚠️ **Modo legacy:**
- PDFs (sistema antigo)
- Arquivos locais (INTERLIGHT_SEPARADOS)

## 📈 Performance

- **Startup:** ~5 segundos
- **Autenticação:** ~2-3 segundos  
- **Busca por produto:** ~1-2 segundos
- **Download imagem:** ~500ms-2s
- **Geração PPT:** ~30-60 segundos (depende da quantidade)

## 🎯 Próximos Passos

1. 📋 Preencher Excel master com dados reais
2. 🗂️ Organizar arquivos no SharePoint
3. 🧪 Executar teste com XML real
4. 🚀 Deploy em produção

---

💡 **Dica:** Execute `python validacao_sistema.py` antes de usar o sistema para verificar se tudo está configurado corretamente!

🎉 **Sucesso total?** Execute `python app.py` e acesse `http://localhost:5001`