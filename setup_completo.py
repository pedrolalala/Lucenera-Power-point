#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Completo - Sistema SharePoint Lucenera
Script de configuração automática do sistema
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_success(msg):
    print(f"✅ {msg}")

def print_warning(msg):
    print(f"⚠️  {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def run_command(command, description):
    """Executa comando e retorna resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{description} - Concluído")
            return True
        else:
            print_error(f"{description} - Falhou: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"{description} - Erro: {e}")
        return False

def check_python():
    """Verifica se Python está instalado"""
    print_header("VERIFICAÇÃO PYTHON")
    
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"Python encontrado: {version}")
        
        # Verificar versão
        import sys
        if sys.version_info >= (3, 8):
            print_success("Versão Python compatível")
            return True
        else:
            print_error("Python 3.8+ necessário")
            return False
            
    except Exception as e:
        print_error(f"Python não encontrado: {e}")
        return False

def install_dependencies():
    """Instala dependências Python"""
    print_header("INSTALAÇÃO DEPENDÊNCIAS")
    
    # Verificar se requirements existe
    if not os.path.exists("requirements_sharepoint.txt"):
        print_error("Arquivo requirements_sharepoint.txt não encontrado")
        return False
    
    # Instalar dependências
    commands = [
        ("pip install --upgrade pip", "Atualizar pip"),
        ("pip install python-dotenv", "Instalar python-dotenv"),
        ("pip install -r requirements_sharepoint.txt", "Instalar dependências SharePoint")
    ]
    
    success = True
    for command, description in commands:
        if not run_command(command, description):
            success = False
    
    return success

def setup_env_file():
    """Configura arquivo .env"""
    print_header("CONFIGURAÇÃO ARQUIVO .env")
    
    if os.path.exists(".env"):
        print_warning("Arquivo .env já existe")
        response = input("Deseja recriá-lo? (y/N): ")
        if response.lower() != 'y':
            print("⏭️  Configuração .env mantida")
            return True
    
    # Verificar se .env.example existe
    if not os.path.exists(".env.example"):
        print_error("Arquivo .env.example não encontrado")
        return False
    
    try:
        # Copiar exemplo para .env
        with open(".env.example", "r", encoding="utf-8") as src:
            content = src.read()
        
        # Substituir placeholders com valores reais do .env
        content = content.replace("your_client_id_here", os.getenv("SHAREPOINT_CLIENT_ID", "your_client_id_here"))
        content = content.replace("your_tenant_id_here", os.getenv("SHAREPOINT_TENANT_ID", "your_tenant_id_here")) 
        content = content.replace("your_client_secret_here", os.getenv("SHAREPOINT_CLIENT_SECRET", "your_client_secret_here"))
        content = content.replace("yoursite.sharepoint.com", "luceneraprojetos.sharepoint.com")
        content = content.replace("YOUR DRIVE NAME", "LUCENERA PROJETOS")
        content = content.replace("C:/caminho/para/seu/master_produtos.xlsx", "C:/Users/pedro/OneDrive/Desktop/lucenera/master_produtos.xlsx")
        
        # Remover linhas de instruções
        lines = content.split('\n')
        cleaned_lines = [line for line in lines if not line.startswith('# INSTRUÇÕES:') and not line.startswith('# 1.') and not line.startswith('# 2.') and not line.startswith('# 3.') and not line.startswith('# 4.')]
        content = '\n'.join(cleaned_lines)
        
        # Salvar .env
        with open(".env", "w", encoding="utf-8") as dst:
            dst.write(content)
        
        print_success("Arquivo .env criado com credenciais reais")
        return True
        
    except Exception as e:
        print_error(f"Erro ao criar .env: {e}")
        return False

def create_excel_master():
    """Cria Excel master"""
    print_header("CRIAÇÃO EXCEL MASTER")
    
    # Verificar se Excel já existe
    excel_path = "C:/Users/pedro/OneDrive/Desktop/lucenera/master_produtos.xlsx"
    
    if os.path.exists(excel_path):
        print_warning("Excel master já existe")
        response = input("Deseja recriá-lo? (y/N): ")
        if response.lower() != 'y':
            print("⏭️  Excel master mantido")
            return True
    
    # Executar gerador de template
    return run_command("python criar_excel_template.py", "Criar template Excel master")

def validate_system():
    """Valida sistema completo"""
    print_header("VALIDAÇÃO SISTEMA")
    
    return run_command("python test_env.py", "Validar configuração completa")

def setup_complete():
    """Executa setup completo do sistema"""
    print("🚀 SETUP AUTOMÁTICO - SISTEMA SHAREPOINT LUCENERA")
    print("Este script configurará todo o sistema automaticamente")
    print()
    
    steps = [
        ("Verificar Python", check_python),
        ("Instalar dependências", install_dependencies),
        ("Configurar arquivo .env", setup_env_file),
        ("Criar Excel master", create_excel_master),
        ("Validar sistema", validate_system)
    ]
    
    results = {}
    
    for step_name, step_func in steps:
        print(f"\n▶️  Executando: {step_name}")
        try:
            results[step_name] = step_func()
        except Exception as e:
            print_error(f"Erro em {step_name}: {e}")
            results[step_name] = False
        
        if not results[step_name]:
            print_error(f"Falha na etapa: {step_name}")
            print("🛑 Setup interrompido")
            return False
    
    # Resumo final
    print_header("SETUP CONCLUÍDO")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"📊 Resultado: {passed}/{total} etapas concluídas")
    
    if passed == total:
        print_success("SISTEMA COMPLETAMENTE CONFIGURADO!")
        print("\n🎉 Próximos passos:")
        print("1️⃣  Execute: python app.py")
        print("2️⃣  Acesse: http://localhost:5001")
        print("3️⃣  Faça upload de um XML de orçamento")
        print("4️⃣  Aguarde a geração do PowerPoint")
        
        # Oferecer executar imediatamente
        print("\n🚀 Deseja executar o sistema agora? (Y/n):")
        response = input().strip().lower()
        if response != 'n':
            print("\n🌟 Iniciando sistema...")
            os.system("python app.py")
        
        return True
    else:
        print_error("Setup incompleto - corrija os problemas acima")
        return False

if __name__ == "__main__":
    try:
        success = setup_complete()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⛔ Setup cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Erro inesperado durante setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)