import pandas as pd
import csv
import unidecode

#--------------------------------------------------------------------------------------------------------------------------#
import pandas as pd
import unicodedata
import csv

# # 1. Carregar CSV
# df_NCS = pd.read_csv('CSV-Files/Original-CSVs/NCMs.csv', encoding='utf-8', sep=',')

# # 2. Ajustar colunas
# df_NCS.rename(columns=lambda x: x.strip(), inplace=True)
# df_NCS['ID'] = df_NCS['Código NCM'].astype(str).str.zfill(8)
# df_NCS['Produto'] = df_NCS['Descrição NCM'].astype(str)

# # 3. Opcional: manter lista de códigos ids_trigo, mas avisar que provavelmente não serão encontrados
# ids_trigo = [
#     '19043000',
#     '10019900', '10011010', '10011090',
#     '10011100', '10011900', '10019010', '10019090', '10019100', '10081010',
#     '10081090'
# ]
# ids_trigo_ajustados = [x.zfill(8).strip() for x in ids_trigo]

# # 4. Normalizar produto (remover acentos e lowercase)
# def remover_acentos(txt):
#     return ''.join(c for c in unicodedata.normalize('NFKD', str(txt)) if not unicodedata.combining(c))

# df_NCS['Produto_normalizado'] = df_NCS['Produto'].str.lower().apply(remover_acentos)

# # 5. Filtrar produtos com "trigo" no nome (em vez de usar código NCM)
# filtro_trigo = df_NCS['Produto_normalizado'].str.contains(r'\btrigo\b', na=False)
# df_trigo = df_NCS[filtro_trigo].copy()

# # 6. Regex para outros grãos e leguminosas
# graos_chave_regex = r'\b(' + '|'.join([
#     'milho', 'arroz', 'soja', 'sojas',
#     'cafe', 'cafes', 'feijao', 'feijoes',
#     'cevada', 'cevadinha', 'sorgo', 'centeio',
#     'ervilha', 'ervilhas', 'lentilha', 'lentilhas',
#     'grao de bico', 'grao-de-bico',
#     'amendoim', 'quinoa', 'chia', 'linhaca'
# ]) + r')\b'

# # 7. Aplicar filtro por palavras-chave (outros grãos)
# filtro_graos = df_NCS['Produto_normalizado'].str.contains(graos_chave_regex, na=False, regex=True)
# df_graos = df_NCS[filtro_graos].copy()

# # 8. Juntar ambos, evitando duplicados
# df_final = pd.concat([df_graos, df_trigo]).drop_duplicates(subset='ID')

# # 8.1. Remover NCMs indesejados
# ncm_excluir = [
#     '69111010', '23067000', '23069010', '12040010', '12040090', '09011190', '09011200', '09012100', '09012200',
#     '09019000', '21031090', '11081100', '11081200', '11090000', '10059090', '11010010', '11010020', '11021000',
#     '11022000', '11023000', '11031100', '11031300', '11031400', '06029083', '10030099', '23099050', '23099060',
#     '07099911', '07099919', '07102100', '07102200', '07104000', '23040010', '23040090', '23050000', '23062000',
#     '23021000', '23022010', '23022090', '23023010', '23023090', '14031000', '14049010', '20054000', '20055100',
#     '20055900', '20058000', '15071000', '15079010', '15079011', '15079019', '15079090', '15081000', '15089000',
#     '15151100', '15151900', '15152100', '15152900', '29396990', '10063029', '10064000', '21011110', '21011190',
#     '21011200', '21013000', '21031010', '11032100', '15152910', '15152990', '85167100', '44079960', '35040020'
# ]

# df_final = df_final[~df_final['ID'].isin(ncm_excluir)]

# # 9. Exportar resultado final
# df_final[['ID', 'Produto']].to_csv(
#     'CSV-Files/Cleaned-CSVs/NCMs_Graos.csv',
#     index=False,
#     encoding='utf-8',
#     sep=',',
#     quoting=1  # csv.QUOTE_NONNUMERIC
# )

# print(f"✅ CSV final exportado com {len(df_final)} produtos contendo grãos e trigo filtrados por nome (excluídos {len(ncm_excluir)} NCMs indesejados).")

#--------------------------------------------------------------------------------------------------------------------------#
# 1. Carrega a tabela com os NCMs considerados relevantes (grãos/trigo)
df_chaves = pd.read_csv('CSV-Files/Cleaned-CSVs/NCMs_Graos.csv', encoding='utf-8', sep=',')
graos_chave = df_chaves['ID'].astype(str).str.zfill(8).tolist()

# 2. Carrega a base EXP_2025 com separador correto
df_EXP = pd.read_csv('CSV-Files/Original-CSVs/EXP_2025.csv', encoding='utf-8', sep=';')

# 3. Garante que CO_NCM é string e sem espaços
df_EXP['CO_NCM'] = df_EXP['CO_NCM'].astype(str).str.strip().str.zfill(8)

# 4. Filtra apenas as linhas cujo CO_NCM está na lista de NCMs filtrados
df_EXP_filtrado = df_EXP[df_EXP['CO_NCM'].isin(graos_chave)].copy()

# 5. Exporta o resultado
df_EXP_filtrado.to_csv('CSV-Files/Cleaned-CSVs/EXP_2025_Revisada.csv', index=False, encoding='utf-8', sep=',')

print(f"✅ Exportado EXP_2023_Revisada.csv com {len(df_EXP_filtrado)} linhas.")

#-------------------------------------------------------------------------------------------------------------------------#
# df_blocos = pd.read_csv('CSV-Files/Cleaned-CSVs/Blocos_Unicos.csv', encoding='utf-8', sep=',')

# df_Exp = pd.read_csv('CSV-Files/Cleaned-CSVs/EXP_2025_Cleaned.csv', encoding='utf-8', sep=',')

# df_NSMs = pd.read_csv('CSV-Files/Cleaned-CSVs/NSMs_Graos.csv', encoding='utf-8', sep=',')

# df_Paises = pd.read_csv('CSV-Files/Cleaned-CSVs/Paises_Limpo.csv', encoding='utf-8', sep=',')

# df_URFs = pd.read_csv('CSV-Files/Cleaned-CSVs/UFRs_Limpo.csv', encoding='utf-8', sep=';')
# df_URFs.to_csv('CSV-Files/Cleaned-CSVs/UFRs_Limpo.csv', encoding='utf-8', sep=',')


# df_Vias = pd.read_csv('CSV-Files/Cleaned-CSVs/Vias_Limpo.csv', encoding='utf-8', sep=';')
# df_Vias.to_csv('CSV-Files/Cleaned-CSVs/Vias_Limpo.csv', encoding='utf-8', sep=',')

# df_UFs = pd.read_csv('CSV-Files/Cleaned-CSVs/UF_Limpo.csv', encoding='utf-8', sep=';')
# df_UFs.to_csv('CSV-Files/Cleaned-CSVs/UF_Limpo.csv', encoding='utf-8', sep=',')

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
#-------------------------------------------------------------------------------------------------------------------------#









# print("✅ Arquivo CSV gerado com sucesso!")