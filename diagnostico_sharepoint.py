"""
Script de Diagnóstico SharePoint - Lucenera
Lista todos os arquivos na pasta de fichas técnicas para debug
"""

import sys
import os

# Adicionar diretório do projeto ao path
sys.path.insert(0, r'C:\script python\script python power point')

from sharepoint_client import SharePointClient

def diagnosticar_sharepoint():
    """Lista todos os arquivos no SharePoint para debug"""
    
    print("=" * 80)
    print("DIAGNÓSTICO SHAREPOINT - Fichas Técnicas")
    print("=" * 80)
    print()
    
    # Inicializar cliente
    sp_client = SharePointClient()
    print(f"[OK] SharePoint Client inicializado")
    print(f"[PASTA] {sp_client.PASTA_FICHAS_UNICA}")
    print()
    
    # Buscar arquivos de teste
    codigos_teste = ['9923', '13535', '8223', '9817', '8603', '9988', '13325']
    
    print("=" * 80)
    print("BUSCANDO CÓDIGOS ESPECÍFICOS")
    print("=" * 80)
    print()
    
    for codigo in codigos_teste:
        print(f"\n[TESTE] Buscando código: {codigo}")
        print("-" * 60)
        
        try:
            # Usar apenas o argumento codigo_interno (assinatura correta)
            arquivos = sp_client.search_files_by_code(codigo)
            
            if arquivos:
                print(f"[OK] {len(arquivos)} arquivo(s) encontrado(s):")
                for arq in arquivos:
                    print(f"  - {arq['name']} (score: {arq['score']}, método: {arq['match_method']})")
            else:
                print(f"[AVISO] Nenhum arquivo encontrado!")
                
        except Exception as e:
            print(f"[ERRO] {str(e)}")
    
    # Listar TODOS os arquivos da pasta para ver o que está lá
    print("\n\n" + "=" * 80)
    print("LISTANDO TODOS OS ARQUIVOS NA PASTA")
    print("=" * 80)
    print()
    
    try:
        # Fazer requisição direta COM PAGINAÇÃO
        search_endpoint = f"/drives/{sp_client.DRIVE_ID_FICHAS_TECNICAS}/root:/{sp_client.PASTA_FICHAS_UNICA}:/children"
        
        all_items = []
        next_link = search_endpoint
        page_count = 0
        
        print("[INFO] Carregando todos os arquivos (com paginação)...")
        print()
        
        while next_link:
            page_count += 1
            
            # Fazer requisição
            if page_count == 1:
                result = sp_client._make_graph_request(next_link)
            else:
                # nextLink já vem com URL completa
                if next_link.startswith('http'):
                    import urllib.parse
                    parsed = urllib.parse.urlparse(next_link)
                    path_and_query = parsed.path + ('?' + parsed.query if parsed.query else '')
                    if path_and_query.startswith('/v1.0'):
                        path_and_query = path_and_query[5:]
                    result = sp_client._make_graph_request(path_and_query)
                else:
                    result = sp_client._make_graph_request(next_link)
            
            # Adicionar itens desta página
            items = result.get('value', [])
            all_items.extend(items)
            
            print(f"[PAGINA {page_count}] {len(items)} itens carregados (total: {len(all_items)})")
            
            # Próxima página?
            next_link = result.get('@odata.nextLink')
        
        print()
        total_items = len(all_items)
        print(f"[OK] Total de itens na pasta: {total_items} (em {page_count} página(s))")
        print()
        
        # Filtrar só arquivos válidos
        EXTENSOES_VALIDAS = ['.docx', '.jpg', '.jpeg', '.png', '.pdf']
        arquivos_validos = []
        
        for item in all_items:
            nome = item.get("name", "")
            nome_lower = nome.lower()
            if any(nome_lower.endswith(ext) for ext in EXTENSOES_VALIDAS):
                arquivos_validos.append(nome)
        
        print(f"[INFO] Arquivos válidos (docx/jpg/png/pdf): {len(arquivos_validos)}")
        print()
        
        # Agrupar por código extraído
        print("ARQUIVOS AGRUPADOS POR CÓDIGO:")
        print("-" * 80)
        
        codigos_dict = {}
        for nome in sorted(arquivos_validos):
            nome_sem_ext = nome.rsplit('.', 1)[0]
            # Extrair código do início
            codigo_extraido = nome_sem_ext.split('_')[0].split(' ')[0].split('-')[0].strip()
            
            if codigo_extraido not in codigos_dict:
                codigos_dict[codigo_extraido] = []
            codigos_dict[codigo_extraido].append(nome)
        
        # Mostrar apenas códigos de teste primeiro
        print("\nCÓDIGOS DE TESTE:")
        for codigo in codigos_teste:
            if codigo in codigos_dict:
                print(f"\n[{codigo}] - {len(codigos_dict[codigo])} arquivo(s):")
                for arquivo in codigos_dict[codigo]:
                    print(f"  - {arquivo}")
            else:
                print(f"\n[{codigo}] - NÃO ENCONTRADO NA PASTA!")
        
        # Mostrar amostra de outros códigos (primeiros 20)
        print("\n\nOUTROS CÓDIGOS (amostra - primeiros 20):")
        outros_codigos = [c for c in sorted(codigos_dict.keys()) if c not in codigos_teste]
        for codigo in outros_codigos[:20]:
            arquivos = codigos_dict[codigo]
            print(f"\n[{codigo}] - {len(arquivos)} arquivo(s):")
            for arquivo in arquivos[:3]:  # Mostrar só 3 primeiros
                print(f"  - {arquivo}")
            if len(arquivos) > 3:
                print(f"  ... e mais {len(arquivos)-3}")
        
        if len(outros_codigos) > 20:
            print(f"\n... e mais {len(outros_codigos)-20} códigos")
            
    except Exception as e:
        print(f"[ERRO] Erro ao listar arquivos: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("FIM DO DIAGNÓSTICO")
    print("=" * 80)

if __name__ == "__main__":
    diagnosticar_sharepoint()
