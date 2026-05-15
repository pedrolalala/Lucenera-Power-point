"""
Módulo para parsing de orçamentos XML e consulta Excel master
Versão atualizada com suporte a variáveis de ambiente (.env), sistema avançado de referências e logging
"""

import xml.etree.ElementTree as ET
import pandas as pd
import os
import sys
import logging
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from reference_extractor import ReferenceExtractor

# Configurar encoding UTF-8 para console Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass  # Se falhar, usar print() normal

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logger para parsing XML
xml_logger = logging.getLogger('xml_parser')

class OrçamentoParser:
    """Parser para arquivos XML de orçamento"""
    
    def __init__(self, xml_path: str):
        self.xml_path = xml_path
        self.produtos = []
        
    def parse_xml(self) -> List[Dict]:
        """
        Parse do XML de orçamento
        
        Returns:
            Lista de produtos extraídos do XML
        """
        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
            
            produtos = []
            
            # Estrutura real do XML:
            # <connect_systems>
            #   <orcamento>
            #     <Item>
            #       <cod_produto>11261</cod_produto>
            #       <desc_produto>F.L. -  FITA LED...</desc_produto>
            #       <qtd_produto>1</qtd_produto>
            #       ...
            #     </Item>
            #   </orcamento>
            # </connect_systems>
            
            # Procurar elementos Item (note o 'I' maiúsculo)
            for item in root.findall(".//Item"):
                # DEBUG: Mostrar TODOS os campos do XML
                xml_logger.info(f"[DEBUG XML] Campos disponíveis no Item:")
                for child in item:
                    xml_logger.info(f"  - {child.tag}: {child.text}")
                
                # Extrair subelementos
                cod_produto = item.find('cod_produto')
                referencia = item.find('referencia')  # Campo de referência separado
                desc_produto = item.find('desc_produto') 
                qtd_produto = item.find('qtd_produto')
                preco_produto = item.find('preco_produto')
                desc_marca = item.find('desc_marca')  # Marca real do XML
                
                # Extrair código L (classificação/ambiente) - tentar vários nomes possíveis
                # IMPORTANTE: Tentar cada campo e logar para debug
                classificacao = None
                for campo in ['desc_classificacao', 'classificacao', 'desc_ambiente', 'ambiente', 'desc_local', 'local']:
                    temp = item.find(campo)
                    if temp is not None:
                        xml_logger.info(f"[DEBUG] Campo '{campo}' encontrado: {temp.text}")
                        if temp.text and temp.text.strip():  # Verificar se não está vazio
                            classificacao = temp
                            xml_logger.info(f"[DEBUG] Usando campo '{campo}' com valor: {temp.text}")
                            break
                        else:
                            xml_logger.info(f"[DEBUG] Campo '{campo}' está vazio, tentando próximo...")
                
                # DEBUG: Mostrar o que encontrou
                xml_logger.info(f"[DEBUG] classificacao final encontrado: {classificacao}")
                if classificacao is not None:
                    xml_logger.info(f"[DEBUG] classificacao.text final: {classificacao.text}")
                
                # Criar produto
                codigo_produto_text = cod_produto.text if cod_produto is not None else ""
                desc_marca_text = desc_marca.text if desc_marca is not None else ""
                desc_produto_text = desc_produto.text if desc_produto is not None else ""
                classificacao_text = classificacao.text if classificacao is not None and classificacao.text else ""
                
                # Extrair número L da classificação (ex: "L06" ou "06" → "06")
                lnum = self._extrair_codigo_l(classificacao_text)
                
                produto = {
                    "codigo": codigo_produto_text,
                    "descricao": desc_produto_text,
                    "quantidade": qtd_produto.text if qtd_produto is not None else "1",
                    "preco": preco_produto.text if preco_produto is not None else "0.00",
                    "ref": referencia.text if referencia is not None else codigo_produto_text,  # Usar referência real
                    "marca": desc_marca_text if desc_marca_text else self._determinar_marca(codigo_produto_text or ""),
                    "lnum": lnum  # Código L (classificação/ambiente)
                }
                
                # Log: Nome da empresa extraído do XML
                empresa_xml = desc_marca_text if desc_marca_text else self._determinar_marca(codigo_produto_text or "")
                xml_logger.info(f"Empresa extraída do XML para produto {codigo_produto_text}: '{empresa_xml}'")
                
                # Log: Código L extraído
                if classificacao_text:
                    xml_logger.info(f"[OK] Código L extraído: '{classificacao_text}' -> L{lnum} (Produto: {codigo_produto_text})")
                    print(f"[OK] Código L extraído: '{classificacao_text}' -> L{lnum} (Produto: {codigo_produto_text})")
                else:
                    xml_logger.warning(f"[AVISO] Nenhum código L encontrado para produto {codigo_produto_text}, usando default L{lnum}")
                    print(f"[AVISO] Nenhum código L encontrado para produto {codigo_produto_text}, usando default L{lnum}")
                
                produtos.append(produto)
                descricao_truncada = desc_produto_text[:50] if desc_produto_text else ""  
                print(f"[OK] Produto encontrado: {codigo_produto_text} - {descricao_truncada}...")
            
            self.produtos = produtos
            print(f"[OK] Total de produtos extraídos do XML: {len(produtos)}")
            return produtos
            
        except ET.ParseError as e:
            raise Exception(f"Erro ao fazer parse do XML: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro geral no parsing: {str(e)}")
    
    def _extrair_codigo_l(self, classificacao_text: str) -> str:
        """
        Extrai o código L da classificação/ambiente
        
        Args:
            classificacao_text: Texto da classificação (ex: "L06", "06", "L48")
            
        Returns:
            Código L formatado (ex: "06", "48") ou "01" se não encontrado
        """
        import re
        
        if not classificacao_text:
            return "01"  # Default
        
        # Remover espaços
        texto = classificacao_text.strip().upper()
        
        # Padrão 1: "L06", "L48" → extrair "06", "48"
        match = re.search(r'L(\d+)', texto)
        if match:
            return match.group(1).zfill(2)  # Garantir 2 dígitos
        
        # Padrão 2: Apenas números "06", "6", "48" → usar direto
        match = re.search(r'(\d+)', texto)
        if match:
            return match.group(1).zfill(2)
        
        return "01"  # Fallback
    
    def _determinar_marca(self, codigo_ref: str) -> str:
        """
        Determina a marca baseada no código de referência
        
        Args:
            codigo_ref: Código de referência do produto
            
        Returns:
            Nome da marca estimada
        """
        # Lógica básica de mapeamento (será refinada com Excel master)
        codigo_upper = codigo_ref.upper()
        
        # Mapeamentos conhecidos (refinados com dados reais)
        if "AB" in codigo_upper or "FE" in codigo_upper:
            return "Interlight"
        elif "BL" in codigo_upper:
            return "Bella Luce"
        elif "JL" in codigo_upper:
            return "Jean Lux"
        elif "DL" in codigo_upper:
            return "Direct Light"
        else:
            return "Interlight"  # Default


