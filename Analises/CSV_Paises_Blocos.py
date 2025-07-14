import requests
import csv
import pandas as pd

def fetch_csv(endpoint, out_file):
    resp = requests.get(endpoint, params={'language':'pt'}, verify=False)
    data = resp.json()['data']

    # Se data[0] for uma lista, são os países; se não, já é a lista de blocos
    if isinstance(data[0], list):
        items = data[0]
    else:
        items = data

    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id','text'])
        for item in items:
            writer.writerow([item['id'], item['text']])

# Países
fetch_csv(
    'https://api-comexstat.mdic.gov.br/general/filters/country?language=pt',
    'paises.csv'
)

# Blocos Econômicos
fetch_csv(
    'https://api-comexstat.mdic.gov.br/general/filters/economicBlock?language=pt',
    'blocos.csv'
)

df = pd.read_csv('blocos.csv')
df.drop_duplicates(inplace=True)
df.to_csv('Blocos_Unicos.csv', index=False)

print("Arquivo de blocos únicos gerado: blocos_unicos.csv")