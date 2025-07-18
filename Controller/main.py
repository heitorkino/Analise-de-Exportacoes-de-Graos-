# Este script se conecta a um banco de dados PostgreSQL utilizando variáveis de ambiente
# para acessar os dados.

import pandas as pd
import os
import psycopg2
# from Model.ml_models.via_transporte_model import treinar_modelo_via_transporte # type: ignore

# Estabelece a conexão com o banco de dados PostgreSQL usando credenciais do ambiente
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],         # Host do banco de dados
    port=os.environ['DB_PORT'],         # Porta de conexão
    dbname=os.environ['DB_NAME'],       # Nome do banco
    user=os.environ['DB_USER'],         # Usuário
    password=os.environ['DB_PASSWORD']  # Senha
)

# Cria um cursor para executar comandos SQL
cur = conn.cursor()