# ✅ CHECKLIST SISTEMA SHAREPOINT LUCENERA

## 🎯 Pré-requisitos

### 1. 🐍 Python e Ambiente
- [ ] Python 3.8+ instalado
- [ ] PowerShell ou terminal disponível
- [ ] Acesso à internet para downloads

### 2. 📁 Estrutura de Arquivos
- [ ] Código fonte baixado na pasta correta
- [ ] Permissões de escrita na pasta de trabalho
- [ ] Espaço livre suficiente no disco

---

## 🚀 Instalação (Execute UMA VEZ)

### ⚡ Opção A: Setup Automático (RECOMENDADO)
```bash
python setup_completo.py
```
**Este comando faz TUDO automaticamente! Pule para "Execução do Sistema" se usar esta opção.**

### 🔧 Opção B: Setup Manual

#### Passo 1: Instalar Dependências
```powershell
# No PowerShell, execute:
.\install_sharepoint_deps.ps1
```
**OU** manualmente:
```bash
pip install -r requirements_sharepoint.txt
```

#### Passo 2: Verificar Credenciais
```bash
python test_env.py
```
- [ ] Arquivo .env existe com credenciais válidas
- [ ] Todas as variáveis obrigatórias estão definidas
- [ ] Teste de conectividade SharePoint passa

#### Passo 3: Criar Excel Master
```bash
python criar_excel_template.py
```
- [ ] Arquivo criado em: `C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx`
- [ ] Template aberto e verificado
- [ ] Dados de exemplo visualizados

#### Passo 4: Configurar Excel Master
- [ ] Preencher dados reais dos produtos
- [ ] Verificar códigos internos corretos
- [ ] Conferir nomes das marcas (devem coincidir com pastas SharePoint)
- [ ] Salvar arquivo após preenchimento

#### Passo 5: Teste do Sistema
```bash
python validacao_sistema.py
```
- [ ] Todos os módulos importados com sucesso
- [ ] Credenciais SharePoint carregadas do .env
- [ ] SharePoint client configurado
- [ ] Excel master carregado corretamente

---

## � Configuração Credenciais (.env)

O sistema usa variáveis de ambiente para segurança. **As credenciais estão PRÉ-CONFIGURADAS:**

### Arquivo .env (Já Configurado ✅)
```env
SHAREPOINT_CLIENT_ID=39ef469c-7496-40cb-ac08-ba01b514cf2d
SHAREPOINT_TENANT_ID=b68c427b-b3f8-4bba-9252-66b24ce29c9d
SHAREPOINT_CLIENT_SECRET=your_client_secret_here
EXCEL_MASTER_PATH=C:/Users/pedro/OneDrive/Desktop/lucenera/master_produtos.xlsx
```

### Verificar Configuração
```bash
python test_env.py
```
- [ ] Arquivo .env encontrado
- [ ] Credenciais SharePoint carregadas
- [ ] Caminho Excel master definido
- [ ] Teste de conectividade opcional realizado

---

## �📊 Preparação do SharePoint

### Estrutura de Pastas
Confirme que existe no SharePoint:
```
LUCENERA PROJETOS/
└── Fichas Técnicas/
    ├── Interlight/           ← Pasta da marca
    ├── Bella Luce/          ← Pasta da marca  
    ├── Direct Light/        ← Pasta da marca
    ├── Jean Lux/           ← Pasta da marca
    └── [outras marcas]/     ← Conforme necessário
```

### Arquivos por Produto
Para cada produto, organize:
- [ ] **Ficha técnica:** `[CODIGO]_ficha_tecnica.docx`
- [ ] **Manual:** `[CODIGO]_BULA_INSTALACAO.pdf`
- [ ] **Especificação:** `[CODIGO]_especificacao.docx`

**Exemplo para produto código 10289:**
- `10289_ficha_tecnica.docx`
- `10289_BULA_INSTALACAO.pdf`
- `3649-AB-S-PX_especificacao.docx`

---

## 📝 Preparação do XML

### Formato Correto
Use como base: `exemplo_orcamento.xml`

### Campos Obrigatórios
Para cada item de orçamento:
- [ ] `codigo` - Deve existir no Excel master
- [ ] `ref` - Referência do produto
- [ ] `preco` - Preço unitário
- [ ] `quantidade` - Quantidade do item
- [ ] `linha` - Número da linha (L43, L44, etc.)

