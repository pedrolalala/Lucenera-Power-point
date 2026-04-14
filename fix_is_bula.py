# -*- coding: utf-8 -*-
"""
Correção para adicionar o método _is_bula_file ao SharePointClient
"""

# Adicionar este método na classe SharePointClient:

def _is_bula_file(self, nome: str) -> bool:
    """
    Detecta se o arquivo é uma bula
    
    Args:
        nome: Nome do arquivo
        
    Returns:
        True se for bula, False caso contrário
    """
    nome_lower = nome.lower()
    keywords_bula = ['bula', 'manual', 'instruction', 'guide', 'info']
    return any(keyword in nome_lower for keyword in keywords_bula)