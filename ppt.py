import os
import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image
import io
import tempfile

# Novos módulos para SharePoint e XML
from sharepoint_client import SharePointClient
from data_manager import DataManager

# Configurações do novo sistema
xml_orcamento = r"C:\Users\pedro\OneDrive\Desktop\lucenera\orcamento.xml"  # Será definido dinamicamente
excel_master = r"C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx"  # Caminho do Excel master
logo_path = r"C:\script python\script python power point\logo.png"

# Instanciar clientes
sharepoint_client = SharePointClient()
data_manager = None  # Será inicializado com dados reais

# Extrair nome do XML sem extensão
xml_nome = "orcamento_sharepoint"  # Nome padrão, será atualizado dinamicamente
ppt_saida = rf"C:\Users\pedro\OneDrive\Desktop\lucenera\Ficha_Tecnica_{xml_nome}.pptx"

img_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

a4_width = Inches(8.27)
a4_height = Inches(11.69)

# Função para processar orçamento XML e gerar PowerPoint
def gerar_powerpoint_sharepoint(xml_path: str, excel_path: str, output_path: str = None):
    """
    Gera PowerPoint a partir de XML usando dados do SharePoint
    
    Args:
        xml_path: Caminho para arquivo XML de orçamento
        excel_path: Caminho para Excel master de produtos
        output_path: Caminho de saída (opcional)
    """
    try:
        print("[INICIO] Iniciando geração PowerPoint com SharePoint...")
        
        # Inicializar gerenciador de dados
        global data_manager
        data_manager = DataManager(xml_path, excel_path)
        
        # Processar orçamento
        print("[XML] Processando orçamento XML...")
        produtos = data_manager.processar_orcamento()
        
        if not produtos:
            raise Exception("Nenhum produto encontrado no XML")
        
        print(f"[OK] {len(produtos)} produtos encontrados!")
        
        # Definir nome de saída
        if output_path:
            ppt_saida_final = output_path
        else:
            xml_base = os.path.splitext(os.path.basename(xml_path))[0]
            ppt_saida_final = rf"C:\Users\pedro\OneDrive\Desktop\lucenera\Ficha_Tecnica_{xml_base}.pptx"
        
        # Criar apresentação
        prs = Presentation()
        prs.slide_width = a4_width
        prs.slide_height = a4_height
        
        # Slide de capa
        criar_slide_capa(prs)
        
        # Processar cada produto
        for i, produto in enumerate(produtos, 1):
            print(f"[PROC] Processando produto {i}/{len(produtos)}: L{produto.get('lnum', '?')} - {produto.get('ref', '?')}")
            
            # Criar slides para o produto
            criar_slides_produto(prs, produto, sharepoint_client)
        
        # Salvar PowerPoint
        prs.save(ppt_saida_final)
        
        print(f"[SUCESSO] PowerPoint gerado com sucesso!")
        print(f"[ARQUIVO] {ppt_saida_final}")
        print(f"[TOTAL] {len(produtos)} produtos processados")
        return ppt_saida_final
        
    except Exception as e:
        print(f"[ERRO] Erro ao gerar PowerPoint: {str(e)}")
        raise


def criar_slide_capa(prs):
    """Cria slide de capa com logo Lucenera"""
    slide_capa = prs.slides.add_slide(prs.slide_layouts[6])
    if os.path.exists(logo_path):
        # Logo centralizada no meio da página
        logo_width = 3
        logo_height = 3
        logo_left = (8.27 - logo_width) / 2
        logo_top = (11.69 - logo_height) / 2
        slide_capa.shapes.add_picture(logo_path, Inches(logo_left), Inches(logo_top), width=Inches(logo_width))


