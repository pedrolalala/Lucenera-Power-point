#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificação Completa do Sistema SharePoint Lucenera
Execute este script para validar se todo o sistema está configurado corretamente
"""

import os
import sys
import json
import traceback
from pathlib import Path

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_success(msg):
    """Imprime mensagem de sucesso"""
    print(f"✅ {msg}")

def print_warning(msg):
    """Imprime mensagem de aviso"""
    print(f"⚠️  {msg}")

def print_error(msg):
    """Imprime mensagem de erro"""
    print(f"❌ {msg}")

def check_python_version():
    """Verifica versão do Python"""
    print_header("VERIFICAÇÃO PYTHON")
    
    version = sys.version_info
    print(f"📍 Python versão: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Versão Python compatível: {version.major}.{version.minor}")
        return True
    else:
        print_error(f"Python 3.8+ necessário. Versão atual: {version.major}.{version.minor}")
        return False

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print_header("VERIFICAÇÃO DEPENDÊNCIAS")
    
    dependencies = [
        ('msal', 'Microsoft Authentication Library'),
        ('requests', 'HTTP Requests Library'),
        ('pandas', 'Data Analysis Library'),
        ('openpyxl', 'Excel File Processing'),
        ('pptx', 'PowerPoint Generation'),
        ('PIL', 'Python Imaging Library'),
        ('flask', 'Web Framework'),
        ('xml.etree.ElementTree', 'XML Processing (Built-in)')
    ]
    
    failed_imports = []
    
    for module, description in dependencies:
        try:
            if module == 'PIL':
                import PIL
                from PIL import Image
                print_success(f"{module} ({description}) - v{PIL.__version__}")
            elif module == 'pptx':
                import pptx
                print_success(f"{module} ({description}) - v{pptx.__version__}")
            elif module == 'pandas':
                import pandas as pd
                print_success(f"{module} ({description}) - v{pd.__version__}")
            elif module == 'msal':
                import msal
                print_success(f"{module} ({description}) - v{msal.__version__}")
            elif module == 'requests':
                import requests
                print_success(f"{module} ({description}) - v{requests.__version__}")
            elif module == 'openpyxl':
                import openpyxl
                print_success(f"{module} ({description}) - v{openpyxl.__version__}")
            elif module == 'flask':
                import flask
                print_success(f"{module} ({description}) - v{flask.__version__}")
            elif module == 'xml.etree.ElementTree':
                import xml.etree.ElementTree as ET
                print_success(f"{module} ({description}) - Built-in")
            else:
                __import__(module)
                print_success(f"{module} ({description}) - Importado com sucesso")
                
        except ImportError as e:
            print_error(f"{module} ({description}) - FALHA: {e}")
            failed_imports.append(module)
        except Exception as e:
            print_warning(f"{module} ({description}) - Aviso: {e}")
    
    if failed_imports:
        print_error(f"Dependências com falha: {', '.join(failed_imports)}")
        print("\n🔧 Para instalar dependências faltantes:")
        print("   pip install -r requirements_sharepoint.txt")
        return False
    else:
        print_success("Todas as dependências estão instaladas!")
        return True

def check_project_files():
    """Verifica se todos os arquivos do projeto existem"""
    print_header("VERIFICAÇÃO ARQUIVOS DO PROJETO")
    
    required_files = [
        'app.py',
        'ppt.py', 
        'sharepoint_client.py',
        'data_manager.py',
        'test_system.py',
        'requirements_sharepoint.txt',
        'exemplo_orcamento.xml',
        'CHECKLIST_SISTEMA.md'
    ]
    
    optional_files = [
        'magica_ppt.py',  # arquivo legado
        'requirements_web.txt'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print_success(f"{file} ({size:,} bytes)")
        else:
            print_error(f"{file} - ARQUIVO FALTANDO")
            missing_files.append(file)
    
    print("\n📋 Arquivos opcionais:")
    for file in optional_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print_success(f"{file} ({size:,} bytes) - Encontrado")
        else:
            print_warning(f"{file} - Não encontrado (opcional)")
    
    if missing_files:
        print_error(f"Arquivos essenciais faltando: {', '.join(missing_files)}")
        return False
    else:
        print_success("Todos os arquivos essenciais estão presentes!")
        return True

def check_sharepoint_client():
    """Verifica se o cliente SharePoint pode ser importado e configurado"""
    print_header("VERIFICAÇÃO SHAREPOINT CLIENT")
    
    try:
        from sharepoint_client import SharePointClient
        print_success("SharePointClient importado com sucesso")
        
        # Tentar instanciar (sem credenciais reais)
        try:
            client = SharePointClient(
                client_id="test-id",
                client_secret="test-secret", 
                tenant_id="test-tenant"
            )
            print_success("SharePointClient pode ser instanciado")
        except Exception as e:
            print_warning(f"Instanciação com credenciais teste: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"Falha ao importar SharePointClient: {e}")
        traceback.print_exc()
        return False

def check_data_manager():
    """Verifica se o gerenciador de dados funciona"""
    print_header("VERIFICAÇÃO DATA MANAGER")
    
    try:
        from data_manager import DataManager, OrçamentoParser
        print_success("DataManager importado com sucesso")
        
        # Testar parser XML
        try:
            parser = OrçamentoParser()
            print_success("OrçamentoParser instanciado com sucesso")
        except Exception as e:
            print_error(f"Falha ao instanciar OrçamentoParser: {e}")
            return False
            
        return True
        
    except Exception as e:
        print_error(f"Falha ao importar DataManager: {e}")
        traceback.print_exc()
        return False

def check_excel_master():
    """Verifica se o Excel master existe e pode ser lido"""
    print_header("VERIFICAÇÃO EXCEL MASTER")
    
    possible_paths = [
        "C:/Users/pedro/OneDrive/Desktop/lucenera/master_produtos.xlsx",
        "master_produtos.xlsx",
        "lucenera/master_produtos.xlsx"
    ]
    
    excel_found = False
    
    for path in possible_paths:
        if os.path.exists(path):
            print_success(f"Excel master encontrado: {path}")
            
            try:
                import pandas as pd
                df = pd.read_excel(path)
                
                print(f"📊 Total de produtos: {len(df)}")
                print(f"📋 Colunas: {list(df.columns)}")
                
                # Verificar colunas essenciais
                required_columns = ['codigo', 'ref', 'marca', 'nome']
                missing_columns = []
                
                for col in required_columns:
                    if col in df.columns:
                        print_success(f"Coluna '{col}' encontrada")
                    else:
                        print_error(f"Coluna '{col}' faltando")
                        missing_columns.append(col)
                
                if missing_columns:
                    print_error(f"Colunas essenciais faltando: {missing_columns}")
                    return False
                
                # Mostrar algumas estatísticas
                if 'marca' in df.columns:
                    marcas = df['marca'].unique()
                    if len(marcas) > 0:
                        print(f"🏷️  Marcas encontradas: {list(marcas)}")
                
                excel_found = True
                break
                
            except Exception as e:
                print_error(f"Erro ao ler Excel: {e}")
                return False
    
    if not excel_found:
        print_warning("Excel master não encontrado")
        print("🔧 Execute: python criar_excel_template.py")
        return False
    
    print_success("Excel master verificado com sucesso!")
    return True

def check_xml_example():
    """Verifica se o exemplo de XML está válido"""
    print_header("VERIFICAÇÃO XML EXEMPLO")
    
    xml_file = "exemplo_orcamento.xml"
    
    if not os.path.exists(xml_file):
        print_error(f"Arquivo {xml_file} não encontrado")
        return False
    
    try:
        import xml.etree.ElementTree as ET
        
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        print_success(f"XML válido - Tag root: {root.tag}")
        
        # Verificar estrutura
        itens = root.find('itens')
        if itens is not None:
            items_count = len(itens.findall('item'))
            print_success(f"Encontrados {items_count} itens no XML")
            
            # Verificar primeiro item
            primeiro_item = itens.find('item')
            if primeiro_item is not None:
                attrs = primeiro_item.attrib
                required_attrs = ['linha', 'codigo', 'ref', 'preco', 'quantidade']
                
                for attr in required_attrs:
                    if attr in attrs:
                        print_success(f"Atributo '{attr}': {attrs[attr]}")
                    else:
                        print_error(f"Atributo '{attr}' faltando no item")
                        return False
        else:
            print_error("Tag 'itens' não encontrada no XML")
            return False
            
        return True
        
    except Exception as e:
        print_error(f"Erro ao validar XML: {e}")
        return False

def check_flask_app():
    """Verifica se a aplicação Flask pode ser importada"""
    print_header("VERIFICAÇÃO APLICAÇÃO FLASK")
    
    try:
        from app import app
        print_success("Aplicação Flask importada com sucesso")
        
        # Verificar rotas principais
        with app.app_context():
            rules = [rule.rule for rule in app.url_map.iter_rules()]
            main_routes = ['/', '/upload', '/status/<job_id>']
            
            for route in main_routes:
                if route in rules or any(route in rule for rule in rules):
                    print_success(f"Rota encontrada: {route}")
                else:
                    print_warning(f"Rota não encontrada: {route}")
        
        return True
        
    except Exception as e:
        print_error(f"Falha ao importar aplicação Flask: {e}")
        traceback.print_exc()
        return False

def run_system_validation():
    """Executa validação completa do sistema"""
    print("🚀 VALIDAÇÃO COMPLETA DO SISTEMA SHAREPOINT LUCENERA")
    print("Verificando todos os componentes...")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies), 
        ("Project Files", check_project_files),
        ("SharePoint Client", check_sharepoint_client),
        ("Data Manager", check_data_manager),
        ("Excel Master", check_excel_master),
        ("XML Example", check_xml_example),
        ("Flask App", check_flask_app)
    ]
    
    results = {}
    
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print_error(f"Erro na verificação {name}: {e}")
            results[name] = False
    
    # Resumo final
    print_header("RESUMO DA VALIDAÇÃO")
    
    passed = 0
    total = len(checks)
    
    for name, result in results.items():
        if result:
            print_success(f"{name}: PASSOU")
            passed += 1
        else:
            print_error(f"{name}: FALHOU")
    
    print(f"\n📊 Resultado: {passed}/{total} verificações passaram")
    
    if passed == total:
        print("\n🎉 SISTEMA COMPLETAMENTE VALIDADO!")
        print("✅ Tudo pronto para usar o sistema SharePoint Lucenera")
        print("\n🚀 Próximo passo: execute 'python app.py' para iniciar o servidor")
        return True
    else:
        print(f"\n⚠️  Sistema parcialmente configurado: {passed}/{total}")
        print("🔧 Corrija os problemas indicados acima antes de prosseguir")
        return False

if __name__ == "__main__":
    try:
        success = run_system_validation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⛔ Validação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Erro inesperado durante validação: {e}")
        traceback.print_exc()
        sys.exit(1)