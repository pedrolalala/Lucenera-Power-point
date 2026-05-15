"""
Parser de Orçamento PDF - Lucenera
Extrai informações de produtos do PDF de orçamento
"""

import re
import sys
import pdfplumber
from typing import List, Dict
import logging

# Configurar encoding UTF-8 para console Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass  # Se falhar, usar print() normal

logger = logging.getLogger(__name__)


def extrair_marca_da_referencia(referencia: str) -> str:
    """
    Tenta identificar a marca baseado no prefixo da referência
    
    Exemplos:
    - STH8536/30 -> STELLATECH (prefixo STH)
    - STL24845/27 -> STELLATECH (prefixo STL)
    - BL1074DR-BMPM -> Sem marca identificada
    - EKPF32 -> EKLART (prefixo EK)
    """
    referencia_upper = referencia.upper()
    
    # Mapeamento de prefixos comuns
    prefixos_marca = {
        'STH': 'STELLATECH',
        'STL': 'STELLATECH',
        'EK': 'EKLART',
        'LUC': 'LUCENERA',
        'BL': 'INTERLIGHT',
        'IL': 'ILUMINAR',
        'EV': 'EVOLED',
        'DS': 'DESSINE',
        'DR': 'DRESSALL',
        'AL': 'ALPERTONE'
    }
    
    for prefixo, marca in prefixos_marca.items():
        if referencia_upper.startswith(prefixo):
            return marca
    
    return 'LUCENERA'  # Marca padrão se não identificar


def extrair_produtos_do_pdf(pdf_path: str) -> List[Dict]:
    """
    Extrai lista de produtos do PDF de orçamento Lucenera/Foco Iluminação
    
    Estrutura esperada da tabela:
    ID | Código | Referência | Descrição | Qtd. | Un. | Vl. Unit. | Vl. Total
    L01 | 9923 | 3649-FE-S-PX | EMBUTIDO DE PISO... | 15 | UN | R$ 734,24 | R$ 11.013,60
    
    Args:
        pdf_path: Caminho do arquivo PDF
        
    Returns:
        Lista de dicts com: {item, codigo, referencia, descricao, quantidade, unidade}
    """
    produtos = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            logger.info(f"[PDF] Abrindo PDF: {pdf_path}")
            logger.info(f"[PDF] Total de páginas: {len(pdf.pages)}")
            
            # Processar todas as páginas
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if not text:
                    logger.warning(f"[PDF] Página {page_num} vazia")
                    continue
                
                logger.info(f"[PDF] Processando página {page_num}")
                
                # Dividir em linhas
                lines = text.split('\n')
                
                for line in lines:
                    # Padrão principal: L01 9923 3649-FE-S-PX DESCRIÇÃO... QTD UN
                    # Captura: ID (L01-L99), Código Interno (4-6 dígitos), Referência (alfanumérico com hífens)
                    pattern = r'^(L\d{2})\s+(\d{1,6})\s+([A-Z0-9\-/]+)\s+(.+?)\s+(\d+)\s+(UN|MT)\s+'
                    
                    match = re.match(pattern, line.strip())
                    
                    if match:
                        item_id = match.group(1)  # L01, L02, etc.
                        codigo_interno = match.group(2)  # 9923, 12895, etc.
                        referencia = match.group(3)  # 3649-FE-S-PX, BL1074DR-BMPM, etc.
                        descricao = match.group(4).strip()  # Descrição do produto
                        quantidade = match.group(5)  # 15, 69, etc.
                        unidade = match.group(6)  # UN, MT
                        
                        # Limpar descrição (remover valores e caracteres extras)
                        descricao = re.sub(r'R\$.*$', '', descricao).strip()
                        
                        produto = {
                            'item': item_id,
                            'codigo': codigo_interno,
                            'referencia': referencia,
                            'descricao': descricao,
                            'quantidade': quantidade,
                            'unidade': unidade,
                            'marca': extrair_marca_da_referencia(referencia)
                        }
                        
                        produtos.append(produto)
                        
                        logger.info(f"[PDF] [OK] {item_id}: Código {codigo_interno} | Ref {referencia} | {quantidade} {unidade}")
                
            logger.info(f"[PDF] [SUCESSO] Total de produtos extraídos: {len(produtos)}")
            
            # Log resumido dos produtos encontrados
            if produtos:
                logger.info(f"[PDF] Resumo:")
                for p in produtos[:5]:  # Mostrar apenas os primeiros 5
                    logger.info(f"[PDF]   - {p['item']}: {p['referencia']} (Código: {p['codigo']})")
                if len(produtos) > 5:
                    logger.info(f"[PDF]   ... e mais {len(produtos)-5} produtos")
            
            return produtos
            
    except Exception as e:
        logger.error(f"[PDF] [ERRO] Erro ao extrair produtos: {str(e)}")
        raise Exception(f"Erro ao processar PDF: {str(e)}")


def validar_produtos(produtos: List[Dict]) -> bool:
    """Valida se encontrou ao menos 1 produto"""
    if not produtos:
        raise Exception("Nenhum produto encontrado no PDF. Verifique o formato do arquivo.")
    
    if len(produtos) == 0:
        raise Exception("PDF vazio ou formato não reconhecido")
    
    logger.info(f"[PDF] [VALIDACAO] {len(produtos)} produto(s) válido(s)")
    return True


if __name__ == "__main__":
    # Teste rápido
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        produtos = extrair_produtos_do_pdf(pdf_path)
        validar_produtos(produtos)
        
        print("\n[SUCESSO] PRODUTOS EXTRAIDOS:")
        for p in produtos:
            print(f"  {p['item']}: Código {p['codigo']} | Ref {p['referencia']} | R$ {p['preco']}")
    else:
        print("Uso: python pdf_parser.py <caminho_do_pdf>")