def criar_slides_produto(prs, produto, sp_client):
    """
    Cria slides para um produto específico usando busca SIMPLIFICADA por código interno
    
    Args:
        prs: Apresentação PowerPoint
        produto: Dados do produto
        sp_client: Cliente SharePoint
    """
    codigo = produto.get('codigo', '')
    ref = produto.get('ref', '')
    marca = produto.get('marca', 'Interlight')
    lnum = produto.get('lnum', '1')
    
    print(f"  [PROC] Processando produto {lnum}: {marca} - Código: {codigo}")
    
    print(f"  [BUSCA_CODIGO] Buscando arquivos .docx no SharePoint por código interno: {codigo}")
    
    # Buscar arquivos no SharePoint pelo CÓDIGO INTERNO
    arquivos = sp_client.search_files_by_code(codigo)
    
    if not arquivos:
        print(f"  [AVISO] Nenhum arquivo .docx encontrado para código {codigo}")
    else:
        print(f"  [OK] {len(arquivos)} arquivo(s) .docx encontrado(s)")
        # Mostrar detalhes dos matches para debug
        for i, arq in enumerate(arquivos[:3]):  # Primeiro 3 apenas
            print(f"    [{i+1}] {arq['name']} (score: {arq.get('score', 0)}, método: {arq.get('match_method', 'N/A')})")
    
    # Todos os arquivos retornados são .docx (Word) desde o novo método
    word_files = arquivos  # Todos são Word files agora
    image_files = []  # Não há imagens na busca .docx
    bula_files = [arq for arq in arquivos if arq.get('is_bula', False)]
    
    # Criar slide de ficha técnica
    slide_ficha = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(slide_ficha)
    
    # Título pequeno em preto abaixo do cabeçalho
    tx_title = slide_ficha.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(3), Inches(0.4))
    tf_title = tx_title.text_frame
    tf_title.text = "LUMINÁRIA DE PROJETO"
    tf_title.paragraphs[0].font.name = 'Calibri'
    tf_title.paragraphs[0].font.size = Pt(12)
    tf_title.paragraphs[0].font.bold = False
    tf_title.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
    
    # Número LXX grande em preto no canto superior direito
    tx_lnum = slide_ficha.shapes.add_textbox(Inches(6.8), Inches(1.2), Inches(1), Inches(0.5))
    tf_lnum = tx_lnum.text_frame
    tf_lnum.text = f"L{lnum}"
    tf_lnum.paragraphs[0].font.name = 'Calibri'
    tf_lnum.paragraphs[0].font.size = Pt(36)
    tf_lnum.paragraphs[0].font.bold = True
    tf_lnum.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
    tf_lnum.paragraphs[0].alignment = PP_ALIGN.RIGHT
    
    # Linha contínua ANTES das fotos
    line1 = slide_ficha.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.5), Inches(2.0), Inches(7.77), Inches(2.0))
    line1.line.color.rgb = RGBColor(0, 0, 0)
    
    # Adicionar imagens do SharePoint
    adicionar_imagens_sharepoint(slide_ficha, word_files, image_files, sp_client, produto)
    
    # Linha contínua DEPOIS das fotos
    line2 = slide_ficha.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.5), Inches(5.5), Inches(7.77), Inches(5.5))
    line2.line.color.rgb = RGBColor(0, 0, 0)
    
    # Adicionar especificações do SharePoint
    adicionar_especificacoes_sharepoint(slide_ficha, word_files, sp_client, produto)
    
    # Criar slide de bula se disponível
    if bula_files:
        print(f"  📋 Criando slide de bula...")
        criar_slide_bula(prs, bula_files[0], lnum, sp_client)


