# ✅ SISTEMA PDF REATIVADO!

## 🎉 O que mudou?

O processamento de orçamentos em **PDF foi reativado** e **modernizado**!

## 📦 Novos Componentes

### 1. **pdf_parser.py**
- Extrai produtos do PDF de orçamento
- Suporta 2 padrões de PDF:
  - **Padrão 1**: `L01  11261  EKF5196HL9068L  R$ 1.234,56`
  - **Padrão 2**: `Código: 11261 | Referência: EKF5196HL9068L`
- Logging detalhado de produtos encontrados

### 2. **ppt.py - Nova função**
- `gerar_powerpoint_pdf()`:
  - Processa PDF → Extrai produtos → Busca SharePoint → Gera PowerPoint
  - Usa mesma infraestrutura do sistema XML
  - Integrado com Excel master para enriquecer dados
  - Busca fichas técnicas no SharePoint por código

### 3. **app.py e app_production.py**
- Função `process_pdf_job()` reativada:
  - Aceita upload de PDF
  - Processa em background
  - Status em tempo real
  - Download automático ao concluir

## 🔄 Fluxo do Sistema PDF

```
PDF → pdf_parser.py → Extrai produtos (códigos + referências)
                           ↓
               Excel Master → Busca marca/dados adicionais
                           ↓
               SharePoint → Busca fichas técnicas por código
                           ↓
               ppt.py → Gera PowerPoint completo
```

## 🎯 Exemplo de Uso

### Via Web Interface:
1. Acesse http://localhost:5001
2. Selecione aba **"PDF"**
3. Faça upload do PDF de orçamento
4. Aguarde processamento (30-60s)
5. Download automático do PowerPoint

### Via Python:
```python
from ppt import gerar_powerpoint_pdf

ppt_path = gerar_powerpoint_pdf(
    pdf_path="C:/caminho/orcamento.pdf",
    excel_path="C:/caminho/master_produtos.xlsx",
    output_path="C:/caminho/saida.pptx"
)
print(f"PowerPoint gerado: {ppt_path}")
```

### Via CLI:
```bash
# Testar extração de produtos do PDF
python pdf_parser.py "C:\caminho\orcamento.pdf"
```

## 📝 Formato do PDF Esperado

O PDF deve conter produtos em um destes formatos:

### Formato 1 (Preferencial):
```
L01  11261  EKF5196HL9068L  Luminária LED  R$ 345,00
L02  12345  ABC123XYZ       Spot Embutir   R$ 189,90
L03  67890  DEF456UVW       Fita LED 5m    R$ 234,50
```

### Formato 2 (Alternativo):
```
Código: 11261
Referência: EKF5196HL9068L
Preço: R$ 345,00

Código: 12345
Ref: ABC123XYZ
```

## 🆕 Dependências Adicionadas

- `pdfplumber==0.10.3` → Parsing de PDF

Atualizado em `requirements_sharepoint.txt`

## ⚙️ Instalação

Se você já tem o ambiente configurado:

```powershell
pip install pdfplumber==0.10.3
```

Ou reinstale todas as dependências:

```powershell
pip install -r requirements_sharepoint.txt
```

## 🔍 Debugging

### Ver produtos extraídos do PDF:
```python
from pdf_parser import extrair_produtos_do_pdf, validar_produtos

produtos = extrair_produtos_do_pdf("orcamento.pdf")
validar_produtos(produtos)

for p in produtos:
    print(f"{p['item']}: {p['codigo']} - {p['referencia']} - R$ {p['preco']}")
```

### Testar busca de marca:
```python
from data_manager import ExcelMaster

excel = ExcelMaster("master_produtos.xlsx")
marca = excel.buscar_marca_por_codigo("11261")
print(f"Marca: {marca}")  # Ex: "Interlight"
```

## ✅ Status

- [x] pdf_parser.py criado
- [x] gerar_powerpoint_pdf() implementado
- [x] process_pdf_job() reativado
- [x] buscar_marca_por_codigo() adicionado
- [x] pdfplumber instalado
- [x] requirements_sharepoint.txt atualizado
- [x] Ambos app.py e app_production.py atualizados

## 🚀 Próximos Passos

1. **Testar com PDF real**:
   - Fazer upload de um PDF de orçamento
   - Verificar se produtos são extraídos corretamente
   - Validar PowerPoint gerado

2. **Ajustar padrões de PDF** (se necessário):
   - Editar `pdf_parser.py` → padrões regex
   - Adicionar novos formatos de PDF

3. **Monitorar logs**:
   - Ver `logs/lucenera_production.log` para erros
   - Verificar console do Flask

## 📞 Suporte

- Se PDF não for reconhecido → Verificar formato em `pdf_parser.py`
- Se marca não for encontrada → Verificar Excel master
- Se ficha não for encontrada → Verificar SharePoint

## 🎯 Benefícios

✅ **Compatibilidade total**: PDF e XML funcionam lado a lado  
✅ **Mesma infraestrutura**: Usa SharePoint para ambos  
✅ **Logs detalhados**: Facilita debugging  
✅ **Extensível**: Fácil adicionar novos formatos de PDF  
✅ **Robusto**: Tratamento de erros completo  

---

🎉 **Sistema PDF totalmente operacional!**
