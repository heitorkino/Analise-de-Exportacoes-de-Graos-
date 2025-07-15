import pandas as pd
import csv

#--------------------------------------------------------------------------------------------------------------------------#
# df = pd.read_csv('CSV-Files/Cleaned-CSVs/NSMs_Graos.csv', encoding='utf-8')

# df[['ID', 'Produto']] = df['NCMs Utilizados'].str.extract(r'^(\d+)\s*-\s*(.*)')
# df['ID'] = df['ID'].astype(str)

# graos_chave = ['milho', 'trigo', 'arroz', 'soja', 'café']
# filtro_graos = df['Produto'].str.lower().str.contains('|'.join(graos_chave), na=False)

# df_graos = df[filtro_graos].copy()

# # ✅ Salvar corretamente, sem aspas duplicadas
# df_graos[['ID', 'Produto']].to_csv(
#     'CSV-Files/Cleaned-CSVs/NSMs_Graos.csv',
#     index=False,
#     encoding='utf-8',
#     quoting=csv.QUOTE_NONNUMERIC
# )

# print("✅ Arquivo CSV gerado sem aspas duplicadas!")
#--------------------------------------------------------------------------------------------------------------------------#

# Lê o CSV
# df = pd.read_csv('CSV-Files/Original-CSVs/EXP_2025.csv', encoding='utf-8', sep=';')

# # Lista de NCMs considerados "grãos-chave"
# graos_chave = [
#     '09011110', '09011190', '09011200',
#     '10011010', '10011090', '10011100', '10011900', '10019010', '10019090',
#     '10051000', '10059010', '10059090',
#     '10061010', '10061091', '10061092',
#     '10062010', '10062020',
#     '10063011', '10063019', '10063021', '10063029',
#     '10064000',
#     '12010010', '12010090', '12011000', '12019000',
#     '15071000', '15079010', '15079011', '15079019', '15079090',
#     '23040010', '23040090'
# ]

# # Garante que CO_NCM é string, sem espaços
# df['CO_NCM'] = df['CO_NCM'].astype(str).str.strip()

# Filtra apenas as linhas com NCM presente na lista
# df_graos = df[df['CO_NCM'].isin(graos_chave)].copy()

# Exporta o novo CSV
df_blocos = pd.read_csv('CSV-Files/Cleaned-CSVs/Blocos_Unicos.csv', encoding='utf-8', sep=',')

df_Exp = pd.read_csv('CSV-Files/Cleaned-CSVs/EXP_2025_Cleaned.csv', encoding='utf-8', sep=',')

df_NSMs = pd.read_csv('CSV-Files/Cleaned-CSVs/NSMs_Graos.csv', encoding='utf-8', sep=',')

df_Paises = pd.read_csv('CSV-Files/Cleaned-CSVs/Paises_Limpo.csv', encoding='utf-8', sep=',')

df_URFs = pd.read_csv('CSV-Files/Cleaned-CSVs/UFRs_Limpo.csv', encoding='utf-8', sep=';')
df_URFs.to_csv('CSV-Files/Cleaned-CSVs/UFRs_Limpo.csv', encoding='utf-8', sep=',')


df_Vias = pd.read_csv('CSV-Files/Cleaned-CSVs/Vias_Limpo.csv', encoding='utf-8', sep=';')
df_Vias.to_csv('CSV-Files/Cleaned-CSVs/Vias_Limpo.csv', encoding='utf-8', sep=',')

df_UFs = pd.read_csv('CSV-Files/Cleaned-CSVs/UF_Limpo.csv', encoding='utf-8', sep=';')
df_UFs.to_csv('CSV-Files/Cleaned-CSVs/UF_Limpo.csv', encoding='utf-8', sep=',')

# df_blocos.info() 
# print("-------------------------------------------")
# df_Exp.info() 
# print("-------------------------------------------")
# df_NSMs.info() 
# print("-------------------------------------------")
# df_Paises.info() 
# print("-------------------------------------------")
# df_URFs.info() 
# print("-------------------------------------------")
# df_Vias.info() 
# print("-------------------------------------------")
# df_UFs.info()










# print("✅ Arquivo CSV gerado com sucesso!")