def adicionar_imagens_sharepoint(slide, word_files, image_files, sp_client, produto=None):
    """Adiciona imagens do SharePoint ao slide"""
    try:
        # Primeiro tentar extrair imagens do Word
        imagens_word = []
        if word_files:
            download_url = word_files[0]['download_url']
            imagens_word = sp_client.get_word_images(download_url)
        
        # Adicionar imagens do Word (produto e ambiente)
        imagens_adicionadas = 0
        for i, img_data in enumerate(imagens_word[:2]):
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img:
                temp_img.write(img_data)
                temp_path = temp_img.name
            
            try:
                if i == 0:
                    # Primeira imagem (produto) - menor à esquerda
                    slide.shapes.add_picture(temp_path, Inches(1.0), Inches(2.3), height=Inches(2.5))
                    imagens_adicionadas += 1
                elif i == 1:
                    # Segunda imagem (ambiente) - maior à direita
                    slide.shapes.add_picture(temp_path, Inches(4.2), Inches(2.3), height=Inches(3.0))
                    imagens_adicionadas += 1
            finally:
                os.unlink(temp_path)
        
        # Se não tiver no Word, usar imagens separadas
        if not imagens_word and image_files:
            for i, img_file in enumerate(image_files[:2]):
                try:
                    img_content = sp_client.download_file_content(img_file['download_url'])
                    
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img:
                        temp_img.write(img_content)
                        temp_path = temp_img.name
                    
                    if i == 0:
                        slide.shapes.add_picture(temp_path, Inches(1.0), Inches(2.3), height=Inches(2.5))
                        imagens_adicionadas += 1
                    elif i == 1:
                        slide.shapes.add_picture(temp_path, Inches(4.2), Inches(2.3), height=Inches(3.0))
                        imagens_adicionadas += 1
                        
                finally:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
        
        # Se não adicionou nenhuma imagem e temos dados do produto, criar placeholders
        if imagens_adicionadas == 0 and produto:
            codigo = produto.get('codigo', '')
            ref = produto.get('ref', '') or produto.get('referencia', '')
            
            # Placeholder para imagem do produto (esquerda) - CÓDIGO DE REFERÊNCIA
            tx_img1 = slide.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(2.5), Inches(2.5))
            tf_img1 = tx_img1.text_frame
            tf_img1.text = f"REFERÊNCIA\n{ref if ref else 'N/A'}"
                
            tf_img1.vertical_anchor = MSO_ANCHOR.MIDDLE
            for p in tf_img1.paragraphs:
                p.font.name = 'Calibri'
                p.font.size = Pt(16)
                p.font.bold = True
                p.alignment = PP_ALIGN.CENTER
                
            # Borda para o placeholder
            tx_img1.line.color.rgb = RGBColor(100, 100, 100)
            tx_img1.line.width = Pt(1)
            tx_img1.fill.solid()
            tx_img1.fill.fore_color.rgb = RGBColor(245, 245, 245)
            
            # Placeholder para imagem de ambiente (direita) - CÓDIGO INTERNO
            tx_img2 = slide.shapes.add_textbox(Inches(4.2), Inches(2.3), Inches(2.5), Inches(3.0))
            tf_img2 = tx_img2.text_frame
            tf_img2.text = f"CÓDIGO INTERNO\n{codigo}"
                
            tf_img2.vertical_anchor = MSO_ANCHOR.MIDDLE
            for p in tf_img2.paragraphs:
                p.font.name = 'Calibri'
                p.font.size = Pt(14)
                p.font.bold = True
                p.alignment = PP_ALIGN.CENTER
                
            # Borda para o placeholder
            tx_img2.line.color.rgb = RGBColor(100, 100, 100)
            tx_img2.line.width = Pt(1)
            tx_img2.fill.solid()
            tx_img2.fill.fore_color.rgb = RGBColor(245, 245, 245)
            
            print(f"  [INFO] Adicionados placeholders - Ref: {ref if ref else 'N/A'} | Código Interno: {codigo}")
                        
    except Exception as e:
        print(f"  [ERRO] Erro ao adicionar imagens: {str(e)}")