class ExcelMaster:
    """Gerenciador do Excel master com códigos de produtos"""
    
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.df = None
        self._mapeamento_ref_codigo = None  # Cache do mapeamento referência → código
        self.reference_extractor = ReferenceExtractor()  # Sistema avançado
        self._load_excel()
    
    @staticmethod
    def _is_file_locked(filepath):
        """Verifica se um arquivo está sendo usado por outro processo"""
        try:
            with open(filepath, 'r+b'):
                return False  # Arquivo não está bloqueado
        except (IOError, OSError):
            return True  # Arquivo está bloqueado ou não existe
    
    def _load_excel(self):
        """Carrega o Excel master com retry logic para problemas de permissão"""
        import time
        import os
        from pathlib import Path
        
        # Verificar se existe arquivo local primeiro (backup rápido para OneDrive)
        local_path = Path(__file__).parent / "master_produtos_local.xlsx"
        if local_path.exists() and not self._is_file_locked(str(local_path)):
            try:
                self.df = pd.read_excel(local_path, engine='openpyxl')
                self.excel_path = str(local_path)
                print(f"[OK] Excel local carregado: {local_path}")
                return
            except Exception as e:
                print(f"[AVISO] Falha ao carregar Excel local: {e}")
        
        max_attempts = 5
        retry_delay = 1  # segundos
        
        for attempt in range(max_attempts):
            try:
                # Verificar se arquivo existe
                if not os.path.exists(self.excel_path):
                    self._criar_excel_master_default()
                    return
                
                # Verificar se arquivo está acessível
                if self._is_file_locked(self.excel_path):
                    if attempt < max_attempts - 1:
                        print(f"[AVISO] Tentativa {attempt + 1}/{max_attempts}: Arquivo bloqueado, aguardando {retry_delay}s...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Backoff exponencial
                        continue
                    else:
                        print("[AVISO] Arquivo permanece bloqueado, tentando backup local...")
                        self._criar_backup_local()
                        return
                
                # Tentar carregar Excel
                possible_sheets = ['Sheet1', 'Produtos', 'Master', 'Códigos', 'Ref']
                
                for sheet in possible_sheets:
                    try:
                        # Usar engine openpyxl para melhor compatibilidade
                        self.df = pd.read_excel(self.excel_path, sheet_name=sheet, engine='openpyxl')
                        print(f"[OK] Excel carregado com sucesso (sheet: {sheet})")
                        return
                    except:
                        continue
                
                if self.df is None:
                    # Se não encontrou sheet específico, usa o primeiro
                    self.df = pd.read_excel(self.excel_path, engine='openpyxl')
                    print(f"[OK] Excel carregado (primeiro sheet)")
                    
                return  # Sucesso
                
            except PermissionError as pe:
                if attempt < max_attempts - 1:
                    print(f"[AVISO] Tentativa {attempt + 1}/{max_attempts}: {str(pe)}")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"[ERRO] Falha após {max_attempts} tentativas. Criando backup local...")
                    self._criar_backup_local()
                    
            except Exception as e:
                if attempt < max_attempts - 1:
                    print(f"[AVISO] Erro na tentativa {attempt + 1}: {str(e)}")
                    time.sleep(retry_delay)
                else:
                    raise Exception(f"Erro ao carregar Excel após {max_attempts} tentativas: {str(e)}")
    
    def _criar_excel_master_default(self):
        """Cria um Excel master padrão se não existir"""
        import pandas as pd
        from pathlib import Path
        
        try:
            # Dados de exemplo para iluminação
            dados_exemplo = {
                'codigo_interno': ['INT001', 'INT002', 'INT003', 'INT004', 'INT005'],
                'referencia': ['REF001', 'REF002', 'REF003', 'REF004', 'REF005'],
                'descricao': ['Luminária LED 10W', 'Spot Direcionável', 'Fita LED 5m', 'Controlador RGB', 'Fonte 12V 5A'],
                'preco': [45.50, 78.90, 125.00, 89.90, 67.80],
                'categoria': ['Iluminação', 'Spots', 'Fitas LED', 'Controladores', 'Fontes']
            }
            
            self.df = pd.DataFrame(dados_exemplo)
            
            # Salvar em arquivo local
            local_path = Path(__file__).parent / "master_produtos_local.xlsx"
            self.df.to_excel(local_path, index=False, engine='openpyxl')
            self.excel_path = str(local_path)
            print(f"[OK] Excel master criado localmente: {local_path}")
            
        except Exception as e:
            print(f"[ERRO] Falha ao criar Excel master: {e}")
            # Usar dados em memória apenas
            self.df = pd.DataFrame({
                'codigo_interno': ['INT001'],
                'referencia': ['REF001'], 
                'descricao': ['Produto Padrão'],
                'preco': [100.0]
            })
            print("[OK] Usando dados em memória")
    
    def _criar_backup_local(self):
        """Cria uma cópia local do arquivo para contornar problemas do OneDrive"""
        import shutil
        from pathlib import Path
        
        try:
            # Verificar se já existe Excel local
            local_path = Path(__file__).parent / "master_produtos_local.xlsx"
            
            if local_path.exists():
                print(f"[OK] Usando Excel local existente: {local_path}")
                self.excel_path = str(local_path)
                self.df = pd.read_excel(local_path, engine='openpyxl')
                return
            
            # Se arquivo original existir, tentar copiar
            if os.path.exists(self.excel_path):
                print("[INFO] Tentando copiar Excel do OneDrive...")
                shutil.copy2(self.excel_path, local_path)
                self.excel_path = str(local_path)
                print(f"[OK] Backup criado: {local_path}")
                
                # Carregar backup
                self.df = pd.read_excel(local_path, engine='openpyxl')
            else:
                # Criar novo arquivo local
                print("[INFO] Criando Excel master local...")
                self._criar_excel_master_default()
                
        except Exception as e:
            print(f"[ERRO] Falha no backup: {e}")
            self._criar_excel_master_default()
    
    def buscar_produto_por_codigo(self, codigo: str) -> Optional[Dict]:
        """
        Busca produto no Excel master por código
        
        Args:
            codigo: Código do produto (interno ou referência)
            
        Returns:
            Informações do produto encontrado (incluindo categoria)
        """
        if self.df is None:
            return None
        
        try:
            # Detectar nome das colunas (case-insensitive)
            col_codigo = None
            col_ref = None
            col_marca = None
            col_desc = None
            col_categoria = None
            
            for col in self.df.columns:
                col_lower = col.lower()
                if 'codproduto' in col_lower or 'codigo' in col_lower:
                    col_codigo = col
                elif 'referencia' in col_lower or 'ref' in col_lower:
                    col_ref = col
                elif 'marca' in col_lower or 'descmarca' in col_lower:
                    col_marca = col
                elif 'descproduto' in col_lower or 'descricao' in col_lower:
                    col_desc = col
                elif 'desccategoria' in col_lower or 'categoria' in col_lower:
                    col_categoria = col
            
            # Buscar por código
            if col_codigo:
                resultado = self.df[self.df[col_codigo].astype(str) == str(codigo)]
                
                if not resultado.empty:
                    produto = resultado.iloc[0]
                    return {
                        "codigo": str(produto.get(col_codigo, '')) if col_codigo else '',
                        "ref": str(produto.get(col_ref, '')) if col_ref and pd.notna(produto.get(col_ref)) else '',
                        "marca": str(produto.get(col_marca, '')) if col_marca and pd.notna(produto.get(col_marca)) else '',
                        "nome": str(produto.get(col_desc, '')) if col_desc and pd.notna(produto.get(col_desc)) else '',
                        "categoria": str(produto.get(col_categoria, '')) if col_categoria and pd.notna(produto.get(col_categoria)) else '',
                        "ficha_tecnica": produto.get('ficha_tecnica', ''),
                        "manual_instalacao": produto.get('manual_instalacao', '')
                    }
            
            # Buscar por referência
            if col_ref:
                resultado = self.df[self.df[col_ref].astype(str).str.upper() == str(codigo).upper()]
                
                if not resultado.empty:
                    produto = resultado.iloc[0]
                    return {
                        "codigo": str(produto.get(col_codigo, '')) if col_codigo else '',
                        "ref": str(produto.get(col_ref, '')) if col_ref and pd.notna(produto.get(col_ref)) else '',
                        "marca": str(produto.get(col_marca, '')) if col_marca and pd.notna(produto.get(col_marca)) else '',
                        "nome": str(produto.get(col_desc, '')) if col_desc and pd.notna(produto.get(col_desc)) else '',
                        "categoria": str(produto.get(col_categoria, '')) if col_categoria and pd.notna(produto.get(col_categoria)) else '',
                        "ficha_tecnica": produto.get('ficha_tecnica', ''),
                        "manual_instalacao": produto.get('manual_instalacao', '')
                    }
            
            return None
            
        except Exception as e:
            print(f"[ERRO] Erro ao buscar produto {codigo}: {str(e)}")
            return None
    
    def buscar_marca_por_codigo(self, codigo: str) -> Optional[str]:
        """
        Busca marca/fabricante por código do produto
        
        Args:
            codigo: Código do produto (interno ou referência)
            
        Returns:
            Nome da marca/fabricante ou None se não encontrado
        """
        produto = self.buscar_produto_por_codigo(codigo)
        if produto and produto.get('marca'):
            return produto['marca']
        
        # Fallback: tentar busca direta na coluna marca
        if self.df is not None:
            try:
                colunas_codigo = ['codigo', 'codigo_interno', 'ref', 'referencia']
                colunas_marca = ['marca', 'fabricante', 'brand', 'manufacturer']
                
                for col_cod in colunas_codigo:
                    if col_cod.lower() in [c.lower() for c in self.df.columns]:
                        resultado = self.df[self.df[col_cod].astype(str).str.upper() == codigo.upper()]
                        
                        if not resultado.empty:
                            for col_marca in colunas_marca:
                                if col_marca.lower() in [c.lower() for c in self.df.columns]:
                                    marca = resultado.iloc[0][col_marca]
                                    if pd.notna(marca):
                                        return str(marca).strip()
            except Exception as e:
                print(f"[AVISO] Erro ao buscar marca para {codigo}: {str(e)}")
        
        return None
    
    def listar_marcas(self) -> List[str]:
        """Lista todas as marcas disponíveis no Excel"""
        if self.df is None:
            return []
        
        colunas_marca = ['marca', 'brand', 'manufacturer']
        
        for coluna in colunas_marca:
            if coluna.lower() in [c.lower() for c in self.df.columns]:
                marcas = self.df[coluna].dropna().unique().tolist()
                return sorted([str(marca) for marca in marcas])
        
        return []
    
    def estatisticas(self) -> Dict:
        """Retorna estatísticas do Excel master"""
        if self.df is None:
            return {}
        
        return {
            "total_produtos": len(self.df),
            "colunas": list(self.df.columns),
            "marcas_unicas": len(self.listar_marcas()),
            "linhas_vazias": self.df.isnull().sum().sum()
        }
    
    def construir_mapeamento_referencias(self) -> Dict[str, str]:
        """
        Constrói mapeamento completo: referência → código interno
        Usa sistema avançado para múltiplas variações de referência
        
        Returns:
            Dicionário {referencia: codigo_interno}
        """
        if self.df is None:
            return {}
        
        if self._mapeamento_ref_codigo is not None:
            return self._mapeamento_ref_codigo  # Cache
        
        mapeamento = {}
        
        # Detectar colunas relevantes
        colunas_ref = self._detectar_colunas_referencia()
        colunas_codigo = self._detectar_colunas_codigo()
        
        print(f"[MAPPING] Construindo mapeamento com {len(self.df)} produtos...")
        print(f"[MAPPING] Colunas referência: {colunas_ref}")
        print(f"[MAPPING] Colunas código: {colunas_codigo}")
        
        for index, row in self.df.iterrows():
            # Extrair código interno
            codigo_interno = None
            for col_cod in colunas_codigo:
                if pd.notna(row[col_cod]):
                    codigo_interno = str(row[col_cod]).strip()
                    break
            
            if not codigo_interno:
                continue
            
            # Extrair referências
            referencias = set()
            for col_ref in colunas_ref:
                if pd.notna(row[col_ref]):
                    ref_original = str(row[col_ref]).strip()
                    if ref_original:
                        referencias.add(ref_original)
                        
                        # Gerar variações usando sistema avançado
                        variacoes = self._gerar_variacoes_referencia(ref_original)
                        referencias.update(variacoes)
            
            # Adicionar ao mapeamento
            for ref in referencias:
                if ref:
                    mapeamento[ref] = codigo_interno
        
        self._mapeamento_ref_codigo = mapeamento
        
        print(f"[MAPPING] Mapeamento construído: {len(mapeamento)} entradas")
        return mapeamento
    
    def buscar_codigo_por_referencia_avancada(self, referencia: str) -> Tuple[Optional[str], str]:
        """
        Busca código interno usando extração avançada de referência
        
        Args:
            referencia: Referência do produto
            
        Returns:
            Tuple (codigo_interno, método_usado)
        """
        mapeamento = self.construir_mapeamento_referencias()
        
        if not referencia or not mapeamento:
            return None, "dados_inválidos"
        
        # Usar sistema avançado de busca
        return self.reference_extractor.buscar_codigo_inteligente(referencia, mapeamento)
    
    def _detectar_colunas_referencia(self) -> List[str]:
        """Detecta colunas que contêm códigos de referência"""
        if self.df is None:
            return []
        
        candidatos = ['ref', 'referencia', 'reference', 'codigo_ref', 'ref_fabricante', 'part_number']
        colunas_encontradas = []
        
        for col in self.df.columns:
            col_lower = col.lower()
            if any(candidato in col_lower for candidato in candidatos):
                colunas_encontradas.append(col)
        
        return colunas_encontradas
    
    def _detectar_colunas_codigo(self) -> List[str]:
        """Detecta colunas que contêm códigos internos"""
        if self.df is None:
            return []
        
        candidatos = ['codigo', 'code', 'codigo_interno', 'internal_code', 'id']
        colunas_encontradas = []
        
        for col in self.df.columns:
            col_lower = col.lower()
            if any(candidato in col_lower for candidato in candidatos):
                colunas_encontradas.append(col)
        
        return colunas_encontradas
    
    def _gerar_variacoes_referencia(self, referencia: str) -> List[str]:
        """
        Gera variações de uma referência para melhorar matching
        
        Args:
            referencia: Referência original
            
        Returns:
            Lista de variações possíveis
        """
        variacoes = set()
        ref = referencia.strip()
        
        # Variações de normalização  
        variacoes.add(ref.replace('-', ' '))     # "091-ACS" → "091 ACS"
        variacoes.add(ref.replace(' ', '-'))     # "091 ACS" → "091-ACS"
        variacoes.add(ref.replace('-', ''))      # "091-ACS" → "091ACS"
        variacoes.add(ref.replace(' ', ''))      # "091 ACS" → "091ACS"
        
        # Variações case
        variacoes.add(ref.upper())
        variacoes.add(ref.lower())
        variacoes.add(ref.title())
        
        # Remover variação vazia ou idêntica
        variacoes.discard('')
        variacoes.discard(ref)
        
        return list(variacoes)


