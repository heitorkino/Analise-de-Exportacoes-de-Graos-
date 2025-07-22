# Este script cria e popula tabelas PostgreSQL com dados de exportações, NCMs, países, vias, URFs, blocos econômicos
# e suas associações. Ele lê os dados de arquivos CSV previamente limpos e realiza a inserção no banco de dados.
# Também verifica conflitos de chave primária para evitar duplicatas.

import psycopg2
import csv

try:
    # Conexão com o banco PostgreSQL local
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="exportacao-graos",
        user="postgres",
        password="1234"
    )
    cursor = conn.cursor()

    # -------------------- Criação e Inserção: Tabela NCMs --------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS NCMs(
            ID_NCM INTEGER PRIMARY KEY NOT NULL,
            PRODUTO VARCHAR(100) NOT NULL        
        )
    """)

    with open('./CSV-Files/Cleaned-CSVs/NCMs_Graos.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO NCMs (ID_NCM, PRODUTO)
                VALUES (%s, %s)
                ON CONFLICT (ID_NCM) DO NOTHING;
            """, (row['ID'], row['Produto']))
    
    # -------------------- Criação e Inserção: Tabela UFs --------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UFs(
            ID_UF VARCHAR(2) PRIMARY KEY NOT NULL,
            NOME VARCHAR(100) NOT NULL        
        )
    """)

    with open('./CSV-Files/Cleaned-CSVs/UF_Limpo.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO UFs (ID_UF, NOME)
                VALUES (%s, %s)
                ON CONFLICT (ID_UF) DO NOTHING;
            """, (row['Sigla'], row['Nome']))

    # -------------------- Criação e Inserção: Tabela URFs --------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS URFs(
            ID_URF INTEGER PRIMARY KEY NOT NULL,
            URF VARCHAR(100) NOT NULL          
        )
    """)

    with open('./CSV-Files/Cleaned-CSVs/URFs_Limpo.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO URFs (ID_URF, URF)
                VALUES (%s, %s)
                ON CONFLICT (ID_URF) DO NOTHING;
            """, (row['Código'], row['Descrição']))

    # -------------------- Criação e Inserção: Tabela Vias --------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vias(
            ID_VIA INTEGER PRIMARY KEY NOT NULL,
            VIA VARCHAR(100) NOT NULL
        )
    """)

    with open('./CSV-Files/Cleaned-CSVs/Vias_Limpo.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO Vias (ID_VIA, VIA)
                VALUES (%s, %s)
                ON CONFLICT (ID_VIA) DO NOTHING;
            """, (row['ID'], row['Via']))

    # -------------------- Criação e Inserção: Tabela Paises --------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Paises(
            ID_PAIS INTEGER PRIMARY KEY NOT NULL,
            PAIS VARCHAR(100) NOT NULL         
        )
    """)

    with open('./CSV-Files/Cleaned-CSVs/Paises_Limpo.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO Paises (ID_PAIS, PAIS)
                VALUES (%s, %s)
                ON CONFLICT (ID_PAIS) DO NOTHING;
            """, (row['id'], row['text']))

    # -------------------- Criação e Inserção: Tabela Blocos_Economicos --------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Blocos_Economicos(
            ID_BLOCO INTEGER PRIMARY KEY NOT NULL,
            BLOCO VARCHAR(100) NOT NULL            
        )
    """)

    with open('./CSV-Files/Cleaned-CSVs/Blocos_Unicos.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO Blocos_Economicos (ID_BLOCO, BLOCO)
                VALUES (%s, %s)
                ON CONFLICT (ID_BLOCO) DO NOTHING;
            """, (row['id'], row['text']))

    # -------------------- Criação e Inserção: Tabela Paises_Blocos --------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Paises_Blocos(
            ID_PAIS_BLOCO SERIAL PRIMARY KEY NOT NULL,
            ID_PAIS INTEGER NOT NULL,
            ID_BLOCO INTEGER NOT NULL,
                        
            UNIQUE (ID_PAIS, ID_BLOCO),
            CONSTRAINT fk_ID_PAIS FOREIGN KEY (ID_PAIS) REFERENCES Paises(ID_PAIS),
            CONSTRAINT fk_ID_BLOCO FOREIGN KEY (ID_BLOCO) REFERENCES Blocos_Economicos(ID_BLOCO)
        )
    """)
    
    with open('./CSV-Files/Cleaned-CSVs/Blocos_Paises.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Verifica previamente os países existentes para evitar erro de chave estrangeira
        cursor.execute("SELECT ID_PAIS FROM Paises")
        paises_existentes = set(row[0] for row in cursor.fetchall())
        
        for row in reader:
            id_pais = int(row['Países'])
            id_bloco = int(row['Bloco'])

            if id_pais in paises_existentes:
                cursor.execute("""
                    INSERT INTO Paises_Blocos (ID_PAIS, ID_BLOCO)
                    VALUES (%s, %s)
                    ON CONFLICT (ID_PAIS, ID_BLOCO) DO NOTHING
                """, (id_pais, id_bloco))
            else:
                print(f"⚠️ País {id_pais} não encontrado em 'Paises'. Linha ignorada.")
    
    # -------------------- Criação e Inserção: Tabela Significado Gargalo  --------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Significado_Gargalo(
            ID_GARGALO_PREDITO INTEGER PRIMARY KEY NOT NULL,
            SIGNIFICADO VARCHAR NOT NULL
        )
    """)

    with open('./CSV-Files/Cleaned-CSVs/Significado_Gargalo_2025.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO Significado_Gargalo (ID_GARGALO_PREDITO, SIGNIFICADO)
                VALUES (%s, %s)
                ON CONFLICT (ID_GARGALO_PREDITO) DO NOTHING;
            """, (row['GARGALO_PREDITO'], row['SIGNIFICADO']))
    
    # -------------------- Criação e Inserção: Tabela Predições Gargalos  --------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Predicoes_Gargalos(
            SG_UF_NCM VARCHAR(2) PRIMARY KEY NOT NULL,
            GARGALO_PREDITO INTEGER NOT NULL,
            
            CONSTRAINT fk_GARGALO_PREDITO FOREIGN KEY (GARGALO_PREDITO) REFERENCES Significado_Gargalo(ID_GARGALO_PREDITO)
        )
    """)

    with open('./CSV-Files/Cleaned-CSVs/Predicoes_Gargalos_2025.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO Predicoes_Gargalos (SG_UF_NCM, GARGALO_PREDITO)
                VALUES (%s, %s)
                ON CONFLICT (SG_UF_NCM) DO NOTHING;
            """, (row['SG_UF_NCM'], row['GARGALO_PREDITO']))

    # -------------------- Criação das Tabelas Exportações --------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exportacoes_2023(
            ID_EXPORTACAO SERIAL PRIMARY KEY, 
            CO_ANO INTEGER NOT NULL,
            CO_MES INTEGER NOT NULL,
            CO_NCM INTEGER NOT NULL,
            CO_UNID INTEGER NOT NULL,
            CO_PAIS INTEGER NOT NULL,
            SG_UF_NCM VARCHAR(2) NOT NULL,
            CO_VIA INTEGER NOT NULL,
            CO_URF INTEGER NOT NULL,
            QT_ESTAT INTEGER NOT NULL,
            KG_LIQUIDO INTEGER NOT NULL,
            VL_FOB INTEGER NOT NULL,

            CONSTRAINT fk_NCM FOREIGN KEY (CO_NCM) REFERENCES NCMs(ID_NCM),      
            CONSTRAINT fk_PAIS FOREIGN KEY (CO_PAIS) REFERENCES Paises(ID_PAIS),
            CONSTRAINT fk_UF FOREIGN KEY (SG_UF_NCM) REFERENCES UFs(ID_UF),      
            CONSTRAINT fk_URF FOREIGN KEY (CO_URF) REFERENCES URFs(ID_URF),      
            CONSTRAINT fk_VIA FOREIGN KEY (CO_VIA) REFERENCES Vias(ID_VIA)       
        )  
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exportacoes_2024(
            ID_EXPORTACAO SERIAL PRIMARY KEY, 
            CO_ANO INTEGER NOT NULL,
            CO_MES INTEGER NOT NULL,
            CO_NCM INTEGER NOT NULL,
            CO_UNID INTEGER NOT NULL,
            CO_PAIS INTEGER NOT NULL,
            SG_UF_NCM VARCHAR(2) NOT NULL,
            CO_VIA INTEGER NOT NULL,
            CO_URF INTEGER NOT NULL,
            QT_ESTAT INTEGER NOT NULL,
            KG_LIQUIDO INTEGER NOT NULL,
            VL_FOB INTEGER NOT NULL,

            CONSTRAINT fk_NCM FOREIGN KEY (CO_NCM) REFERENCES NCMs(ID_NCM),      
            CONSTRAINT fk_PAIS FOREIGN KEY (CO_PAIS) REFERENCES Paises(ID_PAIS),
            CONSTRAINT fk_UF FOREIGN KEY (SG_UF_NCM) REFERENCES UFs(ID_UF),      
            CONSTRAINT fk_URF FOREIGN KEY (CO_URF) REFERENCES URFs(ID_URF),      
            CONSTRAINT fk_VIA FOREIGN KEY (CO_VIA) REFERENCES Vias(ID_VIA)      
        )  
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exportacoes_2025(
            ID_EXPORTACAO SERIAL PRIMARY KEY, 
            CO_ANO INTEGER NOT NULL,
            CO_MES INTEGER NOT NULL,
            CO_NCM INTEGER NOT NULL,
            CO_UNID INTEGER NOT NULL,
            CO_PAIS INTEGER NOT NULL,
            SG_UF_NCM VARCHAR(2) NOT NULL,
            CO_VIA INTEGER NOT NULL,
            CO_URF INTEGER NOT NULL,
            QT_ESTAT INTEGER NOT NULL,
            KG_LIQUIDO INTEGER NOT NULL,
            VL_FOB INTEGER NOT NULL,

            CONSTRAINT fk_NCM FOREIGN KEY (CO_NCM) REFERENCES NCMs(ID_NCM),      
            CONSTRAINT fk_PAIS FOREIGN KEY (CO_PAIS) REFERENCES Paises(ID_PAIS),
            CONSTRAINT fk_UF FOREIGN KEY (SG_UF_NCM) REFERENCES UFs(ID_UF),      
            CONSTRAINT fk_PREDICAO_GARGALO FOREIGN KEY (SG_UF_NCM) REFERENCES Predicoes_Gargalos(SG_UF_NCM),      
            CONSTRAINT fk_URF FOREIGN KEY (CO_URF) REFERENCES URFs(ID_URF),      
            CONSTRAINT fk_VIA FOREIGN KEY (CO_VIA) REFERENCES Vias(ID_VIA)      
        )  
    """)

    # -------------------- Inserção de Dados nas Exportações --------------------
    with open('./CSV-Files/Cleaned-CSVs/EXP_2023_Revisada.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO exportacoes_2023 (
                    CO_ANO, CO_MES, CO_NCM, CO_UNID, CO_PAIS,
                    SG_UF_NCM, CO_VIA, CO_URF,
                    QT_ESTAT, KG_LIQUIDO, VL_FOB
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ID_EXPORTACAO) DO NOTHING;
            """, (row['CO_ANO'], row['CO_MES'], row['CO_NCM'], row['CO_UNID'],
                    row['CO_PAIS'], row['SG_UF_NCM'], row['CO_VIA'], row['CO_URF'],
                    row['QT_ESTAT'], row['KG_LIQUIDO'], row['VL_FOB']))

    with open('./CSV-Files/Cleaned-CSVs/EXP_2024_Revisada.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO exportacoes_2024 (
                    CO_ANO, CO_MES, CO_NCM, CO_UNID, CO_PAIS,
                    SG_UF_NCM, CO_VIA, CO_URF,
                    QT_ESTAT, KG_LIQUIDO, VL_FOB
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ID_EXPORTACAO) DO NOTHING;
            """, (row['CO_ANO'], row['CO_MES'], row['CO_NCM'], row['CO_UNID'],
                    row['CO_PAIS'], row['SG_UF_NCM'], row['CO_VIA'], row['CO_URF'],
                    row['QT_ESTAT'], row['KG_LIQUIDO'], row['VL_FOB']))

    with open('./CSV-Files/Cleaned-CSVs/EXP_2025_Revisada.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO exportacoes_2025 (
                    CO_ANO, CO_MES, CO_NCM, CO_UNID, CO_PAIS,
                    SG_UF_NCM, CO_VIA, CO_URF,
                    QT_ESTAT, KG_LIQUIDO, VL_FOB
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ID_EXPORTACAO) DO NOTHING;
            """, (row['CO_ANO'], row['CO_MES'], row['CO_NCM'], row['CO_UNID'],
                    row['CO_PAIS'], row['SG_UF_NCM'], row['CO_VIA'], row['CO_URF'],
                    row['QT_ESTAT'], row['KG_LIQUIDO'], row['VL_FOB']))
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predicoes_gargalos(
        SG_UF_NCM VARCHAR(2) PRIMARY KEY NOT NULL,
        GARGALO_PREDITO INTEGER NOT NULL,
                   
        CONSTRAINT fk_sg_uf_ncm FOREIGN KEY (SG_UF_NCM) REFERENCES 
    )
    """)
    
    conn.commit() # Confirma todas as operações no banco
    print("Tabelas criadas com sucesso.")

except Exception as e:
    print(f"Erro ao conectar ou criar as tabelas: {e}")

finally:
    # Encerra a conexão com o banco
    if conn:
        cursor.close()
        conn.close()