def adicionar_especificacoes_sharepoint(slide, word_files, sp_client, produto=None):
    """Adiciona especificações técnicas do SharePoint ao slide"""
    try:
        if not word_files:
            # Se não encontrar arquivo Word, adicionar informações do produto
            if produto:
                codigo = produto.get('codigo', '')
                ref = produto.get('ref', '')
                descricao = produto.get('descricao', '')
                marca = produto.get('marca', '')
                
                # Priorizar referência sobre código interno
                if ref and ref != codigo:
                    texto_fallback = f"REFERÊNCIA: {ref}"
                    texto_fallback += f"\nCÓDIGO INTERNO: {codigo}"
                else:
                    texto_fallback = f"CÓDIGO ORÇAMENTO: {codigo}"
                    
                if marca:
                    texto_fallback += f"\nMARCA: {marca}"
                if descricao:
                    texto_fallback += f"\nDESCRIÇÃO: {descricao}"
                    
                texto_fallback += "\n\n[Ficha técnica não encontrada no SharePoint]"
                
                # Adicionar texto de fallback ao slide
                tx_txt = slide.shapes.add_textbox(Inches(0.5), Inches(5.8), Inches(7.27), Inches(5.0))
                tf_txt = tx_txt.text_frame
                tf_txt.word_wrap = True
                tf_txt.text = texto_fallback
                
                for p in tf_txt.paragraphs:
                    p.font.name = 'Calibri'
                    p.font.size = Pt(14)
                    p.font.bold = True if "CÓDIGO ORÇAMENTO" in p.text else False
                    
                print(f"  [INFO] Adicionado código de orçamento no slide: {ref if ref and ref != codigo else codigo}")
            return
        
        # Extrair texto do primeiro arquivo Word
        download_url = word_files[0]['download_url']
        texto_specs = sp_client.get_word_text(download_url)
        
        # Adicionar texto ao slide
        tx_txt = slide.shapes.add_textbox(Inches(0.5), Inches(5.8), Inches(7.27), Inches(5.0))
        tf_txt = tx_txt.text_frame
        tf_txt.word_wrap = True
        tf_txt.text = texto_specs
        
        for p in tf_txt.paragraphs:
            p.font.name = 'Calibri'
            p.font.size = Pt(14)
            
    except Exception as e:
        print(f"  [ERRO] Erro ao adicionar especificações: {str(e)}")


def criar_slide_bula(prs, bula_file, lnum, sp_client):
    """Cria slide dedicado para bula de instalação"""
    try:
        slide_bula = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Número LXX no canto superior direito em preto
        tx_lnum_bula = slide_bula.shapes.add_textbox(Inches(6.8), Inches(0.3), Inches(1), Inches(0.5))
        tf_lnum_bula = tx_lnum_bula.text_frame
        tf_lnum_bula.text = f"L{lnum}"
        tf_lnum_bula.paragraphs[0].font.name = 'Calibri'
        tf_lnum_bula.paragraphs[0].font.size = Pt(36)
        tf_lnum_bula.paragraphs[0].font.bold = True
        tf_lnum_bula.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
        tf_lnum_bula.paragraphs[0].alignment = PP_ALIGN.RIGHT
        
        # Baixar e adicionar imagem da bula
        img_content = sp_client.download_file_content(bula_file['download_url'])
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img:
            temp_img.write(img_content)
            temp_path = temp_img.name
        
        try:
            slide_bula.shapes.add_picture(temp_path, Inches(0.5), Inches(1.0), width=Inches(7.2), height=Inches(9.5))
        finally:
            os.unlink(temp_path)
            
    except Exception as e:
        print(f"  [ERRO] Erro ao criar slide bula: {str(e)}")


# Função main para compatibilidade com sistema existente
def main():
    """Função principal - chama geração com SharePoint"""
    try:
        # TODO: Estes caminhos serão passados dinamicamente pelo app.py
        xml_path = xml_orcamento  
        excel_path = excel_master  
        
        return gerar_powerpoint_sharepoint(xml_path, excel_path)
        
    except Exception as e:
        print(f"[ERRO] Erro na execução principal: {str(e)}")
        raise


# Extrai produtos (substituindo código antigo do PDF)
produtos = []  # Será preenchido pela função gerar_powerpoint_sharepoint()

prs = Presentation()
prs.slide_width = a4_width
prs.slide_height = a4_height

# Header barra preta pequena (apenas para o título, mais abaixo)
def add_header(slide):
    # Barra preta menor - largura reduzida e altura apenas para o título
    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.3), Inches(0.5), Inches(3.5), Inches(0.5))
    rect.fill.solid()
    rect.fill.fore_color.rgb = RGBColor(0, 0, 0)
    txbox = slide.shapes.add_textbox(Inches(0.4), Inches(0.6), Inches(3.3), Inches(0.3))
    tf = txbox.text_frame
    tf.text = "LUCENERA - ATELIER DA LUZ"
    tf.paragraphs[0].font.name = 'Calibri'
    tf.paragraphs[0].font.size = Pt(14)
    tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    tf.paragraphs[0].font.bold = True


# Executar quando chamado diretamente
if __name__ == "__main__":
    try:
        resultado = main()
        print(f"🎉 Processamento concluído: {resultado}")
    except Exception as e:
        print(f"💥 Falha na execução: {str(e)}")