# Classe integradora
class DataManager:
    """Gerencia integração entre XML, Excel e SharePoint"""
    
    def __init__(self, xml_path: str, excel_path: Optional[str] = None):
        """
        Inicializa DataManager
        
        Args:
            xml_path: Caminho para arquivo XML de orçamento
            excel_path: Caminho para Excel master (opcional, carrega do .env se não fornecido)
        """
        self.orcamento_parser = OrçamentoParser(xml_path)
        
        # Usar caminho fornecido ou carregar do .env
        if excel_path is None:
            excel_path = os.getenv('EXCEL_MASTER_PATH')
            if excel_path is None:
                # Caminho padrão se não estiver no .env
                excel_path = "C:/Users/pedro/OneDrive/Desktop/lucenera/master_produtos.xlsx"
                print(f"[AVISO] EXCEL_MASTER_PATH não definido no .env, usando padrão: {excel_path}")
        
        if not os.path.exists(excel_path):
            raise FileNotFoundError(
                f"Excel master não encontrado: {excel_path}\n"
                f"Execute: python criar_excel_template.py"
            )
        
        self.excel_master = ExcelMaster(excel_path)
        print(f"[OK] DataManager configurado com Excel: {excel_path}")
        
    def processar_orcamento(self) -> List[Dict]:
        """
        Processa orçamento completo integrando todas as fontes e agrupando por código L
        
        Returns:
            Lista de grupos por código L, cada um com:
            {
                'lnum': 'LXX',
                'mandante': {...},  # Produto LUMINARIA
                'componentes': [...] # Outros produtos (LED, ACESSORIO, etc.)
            }
        """
        # Parse do XML
        produtos_xml = self.orcamento_parser.parse_xml()
        
        print(f"[AGRUPAMENTO] Iniciando agrupamento de {len(produtos_xml)} produtos por código L...")
        
        # Enriquecer cada produto com dados do Excel
        produtos_enriquecidos = []
        
        for produto in produtos_xml:
            # Buscar no Excel master
            info_excel = self.excel_master.buscar_produto_por_codigo(produto.get('codigo', ''))
            
            if not info_excel:
                # Tentar buscar por referência
                info_excel = self.excel_master.buscar_produto_por_codigo(produto.get('ref', ''))
            
            # Combinar dados
            produto_final = {
                **produto,  # Dados do XML
                "marca": info_excel.get('marca', produto.get('marca', 'Interlight')) if info_excel else produto.get('marca', 'Interlight'),
                "nome_produto": info_excel.get('nome', '') if info_excel else '',
                "categoria": info_excel.get('categoria', '') if info_excel else '',
                "excel_encontrado": bool(info_excel)
            }
            
            produtos_enriquecidos.append(produto_final)
        
        # Agrupar por código L
        grupos = self._agrupar_por_lnum(produtos_enriquecidos)
        
        print(f"[AGRUPAMENTO] {len(grupos)} grupos criados")
        
        return grupos
    
    def _agrupar_por_lnum(self, produtos: List[Dict]) -> List[Dict]:
        """
        Agrupa produtos pelo código L e identifica o item mandante (LUMINARIA)
        
        Args:
            produtos: Lista de produtos enriquecidos
            
        Returns:
            Lista de grupos: [{'lnum': 'L01', 'mandante': {...}, 'componentes': [...]}]
        """
        from collections import defaultdict
        
        # Agrupar por lnum
        grupos_dict = defaultdict(list)
        
        for produto in produtos:
            lnum = produto.get('lnum', '01')
            grupos_dict[lnum].append(produto)
        
        # Criar estrutura de grupos com mandante
        grupos_finais = []
        
        for lnum, produtos_grupo in sorted(grupos_dict.items()):
            print(f"\n[GRUPO L{lnum}] {len(produtos_grupo)} produto(s)")
            
            # Identificar mandante (categoria LUMINARIA)
            mandante = None
            componentes = []
            
            for produto in produtos_grupo:
                categoria = produto.get('categoria', '').upper()
                print(f"  - {produto.get('codigo', '?')}: {categoria or 'SEM CATEGORIA'}")
                
                if 'LUMINARIA' in categoria or 'LUMINÁRIA' in categoria:
                    if mandante is None:
                        mandante = produto
                        print(f"    [OK] MANDANTE identificado")
                    else:
                        # Se já tem mandante, este vira componente
                        componentes.append(produto)
                        print(f"    -> Componente adicional")
                else:
                    componentes.append(produto)
                    print(f"    -> Componente")
            
            # Se não encontrou mandante, usar o primeiro produto
            if mandante is None and produtos_grupo:
                mandante = produtos_grupo[0]
                componentes = produtos_grupo[1:]
                print(f"  [AVISO] Nenhuma LUMINARIA encontrada, usando primeiro item como mandante")
            
            # Criar estrutura do grupo
            grupo = {
                'lnum': lnum,
                'mandante': mandante,
                'componentes': componentes,
                'total_produtos': len(produtos_grupo)
            }
            
            grupos_finais.append(grupo)
        
        return grupos_finais


# Exemplo de uso
if __name__ == "__main__":
    # Teste básico
    print("🧪 Testando módulo de dados...")
    
    # Exemplo de estrutura XML que esperamos
    xml_exemplo = """<?xml version="1.0" encoding="UTF-8"?>
    <orcamento>
        <item linha="43" codigo="10289" ref="3649-AB-S-PX" preco="655.39" quantidade="57"/>
        <item linha="44" codigo="10539" ref="3649-FE-S-PX" preco="872.00" quantidade="30"/>
    </orcamento>"""
    
    print("[XML] Estrutura XML esperada:")
    print(xml_exemplo)