### Exemplo de Item:
```xml
<item 
    linha="43" 
    codigo="10289" 
    ref="3649-AB-S-PX" 
    preco="655.39" 
    quantidade="57"
    marca="Interlight"
    descricao="Luminária de embutir LED 30W"
/>
```

---

## 🌐 Execução do Sistema

### 1. Iniciar Servidor
```bash
python app.py
```
- [ ] Servidor iniciado na porta 5001
- [ ] Mensagem "Running on http://localhost:5001" aparece
- [ ] Sem erros no terminal

### 2. Acessar Interface Web
- [ ] Abrir navegador
- [ ] Ir para: `http://localhost:5001`
- [ ] Interface carregada com abas XML/PDF
- [ ] Sistema de badges funcionando

### 3. Upload de Arquivo XML
- [ ] Clicar na aba "📄 XML (SharePoint)"
- [ ] Selecionar arquivo XML válido
- [ ] Clicar "Processar XML"
- [ ] Aguardar processamento

### 4. Verificar Resultado
- [ ] PowerPoint gerado com sucesso
- [ ] Slides contêm imagens dos produtos
- [ ] Informações de preço e quantidade corretas
- [ ] Layout profissional aplicado

---

## 🔍 Troubleshooting

### Problema: Credenciais não encontradas
**Erro:** `"Credenciais SharePoint não encontradas no arquivo .env"`
**Soluções:**
1. Execute: `python test_env.py` para diagnosticar
2. Verifique se arquivo `.env` existe na pasta do projeto
3. Execute: `python setup_completo.py` para reconfigurar tudo

### Problema: Dependências não instaladas
**Solução:**
```bash
pip install --upgrade pip
pip install python-dotenv
pip install -r requirements_sharepoint.txt
```

### Problema: Excel master não encontrado
**Solução:**
1. Execute: `python criar_excel_template.py`
2. Preencha o template gerado
3. Salve no local correto
4. Verifique variável `EXCEL_MASTER_PATH` no .env

### Problema: Produto não encontrado
**Verificações:**
- [ ] Código existe no Excel master?
- [ ] Marca está correta?
- [ ] Pasta da marca existe no SharePoint?
- [ ] Arquivos nomeados corretamente?

### Problema: Falha autenticação SharePoint
**Verificações:**
- [ ] Execute: `python test_env.py` para testar credenciais
- [ ] Client ID correto no .env?
- [ ] Client Secret válido no .env?
- [ ] Tenant ID correto no .env?
- [ ] Conexão com internet disponível?

### Problema: Variáveis de ambiente não carregam
**Soluções:**
1. Instale: `pip install python-dotenv`
2. Verifique se arquivo `.env` está na pasta do projeto (não em subpasta)
3. Execute: `python test_env.py` para diagnosticar

### Problema: Imagens não aparecem
**Verificações:**
- [ ] Arquivos .docx contêm imagens?
- [ ] Nomes dos arquivos incluem código do produto?
- [ ] Permissões de leitura no SharePoint?
- [ ] Execute: `python test_env.py` para testar conectividade

---

## 📞 Suporte

### Logs do Sistema
Para debugging:
```bash
python app.py --debug
```

### Teste de Credenciais
```bash
python test_env.py
```

### Teste de Conectividade
```bash
python test_sharepoint_connection.py
```

### Validação Completa
```bash
python validacao_sistema.py --verbose
```

### Setup Automático (Resolver Tudo)
```bash
python setup_completo.py
```

---

## ✨ Recursos Disponíveis

### ✅ Implementado
- [x] Autenticação SharePoint via Microsoft Graph
- [x] Upload XML via interface web
- [x] Busca automática de produtos no Excel master
- [x] Download de imagens de arquivos .docx
- [x] Geração de PowerPoint personalizado
- [x] Interface web moderna com abas
- [x] Suporte a múltiplas marcas
- [x] Compatibilidade com sistema PDF legado

### 🔄 Em Desenvolvimento
- [ ] Cache de imagens para performance
- [ ] Validação avançada de XML
- [ ] Relatórios de processo detalhados
- [ ] Interface para gerenciar Excel master

---

## 🎉 Sucesso!

Se você chegou até aqui e todos os itens estão marcados, seu sistema SharePoint Lucenera está pronto para uso!

**🚀 Próximo passo:** Execute `python app.py` e acesse `http://localhost:5001`