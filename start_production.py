"""
Script de inicialização para PRODUÇÃO - Lucenera PowerPoint System
Usa Waitress WSGI Server (production-ready para Windows)

Para rodar:
    python start_production.py
"""

import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def verificar_ambiente():
    """Verificar se ambiente está configurado corretamente"""
    
    print("=" * 70)
    print("🚀 LUCENERA - Sistema PowerPoint - MODO PRODUÇÃO")
    print("=" * 70)
    
    # Verificar arquivo .env
    if not os.path.exists('.env'):
        print("❌ ERRO: Arquivo .env não encontrado!")
        print("   Copie .env_example para .env e configure as credenciais.")
        sys.exit(1)
    
    print("✅ Arquivo .env encontrado")
    
    # Verificar credenciais SharePoint
    client_id = os.getenv('SHAREPOINT_CLIENT_ID')
    client_secret = os.getenv('SHAREPOINT_CLIENT_SECRET')
    tenant_id = os.getenv('SHAREPOINT_TENANT_ID')
    
    if not all([client_id, client_secret, tenant_id]):
        print("❌ ERRO: Credenciais SharePoint não configuradas no .env!")
        sys.exit(1)
    
    print("✅ Credenciais SharePoint configuradas")
    
    # Verificar pasta de upload
    upload_folder = os.getenv('UPLOAD_FOLDER')
    if upload_folder and not os.path.exists(upload_folder):
        print(f"⚠️  Criando pasta de upload: {upload_folder}")
        os.makedirs(upload_folder, exist_ok=True)
    
    print("✅ Pasta de upload configurada")
    
    # Verificar Excel master
    excel_master = os.getenv('EXCEL_MASTER')
    if excel_master and not os.path.exists(excel_master):
        print(f"⚠️  AVISO: Excel master não encontrado: {excel_master}")
        print("   Sistema funcionará, mas sem dados do Excel.")
    else:
        print("✅ Excel master encontrado")
    
    print()
    return True

def start_server():
    """Iniciar servidor Waitress"""
    
    # Verificar ambiente
    if not verificar_ambiente():
        return
    
    # Importar app
    try:
        from app_production import app
    except ImportError:
        print("❌ ERRO: Não foi possível importar app_production.py")
        sys.exit(1)
    
    # Configurações do servidor
    host = '0.0.0.0'  # Escutar em todas as interfaces
    port = int(os.getenv('PORT', 5001))
    threads = 8  # Número de threads para processar requisições
    
    print(f"🌐 Servidor iniciando em:")
    print(f"   - Local:   http://localhost:{port}")
    print(f"   - Rede:    http://0.0.0.0:{port}")
    
    site_url = os.getenv('SITE_URL')
    if site_url:
        print(f"   - Público: {site_url}")
    
    print()
    print("⚙️  Configurações:")
    print(f"   - Threads: {threads}")
    print(f"   - Host: {host}")
    print(f"   - Porta: {port}")
    print()
    print("📊 Para monitorar: acesse /health")
    print("🛑 Para parar: Ctrl+C")
    print()
    print("=" * 70)
    print()
    
    # Importar e iniciar Waitress
    try:
        from waitress import serve
        
        # Iniciar servidor
        serve(
            app,
            host=host,
            port=port,
            threads=threads,
            url_scheme='https',  # Importante para funcionar com SSL/HTTPS
            channel_timeout=1200,  # 20 min timeout para processos longos
            expose_tracebacks=False,  # Não expor stack traces em produção
            clear_untrusted_proxy_headers=True  # Segurança
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor parado pelo usuário.")
    except Exception as e:
        print(f"\n❌ ERRO ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    start_server()
