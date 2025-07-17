# Este Dockerfile define uma imagem personalizada baseada em Python 3.11.
# Ele configura o ambiente de trabalho, copia os arquivos do projeto,
# instala as dependências e define o comando para iniciar o script main.py.

# Usa a imagem oficial do Python 3.11 como base
FROM python:3.11     

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app        

# Copia todos os arquivos do diretório atual para o contêiner
COPY . .            

# Instala as dependências listadas no requirements.txt
RUN pip install -r requirements.txt  

# Comando padrão para executar o script main.py quando o contêiner iniciar
CMD ["python", "main.py"]   