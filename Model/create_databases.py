import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5433",
        database="exportacao-graos",
        user="felipe",
        password="1234"
    )
    cursor = conn.cursor()

    # cursor.execute("""
    #     DROP TABLE exportacoes
    # """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exportacoes(
            ID_EXPORTACAO SERIAL PRIMARY KEY, 
            CO_ANO INTEGER NOT NULL,
            CO_MES INTEGER NOT NULL,
            CO_NCM INTEGER NOT NULL,
            CO_UNID INTEGER NOT NULL,
            CO_PAIS INTEGER NOT NULL,
            SG_UF_NCM CHAR(2) NOT NULL,
            CO_VIA INTEGER NOT NULL,
            CO_URF INTEGER NOT NULL,
            QT_ESTAT INTEGER NOT NULL,
            KG_LIQUIDO INTEGER NOT NULL,
            VL_FOB INTEGER NOT NULL      
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS NCMs(
            ID_NCM INTEGER NOT NULL,
            PRODUTO VARCHAR(100) NOT NULL,

            CONSTRAINT pk_NCMs PRIMARY KEY (ID_NCM),
                   
            CONSTRAINT fk_ID_NCM FOREIGN KEY (ID_NCM) REFERENCES exportacoes(CO_NCM)          
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Paises(
            ID_PAIS INTEGER NOT NULL,
            PAIS VARCHAR(100) NOT NULL,

            CONSTRAINT pk_Paises PRIMARY KEY (ID_PAIS),
                   
            CONSTRAINT fk_ID_PAIS FOREIGN KEY (ID_PAIS) REFERENCES exportacoes(CO_PAIS)           
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS URFs(
            ID_URF INTEGER NOT NULL,
            URF VARCHAR(100) NOT NULL, 

            CONSTRAINT pk_URFs PRIMARY KEY (ID_URF),
                   
            CONSTRAINT fk_ID_URF FOREIGN KEY (ID_URF) REFERENCES exportacoes(CO_URF)          
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Paises_Blocos(
            ID_PAIS INTEGER NOT NULL,
            ID_BLOCO INTEGER NOT NULL,
                   
            CONSTRAINT pk_Paises_Blocos PRIMARY KEY (ID_PAIS, ID_BLOCO),
                   
            CONSTRAINT fk_ID_PAIS FOREIGN KEY (ID_PAIS) REFERENCES Paises(ID_PAIS),
                   
            CONSTRAINT fk_ID_BLOCO FOREIGN KEY (ID_BLOCO) REFERENCES Blocos_Economicos(ID_BLOCO)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vias(
            ID_VIA INTEGER NOT NULL,
            VIA VARCHAR(100) NOT NULL, 

            CONSTRAINT pk_Vias PRIMARY KEY (ID_VIA),          
            
            CONSTRAINT fk_ID_VIA FOREIGN KEY (ID_VIA) REFERENCES exportacoes(CO_VIA)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Blocos_Economicos(
            ID_BLOCO INTEGER NOT NULL,
            BLOCO VARCHAR(100) NOT NULL,
                   
            CONSTRAINT pk_Blocos_Economicos PRIMARY KEY (ID_BLOCO),

            CONSTRAINT fk_ID_BLOCO FOREIGN KEY (ID_BLOCO) REFERENCES Paises_Blocos(ID_BLOCO)           
        )
    """)

    conn.commit()
    print("Tabelas criadas com sucesso.")

except Exception as e:
    print(f"Erro ao conectar ou criar as tabelas: {e}")

finally:
    if conn:
        cursor.close()
        conn.close()
