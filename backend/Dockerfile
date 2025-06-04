# Usa imagem base com Python
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Copia o script de entrypoint
COPY entrypoint.sh .

# Dá permissão de execução ao entrypoint
RUN chmod +x entrypoint.sh

# Usa o script como ponto de entrada
ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]
