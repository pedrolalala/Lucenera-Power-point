# EXEMPLO PRÁTICO: Adicionar Validação de Quantidade

## Objetivo
Validar se produtos têm quantidade > 0 e adicionar alerta visual no slide

## Modificações Necessárias

### 1. data_manager.py - Adicionar validação

```python
# Em DataManager.processar_orcamento()

def processar_orcamento(self) -> List[Dict]:
    # Parse XML
    produtos = self.parser.parse_xml()
    
    # ⭐ NOVA ETAPA: Validar quantidades
    produtos = self._validar_quantidades(produtos)
    
    # Enriquecer com Excel
    for produto in produtos:
        codigo = produto.get("codigo", "")
        marca = self.excel_master.buscar_marca_por_codigo(codigo)
        if marca:
            produto["marca"] = marca
    
    return produtos

def _validar_quantidades(self, produtos: List[Dict]) -> List[Dict]:
    """
    Valida quantidades dos produtos e adiciona flag de alerta
    """
    for produto in produtos:
        quantidade_str = produto.get("quantidade", "0")
        
        try:
            quantidade = int(quantidade_str)
        except ValueError:
            quantidade = 0
        
        # Adicionar flags
        produto["quantidade_numerica"] = quantidade
        produto["quantidade_invalida"] = (quantidade <= 0)
        
        if quantidade <= 0:
            print(f"[ALERTA] Produto {produto.get('codigo')} com quantidade inválida: {quantidade_str}")
    
    return produtos
```

### 2. ppt.py - Adicionar alerta visual no slide

```python
# Em criar_slides_produto()

def criar_slides_produto(prs, produto, sp_client):
    codigo = produto.get('codigo', '')
    ref = produto.get('ref', '')
    marca = produto.get('marca', 'Interlight')
    lnum = produto.get('lnum', '1')
    
    # ⭐ NOVA ETAPA: Verificar quantidade
    quantidade_invalida = produto.get('quantidade_invalida', False)
    
    # ... código de busca SharePoint ...
    
    # Criar slide de ficha técnica
    slide_ficha = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide_ficha)
    
    # ... código de título e número LXX ...
    
    # ⭐ NOVA ETAPA: Adicionar alerta se quantidade inválida
    if quantidade_invalida:
        adicionar_alerta_quantidade(slide_ficha, lnum)
    
    # ... resto do código ...

def adicionar_alerta_quantidade(slide, lnum):
    """
    Adiciona alerta visual de quantidade inválida
    """
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    
    # Banner vermelho de alerta
    from pptx.enum.shapes import MSO_SHAPE
    rect_alerta = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.5),
        Inches(1.8),
        Inches(7.27),
        Inches(0.4)
    )
    rect_alerta.fill.solid()
    rect_alerta.fill.fore_color.rgb = RGBColor(220, 53, 69)  # Vermelho
    rect_alerta.line.color.rgb = RGBColor(180, 0, 0)
    
    # Texto do alerta
    tx_alerta = slide.shapes.add_textbox(
        Inches(0.5),
        Inches(1.85),
        Inches(7.27),
        Inches(0.3)
    )
    tf_alerta = tx_alerta.text_frame
    tf_alerta.text = f"⚠️ ATENÇÃO: Produto L{lnum} com quantidade ZERO ou inválida"
    
    # Formatação
    p = tf_alerta.paragraphs[0]
    p.font.name = 'Calibri'
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)  # Branco
    p.alignment = PP_ALIGN.CENTER
    
    print(f"  [ALERTA] Slide L{lnum} marcado com alerta de quantidade")
```

### 3. app.py - Adicionar status "validating"

```python
# Em process_xml_job()

def process_xml_job(job_id, xml_path, timestamp):
    try:
        print(f"[INICIO] [{job_id}] Iniciando processamento XML com SharePoint...")
        
        # Atualizar status: validando
        jobs[job_id]['status'] = 'validating'
        jobs[job_id]['progress'] = 20
        
        # Verificar se Excel master existe
        if not os.path.exists(EXCEL_MASTER):
            raise Exception(f'Excel master não encontrado: {EXCEL_MASTER}')
        
        # Atualizar status: processando
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['progress'] = 40
        
        # ... resto do código ...
```

### 4. web/script.js - Adicionar feedback visual

```javascript
// Em updateJobStatus()

function updateJobStatus(jobId, status, progress, error) {
    const jobCard = document.querySelector(`[data-job-id="${jobId}"]`);
    if (!jobCard) return;

    const progressBar = jobCard.querySelector('.job-progress-fill');
    const statusText = jobCard.querySelector('.job-status');

    // Atualizar progresso
    progressBar.style.width = `${progress}%`;

    // ⭐ NOVA ETAPA: Status de validação
    if (status === 'validating') {
        statusText.innerHTML = `
            <i class="fas fa-check-circle"></i>
            Validando produtos...
        `;
        statusText.className = 'job-status job-status-processing';
    }
    else if (status === 'processing') {
        statusText.innerHTML = `
            <i class="fas fa-cogs"></i>
            Processando orçamento...
        `;
        statusText.className = 'job-status job-status-processing';
    }
    // ... resto dos status ...
}
```

## Resultado Final

Quando houver produto com quantidade inválida:
1. ✅ Console mostra: `[ALERTA] Produto 12345 com quantidade inválida: 0`
2. ✅ UI mostra status: "Validando produtos..."
3. ✅ Slide tem banner vermelho: "⚠️ ATENÇÃO: Produto L02 com quantidade ZERO ou inválida"
4. ✅ PowerPoint gerado normalmente com alerta visual

## Fluxo Atualizado

```
XML Upload → Validando (20%) → Processando (40%) → Gerando (60%) → Completo (100%)
                  ↓
           _validar_quantidades()
                  ↓
           Adiciona flags aos produtos
                  ↓
           adicionar_alerta_quantidade() (se necessário)
```
