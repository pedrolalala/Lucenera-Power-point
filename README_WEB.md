# 🎨 Sistema de Processamento de Orçamentos - Lucenera

Sistema web para upload e processamento automático de orçamentos em PDF, gerando apresentações PowerPoint profissionais com **monitoramento em tempo real**.

## 📋 Estrutura do Projeto

```
script python power point/
├── app.py                      # Servidor Flask (backend)
├── main.py                     # Script de organização de arquivos
├── magica_ppt.py               # Script de geração de PPT
├── logo.png                    # Logo da Lucenera
├── requirements_web.txt        # Dependências Flask
├── web/
│   ├── index.html             # Página de upload
│   ├── styles.css             # Estilos da página de upload
│   ├── script.js              # Lógica de upload
│   ├── status.html            # Página de status/progresso
│   ├── styles_status.css      # Estilos da página de status
│   ├── status.js              # Monitoramento em tempo real
│   ├── gerenciar.html         # Página de gerenciamento de arquivos
│   ├── styles_gerenciar.css   # Estilos da página de gerenciamento
│   └── gerenciar.js           # Lógica de listagem/download
└── .venv/                     # Ambiente virtual Python
```

## 🚀 Instalação

### 1. Instalar dependências do Flask

```powershell
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Instalar Flask
pip install -r requirements_web.txt
```

## ▶️ Como Usar

### 1. Iniciar o servidor

```powershell
python app.py
```

O servidor iniciará em: **http://localhost:5001**

### 2. Acessar a interface web

Abra o navegador e acesse: **http://localhost:5001**

### 3. Fazer upload do PDF

1. Arraste o PDF do orçamento para a área de upload **OU**
2. Clique na área e selecione o arquivo PDF
3. Clique em "Processar Orçamento"
4. Você será redirecionado para a **página de status**

### 4. Acompanhar o processamento

A página de status mostra:
- ✅ Nome do arquivo sendo processado
- ✅ Timestamp de início
- ✅ Status atual (Aguardando / Processando / Pronto / Erro)
- ✅ Barra de progresso visual (0-100%)
- ✅ Etapas detalhadas:
  - Upload do PDF
  - Organização de Arquivos
  - Geração do PowerPoint
- ✅ Botão de download quando concluído
- ✅ Mensagem de erro clara (se houver falha)

### 5. Baixar o PowerPoint

Quando o status for "Pronto", clique no botão **"Baixar PowerPoint"**

### 6. Processar novo orçamento

Clique no botão **"Processar Novo Orçamento"** para voltar à página inicial

### 7. Gerenciar arquivos gerados

Acesse **http://localhost:5001/gerenciar** para:
- Ver todos os PPTs gerados
- Baixar qualquer arquivo anterior
- Ver informações (data, tamanho, timestamp)
- Criar novo orçamento

## 🎨 Recursos

✅ **Interface Profissional**: Design em preto/branco/cinza conforme padrão Lucenera  
✅ **Drag & Drop**: Arraste e solte arquivos PDF  
✅ **Validação**: Verifica tipo e tamanho do arquivo (máx. 10MB)  
✅ **Status em Tempo Real**: Monitoramento automático a cada 2 segundos  
✅ **Barra de Progresso**: Feedback visual do progresso (0-100%)  
✅ **Etapas Detalhadas**: Mostra exatamente o que está sendo processado  
✅ **Processamento em Background**: Não trava o servidor  
✅ **Tratamento de Erros**: Mensagens claras de erro  
✅ **Responsivo**: Funciona em desktop e mobile  
✅ **Download Direto**: Botão de download quando pronto  
✅ **Gerenciador de Arquivos**: Visualize e baixe todos os PPTs gerados  
✅ **Múltiplos Endpoints**: Download por timestamp ou nome completo  
✅ **Navegação Integrada**: Links entre todas as páginas  

## ⚙️ Fluxo de Processamento

```
1. Upload PDF → 2. Redireciona para Status → 3. Organizar (main.py) → 4. Gerar PPT (magica_ppt.py) → 5. Download
```

### Detalhes do Status

| Status | Progresso | Descrição |
|--------|-----------|-----------|
| `uploading` | 10% | Arquivo sendo enviado |
| `organizing` | 30% | Executando main.py (organização) |
| `generating` | 60% | Executando magica_ppt.py (criação PPT) |
| `completed` | 100% | Pronto para download |
| `error` | - | Erro no processamento |

## 📂 Pastas Utilizadas

- **Upload**: `C:\Users\pedro\OneDrive\Desktop\lucenera\`
- **Arquivos Separados**: `C:\Users\pedro\OneDrive\Desktop\lucenera\INTERLIGHT_SEPARADOS\`
- **PPT Gerado**: `C:\Users\pedro\OneDrive\Desktop\lucenera\orcamento_[timestamp].pptx`

## 🛠️ Tecnologias

- **Backend**: Flask (Python) + Threading (processamento assíncrono)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Processamento**: pdfplumber, python-pptx, python-docx, Pillow
- **Monitoramento**: Polling via AJAX (a cada 2 segundos)

## 🔄 Sistema de Jobs

O sistema usa **UUID** para identificar cada job e armazena em memória:
- Status atual
- Progresso (%)
- Caminho do PDF
- Caminho do PPT gerado
- Mensagens de erro

## 📝 Endpoints da API

### `POST /processar`
Inicia processamento de um PDF
- **Input**: FormData com PDF
- **Output**: `{ success: true, job_id: "uuid" }`

### `GET /status/<job_id>`
Consulta status de um job
- **Output**: `{ status: "...", progress: 0-100, filename: "...", error: "...", download_url: "..." }`

### `GET /download/<timestamp>`
Download do PPT pelo timestamp
- **Formato**: `/download/20260324_143022`
- **Output**: Arquivo .pptx

### `GET /download_file/<filename>`
Download de arquivo específico pelo nome completo
- **Formato**: `/download_file/orcamento_20260324_143022.pptx`
- **Output**: Arquivo (PPT ou PDF)

### `GET /api/listar_arquivos`
Lista todos os arquivos PPT gerados
- **Output**: `{ success: true, arquivos: [...] }`

### `GET /gerenciar`
Página de gerenciamento de arquivos
- **Output**: HTML da interface de gerenciamento

## 🎯 Desenvolvido para

**LUCENERA - ATELIER DA LUZ**  
Av. Nove de Julho 49, Ribeirão Preto (SP)  
www.facebook.com/luceneraatelier
