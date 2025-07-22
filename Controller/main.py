# Este script se conecta a um banco de dados PostgreSQL utilizando variáveis de ambiente
# para acessar os dados.

import pandas as pd
import os
import psycopg2
# from Model.ml_models.via_transporte_model import treinar_modelo_via_transporte # type: ignore

# Estabelece a conexão com o banco de dados PostgreSQL usando credenciais do ambiente
conn = psycopg2.connect(
    host=os.environ['localhost'],         # Host do banco de dados
    port=os.environ['5432'],         # Porta de conexão
    dbname=os.environ['exportacao-graos'],       # Nome do banco
    user=os.environ['postgres'],         # Usuário
    password=os.environ['1234']  # Senha
)

# Cria um cursor para executar comandos SQL
cur = conn.cursor()