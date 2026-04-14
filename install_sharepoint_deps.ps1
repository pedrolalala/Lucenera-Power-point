# Script PowerShell para instalar dependências do sistema SharePoint
# Execute como: .\install_sharepoint_deps.ps1

Write-Host "🚀 INSTALAÇÃO SISTEMA SHAREPOINT - LUCENERA" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

# Verificar se Python está disponível
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado. Instale Python primeiro." -ForegroundColor Red
    exit 1
}

# Verificar se venv existe
$venvPath = ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "📦 Criando ambiente virtual..." -ForegroundColor Yellow
    python -m venv $venvPath
}

# Ativar environment
Write-Host "🔄 Ativando ambiente virtual..." -ForegroundColor Yellow
& "$venvPath\Scripts\Activate.ps1"

# Atualizar pip
Write-Host "🔧 Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Instalar dependências existentes
if (Test-Path "requirements_web.txt") {
    Write-Host "📚 Instalando dependências existentes..." -ForegroundColor Yellow
    pip install -r requirements_web.txt
}

# Instalar novas dependências SharePoint
Write-Host "🌐 Instalando dependências SharePoint..." -ForegroundColor Yellow
pip install -r requirements_sharepoint.txt

# Verificar instalação
Write-Host "✅ Verificando instalação..." -ForegroundColor Yellow

$testScript = @"
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
    print(f'\n❌ Módulos com falha: {failed}')
    sys.exit(1)
else:
    print('\n🎉 Todas as dependências instaladas com sucesso!')
"@

python -c $testScript
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro na verificação das dependências" -ForegroundColor Red
    exit 1
}

# Teste básico do sistema
Write-Host "🧪 Testando sistema..." -ForegroundColor Yellow
python test_system.py

Write-Host ""
Write-Host "✅ INSTALAÇÃO CONCLUÍDA!" -ForegroundColor Green
Write-Host "Para usar o sistema:" -ForegroundColor Cyan
Write-Host "1. Configure o Excel master em:" -ForegroundColor White
Write-Host "   C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Prepare um XML de orçamento no formato correto" -ForegroundColor White
Write-Host ""
Write-Host "3. Execute o servidor:" -ForegroundColor White
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Acesse: http://localhost:5001" -ForegroundColor White