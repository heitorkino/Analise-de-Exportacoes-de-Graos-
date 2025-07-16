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

    cursor.execute("""
        DROP TABLE NCMs
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS NCMs(
            ID_NCM INTEGER NOT NULL,
            PRODUTO VARCHAR(100) NOT NULL,

            CONSTRAINT pk_NCMs PRIMARY KEY (ID_NCM)          
        )
    """)

    cursor.execute("""
        DROP TABLE Paises
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Paises(
            ID_PAIS INTEGER NOT NULL,
            PAIS VARCHAR(100) NOT NULL,

            CONSTRAINT pk_Paises PRIMARY KEY (ID_PAIS)           
        )
    """)

    cursor.execute("""
        DROP TABLE URFs
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS URFs(
            ID_URF INTEGER NOT NULL,
            URF VARCHAR(100) NOT NULL, 

            CONSTRAINT pk_URFs PRIMARY KEY (ID_URF)          
        )
    """)

    cursor.execute("""
        DROP TABLE Vias
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vias(
            ID_VIA INTEGER NOT NULL,
            VIA VARCHAR(100) NOT NULL, 

            CONSTRAINT pk_Vias PRIMARY KEY (ID_VIA)
        )
    """)

    cursor.execute("""
        DROP TABLE Blocos_Economicos
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Blocos_Economicos(
            ID_BLOCO INTEGER NOT NULL,
            BLOCO VARCHAR(100) NOT NULL,
                   
            CONSTRAINT pk_Blocos_Economicos PRIMARY KEY (ID_BLOCO)           
        )
    """)

        
    cursor.execute("""
        DROP TABLE Paises_Blocos
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
        DROP TABLE exportacoes
    """)
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
            VL_FOB INTEGER NOT NULL,

            CONSTRAINT fk_NCM FOREIGN KEY (CO_NCM) REFERENCES NCMs(ID_NCM),      
            CONSTRAINT fk_PAIS FOREIGN KEY (CO_PAIS) REFERENCES Paises(ID_PAIS),      
            CONSTRAINT fk_URF FOREIGN KEY (CO_URF) REFERENCES URFs(ID_URF),      
            CONSTRAINT fk_VIA FOREIGN KEY (CO_VIA) REFERENCES Vias(ID_VIA)      
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
