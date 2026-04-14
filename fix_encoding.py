# -*- coding: utf-8 -*-
"""
Fix para Codificação UTF-8 no Windows
Configure o terminal para suportar UTF-8 se quiser usar emojis
"""
import os
import sys

def configure_utf8_windows():
    """Configura o terminal Windows para suportar UTF-8"""
    if sys.platform == "win32":
        try:
            # Configurar page code para UTF-8 no Windows
            os.system("chcp 65001 > nul")
            print("[UTF8] Terminal configurado para UTF-8")
            return True
        except Exception as e:
            print(f"[AVISO] Não foi possível configurar UTF-8: {e}")
            return False
    return True

def safe_print(message):
    """Função de print segura que evita erros de codificação"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Substituir caracteres problemáticos
        safe_message = message.encode('ascii', errors='replace').decode('ascii')
        print(safe_message)

if __name__ == "__main__":
    print("Teste de configuração UTF-8 no Windows")
    
    if configure_utf8_windows():
        print("✅ Configuração UTF-8 aplicada")
        print("🚀 Emojis devem funcionar agora")
    else:
        print("[OK] Usando modo ASCII compatível")
        print("[INFO] Emojis foram substituídos por texto simples")