import pandas as pd

# Carregar Excel
df = pd.read_excel(r'C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx')

print("="*60)
print("ANÁLISE DO EXCEL MASTER")
print("="*60)

print(f"\nColunas disponíveis: {df.columns.tolist()}")
print(f"\nTotal de registros: {len(df)}")

print("\n" + "="*60)
print("CATEGORIAS ÚNICAS (DescCategoria)")
print("="*60)
categorias = df['DescCategoria'].value_counts()
for cat, count in categorias.items():
    print(f"  {cat:<30} : {count:>5} produtos")

print("\n" + "="*60)
print("EXEMPLO DE PRODUTOS POR CATEGORIA")
print("="*60)

# Mostrar exemplos de cada categoria principal
categorias_principais = ['LUMINARIA', 'LUMINÁRIA', 'LED', 'DRIVER', 'ACESSORIO', 'FONTE']
for cat in categorias_principais:
    matching = df[df['DescCategoria'].str.contains(cat, case=False, na=False)]
    if len(matching) > 0:
        print(f"\nCategoria: {cat}")
        print(matching[['CodProduto', 'Referencia', 'DescProduto', 'DescCategoria']].head(3).to_string())
