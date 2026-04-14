#!/bin/bash
# Script para instalar dependências do sistema SharePoint
# Execute como: bash install_sharepoint_deps.sh

echo "🚀 INSTALAÇÃO SISTEMA SHAREPOINT - LUCENERA"
echo "==========================================="

# Verificar se Python está disponível
if ! command -v python &> /dev/null; then
    echo "❌ Python não encontrado. Instale Python primeiro."
    exit 1
fi

# Verificar se venv existe
VENV_PATH=".venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "📦 Criando ambiente virtual..."
    python -m venv $VENV_PATH
fi

# Ativar environment
echo "🔄 Ativando ambiente virtual..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source .venv/Scripts/activate
else
    # Linux/Mac
    source .venv/bin/activate
fi

# Atualizar pip
echo "🔧 Atualizando pip..."
python -m pip install --upgrade pip

# Instalar dependências existentes
echo "📚 Instalando dependências existentes..."
if [ -f "requirements_web.txt" ]; then
    pip install -r requirements_web.txt
fi

# Instalar novas dependências SharePoint
echo "🌐 Instalando dependências SharePoint..."
pip install -r requirements_sharepoint.txt

# Verificar instalação
echo "✅ Verificando instalação..."
python -c "
import sys
modules = ['msal', 'requests', 'pandas', 'openpyxl', 'pptx', 'PIL']
failed = []

for module in modules:
    try:
        if module == 'PIL':
            import PIL
        elif module == 'pptx':
            import pptx
        else:
            __import__(module)
        print(f'✅ {module}')
    except ImportError:
        print(f'❌ {module}')
        failed.append(module)

if failed:
    print(f'\\n❌ Módulos com falha: {failed}')
    sys.exit(1)
else:
    print('\\n🎉 Todas as dependências instaladas com sucesso!')
"

# Teste básico do sistema
echo "🧪 Testando sistema..."
python test_system.py

echo ""
echo "✅ INSTALAÇÃO CONCLUÍDA!"
echo "Para usar o sistema:"
echo "1. Configure o Excel master em:" 
echo "   C:\\Users\\pedro\\OneDrive\\Desktop\\lucenera\\master_produtos.xlsx"
echo ""
echo "2. Prepare um XML de orçamento no formato correto"
echo ""
echo "3. Execute o servidor:"
echo "   python app.py"
echo ""
echo "4. Acesse: http://localhost:5001"