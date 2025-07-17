# Este script trata a base auxiliar de países e blocos econômicos.
# Ele faz merge com tabelas limpas contendo IDs e nomes padronizados de países e blocos,
# substitui os nomes pelos respectivos IDs e salva o resultado final em CSV para uso em análises.

import requests
import csv
import pandas as pd
import os

# -----------------------------------------------------------------------------------
# BLOCO COMENTADO: Faz download de países e blocos econômicos da API do ComexStat
# A função `fetch_csv` acessa a API pública do ComexStat, extrai os dados em JSON e salva como CSV.
# -----------------------------------------------------------------------------------

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

# -----------------------------------------------------------------------------------
# ETAPA 1: Carrega os arquivos CSV necessários
df_aux = pd.read_csv("CSV-Files/Original-CSVs/20250715_134910_TABELAS_AUXILIARES.csv", encoding='utf-8', sep=';') # Arquivo com dados auxiliares
df_blocos = pd.read_csv("CSV-Files/Cleaned-CSVs/Blocos_Unicos.csv") # Blocos com IDs únicos
df_paises = pd.read_csv("CSV-Files/Cleaned-CSVs/Paises_Limpo.csv") # Países com IDs únicos

# ETAPA 2: Renomeia as colunas para padronizar e permitir merge
df_blocos = df_blocos.rename(columns={'text': 'Bloco', 'id': 'id_bloco'})
df_paises = df_paises.rename(columns={'text': 'Países', 'id': 'id_pais'})

# ETAPA 3: Realiza o merge dos dados principais com os IDs de blocos e países
df_aux = df_aux.merge(df_blocos, on='Bloco', how='left')  # Adiciona o id_bloco
df_aux = df_aux.merge(df_paises, on='Países', how='left') # Adiciona o id_pais

# ETAPA 4: Substitui os nomes originais pelos respectivos IDs
df_aux = df_aux.drop(columns=['Bloco', 'Países']) # Remove colunas com texto
df_aux = df_aux.rename(columns={'id_bloco': 'Bloco', 'id_pais': 'Países'}) # Renomeia os IDs para manter os nomes das colunas

# ETAPA 5: Garante que a pasta de saída existe
output_dir = "CSV-Files/Cleaned-CSVs"
os.makedirs(output_dir, exist_ok=True)

# ETAPA 6: Salva o resultado final em CSV
df_aux.to_csv(f"{output_dir}/Blocos_Paises.csv", index=False, sep=',')

print("✔ Substituição feita e arquivo salvo com sucesso.")