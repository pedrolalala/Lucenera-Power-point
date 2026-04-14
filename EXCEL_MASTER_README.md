# Estrutura do Excel Master - master_produtos.xlsx

## Colunas Necessárias

| Coluna | Nome | Descrição | Exemplo |
|--------|------|-----------|---------|
| A | codigo | Código interno do produto | 10289 |
| B | ref | Referência completa | 3649-AB-S-PX |
| C | marca | Nome da marca | Interlight |
| D | nome | Nome do produto | Luminária de embutir LED 30W |
| E | categoria | Categoria do produto | Embutir |
| F | potencia | Potência em Watts | 30W |
| G | cor_temperatura | Temperatura de cor | 3000K |
| H | fluxo_luminoso | Fluxo luminoso | 2400lm |
| I | ficha_tecnica | Status da ficha | Disponível |
| J | manual_instalacao | Status do manual | Disponível |

## Exemplo de Dados (primeiras linhas)

```
codigo | ref           | marca        | nome                        | categoria | potencia | cor_temp | fluxo  | ficha_tecnica | manual_instalacao
-------|---------------|--------------|-----------------------------|-----------|---------|---------|---------|--------------|-----------------
10289  | 3649-AB-S-PX  | Interlight   | Luminária de embutir LED    | Embutir   | 30W     | 3000K   | 2400lm | Disponível    | Disponível
10539  | 3649-FE-S-PX  | Interlight   | Luminária de sobrepor LED   | Sobrepor  | 45W     | 4000K   | 3200lm | Disponível    | Disponível  
12779  | 3639-AS-S-V2  | Bella Luce   | Pendente decorativo LED     | Pendente  | 25W     | 2700K   | 1800lm | Disponível    | Não
7365   | 3927-S-MRCT   | Direct Light | Spot direcionável LED       | Spot      | 15W     | 3000K   | 1200lm | Disponível    | Disponível
7365   | 3967-AS-S     | Jean Lux     | Lustre cristal LED          | Lustre    | 60W     | 2700K   | 4500lm | Em produção   | Disponível
```

## Mapeamento de Códigos

### O sistema fará a correlação:

1. **XML contém:** `codigo="10289"` e `ref="3649-AB-S-PX"`
2. **Excel master:** Busca linha com `codigo=10289`
3. **Resultado:** Encontra `marca=Interlight`
4. **SharePoint:** Busca em `LUCENERA PROJETOS/Fichas Técnicas/Interlight/`
5. **Arquivos:** Procura por nomes contendo `10289` ou `3649-AB-S-PX`

### Possíveis variações nos nomes dos arquivos SharePoint:

- `10289_ficha_tecnica.docx`
- `3649-AB-S-PX_especificacao.docx`
- `INTERLIGHT_10289_manual.docx`
- `produto_3649_AB_S_PX_info.docx`

## Como Criar o Excel

### Opção 1: Manual
1. Abra o Excel
2. Crie as colunas conforme tabela acima
3. Preencha com dados dos produtos
4. Salve como `master_produtos.xlsx`

### Opção 2: Importar de sistema existente
Se você tem um sistema/banco existente, exporte os dados no formato acima.

### Opção 3: Template
Baixe o template em: [criar arquivo de template]

## Localização

Salve o arquivo em:
```
C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx
```

## Validação

Para testar o Excel master:

```python
# Execute no terminal
python -c "
import pandas as pd
df = pd.read_excel('C:/path/to/master_produtos.xlsx')
print('Colunas encontradas:', list(df.columns))
print('Total de produtos:', len(df))
print('Marcas únicas:', df['marca'].unique())
print('Primeiras 5 linhas:')
print(df.head())
"
```

## Manutenção

### Adicionar novos produtos:
1. Abra o Excel master
2. Adicione nova linha com dados completos
3. Certifique-se que arquivos correspondentes estão no SharePoint
4. Salve o arquivo

### Atualizar marcas:
1. Adicione nova pasta no SharePoint: `Fichas Técnicas/[NOVA_MARCA]/`
2. Atualize campo `marca` no Excel para produtos dessa marca
3. Organize arquivos na nova pasta

## Troubleshooting

### Produto não encontrado:
- Verifique se `codigo` existe no Excel master
- Confirme se `marca` está correta
- Verifique se pasta da marca existe no SharePoint

### Arquivos não encontrados:
- Confirme nomes dos arquivos no SharePoint
- Certifique-se que contêm código ou referência no nome
- Verifique permissões de acesso


Esse Excel master é a "fonte da verdade" para todo o sistema SharePoint!