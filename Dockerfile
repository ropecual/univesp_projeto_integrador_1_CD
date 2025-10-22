# Dockerfile

# Use uma imagem base do Python oficial
FROM python:3.12-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema necessárias para mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements /app/requirements

# Instala as dependências do Python
RUN pip install --upgrade pip && \
    pip install -r requirements

# Copia o restante do código do projeto para o diretório de trabalho
COPY . /app/

# Cria diretórios para arquivos estáticos e de mídia
RUN mkdir -p /app/staticfiles /app/media

# Expõe a porta que o Django runserver usará
EXPOSE 8000

# Comando padrão para iniciar o container (pode ser sobrescrito pelo docker-compose)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Vamos usar um script de entrada para mais controle (próximo passo)

# Copia o script de entrada e o torna executável
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Define o script de entrada
ENTRYPOINT ["/entrypoint.sh"]