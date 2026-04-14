# 🚀 SISTEMA LUCENERA SHAREPOINT

## ✨ Novas Funcionalidades

O sistema foi modernizado para trabalhar diretamente com **SharePoint** e **orçamentos XML**:

### 📋 **COMO USAR O NOVO SISTEMA**

#### 1. **Instalação das Dependências**
```bash
pip install -r requirements_sharepoint.txt
```

#### 2. **Teste da Conectividade**
```bash
python test_system.py
```

#### 3. **Estrutura de Dados Necessária**

**XML de Orçamento (exemplo):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<orcamento id="OR_006020" data="2026-04-10">
    <cliente nome="Cliente Exemplo"/>
    <itens>
        <item linha="43" codigo="10289" ref="3649-AB-S-PX" preco="655.39" quantidade="57"/>
        <item linha="44" codigo="10539" ref="3649-FE-S-PX" preco="872.00" quantidade="30"/>
    </itens>
</orcamento>
```

**Excel Master (estrutura esperada):**
| codigo | ref | marca | nome | ficha_tecnica |
|--------|-----|-------|------|---------------|
| 10289 | 3649-AB-S-PX | Interlight | Luminária Modelo A | doc_link |
| 10539 | 3649-FE-S-PX | Interlight | Luminária Modelo B | doc_link |

#### 4. **Estrutura SharePoint**
```
LUCENERA PROJETOS/
├── Fichas Técnicas/
    ├── Bella/
    │   ├── produto_codigo1.docx
    │   ├── produto_codigo1_BULA.jpg
    │   └── ambiente_codigo1.jpg
    ├── Interlight/
    │   ├── 10289_ficha_tecnica.docx
    │   ├── 10289_INSTALACAO.jpg
    │   └── 10539_especificacao.docx
    └── Jean Lux/
        └── ...
```

---

## 🔧 **CONFIGURAÇÃO**

### **Credenciais SharePoint**
As credenciais já estão configuradas em `sharepoint_client.py`:

- **Client ID:** `39ef469c-7496-40cb-ac08-ba01b514cf2d`
- **Tenant ID:** `b68c427b-b3f8-4bba-9252-66b24ce29c9d`
- **Permission:** `Files.Read.All`

### **Caminhos de Arquivos**

Edite em `ppt.py`:
```python
xml_orcamento = "C:/caminho/para/orcamento.xml"
excel_master = "C:/caminho/para/master_produtos.xlsx"
```

---

## 📊 **FLUXO NOVO VS ANTIGO**

### ❌ **Sistema Antigo**
```
PDF → Parse regex → Busca pasta local → Gera PPT
```

### ✅ **Sistema Novo**
```
XML → Parse estruturado → Consulta Excel master → 
Busca SharePoint por marca → Gera PPT
```

---

## 🧪 **TESTES E DEBUGGING**

1. **Teste básico:** `python test_system.py`
2. **Teste SharePoint:** Verifica conexão e lista marcas
3. **Teste XML:** Parsing da estrutura de orçamento
4. **Teste dependências:** Verifica instalação

### **Scripts Principais**

| Arquivo | Função |
|---------|--------|
| `ppt.py` | Geração de PowerPoint (principal) |
| `sharepoint_client.py` | Cliente Microsoft Graph |
| `data_manager.py` | Parser XML + Excel master |
| `test_system.py` | Testes de conectividade |

---

## 🔍 **PRÓXIMOS PASSOS PARA IMPLEMENTAÇÃO**

1. **Fornecer XML de exemplo real** para ajustar parser
2. **Verificar estrutura do Excel master** 
3. **Testar busca no SharePoint** com códigos reais
4. **Ajustar mapeamento marca ↔ códigos**
5. **Resolver nomes de arquivos "bagunçados"**

---

## ⚡ **VANTAGENS DO NOVO SISTEMA**

- ✅ **Sempre atualizado** (SharePoint online)
- ✅ **Múltiplas marcas** suportadas  
- ✅ **Excel master** como fonte da verdade
- ✅ **Busca inteligente** por códigos
- ✅ **Estrutura escalável** para novas marcas
- ✅ **API Microsoft Graph** robusta

---

## 🆘 **TROUBLESHOOTING**

### **Erro de Autenticação SharePoint**
- Verificar permissões no Azure AD
- Confirmar Client Secret ativado
- Checar acesso à pasta "Fichas Técnicas"

### **XML não encontrado**
- Verificar estrutura XML real
- Ajustar parser em `data_manager.py`

### **Excel master não carrega**
- Verificar caminho do arquivo
- Confirmar estrutura de colunas
- Testar com arquivo exemplo

---

**📧 Para dúvidas:** Sistema criado para automação Lucenera