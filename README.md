# 🚀 Sistema SharePoint Lucenera - PowerPoint Generator

Sistema modernizado para geração de apresentações PowerPoint a partir de orçamentos XML integrado com Microsoft SharePoint via Graph API.

## ⭐ Características Principais

- 🌐 **Integração SharePoint**: Busca automática de imagens e documentos técnicos
- 📄 **Suporte XML/PDF**: Processa arquivos XML (novo) e PDFs (legado) 
- 🤖 **Automação Total**: Geração de PPT sem intervenção manual
- 💻 **Interface Web**: Upload via browser com interface moderna
- 🏷️ **Multi-marcas**: Suporte automático para diferentes fabricantes
- ⚡ **Performance**: Processamento em background com status em tempo real

## 📋 Pré-requisitos

- Python 3.8+
- Credenciais Microsoft Graph API configuradas
- Acesso ao SharePoint Lucenera
- Excel master com dados dos produtos

## 🚀 Instalação Rápida

### 🎯 Opção 1: Setup Automático (RECOMENDADO)
```bash
python setup_completo.py
```
**Este script faz TUDO automaticamente:**
- ✅ Instala dependências
- ✅ Configura arquivo .env com credenciais reais
- ✅ Cria Excel master template
- ✅ Valida sistema completo
- ✅ Opção de executar imediatamente

### 🔧 Opção 2: Setup Manual

#### 1. Instalar Dependências
```powershell
# PowerShell (Windows)
.\install_sharepoint_deps.ps1
```

**OU** manualmente:
```bash
pip install -r requirements_sharepoint.txt
```

#### 2. Configurar Credenciais
```bash
# Testar se credenciais estão funcionando
python test_env.py
```
**✅ Credenciais já estão configuradas no arquivo .env!**

#### 3. Configurar Excel Master
```bash
python criar_excel_template.py
```
- ✅ Cria template em `C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx`
- ✏️ Preencha com dados dos seus produtos
- 💾 Salve o arquivo

#### 4. Validar Sistema
```bash
python validacao_sistema.py
```

#### 5. Executar Sistema
```bash
python app.py
```

Acesse: **http://localhost:5001**

## 📁 Estrutura de Arquivos

```
📦 Sistema SharePoint Lucenera
├── 🐍 Código Principal
│   ├── app.py                      # Servidor Flask web
│   ├── ppt.py                      # Gerador de PowerPoint
│   ├── sharepoint_client.py        # Cliente Microsoft Graph API
│   └── data_manager.py             # Processamento XML/Excel
├── 🌐 Interface Web
│   └── web/
│       ├── index.html              # Interface principal
│       ├── script.js               # Lógica de upload
│       └── styles.css              # CSS moderno
├── 🔧 Configuração e Setup
│   ├── requirements_sharepoint.txt # Dependências Python
│   ├── install_sharepoint_deps.ps1 # Instalador Windows
│   ├── criar_excel_template.py     # Gerador Excel master
│   └── validacao_sistema.py        # Validação completa
├── 📖 Documentação
│   ├── README.md                   # Este arquivo
│   ├── CHECKLIST_SISTEMA.md        # Lista de verificação
│   ├── EXCEL_MASTER_README.md      # Documentação Excel
│   └── exemplo_orcamento.xml       # Exemplo de XML
└── 🧪 Testes
    └── test_system.py              # Testes automatizados
```

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