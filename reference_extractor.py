"""
Módulo para extração inteligente de códigos de referência
Implementa regras avançadas de limpeza e mapeamento de códigos
"""

import re
from typing import Dict, List, Optional, Tuple
import pandas as pd

class ReferenceExtractor:
    """
    Extrator inteligente de códigos de referência com múltiplas estratégias de busca
    """
    
    def __init__(self):
        """Inicializa com prefixos configurados por empresa"""
        
        # Prefixos organizados por empresa
        self.prefixos_por_empresa = {
            "INTERLIGHT": ["INTERLIGHT -", "INTERLIGHT-", "BULA -", "Bula -", "BULA", "Bula"],
            "ILUMINAR": ["ILUMINAR - ", "ILUMINAR -", "ILUMINAR-", "BULA -", "Bula -", "BULA", "Bula"],
            "EVOLED": ["EVL - ", "EVL-", "EVOLED -", "EVOLED-"],
            "STELLATECH": ["STELLA - ", "STELLA-", "STELLATECH - ", "STELLATECH-", "BULA - ", "BULA -", "BULA", "Bula -", "Bula"],
            "DRESSALL": ["DressALL_", "DressALL ", "DRESSALL_", "DRESSALL ", "DRESSALL-", "Dress "],
            "DESSINE": ["DESSINE - ", "DESSINE-", "BULA - ", "BULA -", "BULA", "Bula -", "Bula", "Manual ", "Oscar-"],
            "EKLART": ["EKLART - ", "EKLART-", "Bula_", "Bula ", "BULA - ", "BULA-", "BULA", "Bula -", "Bula"],
            "ALPERTONE": ["ALPERTONE - ", "ALPERTONE-", "BULA DE INSTALAÇÃO - ", "BULA DE INSTALAÇÃO-", "BULA - ", "BULA-", "BULA", "Bula -", "Bula"],
            "REAL LUSTRES - RLT": ["REAL LUSTRES - ", "REAL LUSTRES -", "REAL LUSTRES-", "RLT - ", "RLT-", "BULA - ", "BULA-", "BULA", "Bula -", "Bula"],
            "ALLOY": ["ALLOY - ", "ALLOY-", "BULA - ", "BULA-", "BULA", "Bula -", "Bula"],
            "ACEND": ["ACEND - ", "ACEND -", "ACEND-", "MANUAL_PS_", "BULA - ", "BULA-", "BULA", "Bula -", "Bula"],
            "DIRECTLIGHT": ["DIRECTLIGHT - ", "DIRECTLIGHT -", "DIRECTLIGHT-", "DIRECTLIGHT ", "Manual ", "BULA - ", "BULA-", "BULA", "Bula -", "Bula"],
            "LEDVANCE": ["LEDVANCE - ", "LEDVANCE-", "Manual de instalação- LEDVANCE ", "Manual de instalação - LEDVANCE ", "BULA - ", "BULA-", "BULA", "Bula -", "Bula"]
        }
        
        # Lista unificada de todos os prefixos (ordenados por tamanho decrescente para evitar conflicts)
        self.todos_prefixos = []
        for empresa, prefixos in self.prefixos_por_empresa.items():
            self.todos_prefixos.extend(prefixos)
        
        # Ordenar por tamanho (maiores primeiro) para evitar match parcial
        self.todos_prefixos = sorted(set(self.todos_prefixos), key=len, reverse=True)
        
        print(f"[OK] ReferenceExtractor inicializado com {len(self.todos_prefixos)} prefixos de {len(self.prefixos_por_empresa)} empresas")
    
    def extrair_referencia_do_arquivo(self, nome_arquivo: str) -> Optional[str]:
        """
        Extrai código de referência limpo do nome do arquivo
        
        Args:
            nome_arquivo: Nome do arquivo (ex: "INTERLIGHT - 091-ACS.pdf")
            
        Returns:
            Código de referência extraído (ex: "091-ACS") ou None se não encontrar
        """
        # 1. Remover extensão
        nome_base = self._remover_extensao(nome_arquivo)
        
        # 2. Tentar remover prefixos (case-insensitive)
        referencia = self._remover_prefixos(nome_base)
        
        if referencia:
            # 3. Limpeza adicional
            referencia = referencia.strip()
            print(f"[EXTRACT] '{nome_arquivo}' → '{referencia}'")
            return referencia
        
        print(f"[SKIP] Nenhum prefixo encontrado em: '{nome_arquivo}'")
        return None
    
    def buscar_codigo_inteligente(self, referencia: str, mapeamento: Dict[str, str]) -> Tuple[Optional[str], str]:
        """
        Busca código interno usando 6 estratégias inteligentes
        
        Args:
            referencia: Código de referência extraído 
            mapeamento: Dicionário {referencia: codigo_interno} da planilha
            
        Returns:
            Tuple (codigo_interno, método_usado) ou (None, "não_encontrado")
        """
        if not referencia or not mapeamento:
            return None, "dados_inválidos"
        
        # Estratégia 1: Busca Exata
        if referencia in mapeamento:
            return mapeamento[referencia], f"exata: {referencia}"
        
        # Estratégia 2: Normalização (espaços/hífens)
        resultado = self._busca_normalizada(referencia, mapeamento)
        if resultado[0]:
            return resultado
        
        # Estratégia 3: Extração de Números (4-5 dígitos)
        resultado = self._busca_numeros_4_5_dig(referencia, mapeamento)
        if resultado[0]:
            return resultado
        
        # Estratégia 4: Remoção de Sufixos
        resultado = self._busca_sem_sufixos(referencia, mapeamento)
        if resultado[0]:
            return resultado
        
        # Estratégia 5: Truncamento (primeiros 4 dígitos)
        resultado = self._busca_truncada(referencia, mapeamento)
        if resultado[0]:
            return resultado
        
        # Estratégia 6: Busca por Prefixo
        resultado = self._busca_prefixo(referencia, mapeamento)
        if resultado[0]:
            return resultado
        
        return None, f"não_encontrado_após_6_estratégias: {referencia}"
    
    def _remover_extensao(self, nome_arquivo: str) -> str:
        """Remove extensão do arquivo"""
        if '.' in nome_arquivo:
            return nome_arquivo.rsplit('.', 1)[0]
        return nome_arquivo
    
    def _remover_prefixos(self, nome_base: str) -> Optional[str]:
        """Remove prefixos conhecidos (case-insensitive)"""
        nome_upper = nome_base.upper()
        
        # Tentar cada prefixo
        for prefixo in self.todos_prefixos:
            if nome_upper.startswith(prefixo.upper()):
                # Remover prefixo mantendo case original
                referencia = nome_base[len(prefixo):].strip()
                if referencia:  # Se sobrou algo após remoção
                    return referencia
        
        return None
    
    def _busca_normalizada(self, referencia: str, mapeamento: Dict[str, str]) -> Tuple[Optional[str], str]:
        """Estratégia 2: Normalização de espaços e hífens"""
        
        # Variações para testar
        variações = [
            referencia.replace('-', ' '),    # "091-ACS" → "091 ACS"  
            referencia.replace(' ', '-'),    # "091 ACS" → "091-ACS"
            referencia.replace('-', ''),     # "091-ACS" → "091ACS"
            referencia.replace(' ', ''),     # "091 ACS" → "091ACS"
        ]
        
        for var in variações:
            if var != referencia and var in mapeamento:
                return mapeamento[var], f"normalizada: {referencia} → {var}"
        
        return None, ""
    
    def _busca_numeros_4_5_dig(self, referencia: str, mapeamento: Dict[str, str]) -> Tuple[Optional[str], str]:
        """Estratégia 3: Extração de números de 4-5 dígitos"""
        
        # Encontrar números de 4-5 dígitos
        numeros = re.findall(r'\b\d{4,5}\b', referencia)
        
        for num in numeros:
            # Tentar número original
            if num in mapeamento:
                return mapeamento[num], f"número_extraído: {referencia} → {num}"
            
            # Se for 4 dígitos, tentar com "1" na frente
            if len(num) == 4:
                num_com_1 = "1" + num
                if num_com_1 in mapeamento:
                    return mapeamento[num_com_1], f"número_4dig_+1: {referencia} → {num_com_1}"
        
        return None, ""
    
    def _busca_sem_sufixos(self, referencia: str, mapeamento: Dict[str, str]) -> Tuple[Optional[str], str]:
        """Estratégia 4: Remoção de sufixos por separadores"""
        
        # Dividir por separadores comuns
        partes = re.split(r'[-_\s.]+', referencia)
        
        for parte in partes:
            # Tentar partes que são números de 4+ dígitos
            if re.match(r'^\d{4,}$', parte):
                if parte in mapeamento:
                    return mapeamento[parte], f"sufixos_removidos: {referencia} → {parte}"
                
                # Se for 4 dígitos, tentar com "1"
                if len(parte) == 4:
                    parte_com_1 = "1" + parte
                    if parte_com_1 in mapeamento:
                        return mapeamento[parte_com_1], f"sufixos_removidos_+1: {referencia} → {parte_com_1}"
        
        return None, ""
    
    def _busca_truncada(self, referencia: str, mapeamento: Dict[str, str]) -> Tuple[Optional[str], str]:
        """Estratégia 5: Truncamento (primeiros 4 dígitos)"""
        
        # Extrair primeiros 4 dígitos
        match = re.search(r'\d{4}', referencia)
        if match:
            num_4 = match.group()
            
            # Tentar número truncado
            if num_4 in mapeamento:
                return mapeamento[num_4], f"truncado_4dig: {referencia} → {num_4}"
            
            # Tentar com "1" na frente
            num_4_com_1 = "1" + num_4
            if num_4_com_1 in mapeamento:
                return mapeamento[num_4_com_1], f"truncado_4dig_+1: {referencia} → {num_4_com_1}"
        
        return None, ""
    
    def _busca_prefixo(self, referencia: str, mapeamento: Dict[str, str]) -> Tuple[Optional[str], str]:
        """Estratégia 6: Busca por prefixo (arquivo truncado, Excel completo)"""
        
        # Buscar chaves que começam com a referência
        for chave_excel in mapeamento.keys():
            if chave_excel.startswith(referencia):
                return mapeamento[chave_excel], f"prefixo_expandido: {referencia} → {chave_excel}"
        
        return None, ""
    
    def get_empresas_configuradas(self) -> List[str]:
        """Retorna lista de empresas configuradas"""
        return list(self.prefixos_por_empresa.keys())
    
    def get_prefixos_empresa(self, empresa: str) -> List[str]:
        """Retorna prefixos de uma empresa específica"""
        return self.prefixos_por_empresa.get(empresa, [])
    
    def get_estatisticas(self) -> Dict:
        """Retorna estatísticas do extrator"""
        total_empresas = len(self.prefixos_por_empresa)
        total_prefixos = len(self.todos_prefixos)
        
        by_empresa = {emp: len(prefs) for emp, prefs in self.prefixos_por_empresa.items()}
        
        return {
            "total_empresas": total_empresas,
            "total_prefixos": total_prefixos,
            "prefixos_por_empresa": by_empresa,
            "empresa_com_mais_prefixos": max(by_empresa.keys(), key=lambda k: by_empresa[k]),
            "max_prefixos": max(by_empresa.values())
        }

