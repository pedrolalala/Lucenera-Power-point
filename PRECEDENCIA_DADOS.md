# Sistema de Precedência de Dados: XML > SharePoint

## 📋 Visão Geral

Este documento descreve o sistema de precedência de dados implementado para resolver conflitos entre especificações técnicas do SharePoint (arquivos .docx) e dados do orçamento XML.

**Regra Fundamental**: XML sempre tem prioridade sobre SharePoint para especificações técnicas.

---

## 🎯 Problema Resolvido

### Situação Anterior
- Fichas técnicas no SharePoint (.docx) frequentemente continham dados desatualizados
- Exemplo: potência da fita LED no Word diferia do projeto real (XML)
- Sistema montava slides com informações conflitantes ou incorretas

### Solução Implementada
- **Filtro Inteligente**: Remove automaticamente especificações técnicas desatualizadas do Word
- **Sanitização**: Compara categorias XML vs Word e elimina duplicações
- **Precedência Clara**: XML sobrescreve Word em todas as especificações técnicas

---

## 🔧 Componentes do Sistema

### 1. Filtro no SharePoint Client (`sharepoint_client.py`)

**Método**: `get_word_text(word_file_url, filtrar_tecnico=False)`

**Palavras-chave técnicas filtradas**:
- Componentes: lâmpada, LED, fita LED, driver, fonte, reator, acessórios
- Especificações: potência, watts, lúmens, temperatura de cor, voltagem, IP
- Variações: bivolt, 110V, 220V, 12V, 24V, Kelvin, IPC, IRC, etc.

**Funcionamento**:
```python
# Quando há componentes no XML, ativa filtro automático
filtrar_tecnico = len(componentes) > 0
texto_word = sp_client.get_word_text(download_url, filtrar_tecnico=True)
```

**Resultado**: Remove parágrafos do Word que mencionam componentes técnicos, mantendo apenas informações gerais (dimensões, acabamentos, instalação, etc.).

---

### 2. Função de Sanitização (`ppt.py`)

**Método**: `sanitizar_texto_word(texto_word, componentes, mandante)`

**Estratégia de Sanitização**:
1. **Mapeia categorias do XML**: Identifica todos os componentes presentes (LED, Fita LED, Driver, etc.)
2. **Identifica palavras conflitantes**: Cria lista de termos técnicos relacionados às categorias
3. **Remove linhas conflitantes**: Elimina do Word qualquer linha que mencione categorias presentes no XML
4. **Preserva informações gerais**: Mantém dimensões, acabamentos, aplicações, certificações, etc.

**Exemplo de Sanitização**:
```
ANTES (Word):
---
Luminária de embutir
Dimensões: 60x60cm
LED integrado 36W
Temperatura de cor: 4000K
Corpo em alumínio
IP20
---

DEPOIS (com Fita LED 16W no XML):
---
Luminária de embutir
Dimensões: 60x60cm
Corpo em alumínio
---
(linhas com "LED" e "36W" foram removidas)
```

**Logging Detalhado**:
```
[SANITIZACAO] Removida linha: LED integrado 36W
[SANITIZACAO] Removida linha: Temperatura de cor: 4000K
[SANITIZACAO] 2 linha(s) técnica(s) removida(s) para evitar conflito com XML
[SANITIZACAO] Categorias XML detectadas: fita led
```

---

### 3. Montagem do Slide com Precedência

**Método**: `adicionar_especificacoes_grupo(slide, word_files, sp_client, mandante, componentes)`

**Fluxo de Dados**:

1. **Extração Word com Filtro**:
   ```python
   filtrar_tecnico = len(componentes) > 0
   texto_word_bruto = sp_client.get_word_text(download_url, filtrar_tecnico)
   ```

2. **Sanitização Adicional**:
   ```python
   if componentes:
       texto_specs = sanitizar_texto_word(texto_word_bruto, componentes, mandante)
   ```

3. **Adição de Componentes XML**:
   ```python
   texto_specs += "\n" + "="*60 + "\n"
   texto_specs += "ESPECIFICAÇÕES TÉCNICAS (do Projeto):\n"
   texto_specs += "="*60 + "\n\n"
   
   for comp in componentes:
       texto_specs += f"[{idx}] {categoria} - Ref: {ref} | Qtd: {qtd}\n"
       texto_specs += f"    → {descricao}\n\n"
   ```

4. **Nota de Precedência**:
   ```python
   texto_specs += "* Dados extraídos do orçamento XML (versão mais recente)\n"
   ```

---

## 📊 Resultado Final no Slide

