import os
import shutil
import re

pasta_origem = r"C:\Users\pedro\OneDrive\Desktop\lucenera\INTERLIGHT - ILT"
pasta_destino = r"C:\Users\pedro\OneDrive\Desktop\lucenera\INTERLIGHT_SEPARADOS"

# Códigos PARTIAL do PDF (números principais + variantes reais)
codigos_base = [
    "3651", "3649", "3639", "3927", "3967",  # Núcleos dos L01-L05
    "FE-S-PX", "AB-S-PX", "AS-S-V2-PM", "S-MRCT", "AS-S", "FE-S"  # Sufixos comuns
]

mapeamento = {
    "3651": "10539", "3649": "10289", "3639": "12779", "3927": "7365", "3967": "7365"
}

print("✅ V4: Match partial (3651*, 3649*, etc.) + limpa prefixos!")

os.makedirs(pasta_destino, exist_ok=True)
arquivos = [f for f in os.listdir(pasta_origem) if os.path.isfile(os.path.join(pasta_origem, f))]
print(f"📁 {len(arquivos)} arquivos.")

matchs = 0
for arquivo in arquivos:
    nome_limpo = re.sub(r'^(INTERLIGHT\s*-?\s*|BULA\s*|MANUAL\s*|Bula_Instalacao?\s*|Bula\s*)', '', arquivo, flags=re.I).strip()
    nome_upper = nome_limpo.upper()
    
    match_base = None
    for base in codigos_base:
        if base.upper() in nome_upper:
            match_base = base
            break
    
    if match_base:
        interno = mapeamento.get(match_base, match_base)
        # Extrai resto após código
        for full_codigo in ["3651-FE-S-PX", "3649-FE-S-PX", "3649-AB-S-PX", "3639-AS-S", "3927"]:
            if full_codigo.upper() in nome_upper:
                resto = re.sub(re.escape(full_codigo.upper()), '', nome_upper, flags=re.I).strip()
                break
        else:
            resto = re.sub(re.escape(match_base.upper()), '', nome_upper, flags=re.I).strip()
        resto = re.sub(r'^[-_\s]+', '', resto)
        ext = os.path.splitext(arquivo)[1]
        nome_novo = f"{interno}_{resto}{ext}" if resto else f"{interno}{ext}"
        
        shutil.copy2(os.path.join(pasta_origem, arquivo), os.path.join(pasta_destino, nome_novo))
        print(f"✅ COPIADO: {arquivo} → {nome_novo} (match: {match_base})")
        matchs += 1

print(f"\n🎉 {matchs} copiados! Pasta: {pasta_destino}")