# Função de conveniência para usar fora da classe
def extrair_e_buscar_codigo(nome_arquivo: str, mapeamento_excel: Dict[str, str]) -> Tuple[Optional[str], str]:
    """
    Função de conveniência para extrair referência e buscar código em uma chamada
    
    Args:
        nome_arquivo: Nome do arquivo do SharePoint
        mapeamento_excel: Dicionário da planilha {referencia: codigo_interno}
        
    Returns:
        Tuple (codigo_interno, detalhes_processo) ou (None, erro)
    """
    extrator = ReferenceExtractor()
    
    # 1. Extrair referência
    referencia = extrator.extrair_referencia_do_arquivo(nome_arquivo)
    if not referencia:
        return None, f"prefixo_não_encontrado: {nome_arquivo}"
    
    # 2. Buscar código
    codigo, metodo = extrator.buscar_codigo_inteligente(referencia, mapeamento_excel)
    
    return codigo, f"{metodo} (ref: {referencia})"

if __name__ == "__main__":
    # Teste rápido
    extrator = ReferenceExtractor()
    
    print("\n=== TESTE REFERENCE EXTRACTOR ===")
    
    # Teste de extração
    arquivos_teste = [
        "INTERLIGHT - 091-ACS.pdf",
        "EKLART - EKF5196HL9068L.docx", 
        "Bula - 3041-S.pdf",
        "STELLA-AB123.jpg",
        "ACEND - MANUAL_PS_4991.pdf"
    ]
    
    for arquivo in arquivos_teste:
        ref = extrator.extrair_referencia_do_arquivo(arquivo)
        print(f"'{arquivo}' → '{ref}'")
    
    # Estatísticas
    stats = extrator.get_estatisticas()
    print(f"\nESTATÍSTICAS:")
    print(f"- {stats['total_empresas']} empresas")
    print(f"- {stats['total_prefixos']} prefixos únicos") 
    print(f"- Empresa com mais prefixos: {stats['empresa_com_mais_prefixos']} ({stats['max_prefixos']})")