### Estrutura do Slide:
```
┌─────────────────────────────────────────────┐
│  [CABEÇALHO COM LOGO]                  L08  │
├─────────────────────────────────────────────┤
│  LUMINÁRIA DE PROJETO                       │
│                                             │
│  [IMAGEM DA FICHA TÉCNICA]                  │
├─────────────────────────────────────────────┤
│  Luminária de embutir                       │
│  Dimensões: 60x60cm                         │
│  Corpo em alumínio                          │
│                                             │
│  =========================================== │
│  ESPECIFICAÇÕES TÉCNICAS (do Projeto):      │
│  =========================================== │
│                                             │
│  [1] FITA LED - Ref: EKF5196HL9068L        │
│      Código Interno: 9923 | Qtd: 5 MT       │
│      → Fita LED 16W/m 4000K 220V           │
│                                             │
│  [2] DRIVER - Ref: DR-100-24               │
│      Código Interno: 8223 | Qtd: 1 UN       │
│      → Driver 100W 24V bivolt              │
│                                             │
│  * Dados extraídos do orçamento XML        │
│    (versão mais recente)                    │
└─────────────────────────────────────────────┘
```

### Divisão de Responsabilidades:

| Origem | Conteúdo |
|--------|----------|
| **SharePoint (Imagem)** | Foto do produto, título |
| **SharePoint (Word Sanitizado)** | Dimensões, acabamentos, materiais, aplicações |
| **XML (Prioridade Máxima)** | Componentes elétricos, potências, voltagens, quantidades |

---

## 🛡️ Proteções Implementadas

### 1. Dupla Camada de Filtro
- **Camada 1**: Filtro no `get_word_text` (remove parágrafos técnicos)
- **Camada 2**: Sanitização por categoria (remove linhas conflitantes específicas)

### 2. Fallback Seguro
```python
except Exception as e:
    print(f"[ERRO] Erro ao sanitizar: {str(e)}")
    return texto_word  # Retorna texto original em caso de erro
```

### 3. Logging Completo
- Registra quantidade de parágrafos/linhas removidas
- Mostra categorias XML detectadas
- Exibe preview das linhas removidas (primeiros 60 caracteres)

---

## 🧪 Casos de Teste

### Teste 1: Luminária com Fita LED
**Input XML**:
- L08: Luminária (mandante) + Fita LED 16W (componente)

**Resultado Esperado**:
- Word: Remove parágrafos com "LED", "Potência", "Watts"
- Slide: Mostra dados da Fita LED do XML (16W)

### Teste 2: Luminária com Driver e Acessórios
**Input XML**:
- L12: Luminária + Driver 100W + Suporte de fixação

**Resultado Esperado**:
- Word: Remove "Driver", "Fonte", "Acessórios"
- Slide: Lista Driver (100W) e Suporte separadamente

### Teste 3: Luminária sem Componentes
**Input XML**:
- L15: Apenas Luminária (sem componentes)

**Resultado Esperado**:
- Word: Mantém todas as especificações originais
- Slide: Mostra ficha técnica completa do Word

---

## 📈 Benefícios

1. **Precisão**: Especificações sempre refletem o projeto atual (XML)
2. **Consistência**: Elimina conflitos entre fontes de dados
3. **Manutenibilidade**: Facilita atualização de produtos no Excel master
4. **Transparência**: Logs detalhados facilitam debug e auditoria
5. **Flexibilidade**: Sistema adapta-se automaticamente aos componentes presentes

---

## 🔄 Fluxo Completo

```
1. XML Parse → Extrai grupos com mandante + componentes
                ↓
2. Busca SharePoint → Encontra .docx do mandante
                ↓
3. Extração Word → get_word_text(filtrar_tecnico=True)
                ↓
4. Filtro Técnico → Remove parágrafos com palavras-chave
                ↓
5. Sanitização → Remove linhas conflitantes com categorias XML
                ↓
6. Montagem Slide → Texto Word sanitizado + Componentes XML
                ↓
7. Resultado Final → Slide com precedência XML > Word
```

---

## 🐛 Debug

Para habilitar logs detalhados:

```python
# Em sharepoint_client.py
self.logger.setLevel(logging.DEBUG)

# Logs mostrarão:
# [FILTRO_TECNICO] Removido parágrafo: LED integrado 36W...
# [FILTRO_TECNICO] 3 parágrafo(s) técnico(s) removido(s)
```

Para ver sanitização linha por linha:

```python
# Em ppt.py, função sanitizar_texto_word
# Já imprime automaticamente:
# [SANITIZACAO] Removida linha: Potência: 36W...
# [SANITIZACAO] 5 linha(s) técnica(s) removida(s)
# [SANITIZACAO] Categorias XML detectadas: fita led, driver
```

---

## ✅ Validação

Para validar o sistema:

1. **Processar XML com componentes técnicos** (LED, Driver, etc.)
2. **Verificar logs de sanitização** (quantas linhas removidas)
3. **Abrir PowerPoint gerado** e confirmar:
   - Seção "ESPECIFICAÇÕES TÉCNICAS (do Projeto)"
   - Componentes listados com detalhes do XML
   - Nota de rodapé sobre precedência XML

---

## 📝 Notas de Implementação

- **Compatibilidade**: Sistema mantém compatibilidade com fluxo PDF (sem sanitização)
- **Performance**: Sanitização é leve (uma passagem por linha, regex simples)
- **Extensibilidade**: Fácil adicionar novas palavras-chave ou categorias
- **Type Safety**: Type hints atualizados com `Optional`, `List`, `Dict`

---

**Última Atualização**: Maio 2026  
**Status**: ✅ IMPLEMENTADO E VALIDADO
