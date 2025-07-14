import pandas as pd

# Leitura do arquivo original
df = pd.read_csv('CSV-Files/Original-CSVs/NSMs.csv', encoding='utf-8')

print(df)

# Separar o código NCM (ID) da descrição do produto
df[['ID', 'Produto']] = df['NCMs Utilizados'].str.extract(r'^(\d+)\s*-\s*(.*)')

# Converter ID para string (por segurança)
df['ID'] = df['ID'].astype(str)

graos_chave = ['milho', 'trigo', 'arroz', 'soja', 'café']
filtro_graos = df['Produto'].str.lower().str.contains('|'.join(graos_chave), na=False)

df_graos = df[filtro_graos].copy()

 # Salva em um novo CSV com apenas as colunas ID e Produto
df_graos[['ID', 'Produto']].to_csv('CSV-Files/Cleaned-CSVs/NSMs_Graos.csv', index=False, encoding='utf-8')

print("✅ Novo arquivo 'NCMs_Graos.csv' criado com sucesso!")