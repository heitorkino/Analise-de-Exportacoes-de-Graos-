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
        DROP TABLE exportacoes
    """)

    cursor.execute("""
        CREATE TABLE exportacoes(
            ID SERIAL PRIMARY KEY, 
            CO_ANO INTEGER NOT NULL,
            CO_MES INTEGER NOT NULL,
            CO_NCM INTEGER NOT NULL,
            CO_UNID INTEGER NOT NULL,
            CO_PAIS INTEGER NOT NULL,
            SG_UF_NCM CHAR NOT NULL,
            CO_VIA INTEGER NOT NULL,
            CO_URF INTEGER NOT NULL,
            QT_ESTAT INTEGER NOT NULL,
            KG_LIQUIDO INTEGER NOT NULL,
            VL_FOB INTEGER NOT NULL      
        )
    """)
    cursor.execute("""
        DROP TABLE NCMs
    """)
            
    cursor.execute("""
        CREATE TABLE NCMs(
            ID SERIAL PRIMARY KEY,
            PRODUTO VARCHAR(100) NOT NULL,
            CO_NCM INTEGER NOT NULL,

            CONSTRAINT fk_CO_NCM FOREIGN KEY (CO_NCM) REFERENCES exportacoes(CO_NCM)          
        )
    """)
    
    cursor.execute("""
        DROP TABLE Paises
    """)

    cursor.execute("""
        CREATE TABLE Paises(
            ID SERIAL PRIMARY KEY,
            PAIS VARCHAR(100) NOT NULL,
            CO_PAIS INTEGER NOT NULL,

            CONSTRAINT fk_CO_PAIS FOREIGN KEY (CO_PAIS) REFERENCES exportacoes(CO_PAIS)           
        )
    """)
    
    cursor.execute("""
        DROP TABLE URFs
    """)

    cursor.execute("""
        CREATE TABLE URFs(
            ID SERIAL PRIMARY KEY,
            URF VARCHAR(100) NOT NULL,
            CO_URF INTEGER NOT NULL, 

            CONSTRAINT fk_CO_URF FOREIGN KEY (CO_URF) REFERENCES exportacoes(CO_URF)          
        )
    """)

    cursor.execute("""
        DROP TABLE Paises_Blocos
    """)

    cursor.execute("""
        CREATE TABLE Paises_Blocos(
            ID_PAIS INTEGER NOT NULL,
            ID_BLOCO INTEGER NOT NULL,
                   
            CONSTRAINT pk_Paises_Blocos PRIMARY KEY (ID_PAIS, ID_BLOCO),
            CONSTRAINT fk_ID_PAIS FOREIGN KEY (ID_PAIS) REFERENCES Paises(ID),
            CONSTRAINT fk_ID_BLOCO FOREIGN KEY (ID_BLOCO) REFERENCES Blocos_Economicos(ID)
        )
    """)

    cursor.execute("""
        DROP TABLE Vias
    """)

    cursor.execute("""
        CREATE TABLE Vias(
            ID_VIA INTEGER NOT NULL,
            VIA VARCHAR(100) NOT NULL,           
            
            CONSTRAINT fk_CO_VIA FOREIGN KEY (ID_VIA) REFERENCES exportacoes(CO_VIA)
        )
    """)

    cursor.execute("""
        DROP TABLE Blocos_Economicos
    """)

    cursor.execute("""
        CREATE TABLE Blocos_Economicos(
            ID_BLOCO INTEGER NOT NULL,
            BLOCO VARCHAR(100) NOT NULL,

            CONSTRAINT fk_BLOCO FOREIGN KEY (ID_BLOCO) REFERENCES Paises_Blocos(ID_PAIS)           
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