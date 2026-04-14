"""
Parser de Orçamento PDF - Lucenera
Extrai informações de produtos do PDF de orçamento
"""

import re
import pdfplumber
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


def extrair_produtos_do_pdf(pdf_path: str) -> List[Dict]:
    """
    Extrai lista de produtos do PDF de orçamento
    
    Procura por padrões como:
    - L01  11261  EKF5196HL9068L  R$ 1.234,56
    - Item: 11261 | Ref: EKF5196HL9068L | Preço: R$ 1.234,56
    
    Args:
        pdf_path: Caminho do arquivo PDF
        
    Returns:
        Lista de dicts com: {codigo, referencia, preco, descricao}
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
                
                # Padrão 1: L0X  CODIGO  REFERENCIA  ...  R$ PREÇO
                # Ex: L01  11261  EKF5196HL9068L  ...  R$ 1.234,56
                pattern1 = r'L0(\d+)\s+(\d+)\s+([A-Z0-9\-]+).*?R\$\s*([\d.,]+)'
                matches = re.finditer(pattern1, text, re.DOTALL)
                
                for match in matches:
                    item_num = match.group(1)
                    codigo = match.group(2)
                    referencia = match.group(3)
                    preco = match.group(4)
                    
                    produtos.append({
                        'item': f'L{item_num.zfill(2)}',
                        'codigo': codigo,
                        'referencia': referencia,
                        'preco': preco,
                        'descricao': f'Item L{item_num.zfill(2)}'
                    })
                    
                    logger.info(f"[PDF] ✓ Encontrado L{item_num.zfill(2)}: {codigo} - {referencia} - R$ {preco}")
                
                # Padrão 2: Código mais flexível
                # Ex: Código: 11261 | Referência: EKF5196HL9068L
                pattern2 = r'(?:C[óo]digo|Item|Ref\.?|Cód\.?)[:.\s]*(\d{4,6})'
                codigo_matches = re.finditer(pattern2, text, re.IGNORECASE)
                
                for match in codigo_matches:
                    codigo = match.group(1)
                    
                    # Tentar encontrar referência próxima
                    ref_pattern = r'(?:Ref\.?|Referência)[:.\s]*([A-Z0-9\-]{5,20})'
                    ref_match = re.search(ref_pattern, text[match.end():match.end()+100], re.IGNORECASE)
                    
                    referencia = ref_match.group(1) if ref_match else codigo
                    
                    # Evitar duplicatas
                    if not any(p['codigo'] == codigo for p in produtos):
                        produtos.append({
                            'item': f'Item {len(produtos)+1}',
                            'codigo': codigo,
                            'referencia': referencia,
                            'preco': '',
                            'descricao': ''
                        })
                        
                        logger.info(f"[PDF] ✓ Encontrado (padrão 2): {codigo} - {referencia}")
                
            logger.info(f"[PDF] ✅ Total de produtos extraídos: {len(produtos)}")
            
            # Log dos produtos encontrados
            for p in produtos:
                logger.info(f"[PDF]   - {p['item']}: {p['codigo']} ({p['referencia']})")
            
            return produtos
            
    except Exception as e:
        logger.error(f"[PDF] ❌ Erro ao extrair produtos: {str(e)}")
        raise Exception(f"Erro ao processar PDF: {str(e)}")


def validar_produtos(produtos: List[Dict]) -> bool:
    """Valida se encontrou ao menos 1 produto"""
    if not produtos:
        raise Exception("Nenhum produto encontrado no PDF. Verifique o formato do arquivo.")
    
    if len(produtos) == 0:
        raise Exception("PDF vazio ou formato não reconhecido")
    
    logger.info(f"[PDF] ✅ Validação: {len(produtos)} produto(s) válido(s)")
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
        
        print("\n✅ PRODUTOS EXTRAÍDOS:")
        for p in produtos:
            print(f"  {p['item']}: Código {p['codigo']} | Ref {p['referencia']} | R$ {p['preco']}")
    else:
        print("Uso: python pdf_parser.py <caminho_do_pdf>")
