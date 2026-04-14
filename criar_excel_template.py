import pandas as pd
import os

# Criar template do Excel master
def criar_template_excel():
    """
    Cria um template do Excel master com estrutura completa e alguns dados de exemplo
    """
    
    # Estrutura das colunas
    colunas = [
        'codigo',           # A - Código interno do produto
        'ref',             # B - Referência completa
        'marca',           # C - Nome da marca  
        'nome',            # D - Nome do produto
        'categoria',       # E - Categoria do produto
        'potencia',        # F - Potência em Watts
        'cor_temperatura', # G - Temperatura de cor
        'fluxo_luminoso',  # H - Fluxo luminoso
        'ficha_tecnica',   # I - Status da ficha
        'manual_instalacao'# J - Status do manual
    ]
    
    # Dados de exemplo
    dados_exemplo = [
        {
            'codigo': 10289,
            'ref': '3649-AB-S-PX',
            'marca': 'Interlight',
            'nome': 'Luminária de embutir LED 30W',
            'categoria': 'Embutir',
            'potencia': '30W',
            'cor_temperatura': '3000K',
            'fluxo_luminoso': '2400lm',
            'ficha_tecnica': 'Disponível',
            'manual_instalacao': 'Disponível'
        },
        {
            'codigo': 10539,
            'ref': '3649-FE-S-PX',
            'marca': 'Interlight',
            'nome': 'Luminária de sobrepor LED 45W',
            'categoria': 'Sobrepor',
            'potencia': '45W',
            'cor_temperatura': '4000K',
            'fluxo_luminoso': '3200lm',
            'ficha_tecnica': 'Disponível',
            'manual_instalacao': 'Disponível'
        },
        {
            'codigo': 12779,
            'ref': '3639-AS-S-V2-PM',
            'marca': 'Bella Luce',
            'nome': 'Pendente decorativo LED',
            'categoria': 'Pendente',
            'potencia': '25W',
            'cor_temperatura': '2700K',
            'fluxo_luminoso': '1800lm',
            'ficha_tecnica': 'Disponível',
            'manual_instalacao': 'Não'
        },
        {
            'codigo': 7365,
            'ref': '3927-S-MRCT',
            'marca': 'Direct Light',
            'nome': 'Spot direcionável LED 15W',
            'categoria': 'Spot',
            'potencia': '15W',
            'cor_temperatura': '3000K',
            'fluxo_luminoso': '1200lm',
            'ficha_tecnica': 'Disponível',
            'manual_instalacao': 'Disponível'
        },
        {
            'codigo': 7365,
            'ref': '3967-AS-S',
            'marca': 'Jean Lux',
            'nome': 'Lustre cristal LED',
            'categoria': 'Lustre',
            'potencia': '60W',
            'cor_temperatura': '2700K',
            'fluxo_luminoso': '4500lm',
            'ficha_tecnica': 'Em produção',
            'manual_instalacao': 'Disponível'
        },
        # Linhas vazias para preenchimento
        {col: '' for col in colunas},
        {col: '' for col in colunas},
        {col: '' for col in colunas}
    ]
    
    # Criar DataFrame
    df = pd.DataFrame(dados_exemplo, columns=colunas)
    
    # Definir caminho de destino 
    desktop_path = os.path.expanduser("~/Desktop")
    lucenera_path = os.path.join(desktop_path, "lucenera")
    
    # Criar diretório se não existir
    os.makedirs(lucenera_path, exist_ok=True)
    
    # Caminho completo do arquivo
    arquivo_excel = os.path.join(lucenera_path, "master_produtos.xlsx")
    
    # Salvar Excel com formatação
    try:
        with pd.ExcelWriter(arquivo_excel, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Produtos', index=False)
            
            # Obter worksheet para formatação
            worksheet = writer.sheets['Produtos']
            
            # Ajustar largura das colunas
            column_widths = {
                'A': 8,   # codigo
                'B': 15,  # ref
                'C': 12,  # marca
                'D': 25,  # nome
                'E': 12,  # categoria 
                'F': 8,   # potencia
                'G': 12,  # cor_temperatura
                'H': 12,  # fluxo_luminoso
                'I': 15,  # ficha_tecnica
                'J': 18   # manual_instalacao
            }
            
            for column, width in column_widths.items():
                worksheet.column_dimensions[column].width = width
                
        print(f"✅ Template Excel criado com sucesso!")
        print(f"📁 Arquivo salvo em: {arquivo_excel}")
        print(f"\n📋 Estrutura criada:")
        print(f"   • {len(dados_exemplo)-3} produtos de exemplo")
        print(f"   • {len(colunas)} colunas configuradas")
        print(f"   • 3 linhas vazias para novos produtos")
        
        # Verificar arquivo criado
        if os.path.exists(arquivo_excel):
            file_size = os.path.getsize(arquivo_excel)
            print(f"📏 Tamanho do arquivo: {file_size:,} bytes")
            
        return arquivo_excel
        
    except Exception as e:
        print(f"❌ Erro ao criar template: {e}")
        return None

if __name__ == "__main__":
    print("🏗️  CRIANDO TEMPLATE EXCEL MASTER")
    print("=" * 40)
    
    arquivo = criar_template_excel()
    
    if arquivo:
        print("\n" + "=" * 40)
        print("🎉 TEMPLATE CRIADO COM SUCESSO!")
        print("\nPróximos passos:")
        print("1️⃣  Abra o arquivo Excel gerado")
        print("2️⃣  Preencha com dados dos seus produtos")
        print("3️⃣  Mantenha os cabeçalhos das colunas")
        print("4️⃣  Use os dados de exemplo como referência")
        print("5️⃣  Salve o arquivo antes de usar o sistema")
    else:
        print("\n❌ Falha ao criar template")