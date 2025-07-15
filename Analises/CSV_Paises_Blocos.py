import requests
import csv
import pandas as pd
import os

# def fetch_csv(endpoint, out_file):
#     resp = requests.get(endpoint, params={'language':'pt'}, verify=False)
#     data = resp.json()['data']

#     # Se data[0] for uma lista, são os países; se não, já é a lista de blocos
#     if isinstance(data[0], list):
#         items = data[0]
#     else:
#         items = data

#     with open(out_file, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(['id','text'])
#         for item in items:
#             writer.writerow([item['id'], item['text']])

# # Países
# fetch_csv(
#     'https://api-comexstat.mdic.gov.br/general/filters/country?language=pt',
#     'paises.csv'
# )

# # Blocos Econômicos
# fetch_csv(
#     'https://api-comexstat.mdic.gov.br/general/filters/economicBlock?language=pt',
#     'blocos.csv'
# )

# df = pd.read_csv('blocos.csv')
# df.drop_duplicates(inplace=True)
# df.to_csv('Blocos_Unicos.csv', index=False)

# print("Arquivo de blocos únicos gerado: blocos_unicos.csv")

# 1. Carregar os arquivos
df_aux = pd.read_csv("CSV-Files/Original-CSVs/20250715_134910_TABELAS_AUXILIARES.csv", encoding='utf-8', sep=';')
df_blocos = pd.read_csv("CSV-Files/Cleaned-CSVs/Blocos_Unicos.csv")
df_paises = pd.read_csv("CSV-Files/Cleaned-CSVs/Paises_Limpo.csv")

# 2. Renomear colunas para merge
df_blocos = df_blocos.rename(columns={'text': 'Bloco', 'id': 'id_bloco'})
df_paises = df_paises.rename(columns={'text': 'Países', 'id': 'id_pais'})

# 3. Merge para trazer os IDs
df_aux = df_aux.merge(df_blocos, on='Bloco', how='left')
df_aux = df_aux.merge(df_paises, on='Países', how='left')

# 4. Substituir nomes por IDs
df_aux = df_aux.drop(columns=['Bloco', 'Países'])
df_aux = df_aux.rename(columns={'id_bloco': 'Bloco', 'id_pais': 'Países'})

# 5. Criar diretório de saída, se necessário
output_dir = "CSV-Files/Cleaned-CSVs"
os.makedirs(output_dir, exist_ok=True)

# 6. Salvar resultado
df_aux.to_csv(f"{output_dir}/Blocos_Paises.csv", index=False, sep=',')

print("✔ Substituição feita e arquivo salvo com sucesso.")